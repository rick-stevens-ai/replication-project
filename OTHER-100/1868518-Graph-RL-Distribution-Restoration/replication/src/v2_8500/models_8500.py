"""
GCN-DQN and MLP-DQN models for the 8500-bus restoration env (cell-aggregated).
Action space: n_switches + 1 (NoOp).
Per-switch Q-value computed from the embeddings of its two endpoint cells.
"""
import torch
import torch.nn as nn
import torch.nn.functional as F


class GCNLayer(nn.Module):
    def __init__(self, in_dim, out_dim):
        super().__init__()
        self.lin = nn.Linear(in_dim, out_dim)
    def forward(self, x, A_norm):
        # x: (B, N, F)  A_norm: (N, N) symmetric normalized (shared across batch)
        return torch.matmul(A_norm, self.lin(x))


def normalize_adj(A):
    """A: (N,N) tensor. Returns D^-1/2 (A+I) D^-1/2."""
    N = A.shape[0]
    A_hat = A + torch.eye(N, device=A.device, dtype=A.dtype)
    deg = A_hat.sum(1)
    d_inv = torch.pow(deg.clamp(min=1e-6), -0.5)
    return A_hat * d_inv.unsqueeze(0) * d_inv.unsqueeze(1)


class GCNDQN(nn.Module):
    def __init__(self, n_cells, n_switches, switch_edges,
                 feat_dim=8, hidden=128, n_layers=3):
        super().__init__()
        self.n_cells = n_cells
        self.n_switches = n_switches
        self.register_buffer("switch_edges",
                             torch.as_tensor(switch_edges, dtype=torch.long))
        self.in_proj = nn.Linear(feat_dim, hidden)
        self.gcns = nn.ModuleList([GCNLayer(hidden, hidden) for _ in range(n_layers)])
        self.norms = nn.ModuleList([nn.LayerNorm(hidden) for _ in range(n_layers)])
        # Dueling head
        self.adv_head = nn.Sequential(
            nn.Linear(2 * hidden, hidden), nn.ReLU(),
            nn.Linear(hidden, 1))
        self.val_head = nn.Sequential(
            nn.Linear(hidden, hidden), nn.ReLU(),
            nn.Linear(hidden, 1))
        self.noop_head = nn.Sequential(
            nn.Linear(hidden, hidden), nn.ReLU(),
            nn.Linear(hidden, 1))

    def forward(self, x, A_norm):
        """x: (B, N, F) ; A_norm: (N, N).  Returns Q: (B, n_switches+1)."""
        h = self.in_proj(x)
        for gcn, ln in zip(self.gcns, self.norms):
            h = ln(F.relu(gcn(h, A_norm) + h))
        # Pair embeddings for each switch edge
        e = self.switch_edges                         # (S, 2)
        h_u = h[:, e[:, 0], :]                        # (B, S, H)
        h_v = h[:, e[:, 1], :]                        # (B, S, H)
        pair = torch.cat([h_u, h_v], dim=-1)          # (B, S, 2H)
        adv_sw = self.adv_head(pair).squeeze(-1)      # (B, S)
        # NoOp: use graph-mean embedding
        h_g = h.mean(dim=1)                           # (B, H)
        adv_noop = self.noop_head(h_g)                # (B, 1)
        adv = torch.cat([adv_sw, adv_noop], dim=-1)   # (B, S+1)
        val = self.val_head(h_g)                      # (B, 1)
        adv_centered = adv - adv.mean(dim=-1, keepdim=True)
        return val + adv_centered


class MLPDQN(nn.Module):
    """Baseline: flattens node features (no graph)."""
    def __init__(self, n_cells, n_switches, feat_dim=8, hidden=512):
        super().__init__()
        self.n_cells = n_cells
        self.n_switches = n_switches
        self.net = nn.Sequential(
            nn.Linear(n_cells * feat_dim, hidden), nn.ReLU(),
            nn.Linear(hidden, hidden), nn.ReLU(),
            nn.Linear(hidden, hidden), nn.ReLU(),
            nn.Linear(hidden, n_switches + 1))

    def forward(self, x, A_norm=None):
        b = x.shape[0]
        flat = x.reshape(b, -1)
        return self.net(flat)
