#!/usr/bin/env python3
"""Minimal MEDRAS-MC smoke replication for Rumiantcev et al. 2023 RBE paper.

Goal: WITHOUT running TOPAS-nBio, exercise the downstream MEDRAS-MC repair
model on damage spectra that are *physical analogs* of the two radionuclides
in the paper, and check that the resulting initial-DSB RBE ordering is in
the right ballpark as the paper's (~2.14 for initial damage).

Approach:
  - "177Lu surrogate"  = electron / photon-like sparse damage, Z=0 in MEDRAS
    (177Lu betas have mean ~150 keV; the sparse-track regime is captured by
    Medras' Z=0 case, which is what McMahon's headline X-ray result uses)
  - "225Ac surrogate"  = monoenergetic alpha particles, Z=2, energies chosen
    to span the chain (5.83, 6.34, 7.07, 8.38 MeV). LETs derived from the
    Bethe range tables shipped with Medras (BechtleHelium.xlsx-equivalent
    is `Radial Energy Helium.xlsx`). LETs taken at the corresponding
    proton-equivalent ranges -- exact values are not critical here because
    MEDRAS just samples a Helium track-structure distribution for Z=2.
  - Doses 0.1, 0.5, 1, 2 Gy with 3 repeats per condition.
  - Run Medras `Fidelity` repair simulation and read initial / residual
    DSBs from stdout.

This is a sanity check, NOT a re-derivation of the paper's TOPAS-nBio +
PSMA-source-point output.
"""
from __future__ import annotations

import contextlib
import io
import os
import re
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
WORKDIR = HERE.parent
RESULTS = WORKDIR / "results"
LOGS = WORKDIR / "logs"
FIGURES = WORKDIR / "figures"
SDD_OUT = RESULTS / "sdd_smoke"
for p in (RESULTS, LOGS, FIGURES, SDD_OUT):
    p.mkdir(parents=True, exist_ok=True)

MEDRAS_REPO = (Path.home() / "Dropbox/REPLICATE-PROJECT/LUCID-replications/"
               "lucid-medras-mc/Medras-MC").resolve()
sys.path.insert(0, str(MEDRAS_REPO))

# Conditions:
# (label, Z, energy_MeV, LET_keV_per_um, dose_Gy)
# 225Ac α energies: 5.830 (225Ac), 6.340 (221Fr), 7.067 (217At), 8.376 (213Po).
# LETs at these energies in liquid water ≈ 80, 76, 70, 60 keV/µm (NIST ASTAR).
ALPHA_LINES = [
    ("225Ac_5.83MeV", 2, 5.83, 80.0),
    ("221Fr_6.34MeV", 2, 6.34, 76.0),
    ("217At_7.07MeV", 2, 7.07, 70.0),
    ("213Po_8.38MeV", 2, 8.38, 60.0),
]
ELECTRON_LINE = ("177Lu_electron", 0, 1.0, 0.0)  # Z=0 sparse damage analog

DOSES = [0.1, 0.5, 1.0, 2.0]
REPEATS = 3   # MEDRAS internal repeats per exposure for damage generation
RUNS_REPAIR = 20   # repeats for the repair fidelity analysis


def generate_sdd_files() -> list[Path]:
    from damagegenerator import damageModel

    written = []
    old_cwd = os.getcwd()
    try:
        os.chdir(SDD_OUT)
        # 177Lu surrogate: monoenergetic electron at 1 MeV (sparse damage, Z=0)
        label, Z, energy, LET = ELECTRON_LINE
        for dose in DOSES:
            damageModel.generateExposure(
                energy=energy, LET=LET, dose=dose, particleZ=Z,
                runs=REPEATS, targetRadius=4.229, chromosomes=46,
                timeProfile=[0, 60 * 1e9 * 2],
            )
        # 225Ac chain: 4 alpha lines, equal weighting (smoke only)
        for label, Z, energy, LET in ALPHA_LINES:
            for dose in DOSES:
                damageModel.generateExposure(
                    energy=energy, LET=LET, dose=dose, particleZ=Z,
                    runs=REPEATS, targetRadius=4.229, chromosomes=46,
                    timeProfile=[0, 60 * 1e9 * 2],
                )
    finally:
        os.chdir(old_cwd)

    written = sorted(SDD_OUT.glob("*.txt"))
    return written


def run_repair() -> str:
    from repairanalysis import medrasrepair

    # match paper's MEDRAS settings: defaults are λf=2.07/h, λs=0.259/h,
    # repeats=50, simulationLimit=24 h, addFociDelay=True.
    # We lower repeats to 20 to keep the smoke fast.
    medrasrepair.repeats = RUNS_REPAIR
    buf = io.StringIO()
    sdd_path = str(SDD_OUT) + os.sep
    print(
        f"Running MEDRAS Fidelity (repeats={medrasrepair.repeats}, "
        f"limit={medrasrepair.simulationLimit} h, "
        f"failure={medrasrepair.repairFailure}, foci={medrasrepair.addFociDelay})"
    )
    with contextlib.redirect_stdout(buf):
        medrasrepair.repairSimulation(sdd_path, "Fidelity")
    out = buf.getvalue()
    (LOGS / "medras_smoke_repair.log").write_text(out)
    return out


