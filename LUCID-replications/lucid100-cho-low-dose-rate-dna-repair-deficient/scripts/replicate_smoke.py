#!/usr/bin/env python3
"""
Smoke replication for LUCID100 slot 24:
Buglewicz et al. 2024, "Exploring DNA repair deficient CHO cell response to
low dose rate radiation" (BBRC 10.1016/j.bbrc.2024.149539).

The BBRC 2024 paper is paywalled with no data/code deposit, so we cannot
quantitatively reproduce its actual survival curves. Instead, we build a
closed-form linear-quadratic (LQ) + Lea-Catcheside G(lambda) smoke model
that demonstrates the *qualitative* claims of the paper using LQ parameters
anchored to the lab's open-access companion paper (Buglewicz 2023, Cancer Sci.,
PMC10727999), which uses the same CHO mutant panel (10B2 WT, 51D1 HR-,
V3 NHEJ-).

Claims targeted (qualitatively):
  C1. Acute LQ: NHEJ-deficient (V3) most radiosensitive at low dose;
      HR-deficient (51D1) more sensitive than WT but less than NHEJ at low dose.
  C2. WT and HR-deficient cells show classical dose-rate sparing under LDR
      (G < 1, survival increases as dose rate drops at fixed total dose).
  C3. NHEJ-deficient cells show a paradoxical inverse dose-rate effect (IDRE)
      regime: at some intermediate dose rates and total doses, LDR survival
      is *lower* than acute, because NHEJ-deficient cells accumulate
      unrepaired DSBs during the protracted exposure rather than benefiting
      from sublethal-damage repair.

Implementation:
  - SF_acute(D) = exp(-alpha*D - beta*D^2)         [LQ acute]
  - SF_LDR(D, Dot) = exp(-alpha*D - beta*G(lambda,T)*D^2)
       with T = D / Dot and G(lambda,T) = 2 * (lambda*T - 1 + exp(-lambda*T)) / (lambda*T)^2
       where lambda = ln(2)/tau (tau = sublethal-damage repair half-time).
  - For NHEJ-deficient lines we add an "incomplete-repair penalty" term
    P(Dot) = phi * exp(-Dot/Dot0) that *raises* effective alpha at low Dot,
    simulating accumulated unrepaired DSBs (the IDRE mechanism).
    alpha_eff(Dot) = alpha * (1 + P(Dot))

Anchor data from Buglewicz 2023 (PMC10727999, Table 1 - SOBP proximal D10):
    10B2 (WT)  D10 = 4.67 Gy ; SER = 1.00
    51D1 (HR-) D10 = 2.87 Gy ; SER = 1.63
    V3   (NHEJ-) D10 = 2.71 Gy ; SER = 1.72
These are carbon-ion D10s, *not* the LDR-gamma D10s that the 2024 paper would
report. We use only their ratios to anchor the relative panel ordering; the
absolute LQ parameters here are illustrative low-LET gamma values from the
broader CHO-mutant literature (Jones 1986 RR; Iliakis 1989; Frankenberg-Schwager
1991), not measured numbers from the 2024 paper itself.

Outputs (printed + saved to figures/):
  - acute_survival.png      : LQ acute curves (claim C1)
  - dose_rate_sparing.png   : SF at fixed D = 4 Gy as a function of dose rate
                              (claims C2, C3 — IDRE visible for NHEJ-deficient)
  - smoke_summary.json      : numeric pass/fail for each claim
"""

from __future__ import annotations
import json
import math
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FIGS = os.path.join(ROOT, "figures")
DATA = os.path.join(ROOT, "data")
os.makedirs(FIGS, exist_ok=True)
os.makedirs(DATA, exist_ok=True)

# --------------------------- Model ---------------------------

def G_factor(lam: float, T: float) -> float:
    """Lea-Catcheside time/protraction factor for single-pass exposure of length T."""
    x = lam * T
    if x < 1e-9:
        return 1.0
    return 2.0 * (x - 1.0 + math.exp(-x)) / (x * x)


def sf_acute(D, alpha, beta):
    return np.exp(-alpha * D - beta * D * D)


