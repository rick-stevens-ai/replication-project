# attempt_log

Chronological log, 2026-07-04 evening (America/Chicago).

1. Read `WAVE_BRIEF_2026-07-01.md` — free endpoints only, LLM-judge scoring, real replication, output structure fixed.
2. Created target directory
   `~/Dropbox/REPLICATE-PROJECT/PDE-Sethian-fast-marching-eikonal-1996/{report/evidence,work}`.
3. Fetched the PNAS paper. `curl` of the PNAS DOI PDF returned an HTML wrapper (5.4 kB); the Alberta CS course mirror
   `http://ugweb.cs.ualberta.ca/~vis/courses/CompVis/readings/modelrec/sethian95fastlev.pdf` returned the actual
   356 kB / 17-page PDF (PDF 1.2, Type-3 fonts). Saved as `work/sethian1996.pdf`.
4. Attempted the `pdf` MCP tool — blocked because Anthropic credits are exhausted and the free-endpoint policy
   forbids paid providers. Attempted `pdftotext` — Type-3 glyph tables produced mojibake. Attempted the
   `ocr_pdf` / `ocr_tesseract` MCP wrappers — MCP timeouts. Fell back to `pdftoppm -r 200 -png` to rasterize
   each page and `tesseract` CLI in `--psm 6` mode; that yielded clean, readable text for pp. 3–12 including
   Eqns. 1, 6, 7, 8, 9 and the algorithm listing in Sec. 3.2 / 4.1.
5. From that source, wrote `work/fmm.py`: 2-D FMM with (a) the paper's upwind quadratic
   (Godunov, Eqn. 8/9), (b) heap-based narrow band using `heapq` with a per-cell version counter
   for lazy deletion (equivalent to Sethian's back-pointer bubble-up for correctness; the O(log N)
   push/pop cost is preserved). Self-test on n=65 point source, F=1 → L∞ error ≈ 1.8e-2 (rel ≈ 3.6%),
   consistent with first-order accuracy.
6. Wrote `work/experiments.py` with three experiments:
   - **C2 convergence**: n ∈ {33, 65, 129, 257, 513}, F=1, single point source at the grid center, error
     measured in an annulus 0.15 < r < 0.45 (excluding both the singular pole and the boundary).
   - **C1 complexity**: n ∈ {65, 129, 257, 513, 1025}, median of 3 timed runs after a warmup, checking
     both a power-law fit t ≈ c N^p and the paper's specific N log N claim by looking at t / (N log₂ N).
   - **C3 variable speed**: n=257, two-material F (0.5 in the bottom half, 2.0 in the top half), source
     on the interface, checked (i) that every accepted cell has a smaller-valued accepted neighbor
     (monotone construction) and (ii) that along the axial column T matches the exact straight-ray
     time d/F.
7. Ran `experiments.py`; captured full stdout to `report/evidence/run_log.txt`. All three passed
   (see REPORT.md for the numbers).
8. Wrote `work/make_figures.py` → PNG plots of convergence (log–log h vs error), complexity
   (log–log N vs seconds with N log N reference), and the variable-speed arrival-time field.
9. LLM-judge scoring via Argo proxy (127.0.0.1:44497, key=stevens), `gpt-4o` model. Wrote judgement
   to `report/evidence/llm_judge.json`. No regex-based verdict was used.
10. Assembled `report/REPORT.md`, `brief.md`, `artifact_harvest.md`, this log.
