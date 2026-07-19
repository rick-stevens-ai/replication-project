# Workflow — cheon2018 (arXiv:1803.06428)

## Narrative
1. Fetched PDF; pdftotext (~6.8k words); Nougat stub (GPU, sha256).
2. Extracted the four-band layered-AFM Hamiltonian (Eq.1) + Eq.2 degeneracy structure + SOT definition.
3. Implemented full 4x4 H(k) with exchange (Neel||z + FM canting m||x), Rashba(tau_z), interlayer hopping.
4. First attempt: raw off-diagonal Kubo for delta_S -> the interband/Berry components sat at numerical noise (~1e-18) for all m; only the collinear-allowed delta_S^x(E||x)=0.235 was resolved. Diagnosed via a component scan (all spin comps x E-dirs).
5. Refocused on the cleanly-reproducible mechanism: verified Eq.2 -> zeta bands EXACTLY degenerate at m=0 (3e-16), degeneracy lifted linearly in |m| (slope 0.755, residual 3e-4). This IS the paper's symmetry-breaking mechanism.
6. C3: confirmed collinear-allowed damping-like SOT present at m=0 (agrees with Refs 4,5).
7. Documented the extra-Berry-SOT magnitude as method-limited (honest PARTIAL). LLM-judge (free Argo sonnet-4.6): PARTIAL, coverage 6, agreement 5.

## Tools & codes
Python 3.13, NumPy, Matplotlib; pdftotext. code/cheon2018_replication.py (~180 LOC). 4x4 dense eigh over k-grid. LLM-judge -> argo:claude-sonnet-4.6 (free).

## Effort estimate
CPU-only, ~6s (60x60 k-grid eigh + 90x90 Kubo). Wall clock ~25 min incl. the Kubo-noise diagnosis + refocus. ~180 LOC, 2 major iterations.
