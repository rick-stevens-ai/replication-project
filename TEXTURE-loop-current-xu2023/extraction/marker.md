# Extraction marker — arXiv:2306.16192

**Paper:** Y. Xu, S. Capponi, J.-Y. Chen, L. Vanderstraeten, J. Hasik,
A. H. Nevidomskyy, M. Mambrini, K. Penc, D. Poilblanc,
*"Phase diagram of the chiral SU(3) antiferromagnet on the kagome lattice"*,
arXiv:2306.16192v1 [cond-mat.str-el], 28 Jun 2023.

**Extraction method:** `pdftotext -layout paper.pdf paper.txt` (native text layer
present; no OCR / vision needed). 1505 lines extracted. Equations that render as
images in the two-column layout (esp. matrix A1) were reconstructed by hand from
the surrounding text + the printed matrix fragment.

## Classification note (HONEST)
Assigned class: **loop-current**. This is a **PARTIAL / adjacent** fit, not an exact
one. The paper is a *many-body SU(3) spin* model (chiral / topological spin liquid on
the kagome lattice), solved by exact diagonalization (Lanczos, 21/27-site tori),
MPS on cylinders, and PEPS/PESS tensor networks. It is **not** a tight-binding
loop-current *metal* (no orbital-current order parameter, no Peierls-flux band
Chern insulator as the headline result).

The genuine loop-current *connection* is real but structural: the chiral 3-site
permutation term `iK_I Σ(P_ijk − P_ijk^{-1})` breaks **time-reversal and reflection**
(preserving their product) — the defining symmetry signature of loop-current order —
and in the single-magnon sector this term enters the 3×3 kagome Bloch matrix (Eq. A1)
**exactly as an imaginary (Peierls-like) hopping** `±iK_I`, i.e. the same TRS-breaking
complex-hopping object the shared loop-current kagome kernel builds.

## What is in-scope for an overnight single-node replication
The paper's TSL / CSL / double-Chern-Simons claims require ED + tensor-network
machinery (QSpace SU(3)-symmetric PEPS, CTMRG) that is out of scope here → **marked,
not faked**. What IS fully machine-checkable and analytical:

- **Eq. (1):** the Hamiltonian `H = J Σ P_ij + K_R Σ(P_ijk+P_ijk^{-1}) + iK_I Σ(P_ijk−P_ijk^{-1})`.
- **Eq. (2):** sphere parametrization `J=cosθcosφ, K_R=cosθsinφ, K_I=sinθ`.
- **Sec. III E:** FM energy per site `e_F = 2J + 4K_R/3`.
- **Eq. (A1):** the 3×3 single-magnon Bloch matrix (chiral kagome hopping).
- **Sec. III E:** q=0 magnon energies `{0, −6(J+K_R) ± 2√3 K_I}`.
- **Eq. (3):** one-magnon instability line `J+K_R < −|K_I|/√3` (FM stability).
- Dispersion depends only on `(J+K_R)` and `K_I`.
- On the boundary the 0-energy band becomes **flat**, with chiral hexagon modes
  of amplitude `e^{ijπ/3}`.

These 5 quantitative claims form the replication target.
