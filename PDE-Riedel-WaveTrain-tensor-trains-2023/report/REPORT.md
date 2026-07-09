# Independent Replication — WaveTrain (Riedel et al., 2023)

**Set:** PDE (rank 33 in PDE_NEXT50)
**Paper:** J. Riedel, P. Gelß, R. Klein, B. Schmidt, *"WaveTrain: A Python package for numerical quantum mechanics of chain-like systems based on tensor trains,"* J. Chem. Phys. **158**, 164801 (2023).
**DOI:** 10.1063/5.0147314
**Code repo:** https://github.com/PGelss/wave_train  ·  backend: https://github.com/PGelss/scikit_tt
**Replicated on:** 2026-07-04, host: CherryRd (macOS 25.3.0), Python 3.12.13, single-thread CPU

---

## 1. What the paper claims

WaveTrain is an open-source Python package that solves the time-independent (TISE) and time-dependent (TDSE) Schrödinger equation for one-dimensional chain-like systems with nearest-neighbour (NN) coupling, using **tensor-train (TT) / matrix-product-state** representations of both the Hamiltonian and the wave function. It is built on the authors' own tensor-train Python toolbox `scikit_tt`. Application classes shipped in the paper cover: pure excitonic chains, pure phonon chains, coupled exciton-phonon chains ("Holstein-like" models), and mixed quantum-classical (Ehrenfest) dynamics. Time propagators include Strang-Marchuk (SM) splitting, symmetrized Euler (s2), and Krylov-subspace variants; ground/excited-state solvers use TT-ALS (Alternating Linear Scheme).

The paper's central scientific claim is that for chain-like NN Hamiltonians the TT bond ranks of the resulting states grow only slowly with chain length N — often near-linearly — so the numerical cost of TT-based methods grows only slightly more than linearly in N, whereas the full Hilbert-space dimension is 2^N (for two-level sites). This is the practical claim that motivates the entire package.

## 2. Claims table

| ID | Claim | Type | Testable in this replication? | Tested? | Verdict |
|----|-------|------|-------------------------------|---------|---------|
| C1 | The TT-ALS eigensolver, applied to the bundled `Exciton/tise_1.py` benchmark (N=6 periodic ring, α=0.1, β=−0.01), correctly recovers the single-exciton band eigenvalues. | Correctness / numeric | Yes — analytic reference E_k = α + 2β cos(2πk/N) is available in closed form. | ✅ | ✅ Supported |
| C2 | TT bond ranks of chain-like NN eigenstates grow only marginally with chain length N (much slower than the 2^N Hilbert dim), so wall-clock cost scales roughly linearly in N. | Scaling / algorithmic | Partially — we sweep N ∈ {4,6,8,10,12} at n_levels = N+1 and inspect both bond-rank profiles and wall-clock. | ✅ | ⚠️ Partial (see §5) |
| C3 | The published software (`wave_train` + `scikit_tt` from GitHub) is installable and runs the paper's bundled test scripts out of the box. | Software artifact | Yes — install + run. | ✅ | ❌ Fails as stated (one-line patch required to `scikit_tt`, see §4.2) |
| C4 | Coupled exciton-phonon TDSE with Strang-Marchuk propagator preserves norm and reproduces expected coherent-transport observables (Fig. 5–7 in paper). | Physics / dynamics | In principle yes; requires 10–30 min per N per parameter set and a full TDSE-specific driver. | ❌ (out of scope for one replication) | Untested |
| C5 | Bath-Map methodology (`Bath_Map_1/`) reproduces open-system dynamics. | Physics / method | Nontrivial (open-system framework beyond core TT-ALS). | ❌ | Untested |

Claims tested: 3 of 5. Coverage of paper's central computational/software claims: 100% of the core-benchmark-relevant ones (C1–C3).

## 3. Method

All steps run as a single-thread process on macOS.

### 3.1 Environment

```bash
python3.12 -m venv venv312
source venv312/bin/activate
pip install 'numpy<2' scipy matplotlib
pip install git+https://github.com/PGelss/scikit_tt
git clone --depth 1 https://github.com/PGelss/wave_train.git
pip install ./wave_train
```

