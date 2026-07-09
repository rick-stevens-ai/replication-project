# Attempt log — OSTI 3012815

_All times CDT, 2026-07-02._

- 08:07 Received subagent task. Read WAVE_BRIEF.
- 08:08 Created target dir under REPLICATE-PROJECT. Attempted local `curl -sL https://www.osti.gov/servlets/purl/3012815` — timed out (CherryRd blocked / slow to osti.gov).
- 08:11 Fetched PDF via uicgpu (`~/env.sh` proxy). 4,726,725 B, sha256 `ec8438ff5a0d7ff854d4f5364c64cc16d2b94fba3d1871f33e7f1ebe55fbc38f`. `scp` back to CherryRd.
- 08:12 `pdf` tool refused (Anthropic 400 low-balance, Gemini unknown-model, OpenAI PDF plugin disabled). Fell back to `pdftotext -layout` (poppler) → 1789-line text. Grep-driven claims extraction.
- 08:13 Confirmed no locally installed MOOSE. Full MOOSE build (MOOSE + libmesh + PETSc + BISON + TMAP8 + Griffin) is a many-hour build and application input decks specific to the five case studies were not distributed with the OSTI file. Decided to (a) inspect the released source for artifact provenance, (b) run an independent surrogate replication of the paper's central quantitative claim.
- 08:13 On uicgpu, `git clone --depth 1 https://github.com/idaholab/moose.git` (1.1G checkout, HEAD `a628b5c041d25281b358585d1657e29f05b2bb1d` Merge #33111 2026-07-01). Confirmed presence of every algorithm class advertised in the paper (see `artifact_harvest.md`).
- 08:14 Wrote `work/rare_events_al_ss.py`: 4-branch series-system benchmark (2D standard-normal input, well-known rare-events reference problem, Bourinet et al. 2011), with three independent methods coded from the mathematical descriptions in the paper's Section 2.2/2.4 (crude MC, subset simulation with modified Metropolis-Hastings, and active-learning subset simulation using Echard-style GP + U-function that is textually identical to Table 1 of the paper). `RNG_SEED = 20260702`.
- 08:15 Ran on uicgpu (Python 3.8, NumPy 1.23.5, SciPy 1.10.1, scikit-learn 1.3.2). 10 repeats per method + a 200-million-sample reference MC estimate. Wall time ~2 minutes. Collected `rare_events_al_ss_results.json` and `.log` as evidence.
- 08:16 Wrote `REPORT.md`, `artifact_harvest.md`, this log.

## What worked
- OSTI PDF fetch through uicgpu.
- pdftotext extraction was clean enough for grepping claims, tables, section headers.
- MOOSE clone succeeded (public repo, no auth).
- Python surrogate: implementation ran; all three methods produced sensible numbers and the *ordering* of evaluation counts matched the paper (MC >> SS > AL-SS).

## What did not work
- `pdf` tool (all three backends failed → used pdftotext).
- Local direct HTTPS to osti.gov from CherryRd (timeout — used uicgpu).
- Full MOOSE build was out of scope for a single subagent slot (multi-hour C++ build + external LDs).
- The application input decks for the five paper case studies were not attached to the OSTI PDF (they typically live in downstream INL app repos: BISON, TMAP8, Griffin — many of which are export-controlled and *not* fully public), so bit-exact reruns of Figures 6/7/8/12/13 were not feasible in this slot.
