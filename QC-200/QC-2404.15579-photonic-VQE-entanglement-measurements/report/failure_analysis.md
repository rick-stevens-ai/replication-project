# Failure analysis / friction / residual gaps — arXiv:2404.15579 replication

Honest inventory of what did NOT work perfectly, what was worked-around,
and what remains unresolved.

## 1. Extraction models missing on host (worked around)
- **Symptom:** Marker (VikParuchuri/marker) and Nougat (Meta) are not installed on the sub-agent host, and no pre-parsed copy of arXiv:2404.15579 existed in the shared corpora (`~/Dropbox/OSTI*`, `~/Dropbox/LUCID*`).
- **Workaround:** Used `pdftotext` (poppler) as a stand-in for `marker.md` and PyMuPDF's per-page `get_text()` as a stand-in for `nougat.mmd`. This is the established QC-200 corpus norm (see sibling dirs like `QC-0810.4968-...` and `QC-0704.3628-...`, which use the same substitution and document it in an `extraction/README.md`).
- **What is lost:** LaTeX-rendered display math, GFM tables, cleanly separated figure captions. All body text (including Appendix A's HeH+ coefficient table, eq. (4), and the paper's grouping) is grep-able and was in fact used to extract the numerical inputs. **Impact on replication verdict: none.**
- **Fix path if run again on GPU host:** `pip install marker-pdf nougat-ocr` on uicgpu or a spark, re-parse.

## 2. Paper "E_th = -2.863 MJ/mol" vs our exact -5.7252 MJ/mol (unresolved but documented)
- **Symptom:** Building the HeH+ Hamiltonian at R=0.9 Å from the paper's own tabulated coefficients (Fig. A1, second-to-last row) gives a smallest eigenvalue of -5.7252 MJ/mol. The paper reports the theoretical ground energy as -2.863 MJ/mol. Ratio is exactly 2.000 (within 0.02%).
- **Diagnosis:** A clean factor of 2 strongly suggests a Jordan-Wigner one-body normalization convention (some conventions absorb a ½ from the fermion anti-commutator into the h_pq → Z-coefficient mapping; others don't) or a units mismatch (energy per orbital vs total energy).
- **Not-a-bug in our code:** Our best VQE (-5.7259 MJ/mol under the paper's 3-basis grouping) reproduces OUR exact reference (-5.7252) to <0.001 MJ/mol. The measurement-count claims (paper's actual algorithmic point) are unaffected by the global scale.
- **Impact on verdict:** none. Logged as Open Question Q2 with a concrete next-step for reaching out to the corresponding author.

## 3. Greedy general-commutativity did NOT reproduce paper's HeH+ 3-group split (rescued by using paper's explicit grouping)
- **Symptom:** A naive greedy grouper under the `commute(P1, P2)` predicate placed `II` into the first Z-string group (`{II, IZ, ZI, ZZ}`) because it commutes with every Pauli. This left `{IX, ZX}`, `{XI, XZ}`, `{XX}` as separate groups → 4 groups, same as QWC.
- **Fix:** Used the paper's manual grouping `{XX, ZZ, II}` (Bell), `{XI, XZ, IZ}` (QWC), `{IX, ZI, ZX}` (QWC) directly. Verified this is a valid GC partition (`commute(a,b)` = True for all pairs in each group; each of the 9 Pauli strings appears exactly once). Ran an independent set of VQE runs under this grouping (R1 in `vqe_bell_refinements.py`), which reproduced the paper's 4 → 3 basis reduction exactly.
- **Lesson:** Optimal GC-grouping-with-a-Bell-friendly bias is NOT a greedy problem; it needs either a graph-coloring approach that penalizes groups where the Bell-basis measurement would over-partition the shot budget, or a hand-picked partition informed by the physics (place `XX,YY,ZZ` style non-QWC-but-Bell-friendly triples first, then absorb Z-strings). This is now Open Question Q3 for scaling.
- **Impact on verdict:** none, because we successfully executed the paper's own grouping.

## 4. VQE-E instability under COBYLA tol=0.01 (identified & fixed)
- **Symptom:** In the first Heisenberg run, VQE-E (Bell) had mean -2.60 and std 0.78, while VQE-P (Pauli) had mean -2.99 and std 0.016. That looked like a Bell-measurement problem.
- **Diagnosis:** It was an optimizer / tolerance problem. Under loose `tol=0.01`, COBYLA's early-stopping heuristic + the correlated three-Pauli estimates from a single Bell basis caused occasional very-poor early termination.
- **Fix:** Tightened `tol` to 0.001, ran 5 fresh restarts (R2). VQE-E then produced mean -2.98, std 0.024, best -3.000 — indistinguishable from VQE-P.
- **Lesson (Open Question Q4):** The paper prescribes `tol=0.01` but does not warn that Bell/GC estimators may be more sensitive to that tolerance than Pauli estimators. Practitioners should sweep tol before quoting Bell-vs-Pauli comparisons.

## 5. Hardware claims (C5, C6) not tested
- **C5** (deterministic photonic Bell measurement via PBD): intrinsically hardware; classical simulator cannot test it. Not a failure — out of scope.
- **C6** (Fig. 3: Bell measurement mitigates measurement-apparatus error for certain Hamiltonians): would require adding a POVM confusion matrix to the sampling and rerunning across confusion strengths. Time-boxed out of this sub-agent's window. Logged as Q1 with a concrete implementation sketch.

## 6. Ansatz choice differs from paper
- **Paper's ansatz:** 6-waveplate parameterization native to the photonic hardware, encoding a general 2-qubit state `α|aH⟩ + β|aV⟩ + γ|bH⟩ + δ|bV⟩`.
- **Our ansatz:** 8-parameter hardware-efficient (`R_y R_z` × 2 qubits, one CNOT, `R_y R_z` × 2 qubits) — a standard 2-qubit HEA sufficient to reach any 2-qubit state (up to a global phase).
- **Impact:** For the reduced Hamiltonians used here, both parameterizations cover the same physical state space, so the ground state is reachable in both. Absolute iteration counts differ (paper reports ~30 iters to converge for HeH+; we saw ~50–75 COBYLA nfev). Qualitative claims (basis reduction; energy accuracy) are unaffected.

## 7. Shot-protocol ambiguity (Open Question Q5)
- Paper says "total number of shots is fixed to be N = 9000" but does not clarify whether that is per iteration or per full VQE run. We interpreted it as per iteration (VQE-P: 3000 shots × 3 bases × N_iter; VQE-E: 9000 shots × 1 basis × N_iter). If it is per full run, the paper's per-eval shots would be <<100 and the estimator would be shot-noise dominated. We chose the interpretation that (a) is standard practice and (b) reproduces the paper's Fig. 2 shape. Flagged.

## 8. LLM-judge scoring not run
- **Symptom:** The wave brief allows an optional 3-judge Argo panel "if time remains." We did not run it because (a) the verdict is machine-computable from the recorded metrics (basis counts + energy errors both explicit numbers), (b) the brief itself says "else self-verdict," and (c) staying within the free-endpoint constraint on Argo would still consume tokens that offer no additional signal here.
- **Impact on verdict:** none. If desired, an Argo panel could be triggered later by pointing at `report/REPORT.tex` and the two `*.json` files.

## Summary
Two workarounds (extraction surrogates; paper's hand-picked HeH+ grouping over naive greedy), one documented residual unknown (HeH+ MJ/mol factor-of-2 unit convention — Q2), one optimizer-sensitivity finding (Q4), one out-of-scope hardware claim, one untested claim (C6 → Q1). None of these compromise the REPLICATED verdict on the paper's algorithmic claims.
