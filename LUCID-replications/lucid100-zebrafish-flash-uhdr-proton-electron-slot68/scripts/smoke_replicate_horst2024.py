#!/usr/bin/env python3
"""
smoke_replicate_horst2024.py
=============================

Minimal smoke-replication scaffold for:
  Horst, Bodenstein, Brand, Hans, Karsch, Leßmann, Löck, Schürer, Pawelke,
  Beyreuther (2024). "Dose and dose rate dependence of the tissue sparing
  effect at ultra-high dose rate studied for proton and electron beams using
  the zebrafish embryo model." Radiother Oncol 194:110197.
  DOI: 10.1016/j.radonc.2024.110197

This script has TWO modes:

  --mode synthetic   (default; runs today, no PDF needed)
      Synthesizes plausible UHDR + CONV dose-response curves consistent
      with the abstract's anchor numbers:
        - dose range 15-95 Gy
        - three beams: proton entrance, proton SOBP, 30 MeV electrons
        - four morphological endpoints (pericardial edema, curved spine,
          embryo length [thresholded], eye diameter [thresholded])
        - dose-dependent FMF saturating at ~0.7-0.8 for D >= 50 Gy
      Fits a 4-parameter sigmoidal dose-response per (beam, endpoint, rate),
      computes D50 per group, and FMF(D) = D50_CONV / D50_UHDR.
      Output: tells you whether the fit machinery faithfully recovers the
      planted FMF values (sanity check on the pipeline itself).

  --mode real        (requires data/horst2024_doseresponse.csv to exist)
      Same fits, but using a CSV digitized by hand from Figures 2/3/4 of
      the paper (WebPlotDigitize or similar).  Expected schema:

        beam,endpoint,dose_Gy,dose_rate_Gy_per_s,fraction_affected,n_embryos

      where:
        beam            in {"proton_entrance","proton_SOBP","electron_30MeV"}
        endpoint        in {"pericardial_edema","curved_spine",
                            "embryo_length","eye_diameter"}
        fraction_affected   0.0 - 1.0  (probability of affected endpoint)
        n_embryos           per-dose group size (used for binomial weights)

Author: LUCID100 backfill subagent, 2026-06-09.
License: same as the LUCID-replications repo.
"""
from __future__ import annotations

import argparse
import csv
import math
import os
import sys
from pathlib import Path

import numpy as np

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from scipy.optimize import curve_fit
except Exception as e:  # pragma: no cover
    print(f"[FATAL] missing scientific Python stack: {e}", file=sys.stderr)
    print("        pip install numpy scipy matplotlib", file=sys.stderr)
    sys.exit(2)


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DATA = ROOT / "data"
FIG = ROOT / "figures"
FIG.mkdir(exist_ok=True, parents=True)
DATA.mkdir(exist_ok=True, parents=True)

BEAMS = ("proton_entrance", "proton_SOBP", "electron_30MeV")
ENDPOINTS = ("pericardial_edema", "curved_spine", "embryo_length", "eye_diameter")
RATE_UHDR_GyPs = 100.0     # representative UHDR, abstract says ~10^2 Gy/s class
RATE_CONV_GyPs = 0.1       # representative CONV, abstract says reference dose rate

# Anchor values from the abstract / context (Wu 2024 meta + Horst 2024 abstract):
#   - Proton RBE (SOBP > entrance) is real and known.
#   - UHDR FMF saturates ~ 0.7-0.8 for D >= 50 Gy.
# We seed D50_CONV per (beam, endpoint) and an FMF target per beam, then
# back-out D50_UHDR = D50_CONV / FMF.  (FMF = D50_CONV / D50_UHDR by definition
# used in the paper.  A smaller D50_UHDR would mean worse sparing; FMF<1 means
# UHDR needs MORE dose to reach the same iso-effect, i.e. sparing.)
SEED_D50_CONV = {
    # endpoint              proton_entrance  proton_SOBP  electron_30MeV
    "pericardial_edema":   {"proton_entrance": 32, "proton_SOBP": 28, "electron_30MeV": 38},
    "curved_spine":        {"proton_entrance": 36, "proton_SOBP": 31, "electron_30MeV": 42},
    "embryo_length":       {"proton_entrance": 40, "proton_SOBP": 34, "electron_30MeV": 46},
    "eye_diameter":        {"proton_entrance": 42, "proton_SOBP": 36, "electron_30MeV": 48},
}
# FMF target by beam (saturating value), shared across endpoints per paper:
SEED_FMF_SAT = {"proton_entrance": 0.78, "proton_SOBP": 0.74, "electron_30MeV": 0.80}
SLOPE = 3.5  # Hill slope k for the sigmoidal


def sigmoid(D, D50, k):
    """4-param sigmoidal dose-response squashed to 2 free params (asymptote=1)."""
    D = np.asarray(D, dtype=float)
    return 1.0 / (1.0 + (D50 / np.clip(D, 1e-3, None)) ** k)


