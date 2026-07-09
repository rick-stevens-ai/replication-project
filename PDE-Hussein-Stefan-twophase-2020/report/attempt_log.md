# Attempt Log (chronological)

1. Read `PDE_TOPUP25_2026-06-26.tsv`. Top rows: rank 52 Wang Poisson-Boltzmann (DONE
   tonight), rank 61 Bernardi Darcy-heat (DONE tonight), **rank 63 Adil & Hussein
   "Numerical Solution for Two-Sided Stefan Problem" (2020)** = top still-undone.
2. Dedup: grepped REPLICATE-PROJECT/ and PDE-replications/ for stefan/hussein/two-sided
   and for the other top candidates (Stefan, finite-volume particle, embedded boundary,
   waveform relaxation, Krylov, fractional step, DG, Poisson-Nernst, Nitsche) — no
   collision. Selected rank 63 (OA, repro-ok, clear numerical PDE core with analytic
   test cases and published error tables).
3. Confirmed OA: DOI resolves (HTTP 200) to Iraqi J. Science OJS; downloaded full-text
   PDF galley (687 KB, 9 pp) via curl. NOT the paid `pdf` tool.
4. `pdftotext -layout` gave clean prose but stripped math symbols (equations rendered as
   empty `( )`). Switched to page rasterization (`pdftoppm -r 300`) + local `tesseract`
   OCR to recover equations. (Vision LLM OCR unavailable — no free image endpoint.)
5. Transcribed: governing PDE (eq.1), Landau transform y=(x-h1)/h3, transformed
   fixed-domain PDE (eq.4), IC/BCs, and BOTH test cases + error tables.
6. Implemented from scratch (`work/stefan_cn.py`): transformed variable-coefficient
   parabolic PDE with Crank-Nicolson (theta=1/2), centered 2nd-order space, tridiagonal
   `scipy.linalg.solve_banded` per step, Dirichlet BCs from the exact solution.
7. Example 1 run: max error O(1e-13)-O(1e-14) (machine precision) matching the paper's
   O(1e-13)-O(1e-14). Cross-checked the paper's explicit source term f against my
   manufactured f (max diff = 0.0) -> model decoded correctly.
8. Table check (`work/tables.py`): Example 1 reproduces 3/4 table nodes exactly; the 4th
   (0.1,0.2) I get 3.1424 vs paper-printed 3.4124 — but 3.1424 = the paper's OWN
   transformed exact formula (1+y)^2(1+t)^2+1+2t. => paper Table-1 typo (digit
   transposition); my solver matches the defined exact solution.
9. Example 2 first run with printed u=x^2+2t^2+1 did NOT match Table 2 (got 4.3477 vs
   6.3054 at (0.5,0.5)). Re-OCR of p.449: the paper's transformed exact v and its source
   term f are CUBIC in x. Tested u=x^3+2t^2+1 -> all 4 table nodes match to 4dp exactly.
   Conclusion: the printed "x^2" is a typo for "x^3". Corrected the solver.
10. Re-ran: Example 2 reproduces EVERY Table 2 entry (all meshes, all 4 nodes) to 4dp;
    global max error O(1e-3)->O(1e-5) (paper: O(1e-2)-O(1e-5)); observed convergence
    order p = 1.97 -> 2.00 confirming claimed 2nd-order accuracy.
11. Generated log-log convergence figure (`evidence/convergence.png`) + JSON.
12. LLM-judge (free Argo `argo:gpt-5.2`, localhost:44497): verdict **REPLICATED**.
13. Wrote report set. No files written outside the assigned target dir.

## What worked / failed
- WORKED: pdftotext for prose; tesseract for equations; manufactured-solution derivation;
  CN tridiagonal solver; Argo free judge.
- FAILED/UNAVAILABLE: vision LLM OCR (no free image endpoint, Anthropic credit=0);
  MCP tesseract/paddle tools timed out (cold model load) — used direct `tesseract` CLI.
- Light compute; ran entirely locally on CherryRd, no uicgpu needed.
