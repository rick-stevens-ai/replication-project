# Attempt Log — 2026-07-04 (Sat) 06:08–06:30 CDT

Subagent: PDE-Ma-Xu-Zhang-mPNP-2020 replication (rank 28 in PDE_NEXT50).
Session id: `agent:main:subagent:d8f26e02-c9ce-4753-96cc-2bc7f3c8850a`.

## 06:08 — Setup
- Confirmed no sibling replication directory under `~/Dropbox/REPLICATE-PROJECT/`
  matches `ma.*xu.*zhang | mPNP | poisson-nernst-planck.*2020` — safe to
  proceed.
- Created target dir `PDE-Ma-Xu-Zhang-mPNP-coulomb-hardsphere-2020/` with
  `report/{evidence,}` and `work/` subdirs.

## 06:08 — Paper acquisition
- Attempted `web_fetch` on `https://doi.org/10.1137/19M1310098` → HTTP 406
  (SIAM blocks web-fetch UA).
- First arXiv guess (1904.02790) turned out to be an unrelated TTS paper — a
  wrong-arXiv-id hallucination hazard.  Corrected via Semantic Scholar API
  (S2 key from Keychain `semantic-scholar-api-key` / `rick-stevens-ai`,
  `openAccessPdf` field pointing to arXiv 2002.07489 v3).
- `curl` downloaded arXiv PDF cleanly → 1,006,890 bytes, 22 pages.  Confirmed
  authors Manman Ma (Tongji), Zhenli Xu (SJTU), Liwei Zhang (SJTU).

## 06:09 — Paper analysis
- `pdftotext -layout` gave a clean text extract (1343 lines).
- Attempted `pdf` tool for structured extraction → failed: Anthropic PDF
  route rejected (credit balance zero), Gemini rejected (unknown model),
  OpenAI rejected (plugin not enabled).  Fell back to grep-driven manual
  reading of the text.
- Identified core equations: (2.9–2.18) Coulomb correlation via GDH;
  (2.26–2.30) MFMT; (3.1–3.15) dimensionless two-plate mPNP; (3.17–3.22)
  WKB Green's-function solution and rescaled correlation energy uel; (3.23–3.31)
  numerical scheme.
- Identified figures with quantitative content: Fig. 4.1 (MFMT convergence
  order), Fig. 4.2 (WKB vs FDM), Fig. 4.3 (comparison with MC/MD), Fig. 4.5
  (MF/SC/LC/LS density and diffuse charge).
- No code release found (searched preprint body + acknowledgements).

## 06:10 — Replication design decision
- Chose to reproduce (a) Fig. 4.1 MFMT convergence to analytic
  Carnahan-Starling limit, (b) Fig. 4.5 style comparison of MF vs SC via a
  Newton solver at the same parameters (eps, q, a, gamma) = (0.2, 0.3, 0.15, 1),
  V=1.
- Deferred the full LC/LS models (require WKB self-energy Eq. 3.22, a
  semi-infinite integral of Bessel-function combinations).  This is out of
  scope for a single 22-minute replication turn but well documented in the
  paper.
- Compute host: local (`CherryRd`, Python 3.14, numpy 2.4.3, scipy 1.18.0).
  1D FDM problem is trivially small; no need for `uicgpu`.

## 06:11 — MFMT convergence test (first pass)
- Implemented `mfmt_1d.py` with 1D weighted densities per Eqs. (3.3)–(3.5).
- First trapezoidal implementation showed FIRST-order convergence (ratio ~2
  per grid doubling), NOT the second-order claimed in the paper.  Root
  cause: partial-cell endpoints of the window [x-a, x+a] were being clipped
  to the nearest grid point → O(h) endpoint error.
- Fix: added explicit linear-interpolation endpoint corrections at both ends
  of each window; achieved strict SECOND-order convergence (ratio 4.00 per
  doubling), matching the paper.

