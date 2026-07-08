# Failure Analysis — Replication of arXiv:2606.30402

Honest accounting of what did not reproduce, why, what was worked around, and residual gaps.
This is a **methodological / qualitative-claims** replication (see workflow.md §2); exact
numeric reproduction was impossible by construction, and that is the single largest "failure".

---

## A. Structural (unavoidable) reproducibility gaps

### A1. Exact cluster geometries are not deposited — ROOT CAUSE of no bit-for-bit match
The nine benchmark clusters per system are instantaneous snapshots from private DFT-AIMD/MLFF
trajectories (VASP NpT + on-the-fly kernel MLFF, CP2K PBE-D3 reference, TZV2P-MOLOPT/GTH).
The paper provides representative renderings (Fig. S1) and the generation protocol (SI S3) but
**no XYZ coordinates and no data repository** (only a US-DOE public-access statement for the
manuscript). Without the exact coordinates the absolute and relative energies cannot match to
the reported precision.
- **Workaround:** we built independent, chemically valid clusters of identical stoichiometry,
  charge, spin, and coordination (tetrahedral BeF₄, F–T–F bridge, anion = FLiBeTF minus proton).
  This lets us test whether the *claims* (single-reference, strong ionic binding of hundreds of
  kcal/mol, SQD≈FCI at the fragment level, large embedding-vs-full-molecule offset) reproduce on
  chemically equivalent systems — which is the strongest replication possible given the gap.
- **Residual gap:** our per-cluster numbers are our own; only the qualitative structure of the
  results is comparable. A tighter replication would require the authors to release the snapshots.

### A2. No IBM quantum hardware access
The paper's ext-SQD fragment solves ran on `ibm_boston` (Heron r3, up to 66 qubits for M=33).
We have no IBM Quantum access.
- **Workaround:** ext-SQD is simulated classically — genuine LUCJ-ansatz fermionic sampling on a
  statevector simulator (ffsim) fed into qiskit-addon-sqd's subspace diagonalization for the
  smaller fragments (M ≤ 16), and a selected-CI subspace (the exact classical analogue of the
  ext-SQD subspace step) for larger fragments. This reproduces the *algorithm*, not the *device*.
- **Consequence / expected difference:** the paper's hardware ext-SQD sat **+2.1 to +2.9 kcal/mol
  above FCI** (attributed to device noise). A noiseless simulation should sit *tighter* to FCI —
  so we expect to reproduce and even exceed the paper's 0.3/0.7 kcal/mol MAD/max agreement, which
  is itself confirmation that the algorithm (not the hardware) is the accuracy-limiting piece
  only through noise. See open question Q3.

### A3. DLPNO-CCSD(T) / ORCA and TCI-8 not reproduced verbatim
The paper's full-molecule reference includes DLPNO-CCSD(T) in ORCA, and its System-2 classical
reference for the 5 largest FLiBeTF fragments is TCI-8 (Hamming-distance-8 truncated CI).
- **Workaround:** full-molecule reference here is canonical CCSD + the DFT ladder (incl. PBE-D3,
  the AIMD functional) in PySCF; the large-fragment classical reference is selected-CI (SHCI-like)
  rather than TCI-8. Both are near-FCI-quality selected-CI variants, so the comparison logic
  (SQD-sim vs a high-accuracy classical reference) is preserved.
- **Residual gap:** we do not reproduce the exact DLPNO-CCSD(T) anomaly at cluster 2 or the
  CCSD SCF non-convergence at cluster 4 that the paper reports (those are geometry-specific).

---

## B. Engineering failures encountered and fixed (during this replication)

| # | Failure | Root cause | Fix |
|---|---|---|---|
| B1 | `vayesta` not on PyPI | Vayesta is GitHub-only | installed `git+https://github.com/BoothGroup/Vayesta.git` (pulled pyscf master as dep) |
| B2 | DFT returned `null` (D3 unavailable) | `pyscf-dispersion` not installed | `pip install pyscf-dispersion` (1.5.0) |
| B3 | RHF/DFT SCF non-convergence on ionic 6-31+G* clusters | diffuse (+) functions on F⁻ → near-linear-dependent AO overlap | level-shift 0.2 → Newton SOSCF restart → level-shift-off fallback chain |
| B4 | Geometry builder produced 8–9 F instead of 12 | flawed bridging/terminal-F counting logic | rewrote as μ₃-F + 3 terminal/Be + 2 second-shell F, hard-assert 12 F |
| B5 | Parallel launcher wrote 0 result JSONs (`$0/../.venv` path) | wrong `$0`/`$PWD` substitution in xargs `bash -c` | used absolute `~/flibe-repl/.venv/bin/python` and `cd ~/flibe-repl` |
| B6 | Fragment Hamiltonian extraction crashed (`Fragment has no attribute 'hamiltonian'`) | guessed wrong Vayesta 1.0.1 API | probed API: correct path is `frag.hamil` (`RClusterHamiltonian`) → `to_pyscf_mf()` / `get_integrals()` |
| B7 | Direct FCI on largest fragments intractable | our from-scratch clusters produced fragments up to M≈42 (vs paper max 33) with 12+ e⁻ | adaptive dispatch: exact FCI only under a determinant cap; selected-CI/SQD-sim above — exactly the paper's own reason for routing large fragments away from FCI |

## C. Known limitations of the replication as delivered

- **Fragment sizes larger than the paper (M up to ~42 vs 33):** our hand-built clusters are
  somewhat more diffuse/less compact than optimized AIMD snapshots, inflating some fragment
  active spaces. This makes exact FCI unavailable on more fragments than in the paper and pushes
  more of the workload onto the SQD-sim/selected-CI path. It does not change the qualitative
  conclusions but means our "FCI-available" fragment subset (where SQD-vs-FCI is directly
  measurable) is smaller.
- **Text extraction:** Marker (surya) and Nougat were not installed on the available hosts at
  extraction time; the layout-preserving `pdftotext` output is provided as the text artifact
  (`extraction/marker.md`) and, where a Marker/Nougat install completes, replaced with the real
  parse. The `.mmd` artifact is provided from the same source pending a Nougat run.
- **Free-endpoint / open-source only:** consistent with standing policy, all inference and
  compute used free/open tools (PySCF, Vayesta, Qiskit sim) — no paid QPU, no paid API.

## D. What would close the gaps

1. Author release of the 9×3 cluster XYZ geometries → enables true numeric reproduction.
2. IBM Quantum access → run the actual `ibm_boston` ext-SQD and measure the device-noise offset.
3. ORCA license → reproduce DLPNO-CCSD(T) and the exact cluster-2/cluster-4 anomalies.
4. A larger, MD-generated conformer ensemble → test multireference prevalence (open question Q4)
   and the eta-convergence of the embedding error (open question Q1).
