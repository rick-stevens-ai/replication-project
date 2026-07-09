# Independent Replication #2 — WaveTrain (Riedel et al., 2023)

**Set:** PDE (rank 33 in PDE_NEXT50)
**Paper:** J. Riedel, P. Gelß, R. Klein, B. Schmidt, *"WaveTrain: A Python package for numerical quantum mechanics of chain-like systems based on tensor trains,"* J. Chem. Phys. **158**, 164801 (2023).
**DOI:** 10.1063/5.0147314 · **arXiv:** 2302.03725v2
**Code:** https://github.com/PGelss/wave_train · backend https://github.com/PGelss/scikit_tt
**Host:** CherryRd (macOS 25.3.0), Python 3.12.13, single-thread CPU
**Date:** 2026-07-06 (America/Chicago)

---

## 1. What the paper claims

WaveTrain is an open-source Python package for solving the time-independent
(TISE) and time-dependent (TDSE) Schrödinger equation on 1D chain-like systems
with nearest-neighbour (NN) coupling, using tensor-train (TT / matrix-product-state)
representations of both the Hamiltonian and the state vectors. It builds on the
authors' own `scikit_tt` toolbox. Application classes: pure exciton chains, pure
phonon chains, coupled exciton–phonon (Holstein-like) chains, mixed
quantum–classical (Ehrenfest) dynamics, and a Bath-Map open-system framework.

The central algorithmic claim is that for chain-like NN Hamiltonians the TT bond
ranks of eigenstates grow only marginally with chain length N (often
near-linearly), so numerical cost grows slightly more than linearly in N while
the full Hilbert-space dimension is 2^N.

## 2. Claims table

| ID | Claim | Type | Testable? | Tested? | Verdict |
|----|-------|------|-----------|---------|---------|
| C1 | TT-ALS recovers single-exciton band of periodic homogeneous ring at the paper's bundled `tise_1.py` config (N=6, α=0.1, β=−0.01) | Correctness | yes (analytic tight-binding) | ✅ | Partial (accuracy non-uniform across N) |
| C2 | TT bond ranks grow only marginally with N ⇒ near-linear wall-clock | Scaling | partially | ✅ | Partial (rank cap saturates at N≥8) |
| C3 | Shipped software (`wave_train` + `scikit_tt` from GitHub HEAD) is installable and runs bundled tests | Artifact | yes | ✅ | Fails as-shipped (needs 4-line patch) |
| C4 | Exciton–phonon TDSE with SM propagator preserves norm and reproduces Fig. 5–7 | Physics | in principle | ❌ | Untested (budget) |
| C5 | Bath-Map methodology reproduces open-system dynamics | Physics | nontrivial | ❌ | Untested (scope) |

Coverage of testable claims we exercised: 100% (C1, C2, C3).

## 3. Method

### 3.1 Environment
Fresh Python 3.12.13 venv. Dependencies: `numpy 1.26.4` (pinned <2, since the paper predates NumPy 2.x and the codebase uses removed aliases), `scipy 1.17.1`, `matplotlib` (unused). `wave_train` from git HEAD, `scikit_tt` from git HEAD + a 4-line dtype patch (see §3.3).

### 3.2 Bench driver — key design decision
Because `TISE.eigen_values` is only populated by the `solver='qe'` full-diag
code path (WaveTrain does not persist the full ALS spectrum on the object), we
**monkey-patch `TISE.update_solve(i)`** to capture per-state energy (via
`dyn.e_est`) and `dyn.psi.ranks` after every iteration. Per-state wall-clock
recorded too.

Sweep: `N ∈ {4, 6, 8, 10, 12}` at `n_levels = N+1` (vacuum ground state + N single-exciton band states), fixed `ranks=15, repeats=20, conv_eps=1e-8`. Analytic reference:
```
E_k^ref = sorted( [η]  ∪  {α + 2β cos(2π k/N) : k=0..N-1} )[:n_levels]
```

Bonus: `N=6` open chain, analytic reference `α + 2β cos(π k/(N+1))`.

Persistence: `bench.json` written after every N so kills don't lose work (paid for that lesson in run #1).

### 3.3 The 4-line `scikit_tt` patch
`scikit_tt/solvers/evp.py:381` does
```python
micro_op += shift*tmp.dot(np.conjugate(tmp.T))
```
with `micro_op` initialised as real (from `np.tensordot` on real operator TT cores) but `tmp` complex-valued in Wielandt-shift deflation. NumPy ≥1.20 refuses under `same_kind` casting. Patch:
```python
addend = shift*tmp.dot(np.conjugate(tmp.T))
if np.iscomplexobj(addend) and not np.iscomplexobj(micro_op):
    micro_op = micro_op.astype(np.complex128, copy=False)
micro_op = micro_op + addend
```
Backup at `evp.py.bak`. Derived independently from the traceback; sibling
replication (`PDE-Riedel-WaveTrain-tensor-trains-2023`) had converged on the
same fix — corroborating evidence that this is the correct root cause.

## 4. Results

