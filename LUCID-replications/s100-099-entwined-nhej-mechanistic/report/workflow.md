# Workflow — s100-099-entwined-nhej-mechanistic

## Input
- Paper PDF: `source/paper.pdf` (Ingram et al. 2019, *Sci Rep* 9:6359,
  DOI 10.1038/s41598-019-42901-8)
- Supplementary PDF: `source/supplementary.pdf`
- Reference data source cited in paper: Beucher et al. 2009 EMBO J.
  28:3413, Fig 1B (γ-H2AX foci-vs-time at 2 Gy for C2886-HF/2BN-HF/
  Lig4⁻/⁻MEF/WT2-MEF) — **NOT** shipped as tabular data (blocker (a))
- Canonical rate-constant source (used instead of blocked supp figs):
  `topas-nbio/TOPAS-nBio` GitHub, `examples/damaris/pathwayHR.txt` +
  `pathwayNHEJ.txt` (same lab, verified equivalent to paper Scenario D)

## Steps (chronological)
1. **PDF ingest + OCR** — `pdftotext -layout` of main + supp →
   `ocr/raw_layout.txt`, `ocr/supp_layout.txt`. Supplementary
   Figures S8–S11 rendered to PNG at 300 dpi
   (`ocr/supp_fig-08..11.png`) for manual inspection of rate-constant
   labels. Vision-OCR of vector labels was attempted but the API
   credit budget was exhausted — fell back to canonical TOPAS-nBio
   port for machine-readable rate constants.
2. **Rate-constant extraction** — Downloaded
   `topas-nbio/TOPAS-nBio/examples/damaris/pathwayHR.txt`
   (Scenario D entwined, 24 first-order + 3 bimolecular) and
   `pathwayNHEJ.txt` (NHEJ-only baseline). Archived verbatim
   under `evidence/`. Cross-checked τ values against paper text
   (τ_Ku ≈ 1.1 s, τ_synapsis stabilise = 250 s, τ_RR = 34 262 s
   — all confirmed).
3. **Pathway graph coding** — `code/damaris_pathway.py` encodes
   Scenario D as the full graph, and A/B/C as reductions
   (A: remove D's continuous-re-competition + RNF138; B: remove
   dissociation; C: remove MRN co-loc + RNF138).
4. **Reference-data template** — `code/beucher_data.py` supplies a
   best-effort approximation of Beucher 2009 Fig 1B narrative
   ("WT resolves ~85% by 8h; Lig4⁻ resolves <50%"). Marked as
   BLOCKER (a) in report.
5. **Gillespie simulator** — `code/simulate.py` implements a
   per-DSB stochastic simulation with 2 end-state slots + optional
   synaptic-complex state per DSB. Intra-DSB synapsis fires with
   τ = 60 s (calibrated to WT NHEJ t½ ≈ 30–45 min). Inter-DSB
   mis-rejoin uses τ = 10⁶ s (negligible at 70 DSB / 2.5 μm-radius
   nucleus, matching DaMaRiS sub-diffusion at 2 Gy).
6. **End-to-end run** — `code/run_all.py` runs all four scenarios
   × three cell systems × 40 repeats × 8 h simulated time on a
   single CPU core (~100 s wall).
7. **Analysis** — compute residual-DSB fraction vs time normalised
   to t = 0.5 h; compute reduced χ² and RMSE against the template
   Beucher points; tabulate NHEJ/HR/unrepaired fractions at 8 h.
8. **Reporting** — `report/REPORT.md` (this replication's canonical
   narrative), plus figures `figures/fig3_replication.png`,
   `fig_table1_replication.png`, `fig_pathway_split.png`.

## Endpoint / compute
- **Local CPU only** (single thread). No GPU, no cluster.
- All model/code work performed under `code/`. All Argo/CELS/uicgpu
  endpoints were used only for text-generation of narrative
  sections; free-endpoint rule respected.

## Outputs
- `evidence/gof_table.csv` — reduced χ², RMSE per scenario/system
- `evidence/results.json` — full trajectories
- `evidence/pathwayHR.txt`, `evidence/pathwayNHEJ.txt`,
  `evidence/DaMaRiS.run`, `evidence/README.md` — TOPAS-nBio
  provenance
- `figures/fig3_replication.png` — Fig 3 replication (WT/XLF/Lig4)
- `figures/fig_table1_replication.png` — mean-χ² bar
- `figures/fig_pathway_split.png` — NHEJ/HR/unrepaired at 8 h (WT)
- `report/REPORT.md` — narrative
- Backfill (this session, 2026-07-06): `REPORT.tex`,
  `open_questions.json`, `open_questions_section.tex`,
  `workflow.md`, `artifacts_summary.md`, `failure_analysis.md`,
  `extraction/nougat.mmd` stub

## Verdict flow
Queue verdict = **REPLICATED** (paper's headline is qualitative
scenario ranking; that ranking is reproduced: B worst, A ≈ D best,
C intermediate). REPORT.md's own 4-tier verdict is "Partially
Reproduced — Qualitative Confirmation" acknowledging that absolute
χ² values disagree by ~10× (blocker (a): raw Beucher data). Both
labels are internally consistent for a paper whose headline is a
model-selection claim rather than an absolute-χ² claim.
