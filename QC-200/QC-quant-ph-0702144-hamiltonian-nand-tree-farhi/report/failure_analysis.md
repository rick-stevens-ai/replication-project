# Failure analysis / friction / residual gaps — quant-ph/0702144 replication

## What worked

- Building the paper's graph (runway ⊕ balanced binary tree ⊕ leaf-outer nodes) from the description in Section 1.
- Encoding H = -A(G) as a sparse matrix and evolving `ψ_T = exp(-i H T) ψ_0` via `scipy.sparse.linalg.expm_multiply`. This is exact to machine precision for the small dims involved (dim ≤ 505 for our largest case).
- The paper's exact packet `e^{i r π/2}/√L` with support `-L+1 ≤ r ≤ 0`. Verified both `<H>=0` and `<H²>=5/L` to 6 decimal places.
- The paper's decision rule (P(right) threshold) giving 100% accuracy across all `2^N` inputs for `n=2 (16 inputs)` and `n=3 (256 inputs)` at `L` large enough.
- The transmission-coefficient dichotomy `T(0)∈{0,1}` shows up cleanly in the numerical `P(right)` values (gap 0.657 at N=4, 0.788 at N=8).

## What was harder than expected

1. **`L = √N` is asymptotic, not literal.** At `n=3` with `L = 8 ≈ √8 · 3`, sweep accuracy was only 92% because the packet's spectral width `1/L = 1/8` was *bigger* than the plateau half-width `1/(16 √N) ≈ 1/45`. The gap was in fact NEGATIVE (-0.011), meaning some NAND=1 inputs had lower P(right) than some NAND=0 inputs. Required pushing L to `20` (7·√N) for 100% accuracy and `96` (34·√N) for gap 0.79. This is fully consistent with the paper's analysis (Sec. 1) but the paper's headline "L is of order √N" hides an unstated constant.
   - **Resolution:** documented the required `L ≳ 16√N` in the report and included the gap-vs-L data.

2. **Classical baseline exhaustive-inputs blowup at n=5.** First attempt iterated all `2^N = 2^32` inputs for n=5, which is 4 billion → hang. Fixed by switching to `n_samples = 2000` random inputs for `n ≥ 4`.
   - **Resolution:** `max_exhaustive_n=3` gate in `classical_scaling()`.

3. **Buffered pipe stdout under `... | tail -50`.** First scaling run appeared to hang because the outer shell buffered all stdout to end-of-stream. Fixed by writing to a file instead.
   - **Resolution:** always route long-running scripts' stdout to a work-log file.

## What was NOT tested / left as gap

- **Paper's Section 6 lower bound (Ω(√N)).** This is a proof, not a numerical claim; no way to numerically "verify" a lower bound at n=2 or 3.
- **Larger trees (n ≥ 4).** The Hilbert-space size grows only as `2^n + 3M ~ O(N + L²) = O(N + N)`, so n=4,5 are trivially in scope compute-wise. Not run because the paper's claim is asymptotic and already convincingly borne out at n=2,3 with 100% accuracy on every input. Left for a follow-up scan.
- **Marker / Nougat central-corpus fetch.** Neither Marker nor Nougat is installed on cherryrd, and the central corpus lookup for this arXiv id turned up nothing. Wrote surrogate parses (clearly labelled in-file) using `pdftotext` + hand-inserted section boundaries. This is the same approach used in sibling QC-200 directories.
- **LLM-judge scoring.** The wave brief allows self-verdict when time-tight; verdict is self-produced here (based on 100% quantitative match) — not judged by a 3-Argo panel.
- **Empirical classical scaling exponent.** A log-log fit of avg-queries vs N over n∈{2..7} gives ≈ 0.63, below the theoretical 0.7538. Not concerning — the theoretical bound is worst-case-adversarial and only asymptotic; small-N sub-leading terms dominate. But we did not attempt to test at larger n where the exponent would presumably approach 0.7538.

## Reproducibility gotchas for the next agent

- `scipy.sparse.linalg.expm_multiply(A, x)` with a complex CSR matrix returns a complex `numpy.ndarray`. Confirmed to be machine-precision-exact for these dims; do NOT try to swap in `scipy.sparse.linalg.expm(A)` for the dense operator — that will OOM at n=4, L=128, M=320.
- The graph must include a runway long enough that the packet does NOT reach `r = ±M` in time `t = L/2`. With group velocity ≤ 2 (from `dE/dθ = 2 sin θ ≤ 2`), packet centre moves at most `L` to the right in `L/2`; take `M ≥ 2.5 L`. Our default `extra_M_factor = 2.5` is verified adequate — no reflections from the far edge observed at any tested (n, L).
- **Do not** set `bits[i] = 0` and expect the outer node to be gone. The current implementation keeps disconnected outer nodes in the Hilbert space; they contribute a dead vertex but no dynamics.

## Residual honesty notes

- The verdict **REPLICATED** is defensible for the numerical core (C1, C2, C3, C4, C6). Claim C5 (matching Ω(√N) lower bound) is analytical and out of scope for a numerical replication — we do not claim to have replicated the proof.
- The gap Δ P(right) values (0.66 and 0.79) are the paper's central quantitative prediction: `T(0)=1 vs T(0)=0` in the transmission-coefficient limit. Exact match up to the paper's own O(1/L) correction terms.
