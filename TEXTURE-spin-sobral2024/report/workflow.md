# Workflow — sobral2024 (arXiv:2410.10949)

## Narrative
1. Fetched PDF; pdftotext (~12.7k words); Nougat stub (GPU, sha256).
2. Identified the reproducible headline (subtitle): spin-symmetric band splitting = split Fermi surfaces with preserved spin-rotation symmetry. Located Appendix-C chargon model Eqs C19-C21.
3. Implemented eps_k, g_k (sublattice-space vector), E±=eps±|g_k| exactly.
4. C1: split FS (2|g_k| range [0,8.06]); d-wave g_z node on diagonal, max on axis.
5. C2: verified spin-rotation symmetry via BAND DEGENERACY (within-band spin splitting 2.7e-15) since g.tau acts in sublattice not spin space. (Fixed initial mistake of using individual-eigenvector <Sz>, which is arbitrary for degenerate doublets.)
6. C3: contrast - same d-wave form factor in SPIN space gives spin pol=1.0 (ordinary altermagnet, qualitatively different).
7. LLM-judge (free Argo sonnet-4.6): PARTIAL, coverage 5, agreement 6.

## Tools & codes
Python 3.13, NumPy, Matplotlib; pdftotext. code/sobral2024_replication.py (~180 LOC). LLM-judge -> argo:claude-sonnet-4.6 (free).

## Effort estimate
CPU-only, ~1s. Wall clock ~20 min incl. extracting App-C eqs + fixing the C2 degeneracy metric. ~180 LOC, 2 iterations.
