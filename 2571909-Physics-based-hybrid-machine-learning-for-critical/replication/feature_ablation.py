"""Feature ablation study for the Biasi-hybrid CHF model.

Companion to ``chf_hybrid.py``.  Re-uses the same synthetic NRC-like dataset
and Biasi base correlation, then trains the residual-learning hybrid (and a
pure-DNN baseline) under four feature subsets:

    A. Full      = [D, L, P, G, dh_sub, x_out]                (paper baseline)
    B. Op-only   = [P, G, dh_sub]                             (drop geom+thermo)
    C. Op+phys   = [P, G, dh_sub, x_out]                      (drop geometry)
    D. Geom-only = [D, L]                                     (sanity check)

Important: the Biasi base prediction is computed from the full physical state
(D, L, P, G, x_out) at dataset-construction time and is a *fixed teacher
signal*.  Feature subsetting only changes what the neural-network residual
sees -- which is the realistic deployment scenario for a hybrid model whose
empirical correlation requires the full state.

Outputs:
    feature_ablation_results.json   metrics per (config, model_kind)
    feature_ablation_bars.png       grouped bar plot of rRMSE & mu_err
"""
from __future__ import annotations
import os, json, time
import numpy as np
import torch
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from chf_hybrid import (build_dataset, MLP, train_one, fit_ensemble,
                        predict_ensemble, metrics)

HERE = os.path.dirname(os.path.abspath(__file__))

CONFIGS = [
    ("A_full",      "Full (D,L,P,G,dh,x)",       [0, 1, 2, 3, 4, 5]),
    ("C_op_phys",   "Op+phys (P,G,dh,x)",        [2, 3, 4, 5]),
    ("B_op_only",   "Op-only (P,G,dh)",          [2, 3, 4]),
    ("D_geom_only", "Geom-only (D,L)",           [0, 1]),
]


def slice_splits(splits, idx):
    """Return shallow-copy of Splits with feature columns sliced."""
    class S: pass
    s = S()
    s.X_train = splits.X_train[:, idx]
    s.X_val   = splits.X_val[:,   idx]
    s.X_test  = splits.X_test[:,  idx]
    s.y_train = splits.y_train; s.y_val = splits.y_val; s.y_test = splits.y_test
    s.base_train = splits.base_train
    s.base_val   = splits.base_val
    s.base_test  = splits.base_test
    return s


def run_one(s, *, hybrid, n_models=5, epochs=180, tag=""):
    """Train ensemble on sliced features, return metrics dict."""
    if hybrid:
        target_tr  = s.y_train - s.base_train
        target_val = s.y_val   - s.base_val
    else:
        target_tr  = s.y_train
        target_val = s.y_val
    mu = float(target_tr.mean().item()); sd = float(target_tr.std().item() + 1e-9)
    t_tr  = (target_tr  - mu) / sd
    t_val = (target_val - mu) / sd
    t0 = time.time()
    models = fit_ensemble(s.X_train, t_tr, s.X_val, t_val,
                          n_models=n_models, epochs=epochs, bs=64)
    train_s = time.time() - t0
    mean_z, std_z = predict_ensemble(models, s.X_test)
    pred_target = mean_z * sd + mu
    pred = pred_target + (s.base_test.numpy() if hybrid else 0.0)
    m = metrics(s.y_test.numpy(), pred)
    m.update(tag=tag, hybrid=hybrid, n_train=int(len(s.X_train)),
             n_models=n_models, train_time_s=train_s,
             n_features=int(s.X_train.shape[1]))
    return m


