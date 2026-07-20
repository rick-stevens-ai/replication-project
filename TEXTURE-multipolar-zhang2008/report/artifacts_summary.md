# Artifacts Summary — arXiv:0805.3922 replication

## Paper
Zhang, Cheng, Guo, Feng, "Magnetic field induced incommensurate resonance in
cuprate superconductors," arXiv:0805.3922v2 (2008).
(NB: task label "multipolar texture" does not match this paper — see marker.md.)

## Files
| Path | What |
|---|---|
| `paper.pdf` / `paper.txt` | source + extracted text |
| `extraction/marker.md` | central claims, params, method, scope, label-mismatch flag |
| `code/model.py` | MF spin mode ω_k, schematic Σ, S(k,ω) via Eq.8, peak/δr tools |
| `code/run_checks.py` | runs 5 claim checks → results.json + 3 PNGs |
| `work/results.json` | all computed numbers |
| `work/fig_cut.png` | S along (k_x,π) at ω=0.31J, B=0 vs B~20T |
| `work/fig_delta_vs_field.png` | δr vs field (Eq.9 analytic; cf. Fig.3) |
| `work/fig_omega_spin.png` | MF spin excitation along (k_x,π) |
| `report/REPORT.tex` (+ .pdf) | full writeup |
| `report/open_questions.json` | exactly 5 open questions |
| `report/workflow.md` | reproduce steps |
| `report/failure_analysis.md` | limitations + honest negative result |

## Quantitative comparison
| Claim | Paper | This replication | Verdict |
|---|---|---|---|
| 1. Zeeman branch splitting = 4ε_B (Eq.4) | ω_k±2ε_B | 0.0400 vs 0.0400 (err 3e-17) | ✅ exact |
| 5. ε_B↔B mapping internal consistency | 1.2meV↔20T, 0.24↔4, 0.6↔10 | single slope, all 3 reproduce | ✅ consistent |
| 5b. implied g-factor | (implicitly Cu2+) | g≈1.04 (not ~2.0-2.2) | ⚠️ discrepancy flagged |
| 2/3. commensurate→IC transition (raw S-scan) | yes | dispersion-dominated, no transition | ❌ out of reach (needs full Σ) |
| 2/3b. transition via Eq.9 analytic isolation | commensurate→IC, δr↑ with B | commensurate ≤6T, IC above, monotonic | ✅ mechanism reproduced |
| 3. critical field | Bc1≈4T, Bc2≈10T | Bc≈6.2T (between 4 and 10) | ✅ bracketed |
| 4. energy selectivity (frac shift 2ε_B/ω) | high-E robust, low-E sensitive | 2.9%@0.7J, 6.5%@0.31J, 20%@0.1J | ✅ consistent |
| 4b. hourglass breakdown scale | ω<0.16J≈19meV | 2ε_B/ω=0.125 at ω=0.16J | ✅ scale reproduced |

## Verdict
**PARTIAL REPLICATION — mechanism confirmed, full quantitative map out of scope.**
The paper's core analytic mechanism (Zeeman branch splitting, the (ω−2ε_B)
incoming-neutron shift, field-driven commensurate→IC resonance splitting, the
critical-field scale, and the energy-selectivity/hourglass-breakdown scaling) is
reproduced by a minimal model. The self-consistent self-energy needed for the
exact δr(B) curve and 2D S(k,ω) maps was declared out of scope; one direct check
(raw S-scan) honestly failed for that reason and the analytic Eq.9 isolation was
used to recover the mechanism. Plus one genuine finding: the paper's field-energy
conversion implies g≈1.

- **Coverage: 7/10** (5 of 6 claim-families addressed with real computation; full
  self-consistent Σ and 2D maps not attempted).
- **Agreement: 8/10** (branch splitting exact; scaling & critical-field checks
  consistent/bracketed; one honest failure of the raw S-scan; one flagged
  g-factor discrepancy).