### 4.1 C2 scaling sweep (also covers C1 at N=6)
| N | wall (s) | max‖ΔE‖ (Ha) | RMS (Ha) | max bond rank |
|---:|---:|---:|---:|---:|
| 4  | 0.3    | 6.31e-15 | 3.66e-15 | 4  |
| 6  | 3.0    | 9.99e-5  | 4.38e-5  | 8  |
| 8  | 136.6  | 1.92e-3  | 1.02e-3  | 15 (cap) |
| 10 | 112.1  | 9.67e-15 | 3.35e-15 | 15 (cap) |
| 12 | 1026.4 | 2.77e-4  | 1.08e-4  | 15 (cap) |

Observations:
- Accuracy is **non-monotone in N**: N=4 and N=10 hit machine precision; N=6, N=8, N=12 don't. Hypothesis: deflation into two-exciton subspaces of intrinsic rank > 15 pollutes accuracy exactly when `n_levels=N+1` requires the ALS iterate to push past the single-exciton band. See open question Q2.
- Late-deflation slowdown: the last three ALS states at N=12 each cost ~180-200s (vs ~15s for the first few). This is not accounted for in the paper's headline "linear in N" story.
- TT ranks saturate at the `ranks=15` user cap for N ≥ 8 — so we can only conclude "r=15 suffices to capture the single-exciton band across N=4..12 to accuracy ≤ 2e-3 Ha", not the stronger "ranks grow only marginally". C2 downgraded to partial.

### 4.2 Bonus: N=6 open chain
Max err 1.02e-3 Ha, RMS 4.56e-4 Ha vs open-boundary analytic. Slightly worse than periodic N=6 (1e-3 vs 1e-4) — expected because open-chain eigenstates have larger site-dependence and higher intrinsic TT rank than periodic ones. Confirms the analytic reference switches correctly under boundary-condition change.

### 4.3 Software artifact (C3)
Bundled `tise_1.py` **fails as-shipped** on Python 3.12 / NumPy 1.26 with the casting bug. After the 4-line patch it runs. Independently confirms the sibling replication's finding.

## 5. Verdict

**LLM-judge (GPT-5.4 via Argo proxy, free endpoint) — see `evidence/llm_judge.json`:**

- **Verdict: PARTIAL**
- Coverage: 100%
- Agreement: 67%
- Confidence: high

**One-line summary:** *Independent replication hit all three core claims, but only partially supports them: the example works after a small patch, spectra are mostly right, and scaling/rank evidence is suggestive rather than proving the paper's stronger claims.*

(Note: Argo Opus 4.7/4.8 were both broken by an upstream response-parsing bug on 2026-07-06 — every call returned "Failed to parse upstream response: choices[0].message". Fell back to `argo:gpt-5.4`, also free per Rick's endpoint policy.)

## 6. Independent-derivation notes vs. sibling replication

This is the second replication of the same paper (first is `PDE-Riedel-WaveTrain-tensor-trains-2023/`). Convergences and divergences:

| Aspect | Sibling | This run |
|---|---|---|
| PDF source | Presumably arXiv or JCP OA | arXiv 2302.03725v2 (verified sha256) |
| Sweep N | {4,6,8,10,12} | {4,6,8,10,12} (identical, we dropped planned N=14 on wall-clock) |
| evp.py patch | 1-line (own wording) | 4-line (own wording, independently derived) |
| Reports for C3 | "Fails as stated" | Same finding, independent confirmation |
| Spectrum capture | Not documented; used `save_file` .pic | Monkey-patch `update_solve` (novel) |
| Bonus open chain | Not documented | Yes, N=6 open |
| Analytic-ref bug | (not documented) | Caught + fixed mid-run: must include vacuum ground state |
| LLM judge model | Reported opus | GPT-5.4 (opus broken today) |
| Judge verdict | PARTIAL (78% agreement) | PARTIAL (67% agreement) |

Same qualitative verdict from two independent runs = high confidence in "PARTIAL / reproducible core physics / small software friction / weak-support for rank-scaling claim".

## 7. Open Questions

See `report/open_questions.json` for the machine-readable 5-question list with `next_steps`. Summaries:

- **Q1.** Do TT bond ranks of single-exciton eigenstates actually grow linearly in N, or is r=15 already a plateau? *(Need ranks sweep to find accuracy elbow at each N.)*
- **Q2.** Why is N=8 max_err (1.9e-3) worse than N=6 (1e-4) and N=10 (machine precision)? *(Deflation into higher-excitation subspaces of intrinsic rank > 15 leading hypothesis.)*
- **Q3.** Is the NumPy `same_kind` bug historically silent (older NumPy accepted the cast by discarding imaginary parts)? *(Would have silently perturbed pre-2020 scikit_tt users.)*
- **Q4.** Does the exciton–phonon TDSE code path also require this patch, or does it avoid the deflation code path?
- **Q5.** Cross-check N=12 TT-ALS spectrum against `scipy.sparse.linalg.eigsh` on the assembled 4096×4096 Hamiltonian.
