# Workflow — Lohani et al. 2019 replication (arXiv:1901.03343)

## Method class
Many-body **exact diagonalization (ED)** of a spin-1/2 XXZ frustrated Heisenberg model on a
triangular flake. Routed to CPU (small dense/sparse matrices, seconds of runtime) — no GPU or
HPC queue needed for the 7- and 19-site flakes.

## Pipeline (acquire → parse → extract → build → run → compare → report)

1. **Acquire.** PDF already present: `textures-polar-lohani2019.pdf` (2.2 MB, arXiv:1901.03343v3).
2. **Parse.** `marker`/`nougat` binaries are **not installed** on this host
   (`which marker nougat` → not found). Fell back to `pdftotext` per the
   `computational-replication-execution` skill (§2). Produced:
   - `extraction/marker.md` — `pdftotext -layout` output + interim-status header.
   - `extraction/nougat.mmd` — `pdftotext` raw output + hand-transcribed LaTeX for the key
     equations (Eq. 1 Hamiltonian, Eq. 2 helicity, binding-energy Eq. 4–5, winding Eq. 12).
   Both are flagged as interim; regenerate with real Marker/Nougat when available.
3. **Extract recipe.** Model, couplings, and the two checkable quantities read directly from the
   paper text (Eq. 1; the many-magnon-bound-state definition; the $C_\perp\approx0.6$–$0.8$ range).
4. **Build.** From-scratch Python ED (`work/lohani_ed.py`, copied to `report/evidence/`). No author
   code exists or was used. Fixed-$S_z$ bitstring basis, sparse `csr_matrix` Hamiltonian, flip-flop
   off-diagonals, `scipy.sparse.linalg.eigsh(k=1, which='SA')`.
   *Reuse note:* the skill ships `scripts/spin_ed_probes.py` (fixed-$S_z$ basis, sparse H builder,
   binding sweep, $C_\perp$, correctly-zero chirality probe) — the in-repo `lohani_ed.py` is the
   equivalent per-paper implementation and is the frozen artifact here.
5. **Run.** `/home/stevens/comfyui-env/bin/python work/lohani_ed.py` — 7-site field sweep +
   binding analyses ($J_2=0.5$ and $0.7$) + 19-site flake up to $N_f=6$. Total runtime **~9.2 s**.
5b. **Larger-flake FSS (COVERAGE-FLIP).** `work/lohani_fss.py` reruns the ED with sparse Lanczos on
   flakes $N=7,19,\mathbf{37}$ (37 ≈ the paper's 31-site cluster), computing the **low-lying spectrum**
   ($k{=}4$–$6$ states via `eigsh`, not just $k{=}1$) to resolve the near-degenerate
   skyrmion/antiskyrmion **tunneling splitting** $\Delta_{\rm tun}=E_1-E_0$, plus $C_\perp$ and binding
   vs $N$. $C_\perp$ is vectorized (numpy bit-ops + `searchsorted`) so the $N=37$, $N_f=5$ sector
   (dim ≈ 436k) fits the budget. Total runtime **~74 s** (largest single diagonalization ≈ 46 s).
6. **Compare.** Binding energy $E_0^B<0$ for all $N_f\ge2$ (all flakes); transverse anticorrelation
   $C_\perp=0.73$ (19-site, $N_f=4$) inside the paper's 0.6–0.8 window; raw scalar chirality
   exactly 0 (expected — see failure_analysis.md). **New:** the skyrmion-sector tunneling splitting
   collapses from $\sim0.23$ (N=7, no skyrmion) to $\sim10^{-2}$ and down to $\sim10^{-14}$ (N=19,37),
   reproducing the paper's exponentially-small-bandwidth claim with the correct $N_f\bmod3$ selection
   structure.
7. **Report.** This 8-artifact package.

## Tools & versions
| Tool | Version / note |
|------|----------------|
| Python | `/home/stevens/comfyui-env/bin/python` (numpy/scipy env) |
| scipy | `scipy.sparse.linalg.eigsh` (Lanczos) + `scipy.sparse.csr_matrix` |
| numpy | array/linalg backend |
| pdftotext | `/usr/bin/pdftotext` (Poppler) — extraction fallback |
| marker | **absent** (not installed) |
| nougat | **absent** (not installed) |

## Effort estimate
- Physics build + run: complete. Base ED ~9 s; the COVERAGE-FLIP FSS run (`lohani_fss.py`, N up to 37) ~74 s.
- Packaging (this session): extraction fallback + 8 report artifacts, ~30 min.
- The largest remaining refinement (N=61,91 via matrix-free eigsh for full thermodynamic convergence)
  is estimated ~2–3 days including build and a larger-memory host (nuc13 62 GB or uicgpu A100).

## Compute target
CPU host, local. The 7-site sectors are trivial; the 19-site sectors diagonalize in seconds. The
$N=37$ flake ($N_f=5$ sector, dim ≈ 436k) diagonalizes in ~46 s with sparse Lanczos + vectorized
$C_\perp$ — well within budget. Pushing past $N=37$ (61/91 sites, sectors in the tens of millions)
would need a matrix-free `LinearOperator` and a larger-memory node.