def sf_ldr(D, dot, alpha, beta, tau_h, idre_phi=0.0, idre_dot0=0.05):
    """LDR survival via LQ + G(lambda,T) + optional NHEJ-style IDRE penalty.

    Parameters
    ----------
    D : float or array — total absorbed dose (Gy)
    dot : float — dose rate (Gy/h)
    alpha, beta : LQ params (Gy^-1, Gy^-2)
    tau_h : sublethal-damage repair half-time in hours
    idre_phi : >0 boosts effective alpha at very low dot for NHEJ-deficient lines
    idre_dot0 : Gy/h, dose-rate scale of the IDRE penalty
    """
    D = np.asarray(D, dtype=float)
    T = D / dot                              # hours
    lam = math.log(2.0) / tau_h
    G = np.vectorize(lambda t: G_factor(lam, t))(T)
    alpha_eff = alpha * (1.0 + idre_phi * math.exp(-dot / idre_dot0))
    return np.exp(-alpha_eff * D - beta * G * D * D)


# --------------------------- Panel parameters ---------------------------
# Illustrative low-LET gamma LQ params for CHO panel; absolute values are NOT
# claimed to reproduce Buglewicz 2024 — only the relative ordering anchored
# to PMC10727999 ratios.
PANEL = {
    "WT (10B2/AA8)":      dict(alpha=0.10, beta=0.030, tau_h=1.0, idre_phi=0.00),
    "HR- (51D1)":         dict(alpha=0.25, beta=0.030, tau_h=1.5, idre_phi=0.00),
    "NHEJ- (V3/xrs5)":    dict(alpha=0.55, beta=0.010, tau_h=4.0, idre_phi=0.45),
}

# --------------------------- C1: acute survival ---------------------------

def claim_C1():
    doses = np.linspace(0, 6, 61)
    out = {}
    for name, p in PANEL.items():
        out[name] = sf_acute(doses, p["alpha"], p["beta"])
    # Pass criterion: at D=2 Gy, SF(NHEJ-) < SF(HR-) < SF(WT)
    SF2 = {k: float(sf_acute(2.0, v["alpha"], v["beta"])) for k, v in PANEL.items()}
    ok = (SF2["NHEJ- (V3/xrs5)"] < SF2["HR- (51D1)"] < SF2["WT (10B2/AA8)"])
    return doses, out, SF2, ok


# --------------------------- C2 / C3: dose-rate scan ---------------------------

def claim_C23(D_total=4.0):
    """At fixed total dose D_total, sweep dose rate from acute (10 Gy/h) down to LDR (0.005 Gy/h)."""
    dots = np.logspace(np.log10(0.005), np.log10(10.0), 60)  # Gy/h
    out = {}
    for name, p in PANEL.items():
        sfs = np.array([
            float(sf_ldr(D_total, dot, p["alpha"], p["beta"], p["tau_h"],
                         idre_phi=p["idre_phi"]))
            for dot in dots
        ])
        out[name] = sfs

    # Pass criteria
    # C2: For WT and HR-, SF(LDR low dot) > SF(acute high dot)  [sparing]
    sparing_WT = float(out["WT (10B2/AA8)"][0] / out["WT (10B2/AA8)"][-1])
    sparing_HR = float(out["HR- (51D1)"][0] / out["HR- (51D1)"][-1])
    sparing_ok = (sparing_WT > 1.2) and (sparing_HR > 1.2)

    # C3: For NHEJ-, there exists an interior dose rate where SF drops below SF(acute)
    nhej = out["NHEJ- (V3/xrs5)"]
    sf_acute_val = float(nhej[-1])      # highest dot in our sweep ~= "acute"
    sf_min = float(np.min(nhej))
    idre_ratio = sf_min / sf_acute_val      # <1 means LDR worse than acute → IDRE
    idre_ok = idre_ratio < 0.95

    return dots, out, {
        "sparing_WT_ratio_LDR_over_acute": sparing_WT,
        "sparing_HR_ratio_LDR_over_acute": sparing_HR,
        "NHEJ_sf_acute": sf_acute_val,
        "NHEJ_sf_min_LDR_window": sf_min,
        "NHEJ_idre_ratio_min_over_acute": idre_ratio,
        "sparing_ok": sparing_ok,
        "idre_ok": idre_ok,
    }


# --------------------------- Driver ---------------------------

