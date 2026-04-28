"""Forecasting models for 8x8 BES-like ELM data.

Three models:
  - ConstantBaseline: predict last frame for all horizon steps.
  - FNO2DForecaster: Fourier neural operator over 8x8 grid, AR rollout.
  - ConvLSTMSeq2Seq: ConvLSTM encoder-decoder + attention + smoothing layer.
"""
from __future__ import annotations
import torch
import torch.nn as nn
import torch.nn.functional as F


# ----------------------------- Constant baseline -----------------------------

class ConstantBaseline(nn.Module):
    def __init__(self, H: int):
        super().__init__()
        self.H = H

    def forward(self, hist: torch.Tensor) -> torch.Tensor:
        # hist: (B, delta, 8, 8) -> (B, H, 8, 8)
        last = hist[:, -1:, :, :]
        return last.expand(-1, self.H, -1, -1).contiguous()


# --------------------------------- FNO 2D ------------------------------------

class SpectralConv2d(nn.Module):
    def __init__(self, in_c: int, out_c: int, modes: int = 4):
        super().__init__()
        self.in_c, self.out_c, self.modes = in_c, out_c, modes
        scale = 1.0 / (in_c * out_c)
        self.w1 = nn.Parameter(scale * torch.randn(in_c, out_c, modes, modes, dtype=torch.cfloat))
        self.w2 = nn.Parameter(scale * torch.randn(in_c, out_c, modes, modes, dtype=torch.cfloat))

    def compl_mul2d(self, x, w):
        return torch.einsum("bixy,ioxy->boxy", x, w)

    def forward(self, x):
        B, C, H, W = x.shape
        xf = torch.fft.rfft2(x, norm="ortho")
        out = torch.zeros(B, self.out_c, H, xf.shape[-1], dtype=torch.cfloat, device=x.device)
        m = self.modes
        out[:, :, :m, :m] = self.compl_mul2d(xf[:, :, :m, :m], self.w1)
        out[:, :, -m:, :m] = self.compl_mul2d(xf[:, :, -m:, :m], self.w2)
        return torch.fft.irfft2(out, s=(H, W), norm="ortho")


class FNOBlock(nn.Module):
    def __init__(self, c: int, modes: int = 4):
        super().__init__()
        self.spec = SpectralConv2d(c, c, modes)
        self.w = nn.Conv2d(c, c, 1)

    def forward(self, x):
        return F.gelu(self.spec(x) + self.w(x))


class FNO2DForecaster(nn.Module):
    """One-step predictor f(x_t-delta+1..x_t) -> x_t+1; AR rollout for H steps."""
    def __init__(self, delta: int, H: int, hidden: int = 32, modes: int = 4, n_layers: int = 4):
        super().__init__()
        self.delta = delta
        self.H = H
        self.lift = nn.Conv2d(delta, hidden, 1)
        self.blocks = nn.ModuleList([FNOBlock(hidden, modes) for _ in range(n_layers)])
        self.proj = nn.Conv2d(hidden, 1, 1)

    def step(self, hist: torch.Tensor) -> torch.Tensor:
        # hist: (B, delta, 8, 8) -> (B, 1, 8, 8) prediction of next frame
        x = self.lift(hist)
        for b in self.blocks:
            x = b(x)
        return self.proj(x)

    def forward(self, hist: torch.Tensor, H: int | None = None) -> torch.Tensor:
        H = H or self.H
        outs = []
        cur = hist
        for _ in range(H):
            nxt = self.step(cur)            # (B,1,8,8)
            outs.append(nxt)
            cur = torch.cat([cur[:, 1:], nxt], dim=1)
        return torch.cat(outs, dim=1)        # (B, H, 8, 8)


# ------------------------------- ConvLSTM ------------------------------------