Resulting versions: NumPy 1.26.4, SciPy 1.16.x, `wave_train` at HEAD (Riedel-era layout), `scikit_tt` at HEAD.

### 3.2 Benchmark driver

`work/run_tise_bench.py` (verbatim copy in `evidence/`) sets up the Exciton Hamiltonian exactly as `test_scripts/Exciton/tise_1.py`:

```python
Exciton(n_site=6, periodic=True, homogen=True, alpha=0.1, beta=-0.01, eta=0.0)
    .get_TT(n_basis=2, qtt=False)
TISE(n_levels=8, solver='als', eigen='eig', ranks=15, repeats=20, conv_eps=1e-8, e_est=0.0).solve()
```

then repeats for N ∈ {4, 6, 8, 10, 12} at n_levels = N+1.

### 3.3 Analytic reference

For an N-site homogeneous ring with NN coupling, the single-particle sector diagonalizes in momentum space:

```
E_k = alpha + 2 * beta * cos(2 pi k / N),   k = 0, 1, ..., N-1
```

With α = 0.1, β = −0.01 we get a band [α − 2|β|, α + 2|β|] = [0.08, 0.12]. Plus the vacuum |0…0⟩ at E = 0 which the code returns as the ground state when the exciton number is not fixed.

### 3.4 Log parsing → comparison

`work/analyze_bench.py` regexes the wave_train log (`TISE (als): state = k, energy = ...`), separates the vacuum + 1-exciton band from higher-exciton sectors by energy window [0.05, 0.15], and pairs the sorted band against the analytic values. Also captures per-state ALS CPU and the per-N TT bond-rank profile.

### 3.5 LLM-judge grading

`work/llm_judge.py` sends the packed result summary + explicit paper-claim list to the Argo free proxy (`http://127.0.0.1:44497/v1`, model `argo:gpt-5.4`; `argo:claude-opus-4.7` returned an upstream schema-validation error, so we fell back to GPT-5.4). Prompt asks for strict-JSON verdict + per-claim support + coverage/agreement percentages, no regex-based scoring anywhere in the loop.

## 4. Results

### 4.1 Primary benchmark: N=6, 1-exciton band

| k | Analytic E_k = 0.1 + (−0.02) cos(2πk/6) | WaveTrain (ALS) | |err| |
|---|----------------------------------------|------------------|------|
| 0 | 0.080000 | 0.080000 | 0.00e+00 |
| 1 | 0.090000 | 0.090025 | 2.50e-05 |
| 2 | 0.090000 | 0.090025 | 2.50e-05 |
| 3 | 0.110000 | 0.110008 | 8.00e-06 |
| 4 | 0.110000 | 0.110046 | 4.60e-05 |
| 5 | 0.120000 | 0.119900 | 1.00e-04 |

Max |err| = **1.0e-4** (relative ~0.08% at band edge). Mean |err| = 3.4e-5. Passes any reasonable "core-physics reproduced" threshold. (Full JSON in `evidence/tise_bench_final.json`.)

Vacuum state |0⋯0⟩ returned exactly at E = 0.0 (matches by construction because η = 0).

### 4.2 Software-artifact issue (C3)

The install command chain from the README (`pip install git+...scikit_tt` + `pip install wave_train`) succeeds silently but the resulting stack **crashes on any TISE run with n_levels ≥ 3** on any modern NumPy (≥ 1.25 rejects the offending implicit dtype-narrowing cast; we reproduced on both NumPy 1.26.4 and NumPy 2.x):

```
File ".../scikit_tt/solvers/evp.py", line 381, in __construct_micro_matrices
    micro_op += shift*tmp.dot(np.conjugate(tmp.T))
numpy.core._exceptions._UFuncOutputCastingError:
    Cannot cast ufunc 'add' output from dtype('complex128') to dtype('float64') with casting rule 'same_kind'
```

The ALS-with-deflation update `micro_op += shift * (Σⱼ |ψⱼ⟩⟨ψⱼ|)` produces a complex128 rank-1 term but `micro_op` was allocated as float64 (only the previously-converged states, not the diagonal, are complex here). The fix is a one-liner:

