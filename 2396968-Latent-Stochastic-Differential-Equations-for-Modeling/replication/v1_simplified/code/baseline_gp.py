"""DRW/Matern-1/2 GPR baseline via scipy (no celerite dep needed, small N).

For each light curve, fit a DRW GP:  k(t,t') = sigma^2 * exp(-|t-t'|/tau)
plus diagonal observation noise from err.  Optimise (log tau, log sigma)
by marginal likelihood, then report leave-one-out reconstruction RMSE/MAE/NLL
on observed points (paper reports reconstruction metrics).
"""
from __future__ import annotations

import os, pickle, math, json
import numpy as np
from scipy.optimize import minimize
from scipy.linalg import cho_factor, cho_solve


def _kernel(t, tau, sigma):
    dt = np.abs(t[:, None] - t[None, :])
    return sigma ** 2 * np.exp(-dt / max(tau, 1e-3))


def _nll(params, t, y, err):
    log_tau, log_sigma = params
    tau = np.exp(log_tau)
    sigma = np.exp(log_sigma)
    K = _kernel(t, tau, sigma) + np.diag(err ** 2) + 1e-6 * np.eye(len(t))
    try:
        c, low = cho_factor(K, lower=True)
    except np.linalg.LinAlgError:
        return 1e10
    alpha = cho_solve((c, low), y)
    nll = 0.5 * y @ alpha + np.sum(np.log(np.diag(c))) + 0.5 * len(t) * math.log(2 * math.pi)
    return nll


def _fit_and_loo(t, y, err):
    # Coarse grid init then local search
    best = (1e18, math.log(100.0), math.log(0.2))
    for lt in np.log([10.0, 30.0, 100.0, 300.0, 1000.0]):
        for ls in np.log([0.05, 0.1, 0.2, 0.4]):
            v = _nll([lt, ls], t, y, err)
            if v < best[0]:
                best = (v, lt, ls)
    x0 = np.array([best[1], best[2]])
    try:
        res = minimize(_nll, x0, args=(t, y, err), method="Nelder-Mead",
                       options=dict(xatol=1e-3, fatol=1e-3, maxiter=200))
        log_tau, log_sigma = res.x
        # clip to reasonable range
        log_tau = float(np.clip(log_tau, math.log(1.0), math.log(5000.0)))
        log_sigma = float(np.clip(log_sigma, math.log(0.01), math.log(2.0)))
    except Exception:
        log_tau, log_sigma = x0
    tau, sigma = math.exp(log_tau), math.exp(log_sigma)
    K = _kernel(t, tau, sigma) + np.diag(err ** 2) + 1e-6 * np.eye(len(t))
    c, low = cho_factor(K, lower=True)
    Kinv = cho_solve((c, low), np.eye(len(t)))
    alpha = Kinv @ y
    # LOO predictive:  mu_i = y_i - alpha_i / Kinv_ii, var_i = 1/Kinv_ii
    diagKinv = np.diag(Kinv).clip(min=1e-8)
    mu_loo = y - alpha / diagKinv
    var_loo = 1.0 / diagKinv
    return mu_loo, var_loo, tau, sigma


def evaluate(data_dir, out_path):
    with open(os.path.join(data_dir, "test.pkl"), "rb") as f:
        test = pickle.load(f)
    N = test["y"].shape[0]
    se_sum = ae_sum = nll_sum = 0.0
    cnt = 0
    taus, sigmas = [], []
    for i in range(N):
        m = test["mask"][i] > 0
        t = test["t"][i][m]
        y = test["y"][i][m]
        err = test["err"][i][m]
        mu, var, tau, sigma = _fit_and_loo(t, y, err)
        taus.append(tau); sigmas.append(sigma)
        se_sum += np.sum((mu - y) ** 2)
        ae_sum += np.sum(np.abs(mu - y))
        nll_sum += np.sum(0.5 * (np.log(var) + (y - mu) ** 2 / var + math.log(2 * math.pi)))
        cnt += len(y)
    res = dict(rmse=float(np.sqrt(se_sum / cnt)),
               mae=float(ae_sum / cnt),
               nll=float(nll_sum / cnt),
               n_curves=N, n_points=cnt,
               median_tau=float(np.median(taus)),
               median_sigma=float(np.median(sigmas)))
    with open(out_path, "w") as f:
        json.dump(res, f, indent=2)
    print("GPR baseline:", res)
    return res


if __name__ == "__main__":
    here = os.path.dirname(__file__)
    evaluate(os.path.join(here, "..", "data"),
             os.path.join(here, "..", "results", "gpr_baseline.json"))
