# Failure analysis — QC-quant-ph-0603140

Even for a clean REPLICATED verdict, this section documents the friction,
partial-mismatches, assumptions, and residual gaps.

## What actually failed / friction

### F1. Marker and Nougat not installed
- **Symptom.** `which marker`, `which marker_single`, `which nougat` all returned
  "not found"; `pip list` in the workspace venv had no marker-pdf or nougat-ocr.
- **Root cause.** Marker-pdf's build has historically required numpy < 2.x wheels
  that don't cleanly install on Python 3.14; nougat-ocr similarly gated on
  specific torch versions. This environment matches the sibling QC-200
  replication `QC-quant-ph-0102014-nonabelian-hidden-subgroup` which documented
  the same failure mode in its own `failure_analysis.md`.
- **Workaround.** Wrote pdftotext fallbacks with header notes clearly labelling
  them as fallbacks. Same convention as the sibling replication, so the
  QC-200 corpus is internally consistent.
- **Residual gap.** Any downstream tool expecting real Marker structural
  hierarchy (headings-as-JSON, equation environments, etc.) will get flowed
  text instead. Grep-based tools work fine.
- **What would be needed to close.** Set up a dedicated venv on Python 3.11 with
  numpy 1.26 for marker-pdf, or use the pre-baked Marker service on
  m1-mac-mini/uicgpu if it exists in the central corpus for this arxiv id
  (it doesn't as of 2026-07-05 for `quant-ph/0603140`).

### F2. No end-to-end simulation of the standard non-abelian QHS algorithm
- **Symptom.** Section 9's central claim is "standard non-abelian QHS on S_N
  cannot solve Grover's HSP." A truly end-to-end numerical test would run the
  QHS algorithm as an actual quantum circuit and observe the failure.
- **Root cause.** The standard non-abelian QHS algorithm requires (a) a group
  register of size log|S_N| = O(N log N) qubits (14 qubits already for N=4,
  much larger for N=8,16), and (b) the quantum non-abelian Fourier transform
  on S_N, which is not a built-in Qiskit primitive. Building it correctly
  from Clausen-Baum / Beals circuits is a multi-week project of its own.
- **Workaround.** We verify Section 9 STRUCTURALLY: (i) largest normal
  subgroup of S_N in Stab_0 is {e} (finite exhaustive check for N=3,4,5,
  Part D); (ii) all stabilisers pairwise conjugate (finite check, Part D);
  (iii) induced-rep dimensions (Part E). The paper's own argument is
  group-theoretic and reduces to (i)+(ii) via the cited
  Hallgren-Russell-Ta-Shma theorem, so structural verification is faithful
  to the paper's reasoning.
- **Residual gap.** A direct QHS circuit simulation would strengthen the
  demonstration but is out of scope for a wave-brief replication.

### F3. Zalka's asymptotic bound (C10) not tested
- **Symptom.** The paper cites Zalka (arXiv:quant-ph/9711070) for the
  asymptotic optimality of Grover; we did not verify Zalka's bound.
- **Root cause.** Zalka's bound is an asymptotic Omega(sqrt(N)) query-lower-bound
  proved by an information-theoretic argument, not something reproducible at
  a single small N.
- **Workaround.** Explicitly marked "no" in the claims table and out-of-scope
  in Verdict; the finite-N replication cannot address this.

## Sensitivity / edge cases we checked

- Chose marked = 1 for Grover (arbitrary; any j_0 ∈ {0,...,N-1} yields
  identical statistics by symmetry, which is itself a corollary of the paper's
  Section-7 invariance claim).
- Ran Parts C, D, F with different j_0 values (2, 1, 3, 0) at different N to
  guard against a symmetry-fixing bug that only happens for j_0=0.
- For N=4 specifically we included V_4 in the normal-subgroup check to catch
  the exceptional-normal-subgroup structure of S_4.

## Assumptions inherited from the paper (not tested)

- Hallgren-Russell-Ta-Shma theorem (Fourier-sampling reveals only the
  largest normal subgroup contained in H). We accept this as a cited theorem
  and use it to reduce Section 9 to a finite group-theoretic check.
- Zalka's asymptotic Grover optimality (C10).
- The paper's mathematical formalism for "generic QHS algorithm QRand"
  (Section 3) — used to frame the discussion but not re-implemented here.

## Verdict impact

None of the friction items downgrade the verdict. The REPLICATED verdict is
based on C1-C8 all reproducing to machine precision or exhaustive finite
verification, plus C9 following from the standard HRT reduction (C6+C7).
The two items we could not test (Marker/Nougat parses; direct QHS circuit
simulation) are infrastructure/scope items, not scientific claims.