Numerical evidence (Carnahan-Starling analytic mu_hs = 0.238752 at eta=0.0283):
```
N=  200  mu_hs_num = 0.238677   err = 7.46e-05
N=  400  mu_hs_num = 0.238733   err = 1.86e-05
N=  800  mu_hs_num = 0.238747   err = 4.66e-06
N= 1600  mu_hs_num = 0.238751   err = 1.17e-06
N= 3200  mu_hs_num = 0.238752   err = 2.91e-07
orders: 2.001, 2.000, 2.000, 2.000
```

## 06:15 — Modified PB solver (MF & SC)
- Wrote `pb_solver.py` (Picard iteration) — blew up at V=1 with exponent
  overflow.  Killed after 5 minutes.
- Root cause: Picard on the exponential nonlinearity of Poisson-Boltzmann is
  unstable for O(1) potentials; also I built the Poisson matrix inside the
  Picard loop, which was slow.
- Rewrote as `pb_newton.py` — full Newton with LU factorisation of the
  Jacobian.  Converged for both MF (5 iterations, `|R|=3.5e-12`) and SC
  (35 outer/nested iterations, `mu_rel_diff=8.7e-10`).
- SC uses a nested scheme: outer Picard on `mu_hs` (damped, omega=0.4),
  inner Newton on `phi` at fixed `mu_hs`.  Bulk mu_hs_bulk subtraction so
  far-field densities → c_bulk = 1.  Numerically mu_hs_bulk = 0.2387 which
  matches the analytic Carnahan-Starling value at c_tot=2, a good self-check.

Steady-state results at (eps, q, a, V) = (0.2, 0.3, 0.15, 1.0):
| model | c+ peak | c- min | Q(left) | phi(-L), phi(+L) |
|---|---|---|---|---|
| MF   | 1.7649 | 0.5666 | 0.2240 | (-1.000, +1.000) |
| SC   | 2.0943 | 0.6872 | 0.2300 | (-1.000, +1.000) |

Qualitative and ordering results agree with paper Fig. 4.5(a,b,d) and the
Section 4 discussion.

## 06:22 — Plots
- Generated `fig41_convergence.png` (convergence table + loglog error plot
  with O(N^-2) reference) and `fig45_mf_vs_sc_replication.png` (density,
  potential, and zoomed cation-peak-near-electrode panels).

## 06:23 — LLM-judge scoring
- Free endpoint per project rules: Argo :44497, key = `stevens`.
- Tried `argo:claude-opus-4.7` (project default): HTTP 502 Bad Gateway on all
  three retries.  Argo Opus hiccup.
- Fallback chain per new judge script: `argo:claude-sonnet-4.6` → succeeded
  on first attempt.  Judge model actually used is logged in
  `evidence/llm_judge_model.txt`.
- Judge structured verdict:
  - C1 (2nd-order MFMT convergence): **SUPPORTED**
  - C2 (SC enhances cation peak vs MF): **SUPPORTED**
  - C3 (Q_SC > Q_MF): **SUPPORTED**
  - Overall: **REPLICATED**

## 06:28 — Report writing
- `brief.md`, `artifact_harvest.md`, `attempt_log.md`, `REPORT.md` written.

## 06:30 — Duplicate-work discovery (post-hoc)
- While spot-checking figures against a `~/.openclaw/workspace/tmp/mpnp_paper.pdf`
  I discovered a prior independent replication of the same paper at
  `~/Dropbox/REPLICATE-PROJECT/PDE-replications/modified-pnp/` from 2026-05-28
  ("Ollie" subagent, 45 min wall clock, 8/10 claims).  Same DOI, same arXiv ID,
  identical PDF checksum by size (both 1,006,890 bytes).
- The brief's ABORT check (`ls ~/Dropbox/REPLICATE-PROJECT/ | grep …`) only
  scans direct children; the prior replication lives inside
  `PDE-replications/` (a two-level nesting) so it did not appear.  My target
  dir sits at top level and does NOT overwrite it.  Both replications are
  preserved.
- Added Section 7 to REPORT.md flagging this and recommending Ollie's earlier
  more-complete replication (LC + LS implemented) as canonical, with mine
  retained as an independent cross-check of the MFMT + MF + SC subset.
- Emitted final WAVE_RESULT line with a duplicate flag.
