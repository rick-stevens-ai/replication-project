"""Synthetic 8x8 BES-like ELM dataset generator.

Models DIII-D BES intensity (1 MHz, 8x8 channels) with stochastic Type-I ELM
events: onset (10->90% rise), peak, exponential relaxation. Includes spatial
filament structure, background turbulence/MHD, and per-channel saturation.

The real BES data from the paper is not publicly available; this synthetic
generator preserves the *shape* (8x8 spatial, 1 us sample, ELM-like bursts)
so we can compare model architectures qualitatively.
"""

from __future__ import annotations
import numpy as np
import torch
from torch.utils.data import Dataset


def _filament_pattern(rng: np.random.Generator) -> np.ndarray:
    """Random 8x8 amplitude pattern: radial gradient + ELM filament blob."""
    yy, xx = np.mgrid[0:8, 0:8].astype(np.float32)
    cx, cy = rng.uniform(2, 5), rng.uniform(2, 5)
    sx, sy = rng.uniform(1.0, 2.5), rng.uniform(1.0, 2.5)
    blob = np.exp(-((xx - cx) ** 2 / (2 * sx**2) + (yy - cy) ** 2 / (2 * sy**2)))
    radial = 0.4 + 0.6 * (1 - yy / 7.0)            # higher on outer rows
    pat = 0.5 * radial + 0.8 * blob
    pat /= pat.max()
    return pat.astype(np.float32)


def _elm_profile(n_rise: int, n_peak: int, n_relax: int, tau: float, rng) -> np.ndarray:
    """1D temporal profile of one ELM, normalized to peak 1."""
    rise = np.linspace(0.0, 1.0, n_rise) ** 2
    peak = np.ones(n_peak) + 0.05 * rng.standard_normal(n_peak)
    t = np.arange(n_relax)
    relax = np.exp(-t / tau)
    prof = np.concatenate([rise, peak, relax]).astype(np.float32)
    return prof


def generate_shot(T: int = 80_000, seed: int = 0) -> np.ndarray:
    """Return (T, 8, 8) float32 array simulating one DIII-D BES shot."""
    rng = np.random.default_rng(seed)
    # Background: smoothed turbulence per channel + slow sinusoid (MHD)
    bg = rng.standard_normal((T, 8, 8)).astype(np.float32) * 0.15
    # Smooth in time
    kernel = np.ones(9, dtype=np.float32) / 9
    bg = np.apply_along_axis(lambda v: np.convolve(v, kernel, mode="same"), 0, bg)
    # Sinusoid MHD-like
    t = np.arange(T) / 1e6  # seconds (1 us step)
    for k in range(2):
        f = rng.uniform(2_000, 12_000)  # Hz
        phase = rng.uniform(0, 2 * np.pi)
        amp_pat = 0.05 + 0.05 * rng.random((8, 8)).astype(np.float32)
        bg += amp_pat[None] * np.sin(2 * np.pi * f * t + phase)[:, None, None].astype(np.float32)
    base = 1.5 + bg  # baseline level around 1.5 V

    # ELM events
    n_events = rng.integers(30, 60)
    # Avoid first/last 1000 us so windows fit
    centers = np.sort(rng.integers(2_000, T - 2_000, n_events))
    # ensure >= 600 us spacing
    centers = centers[np.concatenate([[True], np.diff(centers) > 600])]
    out = base.copy()
    for c in centers:
        n_rise = int(rng.integers(150, 250))
        n_peak = int(rng.integers(30, 80))
        n_relax = int(rng.integers(200, 400))
        tau = rng.uniform(80, 200)
        prof = _elm_profile(n_rise, n_peak, n_relax, tau, rng)
        amp = rng.uniform(2.5, 5.0)  # ELM peak amplitude
        pat = _filament_pattern(rng) * amp  # 8x8
        L = prof.shape[0]
        s = c - n_rise
        e = s + L
        if s < 0 or e > T:
            continue
        out[s:e] += prof[:, None, None] * pat[None]

    # Saturation clipping (paper: 10 V top, 5 V bottom half)
    out[:, :4, :] = np.clip(out[:, :4, :], 0.0, 10.0)
    out[:, 4:, :] = np.clip(out[:, 4:, :], 0.0, 5.0)
    return out.astype(np.float32), centers


class WindowDataset(Dataset):
    """Sliding windows of (history, target) from a list of shots."""

    def __init__(self, shots: list[np.ndarray], delta: int = 30, H: int = 30,
                 stride: int = 50, max_per_shot: int | None = None,
                 normalize: tuple[float, float] | None = None):
        self.delta = delta
        self.H = H
        self.windows = []  # (shot_idx, t_start)
        self.shots = shots
        for i, s in enumerate(shots):
            T = s.shape[0]
            starts = np.arange(0, T - delta - H, stride)
            if max_per_shot is not None and len(starts) > max_per_shot:
                idx = np.linspace(0, len(starts) - 1, max_per_shot).astype(int)
                starts = starts[idx]
            for st in starts:
                self.windows.append((i, int(st)))
        self.normalize = normalize  # (mean, std) global

    def __len__(self):
        return len(self.windows)

    def __getitem__(self, idx):
        i, st = self.windows[idx]
        s = self.shots[i]
        hist = s[st:st + self.delta]                # (delta, 8, 8)
        targ = s[st + self.delta:st + self.delta + self.H]  # (H, 8, 8)
        if self.normalize is not None:
            m, sd = self.normalize
            hist = (hist - m) / sd
            targ = (targ - m) / sd
        return torch.from_numpy(hist), torch.from_numpy(targ)


def build_datasets(n_train=32, n_val=4, n_test=4, T=80_000, delta=30, H=30,
                   stride=50, max_per_shot=200, seed0=0):
    train_shots = [generate_shot(T, seed=seed0 + i)[0] for i in range(n_train)]
    val_shots = [generate_shot(T, seed=seed0 + 1000 + i)[0] for i in range(n_val)]
    test_shots = [generate_shot(T, seed=seed0 + 2000 + i)[0] for i in range(n_test)]
    # Global stats from train
    flat = np.concatenate([s.reshape(-1) for s in train_shots])
    m, sd = float(flat.mean()), float(flat.std() + 1e-6)
    norm = (m, sd)
    return (
        WindowDataset(train_shots, delta, H, stride, max_per_shot, norm),
        WindowDataset(val_shots, delta, H, stride, max_per_shot, norm),
        WindowDataset(test_shots, delta, H, stride, max_per_shot, norm),
        norm,
    )


if __name__ == "__main__":
    s, c = generate_shot(20_000, seed=0)
    print("shot shape:", s.shape, "n_elm:", len(c), "min/max:", s.min(), s.max())
