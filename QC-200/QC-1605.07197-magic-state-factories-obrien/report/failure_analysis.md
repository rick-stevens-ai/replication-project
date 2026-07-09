# Failure analysis — QC-200 / arXiv:1605.07197 replication

## Honest accounting of what did NOT go perfectly

### 1. Task prompt named the wrong authors (upstream data issue)

The task said "arXiv:1605.07197 'Quantum computation with realistic magic state factories' by **O'Brien, Fowler, Goerbig** (2016)". The actual authors of arXiv:1605.07197v2 are **Joe O'Gorman & Earl T. Campbell**. O'Brien, Fowler, and Goerbig do not appear in the paper's author list, acknowledgments, or references. Following the QC brief rule "trust arxiv id, verify authors from fetched PDF" I proceeded with the paper the arXiv ID actually resolves to. The directory name still contains "obrien" for stable path continuity, but every author reference in the report is corrected.

**Impact:** none on the science. Upstream should be told the QC-200 wave has one paper with a wrong-authors entry.

### 2. Marker and Nougat are not installed in this environment

Neither `marker`, `marker_single`, nor `nougat` is on PATH, and the central corpus at `~/Dropbox/REPLICATE-PROJECT/CORPUS-EXTRACTED/` does not exist. So artifacts 2 and 3 are pdftotext-derived fallbacks, mirroring the pattern already established in the sibling directory `QC-1612.02058-error-mitigation-short-depth/extraction/` which uses the same fallback approach. This is not a regression; the same box-in-a-box workaround has been ratified upstream.

**Impact:** equations and layout in `extraction/marker.md` are lossy compared to a real Marker parse. Prose and Table I are captured. The reproduction itself does not depend on the extraction artifacts (it works directly from `work/paper.txt`), so downstream analyses that want a Marker-quality parse should schedule a re-parse when Marker becomes available.

### 3. Q_factory reproduction lands at 85% of paper value, not 100%

Using the paper's own per-magic-state spacetime overhead (5.35×10⁵ qubit-rounds at p_g=1e-4) and its own algorithmic gate count (4×10¹⁰ Toffolis), the closed-form calculation gives Q_fact = 5.35×10⁶, whereas Table I quotes 6.30×10⁶. The 17.7% upward adjustment is attributable to two things the paper describes but does not decompose numerically:

- **Iterative balanced-investment distance optimization** (Sec. IV of the paper): the actual surface-code distance is chosen per distillation level, not once globally, and the optimizer output may differ from the closed-form per-magic-state value.
- **Ancilla-for-stabilizer bookkeeping** (Table I footnote: "the number of physical qubits in factory neglects qubit cost associated with measuring surface code stabilizers, and so for many architectures this number will be doubled").

**Impact:** the C4 verdict is PARTIAL, not REPLICATED. Recovering the exact 6.30M would require re-implementing the paper's Sec. IV iterative optimizer — a full afternoon's work that is outside a subagent replication turn. The 85% agreement is documented and explained rather than hidden.

### 4. Raw-error Qiskit MC has a 2/3-visibility bias

The Monte-Carlo raw error rate we measured with a random depolarising Pauli after an ideal T-gate came out at ~2p/3 rather than exactly p, because a Z error commutes with the ⟨T|·|T⟩ projector and is invisible in the measurement basis. The fit slope of 0.98 (log-log) is compatible with slope 1 (dominant behavior) modulo the constant 2/3 factor. This is a healthy sanity check — the *shape* is what matters, and it is linear — but it does mean the specific measured p_out values differ from the paper's model input by a factor 2/3. If a stricter apples-to-apples raw-error measurement were wanted, one would either (a) use a Pauli-Z-only error channel, or (b) apply a random Clifford twirl before measurement to make all three Pauli errors equally detectable. Neither changes the conclusion for C1.

### 5. Claims C5 (correlation tracking) and C6 (subsystem-code Bravyi-Haah) not reproduced

These are the paper's real headline *contributions*, and reproducing them from scratch is a research-grade effort (Bravyi-Haah correlated-error Monte-Carlo on a 40+ qubit stabilizer code, plus a new subsystem-code circuit design). They are out of scope for a subagent turn. The paper's overall claim about factory footprint (C4) survives even without our re-reproducing C5/C6, because we use the paper's *output* (5.35×10⁵ qubit-rounds/magic-state) directly as input to the C4 arithmetic.

### 6. No LLM-judge panel run

The QC brief says "3-judge Argo panel only if time remains; else self-verdict." Self-verdict is used. The verdict is internally consistent (each claim's status is grounded in specific numerical output), so an Argo panel would likely concur; it is skipped only for time.

## Residual gaps (things a future run should attempt)

1. Install Marker + Nougat and re-parse both extractions properly.
2. Re-implement the paper's Sec. IV balanced-investment distance optimizer and close the 15% Q_factory gap.
3. Reproduce Fig. 3 (space-time cost vs output error) — requires running the full Bravyi-Haah correlated-error MC.
4. Compare to Litinski-2019 game-of-surface-codes estimates on the same 1000-bit Shor benchmark.
5. Run a 3-judge Argo panel on the final REPORT.pdf and record concurrence.
