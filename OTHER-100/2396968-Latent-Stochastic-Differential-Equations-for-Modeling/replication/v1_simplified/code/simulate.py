"""Simulate DRW (damped random walk) light curves with LSST-like irregular sampling.

DRW SDE: dX = -(X - mu)/tau dt + sigma_d dW,  with SF_inf = sigma_d * sqrt(tau/2).
Stationary variance = sigma_d^2 * tau / 2 = SF_inf^2.

This is the "driving" variability model used by Fagin et al. 2024 for quasars;
it also matches the DRW kernel used by celerite (Matern-1/2 for single-band).
We use single-band for simplicity (the paper is multi-band ugrizy).
"""
from __future__ import annotations

import numpy as np


def sample_drw_exact(
    t: np.ndarray, tau: float, SF_inf: float, mu: float = 0.0, rng: np.random.Generator = None,
) -> np.ndarray:
    """Exact sampling of DRW at arbitrary times using the OU transition kernel."""
    if rng is None:
        rng = np.random.default_rng()
    assert np.all(np.diff(t) >= 0)
    n = len(t)
    x = np.empty(n)
    # stationary distribution
    x[0] = mu + SF_inf * rng.standard_normal()
    for i in range(1, n):
        dt = t[i] - t[i - 1]
        decay = np.exp(-dt / tau)
        mean = mu + (x[i - 1] - mu) * decay
        var = SF_inf ** 2 * (1.0 - decay ** 2)
        x[i] = mean + np.sqrt(var) * rng.standard_normal()
    return x


def lsst_like_cadence(
    n_years: float = 5.0,
    n_obs: int = 180,
    season_length: float = 180.0,
    season_gap: float = 180.0,
    rng: np.random.Generator = None,
) -> np.ndarray:
    """Return irregular observation times (days) with seasonal gaps."""
    if rng is None:
        rng = np.random.default_rng()
    total_days = n_years * 365.25
    # build 'on-season' windows
    t = 0.0
    windows = []
    while t < total_days:
        windows.append((t, min(t + season_length, total_days)))
        t += season_length + season_gap
    # distribute n_obs uniformly across windows
    total_on = sum(b - a for a, b in windows)
    times = []
    for a, b in windows:
        k = max(1, int(round(n_obs * (b - a) / total_on)))
        u = np.sort(rng.uniform(a, b, size=k))
        times.extend(u.tolist())
    times = np.array(sorted(times))
    # clip/pad to exactly n_obs
    if len(times) > n_obs:
        idx = np.sort(rng.choice(len(times), n_obs, replace=False))
        times = times[idx]
    return times


def make_dataset(
    n_curves: int = 512,
    n_obs: int = 180,
    n_years: float = 5.0,
    sigma_obs_range: tuple = (0.01, 0.03),
    tau_log10_range: tuple = (1.5, 3.0),  # days: ~30 to 1000
    SF_inf_range: tuple = (0.10, 0.35),  # mag
    seed: int = 0,
):
    """Generate a batch of DRW light curves with observation noise.

    Returns a dict with:
      t     (N, T) time grid in days (padded)
      y     (N, T) noisy magnitudes (mean-subtracted)
      err   (N, T) per-obs sigmas
      mask  (N, T) 1 = observed
      params (N, 3) [log10 tau, SF_inf, sigma_obs]
    """
    rng = np.random.default_rng(seed)
    ts, ys, errs, masks, params = [], [], [], [], []
    max_len = n_obs
    for i in range(n_curves):
        t = lsst_like_cadence(n_years=n_years, n_obs=n_obs, rng=rng)
        log10_tau = rng.uniform(*tau_log10_range)
        tau = 10.0 ** log10_tau
        SF_inf = rng.uniform(*SF_inf_range)
        sigma_obs = rng.uniform(*sigma_obs_range)
        x_true = sample_drw_exact(t, tau=tau, SF_inf=SF_inf, mu=0.0, rng=rng)
        noise = sigma_obs * rng.standard_normal(len(t))
        y = x_true + noise
        err = np.full_like(y, sigma_obs)
        mask = np.ones_like(y)
        # pad
        L = max_len - len(t)
        if L > 0:
            t = np.concatenate([t, np.full(L, t[-1] + 1.0)])
            y = np.concatenate([y, np.zeros(L)])
            err = np.concatenate([err, np.ones(L)])
            mask = np.concatenate([mask, np.zeros(L)])
        ts.append(t)
        ys.append(y)
        errs.append(err)
        masks.append(mask)
        params.append([log10_tau, SF_inf, sigma_obs])
    return dict(
        t=np.stack(ts).astype(np.float32),
        y=np.stack(ys).astype(np.float32),
        err=np.stack(errs).astype(np.float32),
        mask=np.stack(masks).astype(np.float32),
        params=np.asarray(params, dtype=np.float32),
    )


if __name__ == "__main__":
    import pickle, os

    out_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(out_dir, exist_ok=True)
    for split, n, seed in [("train", 512, 1), ("val", 128, 2), ("test", 256, 3)]:
        ds = make_dataset(n_curves=n, seed=seed)
        with open(os.path.join(out_dir, f"{split}.pkl"), "wb") as f:
            pickle.dump(ds, f)
        print(split, ds["y"].shape, "mean |y|", np.mean(np.abs(ds["y"])))