class ConvLSTMCell(nn.Module):
    def __init__(self, in_c: int, hid_c: int, k: int = 3):
        super().__init__()
        self.hid_c = hid_c
        pad = k // 2
        self.conv = nn.Conv2d(in_c + hid_c, 4 * hid_c, k, padding=pad)

    def forward(self, x, h, c):
        gates = self.conv(torch.cat([x, h], dim=1))
        i, f, g, o = gates.chunk(4, dim=1)
        i, f, o = torch.sigmoid(i), torch.sigmoid(f), torch.sigmoid(o)
        g = torch.tanh(g)
        c = f * c + i * g
        h = o * torch.tanh(c)
        return h, c

    def init_state(self, B, H, W, device, dtype):
        z = torch.zeros(B, self.hid_c, H, W, device=device, dtype=dtype)
        return z, z.clone()


class ConvLSTMSeq2Seq(nn.Module):
    """Encoder–decoder ConvLSTM with Bahdanau-style attention + smoothing layer.

    Simplified version of the paper's best architecture.
    """
    def __init__(self, delta: int, H: int, hidden: int = 32, k: int = 3,
                 use_attention: bool = True, use_smoothing: bool = True):
        super().__init__()
        self.delta = delta
        self.H = H
        self.hidden = hidden
        self.use_attention = use_attention
        self.use_smoothing = use_smoothing

        self.enc = ConvLSTMCell(1, hidden, k)
        self.dec = ConvLSTMCell(1, hidden, k)
        # Attention
        self.attn_q = nn.Conv2d(hidden, hidden, 1)
        self.attn_k = nn.Conv2d(hidden, hidden, 1)
        self.attn_v = nn.Conv2d(hidden, hidden, 1)
        # Output projection
        self.out_conv = nn.Conv2d(hidden + (hidden if use_attention else 0), 1, 1)
        # Smoothing scalar (learned, sigmoid)
        if use_smoothing:
            self.alpha_logit = nn.Parameter(torch.tensor(0.0))

    def encode(self, hist):
        # hist: (B, delta, 8, 8)
        B, T, H, W = hist.shape
        h, c = self.enc.init_state(B, H, W, hist.device, hist.dtype)
        feats = []
        for t in range(T):
            x = hist[:, t:t+1]  # (B,1,H,W)
            h, c = self.enc(x, h, c)
            feats.append(h)
        return torch.stack(feats, dim=1), (h, c)  # (B,T,hid,H,W)

    def attend(self, q, keys, values):
        # q: (B,hid,H,W) ; keys/values: (B,T,hid,H,W)
        B, T, C, H, W = keys.shape
        qp = self.attn_q(q)                    # (B,C,H,W)
        kp = self.attn_k(keys.reshape(B*T, C, H, W)).reshape(B, T, C, H, W)
        vp = self.attn_v(values.reshape(B*T, C, H, W)).reshape(B, T, C, H, W)
        # Score = mean over channels & space of q*k -> (B,T)
        scores = (kp * qp.unsqueeze(1)).mean(dim=(2, 3, 4))
        weights = F.softmax(scores, dim=1)     # (B,T)
        ctx = (vp * weights.view(B, T, 1, 1, 1)).sum(dim=1)  # (B,C,H,W)
        return ctx

    def forward(self, hist: torch.Tensor, H: int | None = None) -> torch.Tensor:
        H_steps = H or self.H
        feats, (h, c) = self.encode(hist)  # feats (B,T,hid,8,8)
        last_x = hist[:, -1:]               # (B,1,8,8)
        x_t = hist[:, -1:]                  # constant for smoothing
        outs = []
        cur_in = last_x
        for _ in range(H_steps):
            h, c = self.dec(cur_in, h, c)
            if self.use_attention:
                ctx = self.attend(h, feats, feats)
                fused = torch.cat([h, ctx], dim=1)
            else:
                fused = h
            y = self.out_conv(fused)        # (B,1,8,8)
            if self.use_smoothing:
                a = torch.sigmoid(self.alpha_logit)
                y = (1 - a) * y + a * x_t
            outs.append(y)
            cur_in = y
        return torch.cat(outs, dim=1)        # (B, H, 8, 8)


def count_params(m: nn.Module) -> int:
    return sum(p.numel() for p in m.parameters() if p.requires_grad)
