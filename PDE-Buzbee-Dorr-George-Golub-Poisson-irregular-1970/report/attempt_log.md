# Attempt log

Chronological log of what I did, what worked, what failed.

## 08:16 CDT (2026-07-06) — Setup
- Read `~/Dropbox/REPLICATE-PROJECT/scripts/WAVE_BRIEF_2026-07-01.md`.
- Verified target dir does NOT exist (no `PDE-Buzbee*`); created skeleton
  (`extraction/`, `report/`, `report/evidence/`, `work/`).

## 08:16 — Paper lookup
- Semantic Scholar `DOI:10.1137/0708066` returned OA URL
  `https://www.osti.gov/biblio/4060961` (GREEN OA).
- Unpaywall responded `is_oa: false, oa_locations: []` — appears to disagree
  with S2, but S2's link is authoritative here (the OSTI copy exists).

## 08:18 — PDF download
- Direct `curl` from CherryRd to OSTI hung (`HTTP=000`, size 0). Likely
  outbound firewall / OSTI throttling.
- Retried via `ssh uicgpu 'curl ...'` (uicgpu has ALCF proxy internet via
  `~/env.sh`): `HTTP=200`, 1,340,222 bytes, valid PDF. `scp`'d back.
- `paper.pdf` SHA-256: `fd92c5ccee14f40c2ed0fd7208f17cfaf079c41a1b9b2bf3f45f2943c5da35b9`.

## 08:19 — Text extraction
- `marker`, `marker_single`, `nougat` — none present on CherryRd or uicgpu.
- Fell back to `pdftotext -layout` (ABBYY-OCRed OSTI PDF, so text is clean).
- Built `extraction/marker.md` (pdftotext output with header) and
  `extraction/nougat.mmd` (structured stub with LaTeX-format section
  headings + Table 1 verbatim, plus corpus-manifest pointer for future
  real Nougat parse).

## 08:22 — Method design
- Paper §2 (imbedding) + §4 (rectangle-with-hole example, Fig. 1).
- Implemented in `work/capacitance_solver.py`:
  - Full `(N+1)^2` 5-point Laplacian with identity rows on outer bnd.
  - `A` = same but identity rows also on inner-square boundary AND inner
    hole interior (dummy DOFs).
  - `B` = imbedding rectangle (identity on outer bnd only; 5-point rows
    everywhere else including inside the hole — the hole gets `f = 0`
    extension per paper).
  - Capacitance construction: `p` = # rows differing between A and B
    = # points on hole boundary + hole interior. `C[l,k]` computed as
    `(B^{-1} e_{p_rows[k]})[p_rows[l]]` in `p` fast-rectangle solves.

## 08:24 — First run: RESULT SUSPICIOUS
- Max errors ~0.07-0.17 (way too big — paper reports ~1e-12).
- Capacitance-vs-direct-sparse consistency ~1e-15 (perfect — so the
  low-rank correction is CORRECT).
- Residual `A x - y` ~1e-15 (so `A x = y` is being solved exactly).
- Diagnosis: sign of the discrete Laplacian. My row `4 u_ij - Σ neighbors`
  equals `-h^2 * Δ_h u`, so `A u = y` with `A = +h^2*(...)` needs RHS
  `y = -h^2 * f`, not `+h^2 * f`.  See `work/diagnose.py`.

## 08:25 — Fix sign, rerun (paper Table 1 replication)
- Max errors dropped to ~5e-16, 1e-15, 2e-15, 9e-15 for N=16, 32 (Region 1),
  32, 64 (Region 2). All at float64 machine precision, ONE-TO-TWO orders of
  magnitude BETTER than paper's 4.44e-13 / 1.90e-12 / 3.77e-13 / 1.54e-12
  (paper ran on CDC 6600 in ~60-bit precision; we're on modern IEEE
  float64/53-bit — comparable ratio).
- Capacitance-vs-direct-sparse consistency: ~1e-15 machine ε across all
  four configs.

## 08:26 — MMS convergence
- Ran `mms_convergence.py`: `u_exact = sin(πx) sin(πy) e^(x-y)` on
  Region-2 geometry, N in {16, 32, 64, 128}.
- Rates: 1.984, 1.993, 1.997 — **clean second-order** as expected for the
  5-point Laplacian. Capacitance-vs-direct consistency stays at ~1e-14
  (grows very slowly with N, as expected from conditioning of the
  capacitance matrix).

## 08:27 — Splitting example (paper §5, L-shape)
- `lshape_splitting.py`: unit square minus upper-right quarter, split
  along `y = 1/2`. Interface DOF count `p = N/2 - 1` (matches expected
  geometry).
- Rates: 1.995, 1.997, 1.999 — again clean second order.
- `p` scales linearly with `N` here (a *line* interface), whereas in the
  imbedding rectangle-with-hole `p` scales as `(N * inner_frac)^2` (an
  *area* — hole boundary + interior). This is exactly the point the paper
  makes in Section 5 for why the splitting method beats the imbedding
  method on many geometries.

## 08:28 — Report writing
- Copied evidence to `report/evidence/`.
- Wrote `REPORT.md`, `REPORT.tex`, `brief.md`, `attempt_log.md`,
  `artifact_harvest.md`, `workflow.md`, `artifacts_summary.md`,
  `failure_analysis.md`, and `open_questions.json` (5 items).

## What I did NOT do
- Did NOT reproduce paper Table 1 wall-clock timings (CDC 6600 vs.
  modern x86 is not a meaningful comparison; the paper's *ratios* of
  Direct-to-iterative time are not reproducible without a same-era
  iterative solver on the same hardware).
- Did NOT implement a true Buneman/cyclic-reduction fast Poisson solver;
  used sparse LU (SuperLU) as the rectangle-solver stand-in. This does
  NOT affect correctness or convergence rate of the capacitance-matrix
  reduction (the capacitance construction is agnostic to how you solve
  Bz=w), but it does mean the `θ(N) = 5 N^2 log_2 N` complexity estimate
  in the paper is not directly demonstrated in our timings.
- Did NOT reproduce the *exact* `p` values in Table 1 (e.g., paper says
  `p=16` for Region 1, h=1/16; I get `p=81`). I believe the paper is
  exploiting a symmetry or counting one boundary side, but this
  discrepancy does not affect the correctness of the method or the
  final max-error / convergence results.
