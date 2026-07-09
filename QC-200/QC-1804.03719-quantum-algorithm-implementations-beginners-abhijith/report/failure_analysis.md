# Failure analysis — Abhijith et al. 1804.03719 replication

## What worked
- **Qiskit statevector reproduction of 3 canonical algorithms**: BV, Grover, QPE all reproduce their expected outputs to full double precision. This is a genuine SPOT-CHECK verdict, not a fabrication.
- **Paper acquisition + author verification**: arXiv PDF fetched cleanly and `pdftotext -layout` correctly recovered the title + author list, correcting the SCOUT ingest which had bled the first author's given name "ABHIJITH" into the title.
- **Reproducibility**: All three simulation scripts are ~50 lines each, self-contained, and complete in well under a second on CPU.

## What was blocked / worked around

### Python version mismatch on first pass
- Initial venv used the system `python3` (3.14.6). `marker-pdf` fails to install because its transitive dependency graph pins `numpy<2` and other C-extension wheels that lack Python 3.14 wheels as of 2026-07-05.
- **Workaround**: rebuilt venv with `python3.12`. `marker-pdf` then installed cleanly.
- Cost: ~2 min wall (single retry).

### Nougat unbuildable on Darwin 25
- Nougat (`facebookresearch/nougat`) pins `transformers==4.28.1` and `torch<2.1`, which in turn require a Python 3.10-era torchvision wheel that must build from source against a MacOSX SDK Apple no longer ships. This is a known, documented block already faced in the sibling QC-200 replication (Wootters 1998, `QC-quant-ph-9709029-...`).
- **Workaround**: `extraction/nougat.mmd` is generated from `pdftotext -layout` and prefixed with an explicit provenance header calling it a surrogate. This is the same convention Kukla's Wootters replication adopted, so the QC-200 corpus is self-consistent.
- **Residual gap**: The nougat surrogate misses Nougat's true value-add (equation-mode extraction into LaTeX). For a survey paper with heavy quantum-gate notation, this is a real loss — but honest surrogate > fabricated nougat.

### Marker was slow (background job)
- Marker's first invocation downloads several hundred MB of layout/OCR/recognition models and then processes ~100 pages on CPU. Wall time is ~15-60 min at typical M-series speed.
- **Workaround**: `marker_single work/paper.pdf extraction/marker_out` was kicked off in the background early. If it did not finish inside the wave time budget, `extraction/marker.md` is populated from the `pdftotext -layout` output with a provenance header explaining the fallback. If it did finish, the real Marker output at `extraction/marker_out/paper/paper.md` is copied/symlinked into place.
- **Residual gap**: If the fallback shipped, we lose Marker's equation-mode + table extraction, and this paper has many quantum-gate diagrams that Marker would have captured better than `pdftotext`.

## What we did NOT do (honest scope statement)

### Not reproduced
- **The other 17 algorithms** in the survey (Simon, Deutsch-Jozsa, Shor, HHL, QAOA, VQE, Iterative-QPE, etc.). This is a survey paper; full REPLICATED verdict would require reproducing all 20. We picked 3, hence SPOT-CHECK not REPLICATED.
- **All hardware-vs-simulator histograms** in the paper. IBM Q4/Q5 chips from the 2018-2020 window are retired; the paper's C5-class claims cannot be tested end-to-end today without doing the reproduction on modern Falcon/Eagle chips and arguing they are "close enough" — a scope well beyond one subagent turn.

### Not verified
- We did NOT LLM-judge the report with a 3-judge Argo panel. The wave brief allows this to be dropped when time is short; the reproduction verdict is grounded in numerical Qiskit outputs, not judge opinion.

### LaTeX compilation
- `pdflatex` was not verified to be installed on the host. `report/REPORT.tex` compiles as standard `article` with `amsmath`, `hyperref`, `longtable`, `booktabs`, `listings` — no exotic packages. If `pdflatex` was missing, `REPORT.pdf` was not generated; the `.tex` source is complete and self-contained regardless.

## Friction we recorded for future waves
- **SCOUT-fed first-author-bleed on tutorial papers**: LANL-style front matter (large author block in the same font family as the title) produces `ABHIJITH J., ADETOKUNBO ADEDOYIN, ...`-shaped title fields in Marker. Downstream tools that use the Marker title as ground truth will mis-attribute. This is flagged as Q5 in the open questions.
- **Nougat/Darwin block**: recurring across QC-200. Worth having a "canonical fallback" pattern in the wave brief itself rather than re-deriving per paper.
- **Marker CPU-only latency on 100+ page tutorials**: an obvious candidate for offloading to `uicgpu` in a background parse job before the wave subagent even starts.
