"""
Smoke replication driver for Hartzell et al. 2025
(10.1667/rade-24-00164.1).

Reads `data/fragment_spectrum_reference.csv`, runs the four RBE models on each
fragment, and computes the dose-averaged total RBE per beamline region
(entrance / SOBP / tail). Writes:

  figures/per_fragment_rbe.png         — per-fragment RBE_2Gy by model
  figures/total_rbe_vs_model.png       — dose-averaged total RBE per region
  reports/smoke_results.json           — numerical results + provenance
  reports/smoke_results.csv            — long-form table

Pure numpy + matplotlib, < 1 s on CPU.
"""
from __future__ import annotations
import csv, json, math, os, sys, hashlib, datetime
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE  = Path(__file__).resolve().parent
ROOT  = HERE.parent
sys.path.insert(0, str(HERE))

from rbe_models import (
    FragmentInput, MODELS, RBE_at_dose,
    ALPHA_X_DEFAULT, BETA_X_DEFAULT,
)

DOSE_GY    = 2.0
ALPHA_X    = ALPHA_X_DEFAULT
BETA_X     = BETA_X_DEFAULT
REGIONS    = ("entrance", "sobp", "tail")
DATA_CSV   = ROOT / "data" / "fragment_spectrum_reference.csv"
FIG_DIR    = ROOT / "figures"
REPORT_DIR = ROOT / "reports"

FIG_DIR.mkdir(exist_ok=True)
REPORT_DIR.mkdir(exist_ok=True)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def load_fragments():
    rows = []
    with DATA_CSV.open() as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            r = next(csv.DictReader([line], fieldnames=[
                "fragment","Z","A","E_MeV_u","LETd_keV_um",
                "dose_frac_entrance","dose_frac_sobp","dose_frac_tail",
            ]))
            # skip header
            if r["fragment"] == "fragment":
                continue
            rows.append(r)
    return rows


