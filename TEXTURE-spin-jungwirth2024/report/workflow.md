# Workflow — Jungwirth 2024/2025 altermagnetism replication

## Paper
- **Title:** Altermagnetism: an unconventional spin-ordered phase of matter
- **Authors:** Jungwirth, Fernandes, Fradkin, MacDonald, Sinova, Šmejkal
- **Ref:** arXiv:2411.00717v2 (dated 13 Mar 2025)
- **Type:** Perspective / review. No single quantitative benchmark stated.

## Method class
`analytic` → minimal model-Hamiltonian / tight-binding reimplementation (numpy).
Routed to spark-local CPU (small 2×2 matrices; runs in <1 s).

## Pipeline
1. **Parse** — `pdftotext` (`-layout` → marker.md prose; reading-order → nougat.mmd math).
   marker/nougat binaries not installed → documented interim fallback.
2. **Extract claim** — recipe already prepped (`report/evidence/replication_recipe.json`).
   Identified the ONE testable claim from the abstract + Fig. 1b: d-wave altermagnet =
   zero net magnetization + conserved momentum-dependent spin-split channels with a
   symmetry-protected sign structure.
3. **Build** — from-scratch 2-sublattice square-lattice altermagnet tight-binding model,
   no SOC (S_z conserved), C4-swapped anisotropic NNN hopping (t1≠t2) for the d_{x^2-y^2} (m=2)
   baseline, PLUS a **g-wave (m=4) coverage-flip extension** via 3rd-neighbour hopping
   (epsA=tg sin(2kx)sin(ky), swapped by the diagonal mirror), unified by an alpha knob
   (alpha=0→d, alpha=1→g). `work/jungwirth2024_altermagnet.py`.
4. **Run** — coarse-first BZ sweep n_k = 24 → 48 → 96 for BOTH waves + alpha scan, SAVE-EARLY to
   `work/jungwirth2024_result.json` after each grid.
5. **Compare** — 15 symmetry-exact checks vs the headline claim for d- AND g-wave (all 15 pass:
   M=0 exact, m=2/m=4 dominant harmonics, 2/4 nodal lines, C4-odd/C4-even + diagonal-mirror
   protection, 100% sign match, exact reduction to d-wave at alpha=0).
6. **Package** — 8 artifacts + evidence copy.

## Tools / versions
- Python: `/home/stevens/comfyui-env/bin/python`
- numpy 2.3.5, scipy 1.17.0
- pdftotext (poppler) for extraction interim
- pdflatex: not attempted here — REPORT.tex ships as source (standard when latex absent)

## Effort estimate
- Read + claim id: ~10 min
- Model build + run + convergence: ~15 min (runtime itself < 1 s)
- Packaging (8 artifacts): ~20 min
- Total: ~45 min, single spark node, no external compute.

## Reproduce
```bash
cd /home/stevens/textures-100/corpus/textures-spin-jungwirth2024/work
/home/stevens/comfyui-env/bin/python jungwirth2024_altermagnet.py
# -> prints 15/15 checks pass; writes jungwirth2024_result.json
```
