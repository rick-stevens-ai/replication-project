"""
Multi-Step Penalty Neural ODE (MP-NODE) core module.
Implements the training strategy from Chakraborty et al. (2024),
"Divide and Conquer: Learning Chaotic Dynamical Systems with MP-NODEs".

Key idea (Alg. 1 of paper):
  - Split a long trajectory [t0, tN] into K segments of length Ts each.
  - Each segment has an independent, *learnable* initial condition q_k.
  - Loss = data MSE(y_pred, y_true) over ALL segments
         + mu * penalty MSE(q_{k+1}^- , q_{k+1}^+) across the K-1 internal jumps
    where q_{k+1}^- is the endpoint of integrating segment k,
    and q_{k+1}^+ is the *learnable* start of segment k+1 (should match).
  - Anneal mu: start small (e.g. 1e-5) and grow to O(1).
  - After convergence, the jumps vanish and we recover a genuine trajectory.
"""
import torch
import torch.nn as nn
from torchdiffeq import odeint


class MPNODEState:
    """Holds learnable discontinuity initial conditions for each training segment.

    For a batch of B trajectories, each split into K segments of length S steps,
    the discontinuities are the K "segment start" states (shape: [B, K, *state]).
    For the first segment we pin to the data initial condition (not learnable).
    """
    def __init__(self, data_ic_per_segment, device=None, learnable_first=False):
        # data_ic_per_segment: tensor [B, K, *state] giving the *data*
        # initial condition at the start of each segment (used for init).
        if device is None:
            device = data_ic_per_segment.device
        # Learnable parameters
        self.q = nn.Parameter(data_ic_per_segment.clone().to(device))
        self.learnable_first = learnable_first


def integrate_segments(node_func, q_start, t_seg, method='rk4', atol=1e-6, rtol=1e-4):
    """Integrate each segment forward in time.

    q_start: [B, K, *state]     # learnable starts (for each segment)
    t_seg: [S+1] tensor of time points for a single segment (shared across segments)

    Returns:
      traj: [S+1, B, K, *state]  predicted states along each segment
      q_end: [B, K, *state]      endpoints (traj[-1])
    """
    B, K = q_start.shape[:2]
    state_shape = q_start.shape[2:]

    # Flatten (B*K) as batch
    y0 = q_start.reshape(B * K, *state_shape)
    if method in ('dopri5', 'dopri8'):
        sol = odeint(node_func, y0, t_seg, method=method, atol=atol, rtol=rtol)
    else:
        sol = odeint(node_func, y0, t_seg, method=method)
    sol = sol.reshape(-1, B, K, *state_shape)  # [S+1, B, K, *state]
    return sol, sol[-1]


def mp_loss(traj_pred, y_true_per_segment, q_start, mu):
    """
    traj_pred: [S+1, B, K, *state] predicted trajectory (incl. both endpoints).
    y_true_per_segment: [S+1, B, K, *state] ground truth at same times.
    q_start: [B, K, *state] learnable segment initial conditions.
    mu: penalty strength (scalar).

    Data loss: MSE over all B*K*(S+1)*state elements.
    Penalty loss: MSE(integrated_endpoint_of_seg_k, learnable_start_of_seg_{k+1})
                  over k=1..K-1.
    """
    data_loss = ((traj_pred - y_true_per_segment) ** 2).mean()

    # Endpoints of segments 0..K-2 vs starts of segments 1..K-1
    q_end_seg = traj_pred[-1]  # [B, K, *state]
    # penalty: compare q_end_seg[:,:-1] with q_start[:, 1:]
    left = q_end_seg[:, :-1]
    right = q_start[:, 1:]
    pen_loss = ((left - right) ** 2).mean()

    total = data_loss + mu * pen_loss
    return total, data_loss.detach(), pen_loss.detach()


# ---------------- MLP NODE (used for KS & Lorenz) ----------------
class MLPNODE(nn.Module):
    def __init__(self, dim, hidden=256, depth=3, act=nn.GELU):
        super().__init__()
        layers = [nn.Linear(dim, hidden), act()]
        for _ in range(depth - 1):
            layers += [nn.Linear(hidden, hidden), act()]
        layers += [nn.Linear(hidden, dim)]
        self.net = nn.Sequential(*layers)

    def forward(self, t, y):
        return self.net(y)


# ---------------- CNN NODE (Kolmogorov / ERA5) ----------------
class DilatedCNNRHS(nn.Module):
    """7-layer dilated CNN (paper's NODE RHS for Kolmogorov flow).
    Works on [N, C, H, W] with circular padding (periodic domain).
    """
    def __init__(self, channels=6, hidden=16):
        super().__init__()
        dilations = (1, 2, 3, 4, 3, 2, 1)
        layers = []
        in_c = channels
        for i, d in enumerate(dilations):
            out_c = hidden if i < len(dilations) - 1 else channels
            layers.append(nn.Conv2d(in_c, out_c, kernel_size=3, padding=d,
                                    dilation=d, padding_mode='circular'))
            if i < len(dilations) - 1:
                layers.append(nn.GELU())
            in_c = out_c
        self.net = nn.Sequential(*layers)

    def forward(self, t, y):
        return self.net(y)


class Encoder2D(nn.Module):
    """3 conv encoder with kernels (7,5,2) and channels (8,16,4). Paper spec."""
    def __init__(self, in_ch=2, lat_ch=4):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(in_ch, 8, 7, padding=3, padding_mode='circular'),
            nn.GELU(),
            nn.Conv2d(8, 16, 5, padding=2, padding_mode='circular'),
            nn.GELU(),
            nn.Conv2d(16, lat_ch, 2, padding=0, padding_mode='circular'),
        )

    def forward(self, x):
        # Pad one on the right/bottom manually so output stays same spatial size.
        x = torch.nn.functional.pad(x, (0, 1, 0, 1), mode='circular')
        return self.net(x)


class Decoder2D(nn.Module):
    """Mirror of encoder."""
    def __init__(self, out_ch=2, lat_ch=4):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(lat_ch, 16, 2, padding=1, padding_mode='circular'),
            nn.GELU(),
            nn.Conv2d(16, 8, 5, padding=2, padding_mode='circular'),
            nn.GELU(),
            nn.Conv2d(8, out_ch, 7, padding=3, padding_mode='circular'),
        )

    def forward(self, x):
        x = self.net(x)
        # trim if needed to match input size
        return x[..., : x.shape[-2] - 1 if x.shape[-2] % 2 == 1 else x.shape[-2],
                     : x.shape[-1] - 1 if x.shape[-1] % 2 == 1 else x.shape[-1]]


class EncoderNODEDecoder(nn.Module):
    """Encoder-NODE-Decoder architecture (paper Fig. 7)."""
    def __init__(self, in_ch=2, lat_ch=4, augment=2, H=64, W=64):
        super().__init__()
        self.enc = Encoder2D(in_ch=in_ch, lat_ch=lat_ch)
        self.aug = augment
        self.rhs = DilatedCNNRHS(channels=lat_ch + augment, hidden=16)
        self.dec = Decoder2D(out_ch=in_ch, lat_ch=lat_ch + augment)
        self.lat_ch = lat_ch
        self.H, self.W = H, W

    def encode(self, u):
        z = self.enc(u)
        if self.aug > 0:
            pad = torch.zeros(z.shape[0], self.aug, *z.shape[2:], device=z.device, dtype=z.dtype)
            z = torch.cat([z, pad], dim=1)
        return z

    def decode(self, z):
        return self.dec(z)

    def forward(self, t, z):
        return self.rhs(t, z)
