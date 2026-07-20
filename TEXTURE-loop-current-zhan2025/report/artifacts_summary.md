# artifacts_summary.md

## Files
| Path | Description |
|---|---|
| `paper.pdf` / `paper.txt` | Source paper (arXiv:2506.01648v2) + extracted text |
| `extraction/marker.md` | Claim extraction + machine-checkable subset |
| `code/replicate_zhan2025.py` | Replication driver (imports shared kernel) |
| `work/results.json` | All numeric outputs |
| `work/run.log` | Full stdout of the run |
| `report/REPORT.tex` / `REPORT.pdf` | Writeup |
| `report/open_questions.json` | 5 open questions |
| `report/PROVENANCE.md` | Kernel reuse + scope |
| `report/workflow.md` | Reproduction steps |
| `report/failure_analysis.md` | Honest negatives + limits |

## Claim-by-claim results

### Claim A — bare kagome spectrum
- E(Γ) = [−4, 2, 2]; E(K) = [−1, −1, 2]; E(M) = [−2, 0, 2].
- Flat band at +2t (spread = 0). Dirac touching of the two lower bands at K (gap 0).
- **p-type VHS at E=0**: M-point middle band = 0.0 ✓; lower-band DOS log-peak at E=0 ✓.
- **PASS** — matches textbook kagome + the paper's "p-type VHS with µ=0" statement.

### Claim B — LCO imaginary bond order opens a full gap (Fig 3d)
- Folded 12-band model, Δ_1nn=0.1t, Δ_2nn=0.15t: multiple fillings acquire a
  positive **indirect** gap (e.g. filling 4: 0.028; filling 5: 0.032; filling 8: 0.030).
- **PASS (qualitative)** — the imaginary bond order gaps the Fermi surface, as claimed.

### Claim C — Chern insulator, total C=1 (Fig 3d)
- Chern by gapped filling: {4:+1, 5:+1, 8:+2, 10:−1}. A **total Chern C=1**
  is achieved at the physically relevant gapped fillings (4 and 5 of 12).
- Kernel cross-check: genuine staggered flux gives lower-band C=−1 (Haldane/OMN
  mechanism the paper invokes).
- **PASS** — reproduces the paper's headline C=1 quantum-anomalous-Hall claim.

### Claim D — Landau quartic selects 3Q
- Eq.(2) with Z1=1, Z2=0.4 (Z1−Z2=0.6>0): E(1Q)=0.5 > E(2Q)=0.35 > E(3Q)=0.30.
- 20k-sample simplex search converges to equal weights (0.58,0.58,0.58) → 3Q.
- **PASS** — equal-weight 3Q is the global minimum, exactly as the paper states
  (trilinear term vanishes by TRS breaking → 2×2 pattern).

### Claim E — TRS breaking (imag vs real bond) + 3Q ferromagnetism
- Imaginary bond order → loop current ⟨Im⟩ = −0.195 (≠0). Real bond → charge
  ⟨Re⟩ = 0.220, with loop current −0.013 (≈0, residual from the closed-form
  gauge; see failure_analysis).
- 3Q (1,1,1) → magnetic dipole = 1 (ferromagnetic); 2Q (1,1,0) → dipole 0
  (AFM); 2Q3 (1,0,−1) → octupole ≠0.
- **PASS (qualitative)** — loop current arises from the imaginary channel; 3Q
  carries a net FM orbital moment (paper: ~0.03 µB/site in FeGe).

## Overall
Coverage 8/10 · Agreement 8/10 · Verdict: **REPRODUCED (in-scope claims)**.
FRG phase diagram out of scope (documented).
