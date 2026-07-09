# Artifact Harvest

Every external public artifact touched, with URL / method / size.

| Artifact | URL / Origin | Fetched via | Size | Retained where |
|---|---|---|---:|---|
| Paper (PDF) | https://doi.org/10.1088/1361-6404/aac999 (IOP, OA CC-BY 3.0) — copied from sibling `PDE-Figueiras-Schrodinger-BPM-splitstep-2018/work/figueiras.pdf` | `cp` | 2,248,218 B | `paper.pdf` |
| Source repo (`pyNLSE/bpm`) | https://github.com/pyNLSE/bpm.git @ `96d945b` | `git clone` | ~1 MB | `work/bpm/` |
| `bpm/doc/notes_code.pdf` | bundled in the repo (authors' companion installation + usage notes) | git clone | 351,353 B | `work/bpm/doc/notes_code.pdf` |
| 20 example scripts (`examples1D/*.py`, `examples2D/*.py`) | bundled in repo | git clone | ~40 kB | `work/bpm/examples{1D,2D}/*.py` |
| `townes_profile.csv` (Townes profile numeric table) | bundled in repo, used by Collapse_2D initial condition | git clone | 21 kB | `work/bpm/examples2D/townes_profile.csv` |
| LIA2 (Vigo) project page mentioning the code URL | http://lia.ei.uvigo.es/lia/view/r_proyect2.php?r_proyect_id=40 | `web_fetch` | ~3 kB | not retained (referenced only) |
| Durham CM3/PR4 course syllabus mentioning the paper | https://www.maths.dur.ac.uk/users/kasper.peeters/cm3_pr4/PR34_2019_visual_quantum_mechanics.html | `web_fetch` | ~2 kB | not retained |

## Provenance chain

Paper: IOP OA CC-BY 3.0 (2018) → Rick's downloaded copy (sibling dir) → this dir's `paper.pdf` (byte-identical, sha256 verified `034a26a1...e933486`).

Code: LIA2 Vigo page → github.com/pyNLSE/bpm → local clone `work/bpm/`. Commit at time of clone: `96d945b`.

LLM inference (judges): Argo proxy `http://127.0.0.1:44497/v1/chat/completions` (rick-stevens-ai account, key `stevens`) → Argonne LLM gateway → underlying providers (OpenAI, Google, Anthropic). Free-tier only per Wave Brief.

## What was NOT harvested

- The paper's referenced Bernd Thaller *Visual Quantum Mechanics* books (Springer 2000, 2004) — not needed; only cited for pedagogical background.
- QMwebJS follow-up article (Peeters et al., MDPI 2020) — referenced only for context that this paper is cited in the literature.
- The paper's referenced Python installation video tutorials on YouTube (from 2018) — not needed; the software installed cleanly on modern Python without following them.
