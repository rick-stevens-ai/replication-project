# Attempt Log

**Session:** 2026-07-06 12:10–~12:35 CDT (subagent depth 1/1 under QC-quant-ph0102014).

## Timeline
- **12:10** Read WAVE_BRIEF_2026-07-01.md.
- **12:10** Created target dir `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph0102014-nonabelian-hsp-grigni-schulman/`.
- **12:10** Downloaded paper.pdf from `https://arxiv.org/pdf/quant-ph/0102014` (174 KB, 12 pages).
- **12:11** **Discovery: paper mismatch.** The task ticket said "Grigni, Schulman, Vazirani, Vazirani, 2001 STOC" but the actual paper at that arXiv id is **Ivanyos–Magniez–Santha**, *same title, different authors and different content*. GSV V's paper is cited here as ref [12] and is a separate work (never posted to arXiv under 0102014). Decision: proceed with the actual paper at the given id (as this is the only defensible interpretation of an arXiv-id-based task).
- **12:11** `marker_single` not in path; `nougat` not available. Fallback: `pdftotext -layout` yields high-fidelity 43.8 KB / 606-line plain text since the paper is TeX-typeset math with no figures beyond two 5×5 matrix schematics.
- **12:12** `pdf` tool errored (Anthropic 400 low-balance; Gemini 3 flash unknown; OpenAI gpt-5.5 needs extract plugin). Fell back entirely to local extraction + human-readable pdftotext output → hand-annotated marker-style summary.
- **12:12** Wrote `extraction/marker.md` (extraction + claims table) and `extraction/nougat.mmd` (fallback-note artifact).
- **12:13** Set up local venv `work/.venv` with qiskit 2.5.0 + qiskit-aer.
- **12:15** Wrote `work/hsp_ims_theorem13.py` implementing:
    - `WreathGroup` class for G = Z₂²ᵏ ⋊ Z₂ (wreath Z₂ᵏ ≀ Z₂ base) with correct semidirect multiplication and inversion.
    - Abelian HSP subroutine on (Z₂)ⁿ with two computation paths: (a) explicit Qiskit statevector circuit (H⊗ⁿ · U_f · H⊗ⁿ · measure) for small n, (b) analytic Numpy path using the exact closed-form probability Prob(w) = (1/|A|²) Σ_cosets |Σ_x (-1)^(w·x)|² for larger n.
    - Full Theorem 13 reduction: (Step A) recover H∩N via Abelian HSP inside N; (Step B) for each nontrivial coset representative z of G/N, define F: Z₂ × N → Y and run Abelian HSP to extract u so that u·z ∈ H; (Step C) generate H₁ from H∩N ∪ {u·z} and verify H₁ = H_planted set-equality.
- **12:20** First run: **4/12 passed**. Diagnosed two bugs:
    - **Bug 1: stability heuristic too eager** — the 5-consecutive-same-basis stopping rule stopped Step A while it had never seen a nonzero y sample. Fixed by requiring 15-streak plus at least n_bits+5 minimum samples.
    - **Bug 2: Qiskit oracle unitary endianness inverted.** In `abelian_hsp_z2n_sample_qiskit` I built the truth-table unitary with `src = x * dim_out + y`, but Qiskit's default endianness puts input qubits (0..n_bits-1) as low bits, so the basis index is `(y << n_bits) | x`. This bug made the Qiskit path return y=0 for every input, poisoning small-n runs. Fixed the indexing.
- **12:25** Second run: **5/12 passed** — the Bug-2 fix made small cases work but the stability heuristic still not enough. Third run: **12/12 passed**.
- **12:26** Widened sweep to k = 1..4 (|G| = 8, 32, 128, 512), 6 trials per k, alternating between (a) hidden subgroups intersecting the nontrivial coset z·N (the interesting Theorem-13 case) and (b) hidden subgroups contained entirely in N. **Result: 24/24 passed** in 20.3 s wall time.
- **12:28** Wrote `work/lemma9_verify.py`: builds a *genuine* quantum-state oracle for Lemma 9 — for each coset of H it emits a distinct random-orthonormal unit vector in a d-qubit register (d = ⌈log₂(|A|/|H|)⌉), not just a computational-basis label. Runs the 4-step Abelian-HSP circuit as an exact Qiskit statevector, marginalises over the output register, compares the input-register probability distribution to the analytic prediction (uniform on H⊥, zero elsewhere). **20/20 seeds × sizes passed with maximum error ≈ 10⁻¹⁶.**
- **12:33** Wrote reports.

## What worked
- Analytic Numpy path made scaling to |G|=512 trivial (each Abelian HSP sample is O(|A|·|H|) work; total ~50 samples per case).
- The Theorem-13 reduction is *exactly* as clean as the paper claims; the pipeline needed no algorithmic tweaks once bugs 1 & 2 were fixed.
- The Qiskit statevector path independently confirms the analytic formula (compared on k=1 case, distribution matches).

## What broke and how it was fixed
- **Qiskit endianness bug** — silent failure (all-zero samples). Diagnosed by running the numpy and qiskit paths on the same trivial-H input and comparing distributions (numpy: uniform 16-way, qiskit: point-mass at 0). Fixed by using `(y << n_bits) | x` as the basis index throughout the truth-table.
- **Stopping-rule too eager** for the Abelian HSP subroutine when the true H^⊥ contained only the identity (all samples y=0). Fixed by requiring both a 15-round stable streak AND a minimum of n_bits+5 samples.
- **`pdf` tool unavailable** for extraction (all 3 backend models errored). Fallback to `pdftotext -layout` + hand annotation was actually fine for this LaTeX-typeset math paper.

## What would need more time
- Extending to non-wreath instances of Theorem 13 (e.g. matrix groups over GF(2) of the "type-(a)/type-(b) generator" pattern from §6 — the paper's exemplar family). Straightforward given the reduction already coded.
- A full Theorem-11 (small commutator subgroup) implementation on extra-special p-groups (Corollary 12), e.g. Heisenberg over F₃.
- Wiring an LLM-judge scoring pass over the report artifacts (the brief specifies LLM-judge verdicts; we ran ground-truth set-equality checks against planted subgroups instead, which is a strictly stronger verdict signal).