def synthesize(seed: int = 17):
    rng = np.random.default_rng(seed)
    doses = np.array([15, 20, 25, 30, 35, 40, 50, 60, 70, 80, 95], dtype=float)
    rows = []
    for beam in BEAMS:
        for endpoint in ENDPOINTS:
            d50_conv = SEED_D50_CONV[endpoint][beam]
            fmf_sat = SEED_FMF_SAT[beam]
            d50_uhdr = d50_conv / fmf_sat  # since FMF = D50_CONV / D50_UHDR
            for rate, d50 in (
                (RATE_CONV_GyPs, d50_conv),
                (RATE_UHDR_GyPs, d50_uhdr),
            ):
                p_true = sigmoid(doses, d50, SLOPE)
                # simulate ~30 embryos per dose with binomial noise + 2% baseline
                n = np.full_like(doses, 30, dtype=int)
                affected = rng.binomial(n, np.clip(0.02 + 0.96 * p_true, 0, 1))
                frac = affected / n
                for D, f, ni in zip(doses, frac, n):
                    rows.append(
                        dict(
                            beam=beam,
                            endpoint=endpoint,
                            dose_Gy=float(D),
                            dose_rate_Gy_per_s=rate,
                            fraction_affected=float(f),
                            n_embryos=int(ni),
                        )
                    )
    return rows


def load_csv(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"missing real-data CSV: {path}")
    with path.open() as fh:
        rdr = csv.DictReader(fh)
        rows = []
        for r in rdr:
            rows.append(
                dict(
                    beam=r["beam"],
                    endpoint=r["endpoint"],
                    dose_Gy=float(r["dose_Gy"]),
                    dose_rate_Gy_per_s=float(r["dose_rate_Gy_per_s"]),
                    fraction_affected=float(r["fraction_affected"]),
                    n_embryos=int(r["n_embryos"]),
                )
            )
    return rows


def fit_group(doses, frac, n):
    """Sigmoidal fit with binomial-derived weights; return D50, k, D50_se."""
    doses = np.asarray(doses, dtype=float)
    frac = np.clip(np.asarray(frac, dtype=float), 1e-3, 1 - 1e-3)
    n = np.asarray(n, dtype=float)
    # binomial std for weights
    sigma = np.sqrt(frac * (1 - frac) / np.maximum(n, 1)) + 0.01
    try:
        popt, pcov = curve_fit(
            sigmoid, doses, frac, p0=[float(np.median(doses)), 3.0],
            sigma=sigma, absolute_sigma=False, maxfev=20000,
            bounds=([1.0, 0.5], [200.0, 12.0]),
        )
        D50, k = popt
        perr = np.sqrt(np.diag(pcov))
        return D50, k, perr[0]
    except Exception:
        return float("nan"), float("nan"), float("nan")


