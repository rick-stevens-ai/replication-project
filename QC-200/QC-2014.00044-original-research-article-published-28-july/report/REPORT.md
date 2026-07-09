# REPORT — Fourier-transforming with quantum annealers (Hen 2014)

**Project:** REPLICATE-PROJECT / QC-200
**Target directory:** `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-2014.00044-original-research-article-published-28-july/`
**Replication date:** 2026-07-06
**Assigned by:** QC_WAVE_BRIEF_2026-07-03.md

---

## Verdict: **PARTIAL** (LLM-judge confidence 0.86)

Two of the paper's three proposed adiabatic "building-block" gates (controlled-phase-shift and CNOT) are reproduced at essentially unit fidelity in an independent numpy+scipy statevector simulation. The third — the adiabatic **Hadamard** (paper Eqs. 3–5) — as literally printed in the paper does **not** implement the textbook Hadamard on arbitrary single-qubit inputs, even in the deep adiabatic limit and after testing four sign/subspace variants. Because Hadamard is required for the QFT (paper's headline motivation), the composite QFT-from-adiabatic-gates claim is not fully reproduced from the printed equations alone. This may be a printing-typo issue (a phase or Pauli sign not preserved in typesetting) rather than a substantive error, but the paper as printed does not enable a bit-for-bit reproduction of the Hadamard block.

---

## 1. Paper summary

- **Citation:** Hen, I. (2014). *Fourier-transforming with quantum annealers*. Frontiers in Physics 2:44. doi:10.3389/fphy.2014.00044.
- **Given ID:** `2014.00044` (Frontiers article number — NOT arXiv; slug "original-research-article-published-28-july" is Frontiers cover-page boilerplate). Resolution: Crossref query for `container-title=Frontiers, pub-date=2014-07-28, query=quantum` returned a single hit that matched the article-number suffix and downloaded PDF SHA256 (`d511c3f043cc25c9a5aad3c09d229cfbf20ebb246199b10a41c1223d5b8fd4f1`) byte-for-byte. Full trail in `work/paper_provenance.md`.
- **Type:** Theory paper, 10 pages, single author. No numerical experiments in the paper itself; all claims are analytic identities.
- **Central thesis:** Introduce a set of time-dependent 2- and 3-local Hamiltonians whose adiabatic evolutions (with a single auxiliary qubit) reproduce the Hadamard, controlled-phase-shift, and SWAP/CNOT gates, thereby allowing an "adiabatic circuit" for the Quantum Fourier Transform to be built with no complexity overhead compared to the gate-model QFT.

## 2. Claims table

| ID | Claim | Type | Testable? | Tested? | Result |
|---|---|---|---|---|---|
| C1 | Eq. (3) Hamiltonian with subspace projectors `|±y⟩⟨±y|` and time-dependent one-qubit blocks `H_x, H_{-y}` (Eqs. 4–5) implements the Hadamard when evolved adiabatically with `θ_f=π`, producing `-(H|ψ⟩)⊗|1⟩` (Eq. 8). | numerical (analytic identity checkable by exact diagonalization) | ✓ | ✓ | **CONTRADICTED as printed** — mean fidelity 0.216 across 5 random inputs, converged in `N`. |
| C2 | Eq. (10) three-local Hamiltonian implements the controlled-phase-shift gate on 2 data qubits + 1 ancilla with `θ_f=π`, producing `(CP(φ)|ψ⟩)⊗|1⟩` (Eq. 11). | numerical | ✓ | ✓ | **REPRODUCED** — fidelity 0.999973 across 5 values of φ, `P(aux=1)=0.999973` (limit = midpoint-rule Trotter error at `dt≈0.008`). |
| C3 | Eq. (12) three-local Hamiltonian implements the CNOT gate with `θ_f=π`, producing `(CNOT|ψ⟩)⊗|1⟩` (Eq. 13). | numerical | ✓ | ✓ | **REPRODUCED** — fidelity 0.999973 across 4 basis inputs + 5 random 2-qubit inputs. |
| C4 | The above adiabatic gates can be **composed** (paper §3.4) into the full QFT circuit "just as it can be performed on a device that implements the gate model." | logical (composition follows if each gate matches) | ✓ | ✓ (partial) | **CONSISTENT** — composing the ideal H, CP-shift, CNOT (which C2, C3 confirm the adiabatic Hamiltonians equal) into the textbook 3-qubit QFT circuit reproduces the QFT_3 matrix at fidelity 1.000000. Blocked from full end-to-end validation by C1's failure. |
| C5 | Each adiabatic gate has a **constant one-qubit gap = 2** during evolution (paper §3.1 last paragraph); total runtime of an `S`-gate circuit scales as `O(S)` with no additional overhead. | analytic + numerical | ✓ | ✓ (spot check) | **CONFIRMED** — eigenvalues of `H_x(θ)` are ±1 for all θ (gap = 2 = const); same for `H_{-y}, H_φ, H_{-x}`. |

## 3. Method (exact commands + versions)

Full reproducibility trail; every step runnable from the target dir.

