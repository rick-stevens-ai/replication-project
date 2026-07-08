# Failure Analysis — arXiv:2004.10344 replication

**Purpose:** an honest, load-bearing critique of what this replication did NOT properly exercise, phrased so a hostile reviewer (or a re-replicator building on this work) can see exactly where the ice is thin. This complements — and where necessary walks back — the confident "REPLICATED" verdict in REPORT.md §5.

## The verdict in one paragraph, with fair caveats

The **REPLICATED** verdict is correct for the paper's noise-free ansatz-expressiveness core (C1) on the paper's specific headline system (H2/STO-3G, 4 qubits, dissociation curve). It is **NOT** correct as a statement about the paper's practical value proposition, which is that the compact ansatz + error mitigation makes NISQ 2e chemistry actually work on real hardware. That claim (C4) and the auxiliary symmetry-verification claim (C5) were never touched. The verdict is honest at the level of "we reproduced the noise-free curve exactly"; it would be dishonest if read as "we reproduced the paper."

## Load-bearing weaknesses

### 1. Trivial optimisation regime — expressiveness ≠ trainability

H2/STO-3G with a 1-parameter ansatz is a scalar line search over a smooth
cosine-like objective. BFGS from any of 9 starts trivially finds the analytic
global minimum. **This exercises the ansatz's Hilbert-space reachability,
nothing more.** The barren-plateau / initialisation-sensitivity / local-minima
failure modes that dominate realistic VQE at 20+ parameters are not tested.
Anyone reading "18/18 within chemical accuracy" should not infer anything
about how the compact ansatz would fare in a real optimisation landscape at
scale — because there is no analog at 1 parameter.

### 2. Single molecule, single basis — not a benchmark, a sanity check

Paper reports H2 curve AND H3+ curve (6 qubits). We reproduced only H2. Paper
implicitly generalises to arbitrary two-electron systems. We tested one. In a
minimal basis (STO-3G) where the ansatz is trivially expressiveness-complete
by construction. A curve sweep over one molecule in one basis is a sanity
check, not a benchmark. Calling this a "benchmark reproduction" (as the dir
name suggests) is overclaiming.

### 3. Hardware claims: fully unexercised, permanently unreachable

C4 (mhartree accuracy on ibm-5 / ibm-14 with mitigation) and C5 (symmetry
verification improves N-representability metric V) are the paper's actual
NISQ-relevance claims. Both target IBM devices that are retired. No free
endpoint we can access reproduces the *same device noise profile*. What we
CAN do — Qiskit Aer noise-model simulation calibrated to archived device
calibrations — was NOT done here. That is a real gap, not a fundamental
impossibility. Logged as open question #2.

### 4. CNOT count comparison is not apples-to-apples

We report 6 CNOTs (our compact single-Pauli-string) vs 8 CNOTs (paper's
NN-constrained Nam et al. decomposition) vs 14 CNOTs (our UCCSD). Three
different decomposition strategies, one figure. The 6-vs-8 gap is because
we drop 7 Pauli strings that happen to act as identity on the ansatz orbit,
which is legitimate for a statevector benchmark but would not be safe on
noisy hardware where those "identity" strings interact with decoherence
differently. Reporting 6 CNOTs is a mathematically correct lower bound
for our simulation; it is NOT a fair improvement over the paper's 8. We
called this out in REPORT.md §4.3 but did not build the paper's exact
decomposition side-by-side.

### 5. UCCSD baseline is our own build, not the field's canonical

Our UCCSD/H2/STO-3G at 14 CNOTs is one valid decomposition; the literature
range is roughly 8–20 CNOTs depending on grouping strategy (paired-CCD vs
generalised, Trotter step ordering, Givens vs Jordan-Wigner). The ~2×
CNOT-savings headline (6 vs 14, or 8 vs 14) is directionally correct but
not a formal lower bound. A stronger comparison would use a fixed-transpiler-
policy standard from a Qiskit-Nature or OpenFermion reference build.

### 6. Chemical-accuracy verdict is trivial in this regime

"18/18 within 1.6 mhartree" is real, but the max error is 4×10⁻¹² mhartree —
roughly 12 orders of magnitude below the threshold. Any expressiveness-complete
ansatz would clear the bar. Stating the count without stating the margin can
mislead readers who calibrate to the threshold.

### 7. No comparison against modern adaptive ansatze

Since 2020, ADAPT-VQE (Grimsley 2019), iterative-QCC, and qubit-ADAPT (Tang
2021) have become the state-of-the-art baselines for "few-parameter VQE
ansatz." A fair contextualisation of the compact 2e ansatz in 2026 requires
this comparison. Not attempted. Logged as open question #1.

### 8. Natural-orbital basis is silently re-optimised per geometry

`openfermion.MolecularData + run_pyscf` implicitly rebuilds the NO basis at
every R. In production this is not always what you want (e.g. reactive dynamics
along a single potential-energy surface prefers a fixed basis). The
transferability of the compact ansatz across bond-length regimes under a
frozen NO basis is a natural question the paper does not address and we did
not test. Logged as open question #3.

### 9. No embedding / active-space extension

The compact ansatz's practical utility depends on plugging into an active-space
wrapper for molecules bigger than H2. This is what CASSCF(2,2) is for. Not
tested. Logged as open question #4.

### 10. Extraction artifact: pdftotext, not nougat

Paper text was extracted via `pdftotext -layout`, not Nougat OCR. Extracted
text is captured in `work/paper.txt` and was human-verified against the PDF
for claims-table construction; but the `extraction/nougat.mmd` in this
backfill is a stub (Nougat rerun deferred as per the free-endpoint /
no-rerun contract).

## What this replication got right

To be fair to the actual work done:

- The core code path (openfermion + expm_multiply + scipy BFGS) is a clean,
  minimal, independently written implementation. Not a copy of the paper's code.
- The Qiskit cross-check via `Statevector` on an explicit CNOT-staircase circuit
  is a genuinely independent code path (different library, different mathematics
  of state preparation, agrees to 10⁻¹² Ha). This is the single most valuable
  piece of evidence.
- The 18-point curve at wide bond-length range (including strongly dissociated
  geometries where HF fails qualitatively) is meaningful evidence for
  ansatz expressiveness across the whole potential-energy surface, not just
  near equilibrium.
- The UCCSD baseline, while not canonical, is a self-consistent apples-to-apples
  comparison within this replication.
- Scope cuts are declared up front in the claims table (§2), not hidden in
  footnotes.

## Bottom line

**Verdict remains REPLICATED**, correctly scoped: the paper's noise-free
ansatz-expressiveness claim on its headline system is exactly reproduced.
The paper's hardware and error-mitigation claims are neither confirmed nor
refuted here; they remain empirically open pending the noise-model probe in
open question #2. Anyone building on this replication should read this file
before citing "REPLICATED" as endorsement of C4 or C5.
