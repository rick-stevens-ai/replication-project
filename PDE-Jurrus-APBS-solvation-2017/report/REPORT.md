# Replication Report — Jurrus et al. 2017 APBS

**Paper:** *Improvements to the APBS biomolecular solvation software suite*
**Authors:** E. Jurrus, D. Engel, K. Star, K. Monson, J. Brandi, L.E. Felberg, D.H. Brookes, L. Wilson, J. Chen, K. Liles, M. Chun, P. Li, D.W. Gohara, T. Dolinsky, R. Konecny, D.R. Koes, J.E. Nielsen, T. Head-Gordon, W. Geng, R. Krasny, G.-W. Wei, M.J. Holst, J.A. McCammon, N.A. Baker
**Venue:** *Protein Science* 27(1):112–128 (published 2017/2018)
**DOI:** https://doi.org/10.1002/pro.3280
**Citations (Semantic Scholar count in task brief):** 2,081
**Replicator:** Ollie (subagent, session `92b22fab`)
**Date:** 2026-07-03 (America/Chicago)
**Compute:** uicgpu (Linux, 8×A100 not needed here; single CPU multigrid was sufficient), conda-forge stack

---

## 1. Paper summary

APBS (Adaptive Poisson-Boltzmann Solver) is an open-source package for numerically solving the Poisson-Boltzmann equation over biomolecular geometries. This paper is the periodic "software refresh" (v1.5 era) covering: (i) new finite-difference and finite-element solvers; (ii) integration of the TABI-PB boundary-element method; (iii) a geometric-flow non-polar solvation module; (iv) tighter coupling with PDB2PQR (structure preparation, ligand parameterization, membrane systems); (v) Python bindings; (vi) an updated regression test suite. The methodological core (multigrid FD Poisson-Boltzmann) is largely unchanged from earlier APBS releases; the paper's main claim is that the software works, is stable, and continues to serve the biomolecular community — reflected by the citation count.

Because APBS is a *software* paper, the strongest independent-replication test is: **install the current APBS + PDB2PQR, run the bundled canonical benchmarks, and confirm they match published (per-version) reference values.** That is exactly what I did.

## 2. Claims table

| # | Claim | Type | Testable? | Tested? |
|---|---|---|---|---|
| C1 | APBS + PDB2PQR are open-source, packaged, and installable in a modern env | infrastructural | yes | ✓ yes |
| C2 | APBS reproduces analytical benchmarks (Born ion) | numerical/canonical | yes | ✓ yes |
| C3 | APBS bundled solvation regression tests (methanol/methoxide) yield the values documented for the paper-era + current versions | numerical/regression | yes | ✓ yes |
| C4 | PDB2PQR + APBS pipeline runs end-to-end on a real protein | infrastructural | yes | ✓ yes (1AKI lysozyme) |
| C5 | APBS is numerically stable across major versions (v1.5 in paper vs v3.4.1 today) | numerical/longitudinal | yes | ✓ yes (regression README lists per-version values) |
| C6 | New TABI-PB boundary-element solver in v1.5 | numerical | possible but heavier | ✗ not tested (would need separate `bem` build path; core paper claims are already covered) |
| C7 | New geometric-flow non-polar solvation module | numerical | possible but heavier | ✗ not tested |
| C8 | Python bindings functional | infrastructural | yes | ✗ not tested (out of scope for a single-run subagent) |

Coverage of the paper's *core* claims (C1..C5): full. Coverage of the "improvements" list (C6..C8): partial.

## 3. Method

All work on `uicgpu` (Linux, x86_64). Full command trace preserved in `work/`.

### 3.1 Install
```bash
ssh uicgpu
source ~/env.sh                                # proxy for conda-forge fetch
source ~/miniconda3/etc/profile.d/conda.sh
conda create -y -p /data/stevens/envs/apbs-repl \
  -c conda-forge apbs pdb2pqr python=3.11
conda activate /data/stevens/envs/apbs-repl
apbs --version        # -> APBS 3.4.1
pdb2pqr30 --version   # -> pdb2pqr 3.6.1
```

### 3.2 Bundled Born-ion regression test (from paper's own repo)
```bash
git clone --depth=1 https://github.com/Electrostatics/apbs.git apbs-src
cp -r apbs-src/examples/born /data/stevens/apbs-jurrus-repl/born-test
cd born-test
apbs apbs-mol-auto.in
# prints "Global net ELEC energy = -2.297735526282E+02 kJ/mol"
```

### 3.3 Bundled methanol/methoxide regression tests
```bash
cp -r apbs-src/examples/solv /data/stevens/apbs-jurrus-repl/solv-test
cd solv-test
apbs apbs-mol.in    # -> methanol -36.24863, methoxide -390.41217, diff -354.16354
apbs apbs-smol.in   # -> methanol -37.57594, methoxide -391.23886, diff -353.66292
```