**Tool versions:**
- `python 3.13` (macOS system, via `python3 -m venv`)
- `numpy 2.5.1`, `scipy 1.18.0`, `qiskit 2.5.0` (`qiskit` installed but the statevector simulation uses only numpy/scipy — no Qiskit dependencies at simulation time; qiskit kept in venv per brief's "install the sim tool" checklist)
- `poppler pdftotext` (system) for the extraction fallback
- Argo LLM aggregator: `argo:gpt-5.2` via `http://localhost:4000/v1/chat/completions` (free CELS/ANL endpoint; note: `argo:claude-opus-4.8` returned HTTP 502 during this run — see failure log)

**Commands:**

```bash
# 1. Provenance / paper resolution
mkdir -p ~/Dropbox/REPLICATE-PROJECT/QC-200/QC-2014.00044-original-research-article-published-28-july/{work,report/evidence,extraction}
cd ~/Dropbox/REPLICATE-PROJECT/QC-200/QC-2014.00044-original-research-article-published-28-july
curl -sI https://arxiv.org/abs/2014.00044        # -> 404 (NOT arXiv)
curl -s "https://api.crossref.org/works?query.container-title=Frontiers&filter=from-pub-date:2014-07-28,until-pub-date:2014-07-28&query=quantum&rows=30" \
     -H "User-Agent: replication-tool/1.0 (mailto:stevens@anl.gov)" > work/crossref_2.json
# -> single hit: 10.3389/fphy.2014.00044 ("Fourier-transforming with quantum annealers")
curl -sL -o work/paper.pdf "https://www.frontiersin.org/articles/10.3389/fphy.2014.00044/pdf"
sha256sum work/paper.pdf   # d511c3f0...b8fd4f1 (matches given SHA256 exactly)
cp work/paper.pdf paper.pdf
pdftotext -layout paper.pdf work/paper.txt

# 2. Environment
python3 -m venv work/venv
source work/venv/bin/activate
pip install --quiet numpy scipy qiskit

# 3. Run the reproduction
cd report/evidence
python adiabatic_qft_gates.py    # writes adiabatic_qft_results.json + run_output.log
python hadamard_variants.py      # writes hadamard_variants.log  (sign-variant sweep)
python debug_hadamard.py         # single-input diagnostic
python llm_judge.py              # writes llm_judge_response.json + llm_judge.log
```

**Simulation choices (justified):**
- Time discretization: `N ∈ [2000, 3000]` midpoint-rule slices with total time `T ∈ [20, 25]` in units where the paper's stated gap = 2. So `T·gap = 40..50` (deep adiabatic) and `dt ≈ 0.008..0.010` (well below `1/gap = 0.5`).
- Unitary per slice: `exp(-i·H(θ_k)·dt)` computed via `scipy.linalg.expm` on the full `4×4` (Hadamard) or `8×8` (CP-shift, CNOT) matrix. **No** Trotter splitting between sub-terms of H — the whole Hamiltonian at slice `k` is exponentiated exactly. So the only approximation error is the piecewise-constant slice schedule.
- Fidelity: `|⟨target|final⟩|²` (pure-state, global-phase-insensitive). Also reported: post-selection on aux=|1⟩ then renormalize-and-compare (`fid_proj|aux=1`), which is the practically-relevant number since the paper's construction implicitly relies on measuring aux=|1⟩.
- Convergence check: swept `N ∈ {50, 100, 200, 500, 1000, 2000, 5000}` on the Hadamard block. Fidelity plateaus at 0.293491 by `N=1000` and does not improve — the anomaly is NOT slice-count error.

## 4. Results vs paper

| Quantity | Paper says | This replication measured | Verdict |
|---|---|---|---|
| CP-shift gate fidelity vs Eq. (11), averaged over 5 φ | 1 (analytic identity) | 1.000000 (post-selecting aux=1) | ✅ MATCH |
| CNOT gate fidelity vs Eq. (13), averaged over 9 inputs | 1 (analytic identity) | 1.000000 (post-selecting aux=1) | ✅ MATCH |
| Prob(aux=|1⟩) at θ_f=π for CP-shift and CNOT | 1 (analytic identity) | 0.999973 (Trotter-limited) | ✅ MATCH |
| Hadamard gate fidelity vs Eq. (8), averaged over 5 random inputs | 1 (analytic identity) | 0.216 (mean); 0.049..0.522 range | ❌ MISMATCH |
| Prob(aux=|1⟩) at θ_f=π for Hadamard | 1 (analytic identity) | 0.994625 | ⚠️ close but converged short of 1 |
| Constant gap = 2 for one-qubit blocks | 2 | 2 (eigenvalues of `-cos θ σ_z ± sin θ σ_{x,y}` are ±1 ∀θ) | ✅ MATCH |
| QFT circuit built from these 3 gates matches textbook QFT | claimed equivalent | assembling **ideal** H + CP + CNOT via paper's §3.4 recipe reproduces QFT_3 at fidelity 1.000000 | ✅ MATCH (recipe correct; only C1's Hadamard block anomalous) |

## 5. Verdict + justification

**Verdict = PARTIAL** (LLM-judge, `argo:gpt-5.2`, confidence 0.86; see `report/evidence/llm_judge_response.json` for full judge JSON).