# MEDRAS Fidelity output is tab-separated:
#   File \t Break Set \t Break Count \t Misrepair \t Stdev \t Inter-Chromosome Rate
# where Break Count is the initial DSB count for that exposure realization
# and Misrepair is the fractional misrepair (0..1).
# Residual DSBs are NOT directly reported in Fidelity mode; we use
# Break Count * Misrepair as a proxy for misrepaired DSBs and assume
# residual ≈ (Break Count) * residualFraction. Since MEDRAS Fidelity
# converges to ~0 residual at 24 h limit, we treat misrepaired+residual
# as Break Count * (Misrepair + residual_frac). For headline numbers we
# rely on Break Count (initial) only and on the misrepair fraction.
FNAME_RX = re.compile(r"^DNA Damage Z=(?P<Z>\d+)\s+(?P<E>[\d.]+) MeV (?P<D>[\d.]+) Gy")


def parse_summary(log: str):
    rows = []
    for line in log.splitlines():
        s = line.strip()
        if not s.startswith("DNA Damage Z="):
            continue
        parts = [p.strip() for p in re.split(r"\t+", s) if p.strip()]
        if len(parts) < 4:
            continue
        fname = parts[0]
        try:
            break_set = int(float(parts[1]))
            break_count = float(parts[2])
            misrepair_frac = float(parts[3])
        except ValueError:
            continue
        m = FNAME_RX.match(fname)
        if not m:
            continue
        rows.append(dict(
            fname=fname,
            Z=int(m.group("Z")),
            E_MeV=float(m.group("E")),
            dose_Gy=float(m.group("D")),
            break_set=break_set,
            init_DSB=break_count,           # MEDRAS reports per-set DSB count
            misrep_frac=misrepair_frac,
            misrep_DSB=break_count * misrepair_frac,
            resid_DSB=0.0,                  # 24h Fidelity ≈ fully resolved
        ))
    return rows


def main():
    t0 = time.time()
    skip_gen = os.environ.get("MEDRAS_SMOKE_SKIP_GEN") == "1"
    if skip_gen and any(SDD_OUT.glob("*.txt")):
        files = sorted(SDD_OUT.glob("*.txt"))
        print(f"[generate] SKIPPED, reusing {len(files)} SDD files in {SDD_OUT}")
    else:
        files = generate_sdd_files()
        print(f"[generate] {len(files)} SDD files in {SDD_OUT}, {time.time()-t0:.1f}s")
    log = run_repair() if not os.environ.get("MEDRAS_SMOKE_REUSE_LOG") else (LOGS / "medras_smoke_repair.log").read_text()
    t1 = time.time()
    rows = parse_summary(log)
    if not rows:
        print("WARNING: no rows parsed from Medras output. First 40 lines of log:")
        print("\n".join(log.splitlines()[:40]))
        return

    # Aggregate per (Z, dose), averaging over energies for Z=2 (chain proxy)
    import collections
    agg = collections.defaultdict(list)
    for r in rows:
        agg[(r["Z"], r["dose_Gy"])].append(r)

    csv_path = RESULTS / "medras_smoke_summary.csv"
    with csv_path.open("w") as f:
        f.write("Z,dose_Gy,n_realizations,mean_init_DSB,mean_misrep_frac,mean_misrep_DSB\n")
        for (Z, d), lst in sorted(agg.items()):
            mi = np.mean([r["init_DSB"] for r in lst])
            mf = np.mean([r["misrep_frac"] for r in lst])
            mm = np.mean([r["misrep_DSB"] for r in lst])
            f.write(f"{Z},{d},{len(lst)},{mi:.3f},{mf:.4f},{mm:.3f}\n")
    print(f"[summary] wrote {csv_path}")

    # Compute crude RBE_init using slopes through origin: b = DSB/dose averaged.
    # Average DSB counts across break_set realizations for each (Z, energy, dose),
    # then collapse over energy for Z=2 (alpha chain proxy).
    def slope(Z, field):
        xs = [(r["dose_Gy"], r[field]) for r in rows if r["Z"] == Z]
        if not xs:
            return None
        d = np.array([x[0] for x in xs])
        n = np.array([x[1] for x in xs])
        return float(np.dot(d, n) / np.dot(d, d))

    b_Lu = slope(0, "init_DSB")
    b_Ac = slope(2, "init_DSB")
    rbe_init = b_Ac / b_Lu if (b_Lu and b_Ac) else float("nan")

    bR_Lu = slope(0, "misrep_DSB")
    bR_Ac = slope(2, "misrep_DSB")
    rbe_resid = bR_Ac / bR_Lu if (bR_Lu and bR_Ac) else float("nan")

    summary = (
        f"\n=== MEDRAS smoke RBE summary ===\n"
        f"  total wall time           : {t1-t0:.1f} s\n"
        f"  parsed condition rows     : {len(rows)}\n"
        f"  b_Lu_initial   (Z=0)      : {b_Lu:.3f} DSB/Gy\n"
        f"  b_Ac_initial   (Z=2, α)   : {b_Ac:.3f} DSB/Gy\n"
        f"  RBE_initial_smoke         : {rbe_init:.3f}     (paper init RBE ~2.14)\n"
        f"  b_Lu_misrepaired          : {bR_Lu:.3f} DSB/Gy\n"
        f"  b_Ac_misrepaired          : {bR_Ac:.3f} DSB/Gy\n"
        f"  RBE_misrepaired_smoke     : {rbe_resid:.3f}   (paper Eq.7 low-D limit ≈ 9.4)\n"
        f"\n  Notes:\n"
        f"   - MEDRAS Fidelity mode reports per-set DSB count (initial) and misrepair\n"
        f"     fraction; residual DSBs at the 24h limit are ~0 by construction.\n"
        f"   - The 'misrepaired DSB' RBE is the closest analog to the paper's\n"
        f"     post-repair RBE (residual + misrepaired); not directly comparable.\n"
    )
    print(summary)
    (LOGS / "smoke_summary.txt").write_text(summary)


if __name__ == "__main__":
    main()
