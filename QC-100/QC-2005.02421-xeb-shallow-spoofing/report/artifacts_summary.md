# Artifacts summary — QC-2005.02421-xeb-shallow-spoofing

Target: arXiv:2005.02421 (Barak, Chou, Gao — shallow-XEB spoofing)
Verdict: **REPLICATED** (small-instance CPU statevector regime)

## Files produced by this replication

| Path | Kind | Purpose |
|------|------|---------|
| `report/REPORT.md`                         | narrative markdown | Human-readable replication report (source of truth) |
| `report/REPORT.tex`                        | LaTeX              | Publishable version of the same report |
| `report/failure_analysis.md`               | markdown           | Honest critique — what was & was not exercised |
| `report/open_questions.json`               | bare JSON list     | 5 open questions with `{q, basis, next_steps}` each |
| `report/open_questions_section.tex`        | LaTeX              | Same 5 questions, ready to `\input{}` |
| `report/workflow.md`                       | markdown           | One-shot reproduction recipe |
| `report/artifacts_summary.md`              | markdown           | THIS FILE |
| `report/evidence/xeb_results.json`         | JSON               | Structured raw results from `xeb_experiment.py` |
| `report/evidence/run.log`                  | console log        | `xeb_experiment.py` console dump |
| `report/evidence/collision_check.log`      | console log        | `collision_probability_check.py` dump |
| `scripts/xeb_experiment.py`                | Python             | Baseline (exact/uniform) + depth-1 & light-cone-4 spoofers |
| `scripts/collision_probability_check.py`   | Python             | Collision-probability vs depth (Porter-Thomas trajectory) |
| `work/paper.pdf`                           | PDF                | arXiv:2005.02421 source PDF |
| `work/paper.txt`                           | text               | `pdftotext` dump used during review |
| `work/abs.html`                            | HTML               | arXiv abstract page |
| `extraction/nougat.mmd`                    | MMD                | Extraction placeholder (see file for status) |
| `.venv/`                                   | venv               | `cirq-core 1.7.0`, `numpy 2.5.0` |

## Coverage against the 8-artifact standard

| Artifact | Present | Path |
|----------|---------|------|
| 1. REPORT (narrative)           | yes | `report/REPORT.md` |
| 2. REPORT.tex (LaTeX)           | yes | `report/REPORT.tex` |
| 3. open_questions.json (5, bare list) | yes | `report/open_questions.json` |
| 4. open_questions_section.tex   | yes | `report/open_questions_section.tex` |
| 5. workflow.md                  | yes | `report/workflow.md` |
| 6. artifacts_summary.md         | yes | `report/artifacts_summary.md` |
| 7. failure_analysis.md          | yes | `report/failure_analysis.md` |
| 8. extraction stub              | yes | `extraction/nougat.mmd` |

## Provenance / compute

- Host: local CPU (no HPC, no paid API).
- Runtime: `xeb_experiment.py` ~4.5 min; `collision_probability_check.py` ~1 min.
- Seed: `20260703`, bit-for-bit reproducible under `cirq-core==1.7.0`,
  `numpy==2.5.0`.
- No external network calls in any script.
- No LLM was used to fabricate or estimate any numerical value; the
  narrative and open-questions sections may be reviewed / rewritten by a
  free-endpoint LLM (Argo Opus etc.) per standing rule.

## Headline exercised?

**Yes.** The paper's headline mechanism — that a classical algorithm
touching only the light cone of each output bit can achieve
$F_{\mathrm{XEB}}\gg 0$ on shallow random circuits, in $\mathrm{poly}(n,
2^L)$ time — is exercised end-to-end:

- Baselines confirmed: exact sampler → $F\in[1,14]$ across
  $(n,d)\in\{4,6,8\}\times\{1,\ldots,6\}$; uniform → $F\approx 0$.
- Light-cone-$L$ spoofer independently reimplemented at $L=2$ (depth 1)
  and $L=4$ (depth 2), scoring $F\approx 14$ (n=8, d=1) and $F\approx
  2.3$ (n=8, d=2) respectively.
- Predicted $1/15^d$ depth decay observed qualitatively via the
  under-powered $L=4$ controls at $d=3,6$.

Not exercised (out of scope, per REPORT §5): the full $\sqrt{\log n}$-depth
2D construction (Corollary 1.2) and the 53-qubit Sycamore comparison
number (cited but not re-derived by the paper).
