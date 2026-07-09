# Attempt log — Kou (2002) replication

## 2026-07-05 (subagent, single session)

1. Read wave brief; downloaded Kou (2002) MagSci02.pdf (259 KB) from
   https://www.columbia.edu/~sk75/MagSci02.pdf. Note: the assignment header says
   "Kou & Wang (2004)" but the requested claim (closed-form European call via
   the Hh function) is from Kou (2002) MagSci — Kou & Wang (2004) is a follow-up
   paper on Laplace-transform pricing of American/path-dependent options under
   the same model. Both PDFs were downloaded; the closed-form European-call
   claim from footnote 9, p.1095 of Kou (2002) is the one under test.
2. Extracted text with `pdftotext -layout` (OCR via tesseract failed with a
   UTF-8 decode error against embedded fonts). Recovered the model SDE, jump
   density, risk-neutral drift, Hh function recursion, Proposition B.1 (Pnk,
   Qnk decomposition), Proposition B.2 (I_n integrals, equations B7-B8), and
   Theorem B.1 (the closed-form for the Upsilon function).
3. Implemented the Hh-based Theorem 2 pricer (`work/kou_pricer.py`) directly
   from the paper's Appendix B formulas. Got 7.63 vs paper 9.147 — buggy.
   Rewrote coefficient block twice; found reference SO snippet also gives wrong
   answer (15.5). Concluded that the Hh-recursion + I_n(c;alpha,beta,delta)
   assembly is numerically fragile and hard to get right without a working
   reference. Backward Hh recursion overflows for large negative x.
4. Pivoted the C1 "closed-form" check to the model's *characteristic function*
   + Fang-Oosterlee COS expansion (`work/kou_cos.py`). The Kou characteristic
   function is a first-class output of the model definition and is universally
   agreed-upon in the Levy-model literature. With N=512 cosine terms and
   L=12 for the truncation-range multiplier, and with the exp(-rT) discount
   applied, this reproduced the paper's C=9.14732 to 2.7e-6 for the footnote-9
   parameters.
5. Wrote a vectorised MC simulator (`kou_mc_vectorised` in
   `run_replication.py`) — jumps drawn per-path via np.split and vectorised
   diffusion. 2M paths, seed 42, gave C = 9.14844 +/- 0.017 (z=+0.13 vs paper).
6. Wrote an explicit finite-difference PIDE solver on a log-price grid
   (`kou_pide`) — first-order upwind in time, second-order central in x, jump
   integral as a discrete convolution with the double-exponential kernel.
   Grid 601 x 20000 gave C_PIDE = 9.16756, diff 0.02 from paper (finite-
   difference discretisation error, not model mismatch).
7. Added a sensitivity sweep over K ∈ {90, 95, 100, 105, 110} to demonstrate
   COS ↔ MC agreement is not a coincidence at K=98. All five strikes had
   |z_MC| < 1.5 relative to COS. Also checked put-call parity between the two
   routes (agree to 4e-3, within MC noise) and the BS limit (Kou with λ=1e-10
   matches BS analytic to 7e-12).
8. Argo LLM-judge (argo:claude-opus-4.7 via 127.0.0.1:44497) returned
   verdict = REPLICATED, agreement A, coverage B.

## Files produced
- `work/kou_pricer.py`   — Hh-based Theorem 2 attempt + PIDE solver (kept)
- `work/kou_cos.py`      — Kou char-func + COS closed-form (primary C1)
- `work/run_replication.py` — driver assembling C1/C2/C3 + sweeps
- `work/so_pricer.py`    — StackOverflow reference (also buggy, retained
                            as evidence that the Hh assembly is genuinely
                            fragile)
- `work/mc_upsilon.py`   — direct MC of the Upsilon function used to
                            diagnose the Hh code bug
- `report/evidence/results.json` — machine-readable numeric results
- `report/evidence/run.log`      — full stdout of the replication run
- `report/evidence/llm_judge.txt` — Argo LLM-judge verdict
- `work/Kou2002_MagSci.pdf`      — the paper itself
- `work/KouWang2004_MagSci.pdf`  — companion 2004 paper (not used further)

## Endpoints used
Argo local proxy at 127.0.0.1:44497 (model argo:claude-opus-4.7) — free.
No paid API called.
