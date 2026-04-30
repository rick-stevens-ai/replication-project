"""
Neural network models for learning Burgers equation solutions.

Models:
  - BurgersMLPTimestepper: MLP that predicts u^{n+1} from u^n
    with residual connection (u^{n+1} = u^n + NN(u^n))
  - BurgersFNOTimestepper: Fourier Neural Operator variant

Paper: Cassia & Kerswell, arXiv:2405.11674
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np


class BurgersMLPTimestepper(nn.Module):
    """
    MLP time-stepper: u^{n+1} = u^n + dt * NN(u^n)
    Residual connection mimics forward Euler.
    
    Input: u^n (batch, Nx)
    Output: u^{n+1} (batch, Nx)
    """
    
    def __init__(self, Nx, hidden_dim=256, num_layers=5, dt=1.0):
        super().__init__()
        self.Nx = Nx
        self.dt = dt
        
        layers = []
        layers.append(nn.Linear(Nx, hidden_dim))
        layers.append(nn.GELU())
        
        for _ in range(num_layers - 2):
            layers.append(nn.Linear(hidden_dim, hidden_dim))
            layers.append(nn.GELU())
        
        layers.append(nn.Linear(hidden_dim, Nx))
        
        self.net = nn.Sequential(*layers)
        
        # Initialize last layer to small weights for better start
        nn.init.xavier_uniform_(self.net[-1].weight, gain=0.01)
        nn.init.zeros_(self.net[-1].bias)
    
    def forward(self, u_n):
        """
        Args:
            u_n: (batch, Nx) solution at time n
        Returns:
            u_np1: (batch, Nx) predicted solution at time n+1
        """
        delta = self.net(u_n)
        u_np1 = u_n + self.dt * delta
        return u_np1


class SpectralConv1d(nn.Module):
    """1D Fourier layer for FNO."""
    
    def __init__(self, in_channels, out_channels, modes):
        super().__init__()
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.modes = modes
        
        scale = 1.0 / (in_channels * out_channels)
        self.weights = nn.Parameter(
            scale * torch.randn(in_channels, out_channels, modes, dtype=torch.cfloat)
        )
    
    def forward(self, x):
        # x: (batch, in_channels, Nx)
        batch_size = x.shape[0]
        Nx = x.shape[-1]
        
        # FFT
        x_ft = torch.fft.rfft(x, dim=-1)
        
        # Multiply relevant Fourier modes
        out_ft = torch.zeros(batch_size, self.out_channels, Nx // 2 + 1,
                            device=x.device, dtype=torch.cfloat)
        out_ft[:, :, :self.modes] = torch.einsum(
            'bix,iox->box', x_ft[:, :, :self.modes], self.weights
        )
        
        # IFFT
        x = torch.fft.irfft(out_ft, n=Nx, dim=-1)
        return x


class BurgersFNOTimestepper(nn.Module):
    """
    Fourier Neural Operator time-stepper.
    u^{n+1} = u^n + dt * FNO(u^n)
    """
    
    def __init__(self, Nx, modes=16, width=32, num_layers=4, dt=1.0):
        super().__init__()
        self.Nx = Nx
        self.dt = dt
        self.modes = modes
        self.width = width
        
        # Lifting: 1 -> width channels
        self.lift = nn.Linear(1, width)
        
        # Fourier layers
        self.spectral_layers = nn.ModuleList()
        self.linear_layers = nn.ModuleList()
        
        for _ in range(num_layers):
            self.spectral_layers.append(SpectralConv1d(width, width, modes))
            self.linear_layers.append(nn.Conv1d(width, width, 1))
        
        # Projection: width -> 1
        self.proj1 = nn.Linear(width, 64)
        self.proj2 = nn.Linear(64, 1)
    
    def forward(self, u_n):
        """
        Args:
            u_n: (batch, Nx)
        Returns:
            u_np1: (batch, Nx)
        """
        # Reshape: (batch, Nx) -> (batch, Nx, 1)
        x = u_n.unsqueeze(-1)
        
        # Lift
        x = self.lift(x)  # (batch, Nx, width)
        x = x.permute(0, 2, 1)  # (batch, width, Nx)
        
        # Fourier layers
        for spec, lin in zip(self.spectral_layers, self.linear_layers):
            x1 = spec(x)
            x2 = lin(x)
            x = F.gelu(x1 + x2)
        
        # Project back
        x = x.permute(0, 2, 1)  # (batch, Nx, width)
        x = F.gelu(self.proj1(x))
        delta = self.proj2(x).squeeze(-1)  # (batch, Nx)
        
        u_np1 = u_n + self.dt * delta
        return u_np1


def godunov_flux_burgers_torch(uL, uR):
    """
    Exact Godunov flux for Burgers equation f(u) = u^2/2.
    Differentiable PyTorch implementation.
    
    Args:
        uL, uR: tensors of same shape, left/right states
    Returns:
        F: Godunov flux tensor
    """
    fL = 0.5 * uL ** 2
    fR = 0.5 * uR ** 2
    
    # Shock case: uL >= uR
    shock_speed = (uL + uR) / 2.0
    F_shock = torch.where(shock_speed >= 0, fL, fR)
    
    # Rarefaction case: uL < uR
    F_rare = torch.where(uL >= 0, fL, torch.where(uR <= 0, fR, torch.zeros_like(fL)))
    
    F = torch.where(uL >= uR, F_shock, F_rare)
    return F


def lax_friedrichs_flux_torch(uL, uR, alpha):
    """
    Lax-Friedrichs flux for Burgers equation.
    F_LF = 0.5 * (f(uL) + f(uR)) - 0.5 * alpha * (uR - uL)
    where alpha = max|f'(u)| = max|u|
    """
    fL = 0.5 * uL ** 2
    fR = 0.5 * uR ** 2
    return 0.5 * (fL + fR) - 0.5 * alpha * (uR - uL)


def compute_godunov_residual(u_n, u_np1, dx, dt):
    """
    Compute the Godunov FVM residual for 1D Burgers:
      R_i = u_i^{n+1} - u_i^n + (dt/dx) * [F_{i+1/2} - F_{i-1/2}]
    
    where F is the exact Godunov flux evaluated from the NN prediction u^{n+1}.
    
    The loss is then L_G = mean(R^2).
    
    Key insight from Cassia & Kerswell: the intercell flux uses the
    Riemann solver (Godunov/HLLC) applied to the NN-predicted field,
    enforcing conservation and entropy at the discrete level.
    
    Args:
        u_n: (batch, Nx) solution at time n (ground truth input)
        u_np1: (batch, Nx) predicted solution at time n+1
        dx: spatial step
        dt: time step between n and n+1
    Returns:
        residual: (batch, Nx-2) FVM residual at interior cells
    """
    lam = dt / dx
    
    # Godunov flux at interfaces from predicted solution
    # F_{i+1/2} = godunov_flux(u_i^{n+1}, u_{i+1}^{n+1})
    uL = u_np1[:, :-1]  # u_i
    uR = u_np1[:, 1:]   # u_{i+1}
    F = godunov_flux_burgers_torch(uL, uR)  # (batch, Nx-1)
    
    # FVM residual at interior cells [1, Nx-2]
    # R_i = u_i^{n+1} - u_i^n + lam * (F_{i+1/2} - F_{i-1/2})
    residual = (u_np1[:, 1:-1] - u_n[:, 1:-1] + 
                lam * (F[:, 1:] - F[:, :-1]))
    
    return residual


def compute_godunov_loss(model, u_n, u_np1_true, dx, dt):
    """
    Godunov loss: L_G = mean(R^2) where R is the FVM residual
    using Godunov flux applied to the model prediction.
    
    This is the key contribution of Cassia & Kerswell:
    instead of MSE against truth, penalize violation of the
    discrete conservation law with entropy-satisfying flux.
    
    For the supervised+Godunov variant we use:
    L = L_MSE + lambda_G * L_G
    
    But the paper's main point is using L_G as the SOLE physics loss
    (unsupervised). For our simplified 1D replication, we test both.
    """
    u_np1_pred = model(u_n)
    
    residual = compute_godunov_residual(u_n, u_np1_pred, dx, dt)
    loss_godunov = torch.mean(residual ** 2)
    
    return loss_godunov, u_np1_pred


def compute_mse_loss(model, u_n, u_np1_true):
    """Standard MSE loss against ground truth."""
    u_np1_pred = model(u_n)
    loss = F.mse_loss(u_np1_pred, u_np1_true)
    return loss, u_np1_pred


def compute_hybrid_godunov_loss(model, u_n, u_np1_true, dx, dt, lambda_g=1.0):
    """
    Hybrid loss: L = L_MSE + lambda_g * L_Godunov
    
    Combines data-driven MSE with physics-informed Godunov residual.
    """
    u_np1_pred = model(u_n)
    
    loss_mse = F.mse_loss(u_np1_pred, u_np1_true)
    residual = compute_godunov_residual(u_n, u_np1_pred, dx, dt)
    loss_godunov = torch.mean(residual ** 2)
    
    loss = loss_mse + lambda_g * loss_godunov
    return loss, loss_mse, loss_godunov, u_np1_pred


if __name__ == '__main__':
    # Quick shape test
    Nx = 256
    batch = 8
    model = BurgersMLPTimestepper(Nx, hidden_dim=128, num_layers=4)
    u_n = torch.randn(batch, Nx)
    u_np1 = model(u_n)
    print(f"MLP: input {u_n.shape} -> output {u_np1.shape}")
    print(f"  Parameters: {sum(p.numel() for p in model.parameters()):,}")
    
    model_fno = BurgersFNOTimestepper(Nx, modes=16, width=32, num_layers=4)
    u_np1_fno = model_fno(u_n)
    print(f"FNO: input {u_n.shape} -> output {u_np1_fno.shape}")
    print(f"  Parameters: {sum(p.numel() for p in model_fno.parameters()):,}")
    
    # Test Godunov flux
    uL = torch.tensor([1.0, -1.0, 0.5, -0.5])
    uR = torch.tensor([-1.0, 1.0, 1.5, -1.5])
    F = godunov_flux_burgers_torch(uL, uR)
    print(f"\nGodunov flux test: {F}")
    
    # Test residual
    dx = 1.0 / Nx
    dt = 0.001
    res = compute_godunov_residual(u_n, u_np1, dx, dt)
    print(f"Residual shape: {res.shape}")