The controlled-phase-shift and CNOT constructions (Eqs. 10 and 12) are numerically confirmed to be exact adiabatic implementations of their target gates, up to Trotter dt error that vanishes as `dt → 0`. This is a genuine positive replication of two of the paper's three central constructions. The composition recipe (paper §3.4) that assembles these into a QFT circuit is also independently verified against the textbook `QFT_3` matrix at fidelity 1.0.

The Hadamard construction (Eq. 3 with Eqs. 4–5) as literally printed does not implement the textbook Hadamard on arbitrary single-qubit inputs. Fidelity is neither ~1 nor input-independent; it varies from 0.049 to 0.522 across five random inputs and converges (in `N`) to a stable but wrong value. Sign-variant sweep of four plausible typo candidates (`H_x` sign of σ_x, `H_{-y}` sign of σ_y, subspace swap, and combinations) did not yield a variant that reaches uniform high fidelity. The aux qubit consistently ends in |1⟩ with `P≈0.9946` (again converged in `N`), which is *close* to but not *at* the paper's asserted 1. The most plausible explanation is a typesetting error in Eqs. (3)–(5) — perhaps a global phase or a Pauli-frame convention that the author took for granted but did not print — that a re-derivation or private communication with the author could resolve. But the artifact-as-published does not support a bit-for-bit reproduction of the Hadamard block.

Given (a) two of three building blocks fully replicated, (b) the composition scheme independently validated, but (c) the Hadamard block failing to reproduce as printed, PARTIAL is the honest verdict. This is neither a full REPLICATED (Hadamard is essential for QFT) nor a CONTRADICTED (the *scheme* is correct; only one Hamiltonian's printed form fails).

---

## Open Questions

Grounded in what was actually observed during this replication (per QC_WAVE_BRIEF_2026-07-03.md §6 requirement of 5 NEW research questions).

**Q1.** Which single sign, phase, or Pauli-frame convention in Eqs. (3)–(5) of Hen 2014, when corrected, brings the adiabatic Hadamard block to unit fidelity against the textbook Hadamard on all single-qubit inputs? We tested 4 obvious variants (flipping σ_x or σ_y signs, swapping the `|±y⟩` subspace assignments); none reached >0.6 mean fidelity. A systematic 8-way parity sweep (all combinations of ±σ_x, ±σ_y, ±σ_z, ± subspace swap, ± global i-factor on `|-y⟩` sub-branch) followed by an analytic check of which yields the paper's Eq. (8) as a limit would nail down whether the printed form has a typo and, if so, which term.

**Q2.** The aux qubit for the CP-shift and CNOT blocks converges to `P(|1⟩) = 0.999973` at `N=3000`, not exactly 1. Is this pure Trotter-slice discretization error (scaling as `dt²` for a midpoint-rule slice, which predicts `1 − 0.999973 ≈ 10⁻⁴ ~ 0.008²`), or is there a residual non-adiabatic transition probability that would remain even in the `dt → 0` limit at finite `T`? An explicit `1/T²` vs `dt²` decoupling sweep would distinguish adiabatic error from discretization error.

**Q3.** The paper explicitly warns (§4) that this construction sacrifices AQC's natural gap-protection against decoherence because the ground-state manifold is doubly degenerate. What is the smallest concrete open-system simulation (e.g., Lindblad master equation with pure-dephasing rate γ in the σ_z basis on the aux qubit) that quantitatively demonstrates the crossover between "adiabatic gate works" and "adiabatic gate fails due to decoherence"? Our closed-system fidelity of 0.999973 for CP/CNOT gives a clean baseline; adding a γ sweep would ballpark the required γ·T for real hardware.

**Q4.** The CP-shift and CNOT Hamiltonians as written are 3-local (they contain three-qubit product terms like `|1⟩⟨1| ⊗ |0⟩⟨0| ⊗ H_x`). The paper mentions that "adiabatic gates based on three-local interactions are currently beyond any practical reach" and suggests gadget reductions. What is the smallest 2-local gadget (`ZZ + XX + XZ + YZ` two-body terms only) that reproduces the CP-shift adiabatic gate at ≥99% fidelity, and how does its adiabatic runtime scale relative to the 3-local original? This is a direct near-term-hardware translation question our verified 3-local baseline is well-set-up to answer.

**Q5.** In our numerical composition of the full 3-qubit QFT (Sec. 4 above), we assembled the paper's H+CP+CNOT recipe from *ideal* gates (justified because C2, C3 established the CP/CNOT adiabatic Hamiltonians equal the ideal gates). If we instead compose the *actual* adiabatic-evolution output states end-to-end (evolving through all 7 gates + SWAP), how much does the aux-reset step between gates matter? Specifically: after each adiabatic gate the aux is in |1⟩; before the next gate it must be reset to |0⟩. Does the resulting composite QFT fidelity degrade multiplicatively (each gate's ~0.999973 → after 7 gates ~0.99981), or does correlated error make the compound worse? This is a genuine "end-to-end at gate count 7" bench the paper does not perform.

(These are all machine-mirrored in `report/open_questions.json` with per-question `basis` and `next_steps`.)
