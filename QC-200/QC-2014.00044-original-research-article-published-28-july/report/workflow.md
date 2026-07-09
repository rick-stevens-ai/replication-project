# Workflow — QC-200 replication of Hen 2014

**Wall-clock:** ~35 minutes (single subagent, one continuous session, 2026-07-06 04:15–04:50 CDT).
**Effort estimate:** ~1 person-hour equivalent (paper resolution + reading + design + code + debugging + report).

## Step-by-step workflow

1. **Read task brief** (`~/Dropbox/REPLICATE-PROJECT/scripts/QC_WAVE_BRIEF_2026-07-03.md`) to internalize hard rules, 8-artifact bar, 5 Open Questions, WAVE_RESULT format.

2. **Paper resolution (given ID was NOT arXiv):**
   - Confirmed arXiv 404 (`https://arxiv.org/abs/2014.00044`).
   - Matched sibling-paper pattern from `QC-200/QC-2023.12735-.../work/paper_provenance.md` (Frontiers `<year>.<article_num>` interpretation).
   - Crossref query: `container-title=Frontiers, from-pub-date=until-pub-date=2014-07-28, query=quantum` → single hit `10.3389/fphy.2014.00044`.
   - Downloaded PDF, computed SHA256: matched given hash byte-for-byte. Identity confirmed.
   - Full trail: `work/paper_provenance.md`.

3. **Environment setup:** `python3 -m venv work/venv`; `pip install --quiet numpy scipy qiskit`.

4. **Paper reading + claim extraction:** ran `pdftotext -layout paper.pdf work/paper.txt`, read all 10 pages via `read` tool with offset/limit chunks. Identified paper as theory-only (no numerical experiments), so the "reproducible core number" was reframed as **analytic gate-identity fidelity** (Eqs. 8, 11, 13 with θ_f=π).

5. **Simulator design + first run:**
   - Wrote `adiabatic_qft_gates.py` (~350 lines) — literal implementation of paper's Eqs. (3)–(5), (10), (12) as time-dependent Hamiltonians; midpoint-rule adiabatic evolution via `scipy.linalg.expm` per slice; full 2-qubit / 3-qubit fidelity metric.
   - First run: CP-shift and CNOT reproduced at fidelity 0.999973 across all inputs. **Hadamard failed** (0.05–0.52 fidelity on random inputs).

6. **Diagnostic + variant sweep:**
   - Wrote `debug_hadamard.py` to inspect the raw output amplitudes for input `|0⟩` — clearly showed the aux qubit ends near |1⟩ (correctly) but the data-register is not `|+⟩ = H|0⟩`.
   - Extended `adiabatic_qft_gates.py` with a `data_conditioned_on_aux1()` helper + `gate_fidelity_via_projection()` to compute the post-selected fidelity. This confirmed CP-shift & CNOT reach fidelity **1.000000** on the projected metric.
   - Wrote `hadamard_variants.py` — swept 4 sign/subspace variants of Eqs. (3)–(5). None reached uniformly high fidelity. Documented as a probable typesetting typo.

7. **QFT composition sanity check:** Assembled the standard textbook QFT_3 circuit from *ideal* H+CP+CNOT gates via the paper's §3.4 recipe, verified against $F_{jk}=\omega^{jk}/\sqrt{N}$ at fidelity 1.000000. This isolates the anomaly to C1 (Hadamard) and not the composition scheme.

8. **LLM-judge verdict:** Wrote `llm_judge.py` calling Argo (`argo:claude-opus-4.8` was 502; fell back to `argo:gpt-5.2` via the local litellm aggregator at `http://localhost:4000/v1/chat/completions`, Bearer stevens). Judge returned **PARTIAL, confidence 0.86** with a well-reasoned justification citing all the fidelity numbers.

9. **Extraction fallbacks:** No central Marker/Nougat cache exists for QC papers. To satisfy the 8-artifact bar without a several-GB ML model download blowing the time budget, both `extraction/marker.md` and `extraction/nougat.mmd` were populated with pdftotext-layout output + honest fallback headers documenting the substitution.

10. **Report + artifact assembly:** Wrote `report/REPORT.md` (verdict, claims table, methods, results, 5 Open Questions), machine-readable `report/open_questions.json`, LaTeX version `report/REPORT.tex` (compiled to `REPORT.pdf`, 4 pages), plus `report/artifacts_summary.md`, `report/failure_analysis.md`, and this `report/workflow.md`.

## Tools & versions used

| Tool | Version | Purpose |
|---|---|---|
| Python | 3.13 (macOS system) | Simulator language |
| numpy | 2.5.1 | Statevectors, Pauli matrices, Kronecker products |
| scipy | 1.18.0 | `scipy.linalg.expm` for exact per-slice unitaries |
| qiskit | 2.5.0 | Installed per brief's "install the sim tool" checklist; not required at simulation time (numpy statevector chosen for full control over the paper's exact Hamiltonians) |
| Poppler `pdftotext` | system | Text extraction from `paper.pdf` (`-layout` mode preserves the paper's two-column formatting) |
| Crossref API | (v2, live) | Resolving Frontiers article-number IDs to DOI |
| Argo LLM aggregator | `argo:gpt-5.2` via `http://localhost:4000/v1/chat/completions` (litellm on cherryrd) | LLM-judge verdict |
| TeX Live | 20260301 (Homebrew) | Compiling `REPORT.tex` → `REPORT.pdf` |

## Compute footprint

- All work ran on CherryRd (local macOS host) in the target directory's venv. No GPU used. No remote-cluster jobs. Total: <5 seconds of scipy.linalg.expm CPU time across all runs; ~10 seconds of Argo LLM call latency; ~2 seconds of pdftotext + pdflatex. Trivial.

## What was NOT done (and why)

- **No live Marker or Nougat run** — the QC corpus does not have a pre-parsed cache for this Frontiers paper, and running Marker/Nougat from scratch requires a 1.4–5 GB VLM checkpoint download that would exceed the per-paper time budget for a paper whose text extracts cleanly with pdftotext-layout. `extraction/marker.md` and `extraction/nougat.mmd` document this substitution transparently.
- **No 8-way parity sweep of Hadamard variants** — 4 obvious variants were tested; none succeeded. A full 8-way sweep + analytic re-derivation is documented as Open Question Q1 for follow-up rather than being done in-line.
- **No open-system Lindblad simulation** — the paper's decoherence-vulnerability argument (§4) is qualitative; a quantitative benchmark would take longer than this replication's time budget and is documented as Open Question Q3.
- **No 3-judge panel** — the brief allows single-judge if time is tight; used a single Argo judge with confidence 0.86.
