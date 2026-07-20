# Workflow — vedmedenko2008 replication

## Goal
Replicate the central claim of Vedmedenko, Even-Dar Mandel & Lifshitz (2008,
arXiv:0805.1216): odd-parity multipolar rotors on the rhombic Penrose tiling
show an *apparent* decagonal HBS superstructure but only **short-range order**,
with no long-range orientational order, due to 3-body frustration.

## Steps executed
1. **Read** paper text (`work/textures-multipolar-vedmedenko2008.txt`) and recipe
   (`report/evidence/replication_recipe.json`). Identified model: classical
   multipolar rotors Q_l0 (l=1..4, m=0) on Penrose vertices, long-range spherical
   Hamiltonian Eqs (1)-(2), open BC, slow-anneal MC with two-seed equilibration.
2. **Built physics from scratch** (`report/evidence/code/vedmedenko2008_penrose_multipole.py`):
   - Penrose tiling via de Bruijn pentagrid dual (no external tiling libs).
   - Circular open-BC patch, N=151 sites.
   - In-plane odd-parity rotors with dipolar angular kernel, radial exponent
     2l+1 (l=1 dipole, l=3 octopole), no cutoff.
   - Zero-T local-field (Gauss-Seidel) minimization + short annealing preamble,
     two independent seeds (equilibration check).
3. **SAVE-EARLY** to `work/vedmedenko2008_result.json` after first successful run.
4. **Diagnostics** for the claim: orientation histogram (n*pi/10 peaks), net
   magnetization, orientational correlation C(r), orientation structure-factor
   peak vs random baseline, frustration fraction at high-coordination vertices.
5. **Compared** to headline claim; all 5 checks pass for both dipole and octopole.
6. **Packaged** 8 artifacts + copied result JSON and code (incl. shared kernel)
   to `report/evidence/`.

## Runner
`/home/stevens/comfyui-env/bin/python` (numpy 2.3.5). Runtime < 1 s.

## Reproduce
```
cd /home/stevens/textures-100/corpus/textures-multipolar-vedmedenko2008
/home/stevens/comfyui-env/bin/python report/evidence/code/vedmedenko2008_penrose_multipole.py work/vedmedenko2008_result.json
```

## Kernel credit
`ollie_multipolar_stevens_landau_kernel.py` (TEXTURES-100 shared multipolar
kernel) — framing/discipline. Physics purpose-built (classical lattice rotors,
not single-ion CEF).
