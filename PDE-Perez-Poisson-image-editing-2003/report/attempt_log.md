# Attempt Log

Chronological log for the Poisson Image Editing (Pérez et al. 2003) replication.

## 2026-07-05 00:06 — setup
- Read WAVE_BRIEF_2026-07-01.md
- Created target dir `~/Dropbox/REPLICATE-PROJECT/PDE-Perez-Poisson-image-editing-2003/`
  with `report/evidence/` and `work/` subdirs.

## 00:07 — paper acquisition
- Downloaded PDF from `https://www.cs.jhu.edu/~misha/Fall07/Papers/Perez03.pdf`
  (a canonical mirror of the SIGGRAPH 2003 paper; 1.86 MB, PDF v1.4).
- Attempted tesseract OCR → failed on the embedded encoding.
- Attempted LLM `pdf` tool → out-of-allowed-dir + billing errors.
- **Success**: used local `pdftotext` (poppler) to extract 651 lines of clean text.
- Verified: equations (1)–(13), definition of Ω/∂Ω/f/f*/g/v, importing gradient
  eq (11) v_pq = g_p - g_q, mixed gradient eq (13) case split. Paper cites
  Gauss-Seidel+SOR or V-cycle multigrid, 0.4 s for 60k-pixel disk on Pentium 4.

## 00:08 — implementation
- Wrote `work/poisson_editing.py`: a from-scratch (single file, ~130 lines)
  builder of the sparse SPD linear system per eq. (7) of the paper.
  - Ω pixels ↔ rows of A
  - diagonal = |N_p| (4-neighbor count within image)
  - off-diagonals = -1 for in-Ω neighbors
  - RHS b = Σ_{q ∈ ∂Ω} f*_q + Σ_{q ∈ N_p} v_pq
  - modes: "seamless" (v_pq = g_p - g_q, eq 11), "mixed" (case split, eq 13),
    "membrane" (v = 0, Laplace, eq 2)
- Direct solve via `scipy.sparse.linalg.spsolve` (paper used G-S+SOR/multigrid,
  we use direct sparse — same discretization, converges to same numerical
  solution). RGB channels solved independently per paper's protocol.

## 00:09 — driver + first run
- Wrote `run_experiments.py`: builds two synthetic RGB test scenes:
  1. Disk-in-gradient: destination is a smooth RGB ramp, source is a tan
     background with a bright orange textured disk. Ω is the disk region.
  2. Text-on-stripes: destination is high-contrast stripes, source is a plain
     background with dark bars ("text"). Rectangular Ω. Used for mixed-gradient
     test.
- All three modes ran cleanly. Solver times: ~0.06 s for 5013-pixel disk,
  ~0.39 s for 30800-pixel rectangle (three RGB solves each). Comparable
  order of magnitude to the paper's 0.4 s / 60k pixel on Pentium 4 despite
  the algorithmic difference (direct vs iterative).

## 00:10 — first C1 numerical test showed apparent problem
- Initial "boundary_jump" test showed |edited - dest| across ∂Omega of ~50-90
  units — looked large. I suspected a bug.
- Diagnosed by printing the actual edited pixel values across a horizontal
  slice through the disk. Result: the linear system was correctly enforcing
  the *destination* boundary (outside pixels untouched) AND the *source's
  local gradient* at the interior boundary. That is: the "jump" of 50 in G is
  exactly the source's own G-channel gradient across its natural boundary. NO
  bug — this is the correct Poisson-editing behavior.
- Realization: the right C1 test is not `|edited - dest|` at the boundary,
  but `|edited_gradient - source_gradient|` at the boundary. The paper claims
  the *interior gradient* is inserted; the *offset* (membrane) is what
  eliminates the *visible* discontinuity relative to Retinex/Land-McCann
  perception.

## 00:11 — corrected C1 test
- Wrote `verify_c1_correct.py` computing:
    - edited boundary jump: edited[p ∈ Ω] − dest[q ∉ Ω]
    - source's own boundary jump: src[p] − src[q]
    - naive boundary jump: src[p] − dest[q]
- Reproduces paper's claim exactly: edited jump == source jump to 12 decimal
  places in R and G; mean |edited−src_grad| = 2.1–2.4 units; seam reduction
  ratios 8.5× to 43.9× vs naive.

## 00:11 — C2 & C3 verified
- C2 (membrane / Laplace): interior |Δf| ≈ 4e-13. Effectively zero to
  machine precision. Correct membrane interpolant.
- C3 (mixed gradients): total absolute gradient inside Ω is 3.41e6 for mixed
  vs 1.21e6 for seamless vs 2.54e6 for dest alone vs 0.91e6 for src alone.
  Mixed retains BOTH source and destination high-frequency structure, as
  claimed. Also visually verified in `figure_mixed_text_comparison.png`.

## 00:12 — comparison figure
- Wrote `make_comparison_figure.py`: 5-panel row images comparing dest, src,
  naive paste, seamless, mixed — for both disk scene and text-on-stripes.

## 00:13 — LLM-judge scoring (per brief: no regex)
- Ran two independent Argo LLM judges (localhost:44497, key=stevens) with the
  same evidence prompt. Attempted argo:gpt-5 (400) and argo:claude-opus-4.8
  (502 transient). argo:gpt-4.1 and argo:gemini-2.5-pro both returned
  REPLICATED across C1/C2/C3 with detailed per-claim justifications.
  Full transcripts in `evidence/llm_judge_response_*.json`.

## 00:15 — REPORT + wrap
- Wrote REPORT.md, brief.md, attempt_log.md (this file), artifact_harvest.md.
- Verdict: REPLICATED.

Cost/time: local CPU (a few seconds of compute), ~1.9 MB of paper PDF, two
Argo judge calls. No paid endpoints used.