def main():
    print("=== LUCID100 slot 24 — BBRC 2024 CHO LDR DNA-repair smoke ===")
    print()

    doses_c1, sf_c1, sf2, c1_ok = claim_C1()
    print(f"[C1] Acute LQ ordering at D=2 Gy:")
    for k, v in sf2.items():
        print(f"     SF(2 Gy) {k:24s} = {v:.4f}")
    print(f"     PASS criterion: SF(NHEJ-) < SF(HR-) < SF(WT)  -> {c1_ok}")
    print()

    dots, sf_c23, c23 = claim_C23(D_total=4.0)
    print(f"[C2] Dose-rate sparing at D=4 Gy (LDR/acute SF ratio, want > 1.2):")
    print(f"     WT  ratio = {c23['sparing_WT_ratio_LDR_over_acute']:.3f}")
    print(f"     HR- ratio = {c23['sparing_HR_ratio_LDR_over_acute']:.3f}")
    print(f"     PASS: {c23['sparing_ok']}")
    print()
    print(f"[C3] NHEJ- inverse dose-rate effect at D=4 Gy:")
    print(f"     SF acute (10 Gy/h)     = {c23['NHEJ_sf_acute']:.4f}")
    print(f"     SF min in LDR window   = {c23['NHEJ_sf_min_LDR_window']:.4f}")
    print(f"     IDRE ratio (min/acute) = {c23['NHEJ_idre_ratio_min_over_acute']:.3f}")
    print(f"     PASS criterion: ratio < 0.95 -> {c23['idre_ok']}")
    print()

    summary = {
        "C1_acute_LQ_ordering": {"SF_at_2Gy": sf2, "pass": bool(c1_ok)},
        "C2_dose_rate_sparing_WT_HR": {
            "WT_ratio_LDR_over_acute": c23["sparing_WT_ratio_LDR_over_acute"],
            "HR_ratio_LDR_over_acute": c23["sparing_HR_ratio_LDR_over_acute"],
            "pass": bool(c23["sparing_ok"]),
        },
        "C3_NHEJ_IDRE": {
            "SF_acute": c23["NHEJ_sf_acute"],
            "SF_min_in_LDR_window": c23["NHEJ_sf_min_LDR_window"],
            "ratio_min_over_acute": c23["NHEJ_idre_ratio_min_over_acute"],
            "pass": bool(c23["idre_ok"]),
        },
        "overall_pass": bool(c1_ok and c23["sparing_ok"] and c23["idre_ok"]),
        "notes": (
            "Smoke model: LQ + Lea-Catcheside G(lambda) with an NHEJ-specific "
            "low-dose-rate alpha-boost term to represent accumulated unrepaired "
            "DSBs. Anchored qualitatively to PMC10727999 panel ordering. "
            "Absolute parameters are illustrative; we do NOT claim to reproduce "
            "specific Buglewicz 2024 survival values, which are paywalled."
        ),
    }

    with open(os.path.join(DATA, "smoke_summary.json"), "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Wrote {os.path.join(DATA, 'smoke_summary.json')}")

    # Try to render figures (skip silently if matplotlib unavailable)
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(6, 4.5))
        for name in PANEL:
            ax.semilogy(doses_c1, sf_c1[name], label=name)
        ax.set_xlabel("Dose (Gy)")
        ax.set_ylabel("Surviving fraction (acute LQ)")
        ax.set_title("C1: CHO panel acute LQ survival (smoke)")
        ax.legend(); ax.grid(True, which="both", alpha=0.3)
        fig.tight_layout()
        fig.savefig(os.path.join(FIGS, "acute_survival.png"), dpi=120)
        plt.close(fig)

        fig, ax = plt.subplots(figsize=(6, 4.5))
        for name in PANEL:
            ax.semilogx(dots, sf_c23[name], label=name)
        ax.set_xlabel("Dose rate (Gy/h)")
        ax.set_ylabel("Surviving fraction at D = 4 Gy")
        ax.set_title("C2/C3: dose-rate dependence (smoke) — NHEJ IDRE visible")
        ax.legend(); ax.grid(True, which="both", alpha=0.3)
        fig.tight_layout()
        fig.savefig(os.path.join(FIGS, "dose_rate_sparing.png"), dpi=120)
        plt.close(fig)
        print(f"Wrote figures to {FIGS}/")
    except Exception as e:
        print(f"(matplotlib unavailable: {e}) — skipped figure rendering")

    return 0 if summary["overall_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