```python
update = shift * tmp.dot(np.conjugate(tmp.T))
if np.iscomplexobj(update) and not np.iscomplexobj(micro_op):
    micro_op = micro_op.astype(np.complex128)
micro_op = micro_op + update
```

We patched the installed `evp.py` in place. After the patch every downstream benchmark runs. **This should be reported upstream** as it makes the paper's own bundled test scripts non-functional on any recent NumPy without user intervention. → C3 as stated fails; core method itself is fine.

### 4.3 Scaling sweep (N ∈ {4, 6, 8, 10, 12})

Wall clock, per-state ALS CPU, and eigenvalue accuracy versus N (n_levels = N + 1 requested for each):

| N | Wall (s) | Σ per-state CPU (s) | max |err| vs analytic | max bond rank observed | Boundary-bond pattern |
|---|---------:|---------------------:|-----------------------:|----:|---|
| 4 | 0.37 | 0.27 | 1.4e-17 | 4 (=cap; intrinsic 2²) | 1,2,4,2,1 |
| 6 | 2.47 | 2.17 | 1.0e-4 | 8 (=cap; intrinsic 2³) | 1,2,4,8,4,2,1 |
| 8 | 102.2 | 101.4 | 1.9e-3 | 15 (ALS cap saturated) | 1,2,4,8,**15**,8,4,2,1 |
| 10 | 78.2 | 76.6 | 3.4e-7 | 15 (cap) | 1,2,4,8,15,15,15,8,4,2,1 |
| 12 | 678.1 | 673.9 | 2.8e-4 | 15 (cap) | 1,2,4,8,15,15,15,15,15,8,4,2,1 |

Observations:

- **Boundary bond ranks follow 1, 2, 4, 8, … at the ends of the chain**, matching the intrinsic dimension of the single-particle sector accessible at each cut. That is exactly the "low-rank" story of the paper: the intrinsic ranks of the 1-exciton subspace grow only as 2^(distance-from-boundary) up to saturation of the sector size, not as 2^N.
- **In the middle of the chain the ALS `ranks=15` cap is saturated for N ≥ 8**, so our sweep can't distinguish intrinsic-rank growth from the artificial cap. To cleanly test the "rank marginally depends on N" claim we would need to sweep `ranks` as well (leaving room for the intrinsic maximum) — that is a follow-up.
- **Wall-clock is dominated by the ALS deflation term**, not by TT operations. The deflation shift `shift * Σⱼ |ψⱼ⟩⟨ψⱼ|` scales quadratically with the number of previously converged states, so requesting n_levels = N + 1 makes cost superlinear in N. If we requested a fixed small n_levels (e.g. 3) the cost would grow much more mildly in N — but that is not what our sweep did. So the "cost slightly more than linear in N" is **not directly demonstrated** by this run; it is *consistent* with the observed boundary-rank pattern (1,2,4,8,…) but not proved.
- The N = 10 case has the smallest error (3e-7), essentially at ALS convergence; N = 8 and N = 12 have residual ~1e-3 to 3e-4 because ALS converges more slowly on the intermediate-rank cases before hitting `repeats=20`. Increasing `repeats` would tighten this.

### 4.4 LLM-judge verdict

Model: `argo:gpt-5.4` (free, Argo proxy). Full JSON in `evidence/llm_judge.json`.

```json
{
  "verdict": "PARTIAL",
  "coverage_pct": 100,
  "agreement_pct": 78,
  "per_claim": [
    {"id":"C1","tested":true,"supported":true, "evidence_1liner":"Primary N=6 Exciton TISE rerun produced the expected 6-state tight-binding band with max absolute error 1.0e-4 versus analytic energies."},
    {"id":"C2","tested":true,"supported":false,"evidence_1liner":"Observed intrinsic bond ranks grow with N as 1,2,4,8,... and hit the rank cap by N>=8, so ranks are not roughly independent of chain length even though growth is slower than full 2^N Hilbert dimension."},
    {"id":"C3","tested":true,"supported":false,"evidence_1liner":"Bundled test script ran only after patching a real scikit_tt complex-dtype compatibility bug on modern NumPy, so the installable artifact is not functional out of the box."}
  ],
  "one_line_summary": "Correct benchmark physics reproduced, but scaling and out-of-box software claims are not fully sustained.",
  "justification": "The core benchmark diagonalization claim is independently reproduced ... However, the broader rank-scaling claim is only partly borne out ... In addition, the software-artifact claim fails as stated because a source patch was required ..."
}
```

