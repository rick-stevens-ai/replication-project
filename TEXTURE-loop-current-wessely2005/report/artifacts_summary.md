# Artifacts Summary — arXiv:cond-mat/0511224

**Paper:** Wessely, Skubic, Nordström, "Current driven magnetization dynamics in helical spin density waves," arXiv:cond-mat/0511224 → PRB 73, 144431 (2006).
**Class as filed:** loop-current. **Actual:** STT in helical spin density wave (**MISCLASSIFIED** — kagome loop-current kernel not applicable, not imported).

## Files (8-artifact bar)
| Artifact | Path | Status |
|---|---|---|
| Extraction marker | `extraction/marker.md` | ✅ |
| Paper text | `work/paper.txt` (pdftotext -layout) | ✅ |
| Model code | `code/stt_helical_sdw.py` | ✅ runs |
| Driver/checks | `code/run_replication.py` | ✅ runs |
| Numeric results | `work/results.json` | ✅ |
| Report | `report/REPORT.tex` (+ .pdf if latex) | ✅ |
| Open questions (5) | `report/open_questions.json` | ✅ exactly 5 |
| Workflow | `report/workflow.md` | ✅ |
| Artifacts summary | `report/artifacts_summary.md` | ✅ (this) |
| Failure analysis | `report/failure_analysis.md` | ✅ |

## Quantitative comparison
| # | Claim | Paper | Computed | Verdict |
|---|---|---|---|---|
| C1 | C-tensor structure (axis current → single rotate-spiral torque; out-of-plane spin flux = 0) | C = ħ[[0,0,0],[0,0,0.5],[0,0,0]] (single nonzero) | rotate=0.0282, out-of-plane=−2e−16, Sx=Sy=0.0282, Sz≈0 | ✅ PASS |
| C3 | \|P\|=0.5 → tilt from axis | 30° | 30.0000° | ✅ PASS |
| C4 | q=0.20·2π/c → phase per atomic layer | 0.20·π = 0.6283 rad | 0.6283 rad | ✅ PASS |
| C5 | rotation freq ∝ current | linear | max deviation 3.5e−18 (linear) | ✅ PASS |
| C6 | crude analytic / microscopic ratio | ~4× | 0.155 (model-dependent) | ⚠️ PARTIAL (honest negative) |
| — | absolute freq at 1e7 A/cm² | 0.07 GHz | not recomputed (DFT-specific) | ⬜ out of scope |

**Machine-checkable pass rate: 4/5.**

## Key reproduced physics
- Single-nonzero-component torque–current tensor: a current **along** the spiral axis rigidly rotates/slides the planar spiral; out-of-plane spin flux vanishes (planarity confirmed to machine precision, Sx=Sy exactly).
- Geometry: |P|=0.5 ⟺ 30° spin tilt; q=0.20·2π/c ⟺ 0.20π rad per atomic layer.
- Strict linear scaling of the induced torque with current density (bulk linear-response STT).

## Honest caveats
- Toy 1D tight-binding spin-spiral model, NOT Er DFT. Absolute numbers (0.07 GHz, C₂₃=0.5 ħ Å²) intentionally not reproduced.
- C6 numeric factor (~4×) is model-dependent and did not reproduce; reported as-is, not tuned.
