# Failure Analysis / Friction Log

**Paper:** Hastings, arXiv:1802.10124.
**Replication run:** 2026-07-05, sub-agent.

## What went smoothly

- Paper is short (compact 3-page arXiv typeset holds ~30+ pages of dense body) and its algorithm is one equation (Eq. 6): $H_s = H_Z - sB(X/N)^K$. Once the algorithm is on the page, coding it in numpy is straightforward.
- The main numerical claims (P_ov = Ω(1), constant improvement over Grover) are all directly measurable at N ≤ 12 with a plain dense-eigh approach.
- Fixed seed made every result deterministic across reruns.

## What went wrong / took extra time

### F1. Extraction tooling absent on host.
- Marker and Nougat are not installed on CherryRd (checked: `which marker marker_single nougat` → not found; `pip show marker-pdf nougat-ocr` → not installed).
- No central corpus of pre-parsed papers exists (`~/Dropbox/REPLICATE-PROJECT/central-corpus/` does not exist on this host).
- **Impact:** Two required artifacts (`extraction/marker.md`, `extraction/nougat.mmd`) had to be built from `pdftotext` output as clearly-labeled fallbacks. Structural fidelity is lower than a real Marker/Nougat parse (no auto-detected equations, no auto-reconstructed tables); the fallbacks recover text + hand-transcribed key equations, which is enough for the replication report but not enough to be treated as canonical parses.
- **Fix path:** Install Marker (`pip install marker-pdf`) + Nougat (`pip install nougat-ocr`) globally on CherryRd, or populate a central corpus with pre-parsed papers keyed by arXiv ID.

### F2. First simulator was too slow.
- The initial `build_HZ_ising` was a pure-Python triple-nested loop over 2^N basis states × N × N terms. For N=12 (4096 states × 144 terms) this ran at ~15 s just to build one Hamiltonian.
- **Fix:** vectorized the whole thing over the 2^N × N bit-array in one shot using `np.arange(dim)[:, None] >> ...` bit-slicing and a single `einsum('ij,ij->i', spins @ J, spins) * 0.5`. Dropped H_Z build from ~15 s to <10 ms at N=12.

### F3. `np.linalg.eigh` on 4096×4096 dense was still expensive.
- Full eigh was ~8.7 s per call at 4096×4096.
- **Fix:** switched to `scipy.linalg.eigh(..., subset_by_index=[0, 1])` (LAPACK `dsyevr`), which computes only the two smallest eigenvalues in ~4.2 s. That halves N=12 wall time.

### F4. Crash at the very end of the first full run because of a leftover variable name.
- After the full sweep completed (~20 minutes of compute), the `json.dump` block referenced `n_instances` (from an old version of the code) instead of the new `n_instances_per_N` dict. `NameError` → all 736 result rows lost. `results.json` was created as a 0-byte file.
- **Impact:** Had to rerun the full sweep. Total time cost ~15 additional minutes.
- **Fix:** Guarded the summary and dumped config with the new names; the second run completed cleanly in 716 s and produced the full `results.json` (478 kB, 736 rows).
- **Lesson learned:** Every future long-running experiment must write incremental checkpoints (e.g., append to `results.jsonl` per (ensemble, N, instance)) so a crash at the end doesn't destroy all evidence. Not fixed in this run because time budget forbid a third rerun, but noted for the workflow.

### F5. The paper's ``uniqueness / degeneracy'' promise is violated by every random ensemble we tested.
- Random unit-weight MAX-2-SAT and h=0 SK instances always have Z_2-flip symmetry (h=0 case) or accidental ties (integer weights case), giving 2--4 exact classical ground states per instance.
- Consequence: `min_gap` along the s-path is 0.0 for every instance (because the gap at s=0 vanishes with the classical degeneracy). Cannot directly test Theorem 3's ``gap stays Ω(1)'' statement without either (a) enforcing the paper's aux-spin reduction to N+1 spins, or (b) restricting to non-degenerate random instances.
- **Impact:** C2 (spectral gap) marked ``PARTIAL'' in the claims table. Every other claim was still reproducible: the algorithm returns the correct ground manifold (P_succ_direct = 1.000 always), the P_ov and the s=0/s=1 overlap are Ω(1), and the constant improvement over Grover is observed.
- **Fix path:** Implement the N → N+1 aux-spin embedding in a follow-up and rerun on those transformed instances. That is Q2 in the open-questions list.

### F6. N=12 pushed the edge of the compute budget.
- At $N=12$, dense-eigh cost dominates: 12 (K,b) × (X/N)^K evals × 6 s-values ≈ 12 s per instance × 4 instances × 2 ensembles = ~10 min for N=12 alone.
- **Impact:** Had to drop from 20 instances to 4 at N=12, and drop $K=5$ + $b=0.6$ at that size, to keep the whole sweep under ~15 min wall.
- **Fix path:** Switch to Lanczos-style sparse matvec: H_s is not sparse (X^K makes it dense) but the top of the spectrum can be reached via a symmetry-adapted basis reduction, exploiting the fact that (X/N)^K is a polynomial in the total-X operator which is diagonal in the Hadamard-rotated basis. That would give an ~50× speedup at N=12 and enable N=14--16 next time.

## Residual gaps (not fixed in this run)

- No test of Theorem 1's *log(N)* prefactor — needs N large enough that log N is meaningfully distinct from a constant (say N ≥ 32), which is beyond dense-simulation reach.
- No test of the ``hybrid algorithm'' correctness branch (Corollary 1) — that would need actually running the classical random-sampling fallback and verifying it succeeds when the exact algorithm fails. We validated the paper's exact-only branch.
- No hardware / real-quantum implementation. The paper's assumption of poly(N)-cost Hamiltonian simulation of H_s is inherited without further stress testing. See Q5 in open_questions.
- No independent verification of Theorem 3's exact spectral-gap proof — we did not test the analytic construction of the gap lower bound at all (paper's Sections V--VI), only the *consequence* (constant improvement over Grover in typical cases).
- Extraction fallbacks (Marker/Nougat) are not real parses. Reader should treat them as pointers to `work/paper.txt` + the paper PDF itself.