def main():
    print("Building dataset (matches chf_hybrid.py master seed)...")
    splits = build_dataset()
    print(f"  train={len(splits.X_train)} val={len(splits.X_val)} test={len(splits.X_test)}")

    # Biasi-bare baseline (independent of feature ablation)
    m_biasi = metrics(splits.y_test.numpy(), splits.base_test.numpy())
    m_biasi.update(tag="Biasi_bare", hybrid=False, n_features=0,
                   n_train=0, model="correlation")
    results = [m_biasi]
    print(f"  Biasi-bare: rRMSE={m_biasi['rRMSE']:.3f}%  mu_err={m_biasi['mu_err']:.3f}%")

    for slug, label, idx in CONFIGS:
        s = slice_splits(splits, idx)
        print(f"\n--- {slug}: {label}  (d_in={len(idx)}) ---")
        m_h = run_one(s, hybrid=True,  tag=f"hybrid_{slug}")
        m_h.update(config=slug, label=label)
        print(f"  hybrid : rRMSE={m_h['rRMSE']:7.3f}%  mu_err={m_h['mu_err']:6.3f}%  R2={m_h['R2']:.4f}  ({m_h['train_time_s']:.1f}s)")
        m_p = run_one(s, hybrid=False, tag=f"pure_{slug}")
        m_p.update(config=slug, label=label)
        print(f"  pure   : rRMSE={m_p['rRMSE']:7.3f}%  mu_err={m_p['mu_err']:6.3f}%  R2={m_p['R2']:.4f}  ({m_p['train_time_s']:.1f}s)")
        results.extend([m_h, m_p])

    out_json = os.path.join(HERE, "feature_ablation_results.json")
    with open(out_json, "w") as fh:
        json.dump(results, fh, indent=2)
    print(f"\nSaved {out_json}")

    # ---- Bar plot ----------------------------------------------------------
    cfg_order = [c[0] for c in CONFIGS]
    labels    = [c[1] for c in CONFIGS]
    hyb_rmse  = [next(r for r in results if r.get('config') == c and r['hybrid'])['rRMSE']
                 for c in cfg_order]
    pur_rmse  = [next(r for r in results if r.get('config') == c and not r['hybrid'])['rRMSE']
                 for c in cfg_order]
    hyb_mu    = [next(r for r in results if r.get('config') == c and r['hybrid'])['mu_err']
                 for c in cfg_order]
    pur_mu    = [next(r for r in results if r.get('config') == c and not r['hybrid'])['mu_err']
                 for c in cfg_order]
    biasi_r = m_biasi['rRMSE']
    biasi_m = m_biasi['mu_err']

    x = np.arange(len(cfg_order)); w = 0.38
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    for ax, (h, p, base, ttl) in zip(axes, [
        (hyb_rmse, pur_rmse, biasi_r, "rRMSE [%]"),
        (hyb_mu,   pur_mu,   biasi_m, "μ_err [%]"),
    ]):
        ax.bar(x - w/2, h, w, label="Biasi hybrid",  color="#2b7bba")
        ax.bar(x + w/2, p, w, label="Pure DNN",      color="#d97a3a")
        ax.axhline(base, color="k", ls="--", lw=1, label=f"Biasi alone ({base:.2f}%)")
        ax.set_xticks(x); ax.set_xticklabels(labels, rotation=15, ha="right", fontsize=9)
        ax.set_ylabel(ttl); ax.set_title(ttl)
        ax.grid(axis="y", alpha=0.3)
    axes[0].legend(loc="upper left", fontsize=9)
    fig.suptitle("Feature ablation: hybrid vs pure DNN on NRC-like CHF test set", y=1.02)
    fig.tight_layout()
    out_png = os.path.join(HERE, "feature_ablation_bars.png")
    fig.savefig(out_png, dpi=150, bbox_inches="tight")
    print(f"Saved {out_png}")

    # Markdown table
    lines = ["| Configuration | Features | hybrid rRMSE | pure rRMSE | hybrid μerr | pure μerr | hybrid R² | Δ vs Biasi-bare |",
             "|---|---|---:|---:|---:|---:|---:|---:|"]
    for slug, label, idx in CONFIGS:
        h = next(r for r in results if r.get('config') == slug and r['hybrid'])
        p = next(r for r in results if r.get('config') == slug and not r['hybrid'])
        delta = h['rRMSE'] - biasi_r
        lines.append(f"| {label} | {len(idx)} | {h['rRMSE']:.2f}% | {p['rRMSE']:.2f}% | "
                     f"{h['mu_err']:.2f}% | {p['mu_err']:.2f}% | {h['R2']:.4f} | {delta:+.2f} pp |")
    table = "\n".join(lines)
    with open(os.path.join(HERE, "feature_ablation_table.md"), "w") as fh:
        fh.write(table + "\n")
    print("\n" + table)


if __name__ == "__main__":
    main()
