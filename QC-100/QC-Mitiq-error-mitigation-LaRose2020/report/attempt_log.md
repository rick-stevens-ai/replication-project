# Attempt Log — QC-Mitiq-error-mitigation-LaRose2020

Chronological. All times CDT, 2026-07-01.

1. **Dedup check** — `ls ~/Dropbox/REPLICATE-PROJECT/QC-100/` + `grep -iE "mitiq|larose|error-mitig"`. Only hit was `W1-zne-error-mitigation-temme`, which is a DIFFERENT paper (Temme ZNE, not the Mitiq software paper). No existing dir for arXiv:2009.04417 → proceed.
2. **Read brief** — `scripts/WAVE_BRIEF_2026-07-01.md`. Free endpoints only; real replication; LLM-judge verdict.
3. **Created target dir** with `report/{evidence}` + `work/`.
4. **Fetched paper** — arXiv abstract page + ar5iv HTML (`2009.04417`). Confirmed correct title/abstract. Stripped ar5iv HTML → `work/paper_text.txt` (95 KB) for number extraction.
   - PDF vision tool (`pdf`) failed: Anthropic out of credits, gemini model name stale, openai PDF-extract disabled. Fell back to ar5iv text extraction — successful and sufficient (all numbers present in prose).
5. **Extracted testable claims** from paper text:
   - Fig 5 PEC toy: circuit `CNOT_{1,2}∘X_1∘H_2`, obs `|00⟩⟨00|` (ideal 0), depol p=0.1 after each gate, density-matrix sim, 1000 samples. **Unmitigated 0.0622, PEC 0.0071.**
   - Fig 4 ZNE (H2 VQE, depol p=0.05) + Fig 3 ZNE (RB circuits, ideal ⟨00|ρ|00⟩=1).
6. **venv setup** — first attempt with system `python3` = **3.14**; `setuptools.build_meta` unavailable, mitiq build failed. Recreated with **python3.12** → `mitiq 1.0.0`, `cirq 1.6.1` installed cleanly.
7. **Ran `rep_pec.py`** (Fig 5 exact setup, seed variety). Result: **unmitigated = 0.062222** (paper 0.0622 — exact 4 sig-fig match). Single-seed PEC = -0.0178 (improvement factor 3.5×; in the right direction but noisy — PEC is a Monte-Carlo estimator).
8. **Ran `rep_pec_multiseed.py`** — to characterize PEC's stochastic distribution. First version (20 seeds × {1k,10k} samples) was too slow (density-matrix re-sim per sample); killed after ~10 min and reduced to 10 seeds × 1000 samples (the paper's exact setting). Result: **mean |PEC err| = 0.0097** (paper 0.0071, within distribution; min 0.0006), **100% of seeds beat unmitigated**, **mean improvement factor 6.4×** ("almost an order of magnitude" ✓).
9. **Ran `rep_zne.py`** — 20 RB circuits, depol p=0.01, default ZNE (local folding + Richardson). **mean err 0.577→0.326, 1.77× reduction, 100% circuits improved.**
10. **LLM judge** — free Argo proxy (localhost:44497). `argo:claude-opus-4.8` hit an upstream response-parse bug on the proxy; fell back to `gpt-5.2` (also free Argo). Verdict: **REPLICATED**, all three claims REPRODUCED.
11. **Wrote report/** (REPORT.md, brief.md, this log, artifact_harvest.md, results.json, evidence/).

## What worked
- ar5iv text extraction gave every needed quantitative claim without the (broken) PDF vision tool.
- python3.12 venv; mitiq's built-in `represent_operations_in_circuit_with_local_depolarizing_noise` + `execute_with_pec` reproduced Fig 5 out of the box.
- The unmitigated noise-model number matched the paper to 4 sig figs — a clean, unambiguous reproduction.

## What was tricky
- python3.14 too new for mitiq build backend.
- PEC point estimate is stochastic; single-seed match to 0.0071 is not expected. Multiseed characterization was the correct way to test the claim (direction + order-of-magnitude).
- 10k-sample multiseed sweep too slow locally; 1000-sample (paper's setting) was sufficient and fast enough. Local compute was adequate; uicgpu not needed for this toy-scale density-matrix work.