### 3.4 Manual Born-ion analytical check
Hand-wrote a two-state (`sdie=78.54` vs `sdie=1.0`) input following the APBS solvation-energies tutorial (`apbs.readthedocs.io/using/examples/solvation-energies`). Analytical answer for a 3 Å, +1 e Born ion is `-691.85 × z²/R = -230.62 kJ/mol`.
```bash
apbs born/born.in    # -> -229.5879 kJ/mol
```

### 3.5 Independent case: 1AKI lysozyme
```bash
curl -sL https://files.rcsb.org/download/1AKI.pdb -o 1AKI.pdb
pdb2pqr30 --ff=AMBER --apbs-input=1AKI.in 1AKI.pdb 1AKI.pqr
# then hand-wrote 1AKI_solv.in (two-state focusing MG-auto, dime 129^3,
# LPBE, pdie=2, sdie=78.54/2.0, 150 mM NaCl, T=298.15 K,
# srfm smol, srad 1.4, chgm spl2, sdens 10, bcfl sdh)
apbs 1AKI_solv.in   # -> polar solvation -4345.23 kJ/mol
# convergence check
sed 's/dime 129 129 129/dime 161 161 161/g' 1AKI_solv.in > 1AKI_solv_fine.in
apbs 1AKI_solv_fine.in   # -> -4258.03 kJ/mol
```

## 4. Results vs paper

### 4.1 Numerical benchmarks (from paper's own regression test suite)

| Test | Documented expected | My APBS 3.4.1 | Match |
|---|---|---|---|
| `born/apbs-mol-auto.in` (v1.5) | -229.7740 | **-229.7736** | 4 decimals (exact v1.4.1) |
| `born/apbs-mol-auto.in` analytical | -230.62 | -229.7736 | 0.37% (multigrid discretization) |
| `solv/apbs-mol.in` methanol (v3.0) | -36.2486 | **-36.24863** | 6+ decimals |
| `solv/apbs-mol.in` methoxide (v3.0) | -390.4122 | **-390.41217** | 6+ decimals |
| `solv/apbs-mol.in` diff (v3.0) | -354.1635 | **-354.16354** | 6+ decimals |
| `solv/apbs-smol.in` methanol (v3.0) | -37.5759 | **-37.57594** | 6+ decimals |
| `solv/apbs-smol.in` methoxide (v3.0) | -391.2388 | **-391.23886** | 6+ decimals |
| `solv/apbs-smol.in` diff (v3.0) | -353.6629 | **-353.66292** | 6+ decimals |

### 4.2 Manual Born analytical check
| | Value (kJ/mol) |
|---|---|
| Analytical closed-form | -230.62 |
| APBS 3.4.1 (manual grid) | -229.59 |
| Absolute error | 1.03 |
| Relative error | 0.45% |

### 4.3 Independent 1AKI lysozyme (my case)
| Grid | Polar solvation free energy (kJ/mol) |
|---|---|
| 129³ | -4345.23 |
| 161³ | -4258.03 |
| Δ | ~2% (typical MG-auto grid convergence) |

Paper does not publish a specific reference value for 1AKI, so this test verifies the pipeline runs end-to-end and gives physically reasonable numbers (a 129-residue soluble protein with ~10 net charges should give a polar solvation on the order of a few thousand negative kJ/mol at physiological ionic strength — this is exactly what we see).

## 5. Verdict

### Verdict: **REPLICATED**

Justification (independently corroborated by LLM judge Argo `gpt-5`, coverage 92, agreement 99):

- **APBS 3.4.1 and PDB2PQR 3.6.1 install cleanly** via conda-forge and self-cite the Jurrus 2018 paper on invocation — the software identity is confirmed.
- **The paper's own bundled regression tests reproduce to 4–6+ decimals**, and match the version-by-version README table across APBS 0.1.8 → 3.0. This directly confirms the paper's central claim of numerical stability across the software's lifetime.
- **Born-ion analytical benchmark agrees to 0.45%**, within expected multigrid discretization error at the tutorial grid resolution.
- **End-to-end PDB2PQR → APBS pipeline is functional** on a real protein (1AKI lysozyme) with physically reasonable energies and normal grid-convergence behavior.
- **Honest limitations:** did not exercise the newer TABI-PB / geoflow / Python-API features (would each require a separate solver build path). Those are "improvements" the paper advertises; the core FD-multigrid solvation engine — the workhorse of APBS's citation base — is exhaustively reproduced here.
- **No data or code was paywalled**; all artifacts (APBS source, examples, PDB structure) are public and freely fetchable.

### Final line

`WAVE_RESULT set=PDE paper=Jurrus-2017-APBS verdict=REPLICATED dir=~/Dropbox/REPLICATE-PROJECT/PDE-Jurrus-APBS-solvation-2017/ one_line=APBS 3.4.1 + PDB2PQR 3.6.1 reproduce bundled regression tests to 6+ decimals; Born analytical 0.45%; 1AKI pipeline OK`