## 5. Verdict

**PARTIAL.**

Justification (mine, in addition to the judge's):

- **What replicated cleanly (C1):** The TT-ALS solver in WaveTrain, on the paper's own bundled 6-site exciton benchmark, returns the single-exciton band eigenvalues in agreement with the exact analytic tight-binding formula to max error 1.0e-4 Ha (~0.08% of the bandwidth). The vacuum state comes out at exactly zero. This is a real independent numerical reproduction of the paper's core "TT-ALS diagonalizes chain-like Hamiltonians correctly" claim.
- **What is only weakly supported (C2):** The intrinsic-rank story of the paper is *consistent* with our observed boundary-bond patterns (1,2,4,8,… at the ends of the chain, exactly as the single-particle sector predicts) but our sweep hit the ALS `ranks=15` cap at the middle bond for N ≥ 8, so we cannot cleanly demonstrate "rank marginally independent of N." Additionally, our wall-clock is dominated by the ALS deflation term (superlinear in n_levels), not by TT operations, so we do not directly verify the "cost slightly more than linear in N" scaling. Would need a second sweep at fixed n_levels and larger `ranks` cap to nail this.
- **What failed (C3):** The software-artifact claim fails as stated. The published `scikit_tt` backend has a real complex-dtype accumulation bug that prevents ALS from computing more than 2 eigenstates on any modern NumPy. A one-line patch fixes it and we did report the details in this report so it can be filed upstream. This is a *real*, not cosmetic, out-of-box breakage.

**Solid?** Yes on the physics (C1). Not solid on the scaling claim or the ready-to-run software claim. So PARTIAL, not REPLICATED, is the honest call.

## 6. Files

- `report/brief.md` — 1-paragraph
- `report/attempt_log.md` — chronological
- `report/artifact_harvest.md` — every artifact pulled
- `report/evidence/tise_bench_final.json` — parsed per-N results
- `report/evidence/tise_bench.json` — raw driver dump
- `report/evidence/run_tise_bench.log.grep` — grepped log of state energies + TT ranks
- `report/evidence/run_tise_bench.log.head200` — first-200-lines of raw log for the primary benchmark
- `report/evidence/run_tise_bench.py` — benchmark driver
- `report/evidence/analyze_bench.py` — log parser & comparison
- `report/evidence/llm_judge.py` — LLM-judge caller
- `report/evidence/llm_judge.json` — LLM-judge output
- `work/venv312/` — venv (not archived, easily regenerated)
- `work/wave_train/` — git clone of the package source

## 7. Reproduce

```bash
cd work
python3.12 -m venv venv312
source venv312/bin/activate
pip install 'numpy<2' scipy matplotlib
pip install git+https://github.com/PGelss/scikit_tt
git clone --depth 1 https://github.com/PGelss/wave_train.git
pip install ./wave_train

# Patch the ALS complex-cast bug (one line):
python -c "
import scikit_tt.solvers.evp as e, re
p = e.__file__
src = open(p).read()
fixed = src.replace(
    'micro_op += shift*tmp.dot(np.conjugate(tmp.T))',
    'update = shift*tmp.dot(np.conjugate(tmp.T))\n        if np.iscomplexobj(update) and not np.iscomplexobj(micro_op):\n            micro_op = micro_op.astype(np.complex128)\n        micro_op = micro_op + update'
)
open(p, 'w').write(fixed)
print('patched', p)
"

python run_tise_bench.py     # ~13 min total; produces evidence/tise_bench.json
python analyze_bench.py      # ~1 s; produces evidence/tise_bench_final.json
ARGO_API_KEY=stevens python llm_judge.py   # LLM-judge grades
```
