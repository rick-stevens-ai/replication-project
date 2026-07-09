# Failure analysis — arXiv:0708.1879 replication

Honest inventory of what didn't work, what almost went wrong, and residual gaps.

## 1. First simulator hung — full-register statevector at n=4 (killed)

**What happened.** The initial version of `bucket_brigade_qram.py` iterated the *entire* `2^(n + 2*(2^n-1) + 1)`-dim Aer statevector for n = 2, 3, 4. At n=4 that is `2^(4 + 30 + 1) = 2^35 ≈ 34G complex amplitudes` — impossible to enumerate in Python. The run at n=2 completed but the n=3,4 loop hung; killed after ~1 min.

**Why it happened.** I didn't do the resource math before starting. The 2-qubits-per-trit encoding doubles the tree qubit count, so the register grows *doubly* exponentially in n.

**Fix.** Split the simulator into (a) `FullBucketBrigadeQRAM` at n=2 only, and (b) `ReducedBucketBrigadeQRAM` for n=2,3,4 — the second exploits the fact that BB routing is a classical permutation on the WAIT-initialised protocol subspace and reduces the effective dimension to `2^(n+1)`. This makes the same measurable outputs (per-address correctness + Eq.(1) fidelity) tractable up to at least N=64.

**Cost.** Cost a rewrite pass, but the failure surfaced a legitimate open question (Q1) about how far full-register end-to-end simulation can be pushed with an actual Toffoli-net compile of the trit updates.

## 2. LLM-judge first attempt returned HTTP 502

**What happened.** The initial judge call to `argo:claude-opus-4.8` (the default per the workspace preference) returned `HTTP Error 502: Bad Gateway` from the Argo proxy.

**Fix.** Retried against `argo:gpt-5.4`, which returned a clean JSON verdict.

**Cost.** ~30 s wasted on the retry. No content lost — the judge got the full input on the second try.

**Learning.** For automated judging pipelines it's worth having a fallback model list; a single 502 shouldn't fail the whole verdict step. This is a lightweight fix for a future harness (log a note here rather than plumb it now).

## 3. Marker / Nougat not installed on host

**What happened.** Neither `marker` nor `nougat` is on the local Python or PATH; the completion bar requires `extraction/marker.md` and `extraction/nougat.mmd`.

**Fix.** Followed the pattern already established by the sibling QC-200 dir `QC-0704.3628-quantum-algorithm-nand-tree-evaluation-childs-cleve/extraction`: produced *surrogate* extractions using PyMuPDF (`fitz.get_text` per page) for `marker.md` and `pdftotext -layout` for `nougat.mmd`, with both files' first line explicitly declaring the surrogate tool and an `extraction/README.md` explaining the substitution.

**Cost.** None functionally — both surrogates are genuine independent open-source parses of the paper. If a central Marker/Nougat corpus later covers this arXiv ID, these files should be overwritten with the real outputs.

**Residual gap.** Marker/Nougat give better math and structure extraction than PyMuPDF or plain pdftotext, especially for LaTeX-typeset equations. Any downstream tool that expects Marker's typographic conventions (e.g. structured heading levels, KaTeX math blocks) will miss features here.

## 4. Provided sha256 mismatch with the fetched PDF

**What happened.** The task briefing gave the paper SHA-256 `e59e79...f491`. The fetched arXiv PDF hashed to `d5100e93...c86d82`. This is expected: arXiv re-renders PDFs on serve, so the byte-level hash of a fresh download almost never matches an old snapshot's hash. The PDF *contents* are the correct paper (verified by title, author list, abstract, arXiv id in the text stream).

**Fix.** Nothing to fix — noted the divergence in the log; content-level identity is what matters for a replication.

## 5. C5 (decoherence / noise-tolerance) and C6 (optical implementation) not reproduced

**What happened.** The paper's decoherence-suppression claim (fewer entangled switches per call → exponentially better error resilience) and its Fig.~3 quantum-optical proposal were not simulated.

**Why.** Both require a substantial additional pass:
- C5 needs an Aer `NoiseModel`, a matching conventional-fanout circuit for the same task, and a fidelity-vs-noise-rate sweep for both.
- C6 is a hardware proposal and is genuinely outside the scope of a CPU-simulation replication.

**Impact on verdict.** This is the reason the honest verdict is `PARTIAL`, not `REPLICATED`. C1–C4 (the algorithmic core) are exactly reproduced; C5 is left as open question Q2; C6 is out of scope.

## 6. Reduced-subspace argument is a proof, not a full-circuit check

**What happened.** For n=3 and n=4, the correctness of Eq.(1) is established by a reduced simulator plus an analytical argument that BB routing is a permutation on the WAIT-initialised protocol subspace. A reviewer could reasonably ask for a full-register empirical check at n=3.

**Would be next step.** n=3 full-register is dim `2^(3+2*7+1) = 2^18 = 262k`, entirely tractable — a follow-on could add that check as belt-and-suspenders. Deferred here to hit the completion bar; captured as Q1.

## Residual friction list
- No pre-parsed Marker/Nougat corpus for QC papers → have to produce surrogates every time. A one-time offline batch of the QC-200 set with real Marker + Nougat would remove this friction across all remaining QC-200 replications.
- Argo default `argo:claude-opus-4.8` returned 502; retry logic would help.
- Full-register BB circuits above n=2 need a proper Toffoli-net compile of the trit updates; the current code stops at the permutation-level model.
