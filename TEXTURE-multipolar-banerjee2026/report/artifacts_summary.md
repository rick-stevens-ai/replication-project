# Artifacts Summary — banerjee2026

Paper: *Light-driven octupolar inverse Faraday effect and multipolar order in
Mott insulators*, Banerjee, Steinhoefel, Lange, Eschrig, Fehske
(arXiv:2605.08049v1, 2026).

Verdict: **REPLICATED (headline)** — Coverage 7/10, Agreement 9/10.

## Files (absolute paths)

### Extraction
- `/home/stevens/textures-100/corpus/textures-multipolar-banerjee2026/extraction/marker.md`
  — interim pdftotext dump (header `INTERIM: pdftotext fallback`), page breaks marked.
- `/home/stevens/textures-100/corpus/textures-multipolar-banerjee2026/extraction/nougat.mmd`
  — interim pdftotext dump in .mmd form (header `INTERIM: pdftotext fallback`).

### Report
- `/home/stevens/textures-100/corpus/textures-multipolar-banerjee2026/report/REPORT.tex`
  — REVTeX replication report (model, methods, results table, assessment).
- `/home/stevens/textures-100/corpus/textures-multipolar-banerjee2026/report/open_questions.json`
  — 5 open questions (question/why_it_matters/next_step) + top-level next_steps[].
- `/home/stevens/textures-100/corpus/textures-multipolar-banerjee2026/report/workflow.md`
  — step-by-step reproduction workflow.
- `/home/stevens/textures-100/corpus/textures-multipolar-banerjee2026/report/artifacts_summary.md`
  — this file.
- `/home/stevens/textures-100/corpus/textures-multipolar-banerjee2026/report/failure_analysis.md`
  — gaps, limitations, and what was not attempted.

### Evidence
- `.../report/evidence/banerjee2026_result.json` — full numerical results.
- `.../report/evidence/replicate_banerjee2026.py` — replication code.
- `.../report/evidence/ollie_multipolar_stevens_landau_kernel.py` — reused kernel (provenance).
- `.../report/evidence/replication_recipe.json` — original recipe.

### Result JSON (also in work/)
- `/home/stevens/textures-100/corpus/textures-multipolar-banerjee2026/work/banerjee2026_result.json`

## Headline verification (key numbers)
| Quantity | Value | Paper expectation |
|---|---|---|
| pseudospin SU(2) algebra | confirmed (<1e-9) | Eq.(2) SU(2) |
| induced field channel | sigma_y = T_xyz octupole | OIFE (linear in octupole) |
| h_m small-zeta log-log slope | 1.96 ≈ 2 | ~ |E x E*| helicity |
| h_m / Gamma^(3) | 1.125 = 9/8 (exact) | proportional (Fig.3b) |
| Gamma^(3)/J_eff growth | 7.7e-4 → 2.7e-3 (zeta 0.5→4) | grows with zeta (Fig.3a) |
| J_eff, Gamma^(3), h_m @ zeta=2 | 1.5e-2, -1.7e-4, -1.9e-4 eV | ~1e-2 / ~1e-3 eV scales |

## Kernel provenance
Stevens-operator / pseudospin construction reuses Ollie's
`ollie_multipolar_stevens_landau_kernel.py`. Floquet coupling evaluation and
van Vleck octupolar-field demo are original to this replication.
