# Artifacts Summary — OSTI 3020556

**Paper:** Powis et al 2026, PSST **35** 025002 — 2D E×B Penning-spoke community benchmark.
**Verdict:** REPLICATED (analytic core; C6 full-PIC not attempted).

---

## Primary sources

| File | Role | Source | MD5 (prefix) | Notes |
|---|---|---|---|---|
| `work/osti_3020556.pdf` | Target paper (OA) | https://www.osti.gov/servlets/purl/3020556 | `be1c310a…` | Digital PDF, no OCR needed |
| `work/ref93_powis2018_arxiv1805.04438.pdf` | Formula source (Ref [93] → CSHI Eq.4) | https://arxiv.org/pdf/1805.04438 | `6f7769ad…` | Powis 2018 |

## Code (reimplementation)

| File | Purpose |
|---|---|
| `work/replicate_spoke.py` | Reimplements Ref [93] Eq.4 from first principles: computes f_s,th, characteristic velocity, R_0 back-solve, 1/√m_i mass scaling (He → Ar), He-4 mass = amu consistency, E×B kinematic cross-check. Emits `evidence_spoke.json`. |
| `work/judge.py` | Sends claims + reproduced numbers to Argo `argo:gpt-5.2` (free endpoint at `http://127.0.0.1:44497/v1`, temp 0). Emits `judge_result.json`. |

## Evidence

| File | Contents |
|---|---|
| `report/evidence/evidence_spoke.json` | All reproduced numeric values with units (f_s,th at 25 mm = 52.69 kHz; at back-solved R_0 = 53.00 kHz; characteristic velocity 4.14 km/s; theory/measured ratio 1.227; He-4 mass 4.000 amu; f_Ar/f_He = 0.3162 → f_Ar ≈ 16.8 kHz; v_ExB = 10 km/s → E×B kinematic 64 kHz; spoke/E×B = 0.67). |
| `report/evidence/judge_result.json` | Argo gpt-5.2 output: `{agreement_pct: 95, verdict: "REPLICATED", coverage: "...", justification: "..."}` |

## Reports (this bundle)

| File | Kind | Notes |
|---|---|---|
| `report/REPORT.md` | Markdown (primary human-readable) | 9 KB; verdict block + WAVE_RESULT trailer. |
| `report/REPORT.tex` | LaTeX (typeset version) | Includes dedicated **GENUINE CRITIQUE** section beyond REPORT.md. |
| `report/open_questions.json` | 5 open scientific questions | E×B / Penning-spoke domain; each with basis + next_steps. |
| `report/workflow.md` | End-to-end pipeline description | 7 stages: harvest → extract → resolve formula → reimplement → LLM-judge → write → backfill. |
| `report/artifacts_summary.md` | This file | Index of all artifacts. |
| `report/failure_analysis.md` | Explicit not-attempted / limitations record | Full 2D PIC (C6), uncertainty propagation, back-solve circularity. |

## Headline reproduced numbers

- **f_s,th @ R_0 = 25 mm:** 52.69 kHz (paper: ~53 kHz; match −0.6%)
- **f_s,th @ back-solved R_0 = 24.85 mm:** 53.00 kHz (self-consistency, <0.01%)
- **Theory/measured ratio:** 53 / 43.2 = 1.227 (matches exactly)
- **He-4 mass consistency:** 7291.712 mₑ = 4.000 amu (4-decimal match)
- **1/√m_i scaling:** f_Ar / f_He = 0.3162 → f_Ar ≈ 16.8 kHz (verified analytically)
- **E×B kinematic cross-check:** v_ExB = 10 km/s → 64 kHz; measured spoke/E×B ≈ 0.67 (consistent with Ref [93])

## Compute / provenance

- **Host:** uicgpu (for PDF fetch via `~/env.sh` proxy).
- **Language:** Python 3 (standard SI constants only).
- **LLM judge:** Argo `argo:gpt-5.2` @ `http://127.0.0.1:44497/v1`, temperature 0 (free endpoint).
- **Cost:** $0 (all free endpoints, one small analytic script).
- **Runtime:** analytic script <1 s; judge call ~seconds; total wall clock well under 25-min budget.

## What is intentionally NOT in this bundle

- Any full 2D PIC output (density/potential/temperature profiles) — C6 was out of scope.
- Any independent reimplementation of Ref [93]'s dispersion-relation derivation — we take Eq.4 as given and verify only its numerical evaluation.
- Any experimental Hall-thruster cross-validation — outside the benchmark's scope.
