"""
Refit IMK model parameters via MCMC on the digitized Fig 5 data.

Goal: independently recover Table 1 parameters from the (noisy) digitized
survival points, using the same likelihood as Eq 15 of the paper:

    P(d_i | theta) = (1/sqrt(2 pi sigma)) * exp(- ( -ln S_exp,i + ln S_cal,i)^2 / (2 sigma^2))

and the same prior assumptions:
    alpha0_p, beta0_p, alpha0_s, beta0_s, w_SLDR ~ Uniform on positive interval
    f_s prior centered on experimental ALDH+ value
    (a+c)_p prior = the split-dose-derived value
    constraint: alpha0_s < alpha0_p and beta0_s < beta0_p (per paper)

We use a Metropolis-Hastings random-walk MCMC (matches the paper's
description; the paper cites refs 32-33 for MCMC and notes uniform priors).

This refit is performed PER FAMILY (SAS+SAS-R simultaneously, sharing
stem-cell parameters and parental (a+c)_p, with w_SLDR for the resistant
line).  Same for HSC2 family.
"""
from __future__ import annotations
import os
import json
import math
import numpy as np

from imk_model import S_total_single_dose, DOSE_RATE_ACUTE_GY_PER_H
from params_table1 import TABLE1
from digitized_fig5 import FIG5_DATA

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.normpath(os.path.join(HERE, "..", "results"))
os.makedirs(RESULTS, exist_ok=True)

# ----------------------------------------------------------------------
# Likelihood
# ----------------------------------------------------------------------

def neg_log_likelihood(family, theta, sigma=0.6):
    """
    family: 'SAS' or 'HSC2'.
    theta = (alpha0_p, beta0_p, apc_p,
             alpha0_s, beta0_s, apc_H,
             f_s_parent, f_s_resistant,
             w_SLDR_resistant)
    Returns sum of squared residuals in -ln S, weighted as in Eq 15.
    """
    (alpha0_p, beta0_p, apc_p,
     alpha0_s, beta0_s, apc_H,
     f_s_p, f_s_r, w_SLDR_r) = theta

    # Hard constraints from priors
    if any(v <= 0 for v in (alpha0_p, beta0_p, apc_p,
                            alpha0_s, beta0_s, apc_H, w_SLDR_r)):
        return np.inf
    if not (0 < f_s_p < 0.5 and 0 < f_s_r < 0.5):
        return np.inf
    if alpha0_s > alpha0_p:  # stem cells more resistant (smaller alpha)
        return np.inf
    if beta0_s > beta0_p:
        return np.inf

    resistant = f"{family}-R"
    # parental:
    pred_p = S_total_single_dose(
        [d for d, _ in FIG5_DATA[family] if d > 0],
        alpha0_p_star=alpha0_p, beta0_p_star=beta0_p, apc_p_star=apc_p,
        alpha0_s=alpha0_s, beta0_s=beta0_s, apc_H=apc_H,
        f_s=f_s_p,
    )
    obs_p = np.array([s for d, s in FIG5_DATA[family] if d > 0])

    # resistant — modulated parental params:
    pred_r = S_total_single_dose(
        [d for d, _ in FIG5_DATA[resistant] if d > 0],
        alpha0_p_star=alpha0_p / w_SLDR_r,
        beta0_p_star=beta0_p / w_SLDR_r,
        apc_p_star=apc_p * w_SLDR_r,
        alpha0_s=alpha0_s, beta0_s=beta0_s, apc_H=apc_H,
        f_s=f_s_r,
    )
    obs_r = np.array([s for d, s in FIG5_DATA[resistant] if d > 0])

    # Residuals in -ln S
    res_p = -np.log(np.maximum(obs_p, 1e-30)) + np.log(np.maximum(pred_p, 1e-30))
    res_r = -np.log(np.maximum(obs_r, 1e-30)) + np.log(np.maximum(pred_r, 1e-30))
    ss = float(np.sum(res_p ** 2) + np.sum(res_r ** 2))
    n = len(res_p) + len(res_r)
    return 0.5 * ss / (sigma ** 2) + n * math.log(sigma)


# ----------------------------------------------------------------------
# Metropolis-Hastings
# ----------------------------------------------------------------------

