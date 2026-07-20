# Workflow — chung2009 replication (chiral spin liquid, flux 1/3)

## Paper
Chung, Yao, Hughes, Kim, "Nature of a topological quantum phase transition in a
chiral spin liquid model", arXiv:0909.2655 (2009). Model = Yao–Kivelson
(PRL 99, 247203, 2007) Kitaev-type exactly-solvable CSL on the star /
decorated-honeycomb lattice.

## Method class
Analytic / exactly-solvable model-Hamiltonian → **Majorana free-fermion
diagonalization** + **projection/fermion-parity counting**. No public code
(theory paper); full from-scratch rebuild. Runs on CPU in ~9 s.

## Pipeline
1. **Read** paper text (`work/textures-loop-current-chung2009.txt`) + recipe
   (`report/evidence/replication_recipe.json`). Identified the two checkable
   claims: `<Phi_x>(T=0)=1/3` (nA) and the transition at `g_c=sqrt3`.
2. **Build** `work/chung2009_kernel.py`:
   - 6-Majorana-site decorated-honeycomb unit cell; intra-triangle bonds `J`,
     inter-triangle bonds `J'=gJ`; anti-Hermitian `A(k)`, Hermitian `h(k)=iA(k)`.
   - Bulk gap `Delta(g)=min_k eps_+(k)` over a BZ grid → locate `g_c`.
   - Fukui–Hatsugai–Suzuki Chern number of the 3 occupied Majorana bands.
   - Sector counting for `<Phi_x>` and `n_DEG=4-3<Phi_x>`.
   - Finite-T `<Phi_x>(T)=P/(2+P)`, `P=prod tanh(eps/2T)` (Eq.13).
3. **Run** with `~/comfyui-env/bin/python` (numpy 2.3.5). SAVE-EARLY: headline
   counting written to `chung2009_result.json` before the gap scan.
4. **Compare** to paper: flux fraction exact; `g_c` to 0.41%; Chern nonzero→0.
5. **Package** the 8 artifacts (this file + REPORT.tex, extraction/*, etc.).

## Tools / versions
- Python: `~/comfyui-env/bin/python`, numpy 2.3.5, scipy 1.17.0
- Text extraction: `pdftotext` (poppler) — `marker`/`nougat` NOT installed
  (interim fallback, see extraction/ headers)
- `pdflatex` NOT installed → REPORT.tex ships as source
- Host: spark (ARM64 Linux)

## Effort
- Physics build + run: ~1 core-hour of agent time; compute ~9 s wall.
- Packaging (8 artifacts): ~0.5 hr.
- Reusable: the Majorana Bloch + FHS-Chern + finite-T flux kernel generalizes to
  any Kitaev-type / Yao–Kivelson free-Majorana CSL paper.

## Reproduce
```bash
cd /home/stevens/textures-100/corpus/textures-loop-current-chung2009/work
~/comfyui-env/bin/python chung2009_kernel.py
# -> writes chung2009_result.json (also copied to report/evidence/)
```