def main():
    rows = load_fragments()
    fragments = [
        FragmentInput(
            name=r["fragment"],
            Z=int(r["Z"]),
            A=int(r["A"]),
            E_MeV_u=float(r["E_MeV_u"]),
            LETd_keV_um=float(r["LETd_keV_um"]),
        )
        for r in rows
    ]
    dose_fracs = {
        region: np.array([float(r[f"dose_frac_{region}"]) for r in rows])
        for region in REGIONS
    }

    # Sanity check: dose fractions should sum to ~1 per region
    sums = {r: float(dose_fracs[r].sum()) for r in REGIONS}

    # Secondary-fragment fraction = everything except prim_C, electrons, other
    secondaries = {"H", "He", "Li", "Be", "B", "sec_C"}
    sec_mask = np.array([r["fragment"] in secondaries for r in rows])
    sec_frac = {r: float(dose_fracs[r][sec_mask].sum()) for r in REGIONS}

    # Per-fragment alpha,beta,RBE per model
    per_frag = {}        # per_frag[model][frag.name] = {alpha,beta,RBE}
    for model, fn in MODELS.items():
        per_frag[model] = {}
        for f in fragments:
            a, b = fn(f, alpha_x=ALPHA_X, beta_x=BETA_X)
            rbe = RBE_at_dose(a, b, DOSE_GY, ALPHA_X, BETA_X)
            per_frag[model][f.name] = {"alpha": a, "beta": b, "RBE": rbe}

    # Dose-averaged total RBE per region, per model.
    # We weight per-fragment RBE by the per-fragment dose-fraction, then
    # additionally compute a "true" dose-averaged RBE via LQ-additive damage:
    #   For each region, the mixed-field LQ is alpha_mix*D + beta_mix*D^2
    #   with alpha_mix = sum_i f_i * alpha_i and beta_mix = (sum_i f_i*sqrt(beta_i))^2
    total_rbe = {region: {} for region in REGIONS}
    mixed_ab  = {region: {} for region in REGIONS}
    for model in MODELS:
        for region in REGIONS:
            fracs = dose_fracs[region]
            alphas = np.array([per_frag[model][f.name]["alpha"] for f in fragments])
            betas  = np.array([per_frag[model][f.name]["beta"]  for f in fragments])
            alpha_mix = float((fracs * alphas).sum())
            beta_mix  = float(((fracs * np.sqrt(np.maximum(betas, 0))).sum()) ** 2)
            rbe_mix   = RBE_at_dose(alpha_mix, beta_mix, DOSE_GY, ALPHA_X, BETA_X)
            total_rbe[region][model] = rbe_mix
            mixed_ab[region][model]  = {"alpha_mix": alpha_mix, "beta_mix": beta_mix}

    # Highest-RBE fragment per model (in SOBP region) — paper says secondary C
    highest = {}
    for model in MODELS:
        rbes = {f.name: per_frag[model][f.name]["RBE"] for f in fragments}
        highest[model] = max(rbes.items(), key=lambda kv: kv[1])

    # ----- figures -----
    frag_names = [f.name for f in fragments]
    x = np.arange(len(frag_names))
    width = 0.2
    fig, ax = plt.subplots(figsize=(10, 5))
    for i, model in enumerate(MODELS):
        rbes = [per_frag[model][n]["RBE"] for n in frag_names]
        ax.bar(x + (i - 1.5) * width, rbes, width, label=model)
    ax.set_xticks(x)
    ax.set_xticklabels(frag_names, rotation=30, ha="right")
    ax.set_ylabel("RBE_{2 Gy}")
    ax.set_title("Per-fragment RBE by model (smoke replication of Hartzell 2025)")
    ax.legend()
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "per_fragment_rbe.png", dpi=120)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 4))
    for i, region in enumerate(REGIONS):
        vals = [total_rbe[region][m] for m in MODELS]
        ax.bar(np.arange(len(MODELS)) + (i - 1) * 0.25, vals, 0.25, label=region)
    ax.set_xticks(np.arange(len(MODELS)))
    ax.set_xticklabels(list(MODELS.keys()))
    ax.set_ylabel("Dose-averaged total RBE_{2 Gy}")
    ax.set_title("Total RBE by model and beamline region")
    ax.legend()
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "total_rbe_vs_model.png", dpi=120)
    plt.close(fig)

    # ----- json + csv -----
    out = {
        "paper": {
            "doi":   "10.1667/rade-24-00164.1",
            "title": "Contribution of Nuclear Fragmentation to Dose and RBE in Carbon-Ion Radiotherapy",
            "authors": "Hartzell S, Guan F, Magro G, Taylor P, Taddei PJ, Peterson CB, Kry S",
            "year":  2025,
        },
        "smoke_replication": {
            "dose_Gy":      DOSE_GY,
            "alpha_x":      ALPHA_X,
            "beta_x":       BETA_X,
            "data_csv":     str(DATA_CSV.relative_to(ROOT)),
            "data_csv_sha256": sha256(DATA_CSV),
            "dose_fraction_sums_per_region": sums,
            "secondary_fragment_dose_fraction_per_region": sec_frac,
            "per_fragment": per_frag,
            "mixed_alpha_beta": mixed_ab,
            "total_RBE": total_rbe,
            "highest_RBE_fragment_per_model": {m: {"name": n, "RBE": v} for m, (n, v) in highest.items()},
        },
        "claims_check": {
            "claim_1_secondary_fragment_dose_gt_30pct_in_SOBP": {
                "value":  sec_frac["sobp"],
                "passes": sec_frac["sobp"] > 0.30,
            },
            "claim_2_intermodel_RBE_spread_gt_zero": {
                "sobp_spread": max(total_rbe["sobp"].values()) - min(total_rbe["sobp"].values()),
                "passes": (max(total_rbe["sobp"].values()) - min(total_rbe["sobp"].values())) > 0.05,
            },
            "claim_3_secondary_C_is_highest_RBE_fragment": {
                "per_model_highest": {m: n for m, (n, _) in highest.items()},
                "passes": all(n == "sec_C" for m, (n, _) in highest.items()),
            },
        },
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
    }
    (REPORT_DIR / "smoke_results.json").write_text(json.dumps(out, indent=2))

    with (REPORT_DIR / "smoke_results.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["model", "fragment", "alpha", "beta", "RBE_2Gy"])
        for model in MODELS:
            for f_ in fragments:
                d = per_frag[model][f_.name]
                w.writerow([model, f_.name, f"{d['alpha']:.6g}", f"{d['beta']:.6g}", f"{d['RBE']:.4f}"])

    # ----- console summary -----
    print(f"[smoke] dose fractions per region: {sums}")
    print(f"[smoke] secondary-fragment dose fraction per region: {sec_frac}")
    for region in REGIONS:
        line = "  ".join(f"{m}={total_rbe[region][m]:.3f}" for m in MODELS)
        print(f"[smoke] total RBE  {region:8s}  {line}")
    for model, (name, v) in highest.items():
        print(f"[smoke] highest-RBE fragment ({model}): {name}  RBE={v:.3f}")
    for k, v in out["claims_check"].items():
        print(f"[claim] {k}: passes={v['passes']}")


if __name__ == "__main__":
    main()
