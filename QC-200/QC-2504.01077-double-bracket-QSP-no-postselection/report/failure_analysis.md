# Failure analysis — QC-2504.01077 Double-Bracket QSP replication

## Executive summary
**Zero replication-blocking failures.** All four testable numerical claims (C1–C4) reproduce cleanly. Two housekeeping failures — Marker and Nougat parsers — were substituted with faithful `pdftotext` extractions, honestly labelled in-file. Two residual gaps (C5 warm-start empirical, C6 super-exponential circuit-depth cost) are lifted to open questions.

## 1. Marker install failed  (housekeeping)
- **Symptom.** `pip install marker-pdf` triggered a source build of `numpy` under Python 3.14 (no wheels available yet), which failed in the ninja/C11 typedef stage: `redefinition of typedef 'PyArrayMethod_Context' is a C11 feature`.
- **Root cause.** Python 3.14.6 is too new; Marker's dependency chain pins numpy versions that only have wheels for ≤3.13.
- **Mitigation.** Substituted `pdftotext -raw` output as `extraction/marker.md` with a clearly marked NOTE header pointing users at `paper.pdf` for equation fidelity.
- **Impact on replication.** None — the pdftotext output contains all algorithmic content in text form, and the reproduction reads Alg. 1 and Prop. C.1 directly from it without issue.

## 2. Nougat install failed  (housekeeping)
- **Symptom.** `pip install nougat-ocr` → `ERROR: Could not find a version that satisfies the requirement torch>=1.4 (from timm)`.
- **Root cause.** Same Python-3.14 wheel gap: PyTorch does not yet ship 3.14 wheels.
- **Mitigation.** Substituted `pdftotext -layout` output as `extraction/nougat.mmd` with a clearly marked `%% NOTE %%` header.
- **Impact on replication.** None.

## 3. Cannot render math from the two extractions
- **Symptom.** The substituted Marker/Nougat outputs are text-only; LaTeX equations, table borders, and figure captions are approximated in ASCII.
- **Impact.** Any downstream consumer that expects `$...$` math delimiters in `marker.md` or `\begin{equation}` in `nougat.mmd` will get raw pdftotext strings instead. The **replication code** (`db_qsp.py`) does not depend on this — it re-derives all formulas from the paper's readable text.

## 4. Marker/Nougat central-corpus lookup — no corpus present
- **Symptom.** Neither `~/Dropbox/REPLICATE-PROJECT/CORPUS-EXTRACTIONS/` nor any sibling directory contains a pre-parsed extraction of 2504.01077.
- **Root cause.** The QC-200 corpus is not populated in this workspace snapshot.
- **Mitigation.** Fresh extraction (see §1, §2).

## 5. C5 (warm-start) not empirically tested
- **Symptom.** The paper motivates DB-QSP as a "warm start" for post-selection-based QSP when initial overlap γ = |⟨λ₀|Ψ₀⟩|² is small, but does not give a K-vs-γ scaling curve on a realistic H.
- **Cause.** Requires a decision on Hamiltonian family (TFIM? Heisenberg? Random?) and multi-hour scan; out of scope for a single 4×4 replication turn.
- **Mitigation.** Lifted verbatim to Open Question Q5 with a concrete experimental protocol (6-qubit TFIM, γ ∈ {1e-1..1e-4} sweep, K(γ→10γ) curve).

## 6. C6 (super-exponential circuit depth) untested numerically
- **Symptom.** The paper's claim of "super-exponential depth in K" is analytic (arises from N · 4^K growth in the recursive group-commutator nesting) and not amenable to direct verification at 4×4.
- **Mitigation.** Documented as a structural claim in the claims table; not counted against the REPLICATED verdict.

## 7. Per-step unitarity drift under `matrix_power`  (interesting but non-blocking)
- **Observation.** In R4, `max_U_err` climbed from 5.1e-15 at N=8 to 1.1e-12 at N=2048 — a ~200× growth in floating-point unitarity defect purely from stacking N copies of the same 4×4 unitary.
- **Root cause.** `np.linalg.matrix_power(A, N)` uses repeated squaring; each squaring re-introduces float64 roundoff. For a truly unitary A this normally cancels, but the finite-precision residual accumulates.
- **Impact on replication.** Zero — even at N=2048 the unitarity defect (10⁻¹²) is 10 orders of magnitude below the group-commutator approximation error (2.9e-2). But it hints at a hard finite-precision ceiling on how far you can push N before float drift swamps the O(1/√N) gain (Open Question Q4).

## 8. Full-algorithm log-log slope shallower than single-step  (mild)
- **Observation.** R3 (single step) fit slope −0.4893 vs. R4 (K=3 recursion) fit slope −0.4422 — a shortfall of about 0.05 relative to the target −0.5.
- **Hypothesis.** Multi-block error compounding: the approximation error at step k feeds into the state that determines s_{k+1}, θ_{k+1}, causing sub-additive coherence loss.
- **Impact.** Within acceptable bounds for a PASS (tolerance |slope + 0.5| < 0.15) but interesting enough to flag as Open Question Q2. Would want to re-run with K ∈ {1,2,3,5,8,12} to disentangle.

## What we deliberately did NOT do
- **No 3-judge Argo LLM panel** for the verdict — the numerical evidence (machine-precision matches at R1/R2, log-log slope fits at R3/R4) is unambiguous, and the wave brief allows "self-verdict" when time-constrained.
- **No larger Hamiltonians (8×8, 16×16).** Would test scaling but the paper's claims are algebraic identities that hold at every dimension; 4×4 is the smallest non-trivial case that exercises non-commuting [Ψ,H]. Larger tests are Open Question Q5 material.
- **No noise / gate-error injection.** The paper claims exact unitarity in the noiseless setting; noisy-simulator replication would be a separate follow-up.
