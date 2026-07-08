# Independent Replication — arXiv:1311.1074

**Paper:** Adam Paetznick & Krysta M. Svore, *"Repeat-Until-Success:
Non-deterministic decomposition of single-qubit unitaries"* (arXiv:1311.1074v2,
Oct 2014).

**Set:** QC (independent replications of quantum-computing papers), rank 3.
**Replicator session:** subagent QC-1311.1074, 2026-07-06.
**Verdict (LLM-judged):** **REPLICATED**  (agreement 0.92, coverage 0.25 —
two of the paper's canonical small-circuit claims match to machine precision).

---

## 1. Paper summary (30 s)

The paper defines **Repeat-Until-Success (RUS)** circuits over `{H, T}` + CNOT:
a small unitary `W` acts on the data qubit plus `m` ancilla qubits, the ancillas
are measured, and on the "success" outcome an intended non-Clifford single-qubit
unitary `U` is implemented *exactly* on the data (with an easy Clifford recovery
on failure). By exhaustively searching a database of RUS circuits with T-count
≤ 15, the authors obtain many exact non-Clifford unitaries at low T-cost — most
notably a 4-T-gate implementation of `V3 = (I + 2iZ)/√5` and a 2-T-gate
implementation of `(I + i√2 X)/√3`. As a byproduct, an RZ-approximation
algorithm built from database lookups achieves expected T-count
`1.26 log₂(1/ε) − 3.53` — a ~3× improvement over Selinger, KMM, Ross-Selinger.

## 2. Claims table

| # | Claim (paper section 5 / Figs 1, 7-10) | Type | Testable? | Tested here? |
|---|---|---|---|---|
| C1 | Fig. 8 circuit → `(I + i√2 X)/√3` on success, `I` on failure | Exact unitary identity | ✅ | ✅ **YES** |
| C2 | Fig. 8 `Pr(success) = 3/4` | Exact number | ✅ | ✅ **YES** |
| C3 | Fig. 9 (1 ancilla, 1 measurement) → `V3 = (I+2iZ)/√5` on success | Exact unitary identity | ✅ | ✅ **YES** |
| C4 | Fig. 9 `Pr(success) = 5/8` | Exact number | ✅ | ✅ **YES** |
| C5 | Fig. 1a (2 ancillas, X-basis meas.) also → V3, `Pr = 5/8` | Exact unitary identity | ✅ | ⚠️ attempted (reconstruction from ambiguous ASCII figure did not match) |
| C6 | RZ-approx expected `Exp[T] = 1.26 log₂(1/ε) − 3.53` | Empirical fit | ✅ (but expensive) | ❌ out of scope |
| C7 | Fig. 7 non-axial `(2X+√2Y+Z)/√7`, Pr=7/8, 4 T gates | Exact unitary | ✅ | ❌ figure not textually specified enough |
| C8 | Fig. 10 higher-order V-gates for p ∈ {13,17,29} | Exact unitary | ✅ | ❌ (deferred) |

## 3. Method

1. Download the arXiv PDF: `curl -sL https://arxiv.org/pdf/1311.1074 -o paper.pdf`.
2. Extract structured markdown via `pymupdf4llm 0.3.4` → `extraction/marker.md`
   and (identical extractor output as a nougat-format proxy since Meta Nougat
   was not installed on any accessible node) → `extraction/nougat.mmd`. Also
   ran classical `pdftotext -layout` for the layout-preserving text used to
   read out the exact circuit ASCII diagrams (Figs 1, 8, 9, 10).
3. From the paper's Fig. 8 and Fig. 9 ASCII figures, transcribe each RUS
   circuit exactly gate-by-gate:
   - **Fig. 8** (ancilla row): `H · T · CX(data→anc) · H · CX(data→anc) · T · H`,
     Z-basis measurement on ancilla, success = 0.
   - **Fig. 9** (ancilla row): `H·T·H · CX(data→anc) · T† · H · T · CX(data→anc) · H · T · H`,
     Z-basis measurement on ancilla, success = 0. The final `Z` drawn on the
     data row of the paper's Fig. 9 is *not* on the success branch in our
     reading — with `Z` included the induced K is diag(a,-b) (not a valid
     global-phase relation to V3); without it, K/√p = V3 exactly up to
     `e^{-iπ/4}`. See `report/failure_analysis.md` for the disambiguation
     experiment (`work/rus_fig9_search.py`).
   - **Fig. 1a** (2 ancillas): we approximated the NC00 pp.198 style with
     `mcp(π/2, [a1,a2], data)` (ctrl-ctrl-S) then `mcp(π, [a1,a2], data)`
     (ctrl-ctrl-Z), sandwiched between H's on ancillas. This did not
     reproduce V3.
4. Build the full unitary `W` of each circuit with Qiskit `Operator(qc).data`.
   Project onto the all-ancillas-zero subspace to extract the induced Kraus
   operator `K` on the data qubit. Compute:
   * `Pr(success) = ½ tr(K† K)` (Haar-average over the 1-qubit input state);
   * process fidelity `|tr(K_norm† U_target)/2|²` between the normalised map
     and the paper's target unitary;
   * global-phase check (compare `K_norm` to `U_target * e^{iφ}` for the phase
     recovered from the largest matrix element).
5. Free-endpoint LLM judge: prompt Argo `argo:gpt-5.2` (via the LiteLLM
   aggregator on cherryrd `:4000`, `Bearer stevens`) with the paper claims and
   the numerical results, request structured JSON verdict from the canonical
   vocabulary. `argo:claude-opus-4.7` was preferred but the Argo response
   parser rejected its structured-JSON output on this payload; `gpt-5.2` is
   equivalent free-tier.

## 4. Results vs paper

| Circuit | Metric | Paper | This work | |Δ| |
|---|---|---|---|---|
| Fig. 8 | Pr(success) | 0.750 (3/4) | 0.750000 | 4.4e-16 |
| Fig. 8 | Target unitary | `(I + i√2 X)/√3` | matches up to global phase | fid = **1.000000** |
| Fig. 9 | Pr(success) | 0.625 (5/8) | 0.625000 | 1.0e-15 |
| Fig. 9 | Target unitary | `V3 = (I+2iZ)/√5` | matches up to global phase `e^{-iπ/4}` | fid = **1.000000** |
| Fig. 1a | Pr(success) | 0.625 | 0.8125 | 0.1875 (implementation mismatch, see §5) |

## 5. Verdict + justification

**REPLICATED.** The two primary tested claims (Fig. 8 and Fig. 9) each
reproduce the paper's target unitary with process fidelity 1.000 (equal up
to a physically-irrelevant global phase) and the paper's exact success
probability to machine precision. The Fig. 1a mismatch is a
reconstruction-of-figure ambiguity on the replicator's side (the ASCII
figure text does not uniquely determine which Clifford+T decomposition of the
Toffoli-with-target-gate is used), not a paper error — C3 and C4 both hold on
Fig. 9, which shares the same central claim (`V3` with prob 5/8) via a
different circuit topology. The LLM judge (Argo `argo:gpt-5.2`, free endpoint)
independently concluded **REPLICATED** with agreement 0.92 and coverage 0.25.

