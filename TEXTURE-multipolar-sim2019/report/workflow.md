# Workflow — Sim et al. 2019 replication (arXiv:1911.13224)

## Pipeline
acquire → parse → extract recipe → **build from scratch** → run → compare → package

1. **Read** paper text (`work/textures-multipolar-sim2019.txt`) + prepped recipe
   (`report/evidence/replication_recipe.json`). Identified the model: cubic j=3/2 Luttinger
   semimetal (4-band) with attractive d-wave (j=2 quintet) pairing; headline = weak-coupling
   TR-breaking d-wave eg=(1,i).
2. **Build** `work/sim2019_luttinger_bdg.py` from scratch:
   - 5 anti-commuting Dirac gamma matrices via Kronecker products; Clifford algebra verified.
   - Normal-state H0(k) Eq.(1) with PrBi params (c0=-6, c_eg=-2, c_t2g=-1, mu=-0.6).
   - Even-parity quintet pairing vertices M_a = gamma45 gamma_a.
   - Part A: linearized-gap pairing susceptibility per channel (leading instability).
   - Part B: 8x8 BdG condensation energy → quartic coefficient / q2 invariant (eg state selection),
     on a Fermi-surface shell (weak coupling) and whole-BZ (strong coupling).
   - Cross-checked O20 = 3Jz^2 - J^2 against the reused kernel's Stevens conventions.
3. **Run** on `~/comfyui-env/bin/python` (numpy 2.3.5). SAVE-EARLY after Part A first solve.
4. **Compare** to the three claims; scored honestly.
5. **Package** the 8 artifacts.

## Tools / versions
- Python: `/home/stevens/comfyui-env/bin/python` — numpy 2.3.5, scipy 1.17.0
- Extraction: `pdftotext` (poppler). `marker`/`nougat`/`pdflatex` NOT installed → documented interim.
- Runtime: ~11 s total (22^3 and up-to-46^3 grids; small 4x4/8x8 matrices).

## Reused kernel (provenance)
`ollie_multipolar_stevens_landau_kernel.py` (Stevens/multipole operators) — used to CROSS-CHECK
the j=3/2 O20 quadrupole convention against the paper's eg-quadrupole definition. The BdG/pairing
physics is a from-scratch build (the kernel is a CEF-susceptibility tool, not a BdG solver).

## Effort estimate
- Recipe + paper read: ~15 min (recipe pre-prepped)
- From-scratch code build + 3 physics-iteration refinements of Part B: ~40 min
- Packaging (8 artifacts): ~30 min
- Total: ~1.5 h. Closing the primary gap (one-loop q2 + self-consistent multi-gap BdG +
  topological invariants) is a substantial additional build, est. 1–2 days.