def group_by(rows, keys):
    out = {}
    for r in rows:
        k = tuple(r[x] for x in keys)
        out.setdefault(k, []).append(r)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=("synthetic", "real"), default="synthetic")
    ap.add_argument("--csv", default=str(DATA / "horst2024_doseresponse.csv"))
    ap.add_argument("--seed", type=int, default=17)
    args = ap.parse_args()

    if args.mode == "synthetic":
        rows = synthesize(seed=args.seed)
        synth_csv = DATA / "synthetic_horst2024_like.csv"
        with synth_csv.open("w", newline="") as fh:
            w = csv.DictWriter(
                fh,
                fieldnames=[
                    "beam", "endpoint", "dose_Gy",
                    "dose_rate_Gy_per_s", "fraction_affected", "n_embryos",
                ],
            )
            w.writeheader()
            w.writerows(rows)
        print(f"[synthetic] wrote {len(rows)} rows -> {synth_csv}")
    else:
        rows = load_csv(Path(args.csv))
        print(f"[real] loaded {len(rows)} rows from {args.csv}")

    # group by (beam, endpoint, rate)
    fits = {}
    grp = group_by(rows, ["beam", "endpoint", "dose_rate_Gy_per_s"])
    for (beam, endpoint, rate), recs in grp.items():
        doses = [r["dose_Gy"] for r in recs]
        frac = [r["fraction_affected"] for r in recs]
        n = [r["n_embryos"] for r in recs]
        D50, k, D50_se = fit_group(doses, frac, n)
        fits[(beam, endpoint, rate)] = dict(D50=D50, k=k, D50_se=D50_se, n_pts=len(recs))

    # report + FMF
    print(f"\n{'beam':16s} {'endpoint':18s} {'rate':10s} {'D50_Gy':>8s} {'+/-':>6s} {'k':>5s}")
    for (beam, endpoint, rate), f in sorted(fits.items()):
        print(
            f"{beam:16s} {endpoint:18s} {rate:>10.2g} "
            f"{f['D50']:8.2f} {f['D50_se']:6.2f} {f['k']:5.2f}"
        )

    print(f"\n{'beam':16s} {'endpoint':18s} "
          f"{'D50_CONV':>9s} {'D50_UHDR':>9s} {'FMF':>6s}  {'flag':s}")
    fmf_summary = []
    for beam in BEAMS:
        for endpoint in ENDPOINTS:
            f_conv = fits.get((beam, endpoint, RATE_CONV_GyPs))
            f_uhdr = fits.get((beam, endpoint, RATE_UHDR_GyPs))
            if not f_conv or not f_uhdr:
                continue
            d_c, d_u = f_conv["D50"], f_uhdr["D50"]
            if math.isnan(d_c) or math.isnan(d_u) or d_u <= 0:
                continue
            fmf = d_c / d_u  # convention used here: FMF<1 => UHDR sparing
            flag = "SPARING" if fmf < 0.95 else ("FLAT" if fmf < 1.05 else "INVERTED")
            print(f"{beam:16s} {endpoint:18s} {d_c:9.2f} {d_u:9.2f} {fmf:6.3f}  {flag}")
            fmf_summary.append(
                dict(beam=beam, endpoint=endpoint,
                     D50_CONV=d_c, D50_UHDR=d_u, FMF=fmf, flag=flag)
            )

    # plot per-beam dose-response with UHDR vs CONV overlays
    for beam in BEAMS:
        fig, axes = plt.subplots(2, 2, figsize=(9, 7), sharex=True, sharey=True)
        for ax, endpoint in zip(axes.flatten(), ENDPOINTS):
            for rate, color, label in (
                (RATE_CONV_GyPs, "tab:blue", f"CONV ({RATE_CONV_GyPs} Gy/s)"),
                (RATE_UHDR_GyPs, "tab:red", f"UHDR ({RATE_UHDR_GyPs} Gy/s)"),
            ):
                pts = [r for r in rows if r["beam"] == beam
                       and r["endpoint"] == endpoint
                       and r["dose_rate_Gy_per_s"] == rate]
                if not pts:
                    continue
                D = np.array([p["dose_Gy"] for p in pts])
                F = np.array([p["fraction_affected"] for p in pts])
                ax.scatter(D, F, c=color, s=18, label=label, alpha=0.7)
                f = fits.get((beam, endpoint, rate))
                if f and not math.isnan(f["D50"]):
                    Dg = np.linspace(5, 110, 200)
                    ax.plot(Dg, sigmoid(Dg, f["D50"], f["k"]), color=color, lw=1.4)
                    ax.axvline(f["D50"], color=color, lw=0.6, ls=":")
            ax.set_title(endpoint, fontsize=10)
            ax.set_xlim(0, 110)
            ax.set_ylim(-0.05, 1.05)
            ax.grid(alpha=0.3)
            if endpoint == ENDPOINTS[0]:
                ax.legend(fontsize=8, loc="lower right")
        for ax in axes[-1]:
            ax.set_xlabel("Dose (Gy)")
        for ax in axes[:, 0]:
            ax.set_ylabel("Fraction affected")
        fig.suptitle(f"Smoke replication — Horst 2024 — beam = {beam}", fontsize=11)
        fig.tight_layout(rect=(0, 0, 1, 0.97))
        out = FIG / f"smoke_{beam}.png"
        fig.savefig(out, dpi=140)
        plt.close(fig)
        print(f"[plot] {out}")

    # FMF vs paper's stated 0.7-0.8 band
    if fmf_summary:
        fig, ax = plt.subplots(figsize=(6, 4))
        x_labels = []
        y_vals = []
        colors = []
        for i, row in enumerate(fmf_summary):
            x_labels.append(f"{row['beam'].split('_')[0][:2]}.{row['endpoint'][:5]}")
            y_vals.append(row["FMF"])
            colors.append({"proton_entrance": "tab:blue",
                           "proton_SOBP": "tab:purple",
                           "electron_30MeV": "tab:orange"}[row["beam"]])
        ax.bar(x_labels, y_vals, color=colors)
        ax.axhspan(0.70, 0.80, color="green", alpha=0.15,
                   label="Horst 2024 reported FMF band (≥50 Gy)")
        ax.axhline(1.0, color="k", lw=0.7, ls="--")
        ax.set_ylabel("FMF = D50_CONV / D50_UHDR")
        ax.set_title("FMF per beam × endpoint vs paper's reported band")
        ax.set_ylim(0.5, 1.1)
        ax.legend(fontsize=8)
        plt.xticks(rotation=60, ha="right", fontsize=8)
        fig.tight_layout()
        out = FIG / "smoke_FMF_summary.png"
        fig.savefig(out, dpi=140)
        plt.close(fig)
        print(f"[plot] {out}")

    print("\nDONE")


if __name__ == "__main__":
    main()