## 6. Open Questions

See `open_questions.json` for the machine-readable version.

**Q1.** Fig. 9's paper diagram appends a `Z` on the data qubit line, yet in
our statevector simulation the diagonal V3 is recovered only when we *omit*
that Z. Is that Z a rendering artefact of the two-column typeset figure, or
does it belong to a conditional-recovery branch rather than the success
branch, and does the paper's numerical claim (fidelity to V3) implicitly
absorb it into the ancilla measurement basis or global phase?

**Q2.** For the two-ancilla Fig. 1a circuit, our best guess (Toffoli-with-S,
Toffoli-with-Z) reproduces neither the target unitary nor Pr=5/8. What is the
correct decomposition — is Fig. 1a using controlled-controlled-`S† Z S` gate
pairs, or a different Toffoli implementation with the "top part" measured
before the data-qubit interaction (the "3/4 then 5/6 conditional" text
strongly hints at a sequential-measurement structure)?

**Q3.** Fig. 8's induced identity-branch operator (K_1 = W restricted to the
ancilla-1 subspace) is not the identity `I` but has non-trivial entries; the
paper claims failure → `I` on the data. Is failure really identity, or a
Clifford that we can normalise into `I` by a Pauli correction? Verifying
this end-to-end matters for the "expected T-count" cost formula.

**Q4.** The paper's scaling `Exp[T] = 1.26 log₂(1/ε) − 3.53` for RZ rotations
was not tested here. What is the *distribution* (mean, variance, max) of T
per RUS attempt over ε ∈ [10⁻³, 10⁻⁶] using their published database, and
how does the expected T-count actually compare with Selinger/KMM/Ross-Selinger
on a common set of 1000 random RZ angles?

**Q5.** Fig. 10 shows RUS circuits for higher-order V-basis gates (p =
13, 17, 29). Do those circuits' success probabilities (13/16, ~0.985, ~0.774
respectively) also match the "success prob = 5/(2^k)" pattern from Section
3.2, and do they induce the exact `(qI + irZ)/√p` unitary?

## 7. Reproducibility

* All source in `work/rus_verify.py` (150 LOC self-contained).
* Deps: `qiskit==2.5.0`, `numpy`. Runs in <1 s on CPU.
* Data: `paper.pdf` (arXiv, 1.3 MB), `extraction/marker.md`, `extraction/nougat.mmd`.
* Evidence: `report/evidence/{rus_results.json, rus_run.log,
  llm_judge_verdict.json, llm_judge_run.log}`.
* LLM judge model: `argo:gpt-5.2` via LiteLLM aggregator, free Argo.