def run_mcmc(family, n_iter=40000, burn=10000, seed=0):
    rng = np.random.default_rng(seed)
    # Initialize at Table 1 means
    t1_p = TABLE1[family]
    t1_r = TABLE1[f"{family}-R"]
    theta = np.array([
        t1_p["alpha0_p_star"][0],
        t1_p["beta0_p_star"][0],
        t1_p["apc_p_star"][0],
        t1_p["alpha0_s"][0],
        t1_p["beta0_s"][0],
        t1_p["apc_H"][0],
        t1_p["f_s"][0],
        t1_r["f_s"][0],
        t1_r["w_SLDR"][0],
    ])

    # Proposal scales: ~10-20% of Table 1 SDs
    sd = np.array([
        t1_p["alpha0_p_star"][1] * 0.20,
        t1_p["beta0_p_star"][1] * 0.20,
        t1_p["apc_p_star"][1] * 0.20,
        t1_p["alpha0_s"][1] * 0.20,
        t1_p["beta0_s"][1] * 0.20,
        t1_p["apc_H"][1] * 0.20,
        t1_p["f_s"][1] * 0.20,
        t1_r["f_s"][1] * 0.20,
        max(t1_r["w_SLDR"][1] * 0.20, 0.02),
    ])
    sd = np.maximum(sd, 1e-4)

    current_nll = neg_log_likelihood(family, tuple(theta))
    chain = np.zeros((n_iter, len(theta)))
    n_accept = 0

    for i in range(n_iter):
        cand = theta + rng.normal(0, sd)
        cand_nll = neg_log_likelihood(family, tuple(cand))
        log_a = current_nll - cand_nll  # accept ratio in log space
        if math.log(rng.random()) < log_a:
            theta = cand
            current_nll = cand_nll
            n_accept += 1
        chain[i] = theta

    samples = chain[burn:]
    accept = n_accept / n_iter
    return samples, accept


# ----------------------------------------------------------------------
def summarize_chain(samples, names):
    out = {}
    for j, nm in enumerate(names):
        col = samples[:, j]
        out[nm] = {
            "mean": float(col.mean()),
            "sd": float(col.std()),
            "q05": float(np.quantile(col, 0.05)),
            "q50": float(np.quantile(col, 0.50)),
            "q95": float(np.quantile(col, 0.95)),
        }
    return out


def main():
    names = [
        "alpha0_p", "beta0_p", "apc_p",
        "alpha0_s", "beta0_s", "apc_H",
        "f_s_parent", "f_s_resistant", "w_SLDR_resistant",
    ]
    report = {}
    for family in ["SAS", "HSC2"]:
        print(f"\n=== MCMC refit for {family} family ===")
        samples, acc = run_mcmc(family, n_iter=40000, burn=10000, seed=1)
        summary = summarize_chain(samples, names)
        print(f"  Acceptance rate: {acc:.3f}")
        for nm in names:
            s = summary[nm]
            print(f"  {nm:18s}  mean={s['mean']:.4f}  sd={s['sd']:.4f}  "
                  f"[{s['q05']:.4f}, {s['q95']:.4f}]")
        report[family] = {"acceptance_rate": acc, "params": summary}

    out = os.path.join(RESULTS, "mcmc_refit_summary.json")
    with open(out, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\nWrote {out}")

    # Markdown comparison table
    lines = ["# MCMC refit vs. Table 1 (paper)\n",
             "Parameters obtained by re-running MH-MCMC on the digitized Fig 5 "
             "points, compared to Table 1 from the paper.\n"]
    for family in ["SAS", "HSC2"]:
        t1_p = TABLE1[family]
        t1_r = TABLE1[f"{family}-R"]
        rp = report[family]["params"]
        lines.append(f"\n## {family} family\n")
        lines.append("| parameter | refit mean ± sd | Table 1 mean ± sd | ratio |")
        lines.append("|-----------|-----------------|-------------------|-------|")
        pairs = [
            ("alpha0_p",      rp["alpha0_p"], t1_p["alpha0_p_star"]),
            ("beta0_p",       rp["beta0_p"],  t1_p["beta0_p_star"]),
            ("apc_p",         rp["apc_p"],    t1_p["apc_p_star"]),
            ("alpha0_s",      rp["alpha0_s"], t1_p["alpha0_s"]),
            ("beta0_s",       rp["beta0_s"],  t1_p["beta0_s"]),
            ("apc_H",         rp["apc_H"],    t1_p["apc_H"]),
            ("f_s (parent)",  rp["f_s_parent"], t1_p["f_s"]),
            ("f_s (resistant)", rp["f_s_resistant"], t1_r["f_s"]),
            ("w_SLDR (resistant)", rp["w_SLDR_resistant"], t1_r["w_SLDR"]),
        ]
        for nm, refit, paper in pairs:
            ratio = refit["mean"] / paper[0] if paper[0] != 0 else float("nan")
            lines.append(
                f"| {nm} | {refit['mean']:.3f} ± {refit['sd']:.3f} | "
                f"{paper[0]:.3f} ± {paper[1]:.3f} | {ratio:.2f} |"
            )

    out_md = os.path.join(RESULTS, "mcmc_refit_summary.md")
    with open(out_md, "w") as f:
        f.write("\n".join(lines))
    print(f"Wrote {out_md}")


if __name__ == "__main__":
    main()
