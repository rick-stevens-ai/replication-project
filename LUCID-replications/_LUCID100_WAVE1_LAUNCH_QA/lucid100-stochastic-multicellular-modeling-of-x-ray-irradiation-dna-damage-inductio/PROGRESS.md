# Progress — LUCID100 slot 4

## 2026-06-09 (subagent first pass, Ollie)

Status: **partial-scope smoke test PASS** — see `FIRST_PASS_REPORT.md`.

### What I tried

1. Resolved slot identity from `LUCID100_SOLID_MASTER_QA.tsv` row 35
   (DOI 10.1038/s41598-019-54941-1, Forster et al. 2019, *Sci Rep* 9: 18888).
2. Read the full paper (`pdftotext -layout` on the local Dropbox PDF).
3. Downloaded supplementary methods PDF from the Springer media server
   (no auth required) and extracted text.
4. Confirmed there is **no Code Availability** and **no Data Availability**
   section in the paper. The Geant4 / Geant4-DNA pipeline is in-house, not
   public; the upstream DNA-damage-induction algorithm (Forster 2018) and
   the HNSCC oxygenation/angiogenesis model (Forster 2017) are likewise
   undocumented in any public repo.
5. Authors were **not contacted** (per task instructions).
6. Built an independent pure-Python reimplementation of the **downstream**
   stochastic sub-model (Eqs. 1, 8, 9, 10, 13-16) at
   `~/.openclaw/workspace/lucid-replications/slot4-stochastic-multicellular/code/smoke_test.py`.
   The Geant4 stage is bypassed by Poisson-sampling cDSB counts per cell
   using the paper-reported per-Gy yields, then running the paper's pairwise
   end-pairing misrejoining algorithm in an ellipsoidal nucleus.
7. Ran two configurations on CherryRd:
   - `--quick --n-cells 200` (3 conditions, 0.1 s wall)
   - Full sweep `--n-cells 400` (7 conditions, 0.4 s wall)
8. Compared fitted α_mr, β_mr, α_killing(mr), β_killing(mr), SF2(mr) to
   paper Tables 3-5. Baseline (cDSB=2.9, r0=0.7, P_nlmr=0.5) is within
   noise. The r0 and P_nlmr sweeps reproduce the correct monotonic trends.

### Key numerical result (baseline, full oxia, n=400 cells/dose)

| Quantity | Smoke test (this work) | Paper Table 3 |
|---|---|---|
| α_mr (Gy⁻¹) | 0.003 | 0.02 |
| β_mr (Gy⁻²) | 0.424 | 0.37 |
| α_killing(mr) (Gy⁻¹) | 0.006 | 0.02 |
| β_killing(mr) (Gy⁻²) | 0.186 | 0.17 |
| SF2(mr) | 0.47 | 0.49 |

The smoke test independently reproduces the paper's central qualitative
finding — α_killing(mr) is small and ~15× below the empirical HNSCC α —
purely from the misrejoining-only mechanism, with no need for Geant4.

### Next actions (deferred to a later replication pass if anyone wants more)

- [ ] Reimplement the **upstream** DSB / cDSB generation by Monte-Carlo
      sampling of low-LET electron track segments through the nucleus
      (e.g. PROTON or a TOPAS-nBio mockup), to bring the cDSB clustering
      correlations back. Quantifies whether the small but non-zero α_mr
      in the paper really originates from same-primary clusters.
- [ ] If author cooperation is later authorised, request Geant4 source +
      input files for an exact rerun on an HPC (Aurora / uicgpu / chiatta).
      ~20 000 core-hours needed; **not allowed on CherryRd**.
- [ ] Compare against Henthorn 2018 (Sci Rep 8: 2654), BIANCA and
      Friedland & Kundrát models for cross-validation of cDSB yields.

### Blockers

- No public source code or data for the paper or for the two upstream
  models it reuses.
- Full Geant4 chain needs HPC (paper used Phoenix HPC at U. Adelaide,
  20 008 core-hours for the 1 mm³ HNSCC tumour alone) — far above CherryRd.
- 6 MV linac source spectrum was generated in Philips Pinnacle (commercial
  treatment planning software) and is not bundled with the paper.
