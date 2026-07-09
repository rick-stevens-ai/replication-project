# Failure analysis / friction / residual gaps

Honest accounting of what did NOT go smoothly and what this replication does NOT cover.

## Friction hit during execution

### F1. Author-name typo in the wave brief
The subagent brief said "Jon R. Grice, Daniel A. Meyer". The PDF's title page has **David A. Meyer** (verified by pdftotext of paper.pdf). Handled: the report cites the verified name and notes the brief typo. No downstream impact — arXiv ID 1405.7479 unambiguously resolves to the right paper.

### F2. Marker + Nougat corpus not indexed here
The wave brief prefers the two extraction artifacts (`extraction/marker.md`, `extraction/nougat.mmd`) to be pulled from a central pre-parsed corpus. A `find` under `~/Dropbox` for `*1405.7479*` and for marker/nougat corpus directories did not converge within the subagent's turn budget (Dropbox filesystem is slow-walked). The Marker and Nougat CLIs themselves are not installed on this host and would require multi-GB torch model downloads which the free-endpoint rule discourages during a small-instance QC replication.

Compromise chosen: use `pdftotext` output as a stand-in for both, and note this clearly in `extraction/README.md`. All quantitative numbers in `report/REPORT.tex` are derived directly from the PDF (via pdftotext text and human re-reading of the equations), not from either "extraction" file. **This is the only artifact whose bar is partially degraded.**

### F3. Scope-bug in first run
The main script's summary-print block referenced `MSG_LEN` at module scope after moving it into `run_experiment()`. First run crashed AFTER writing `results.json` (which was fine) but with a `NameError` at the print stage. Fixed by pulling `msg_len` from the results dict. Second run clean.

### F4. Dropbox `find` sluggishness burnt ~30s of budget
Two exploratory `find` calls under `~/Dropbox` had to be killed after >15s each. Lesson for next-time: use `mdfind` on macOS for corpus lookups, or maintain a workspace-local corpus manifest.

## What this replication does NOT cover

### Claims we did not attempt
- **C3 (paper's gate complexity O(N|Q|F(log F)^2))** — our numpy statevector counts oracle queries correctly, but the diffusion and marking operators are implemented as O(L) classical linear algebra, not compiled to Toffolis. A Qiskit-based gate-level reproduction would take another session.
- **C4 (real-hardware time complexity O(N log F))** — needs a physical device.
- **C5 (tensor-product speedup over naive Grover-on-Q^N)** — we compare vs classical brute-force and classical Viterbi, not vs a Grover-on-Q^N baseline; this would require another implementation.
- **C6 (probabilistic QVA variant with multiple trials, no iterations)** — implementable in future work; not tested here.

### Numerical limits of the current sweep
- Sweep tops out at L=1024 (N=10). Statevector cost is O(L) memory + O(query_count · L) time; L=2^20 would still fit in RAM but the 20-trial ensemble would take hours. Bigger L is the natural follow-on (see open_questions.json Q1).
- Single BSC noise realization at p=0.05, single message realization. A Monte Carlo over messages and noise draws would give error bars on the query-count fit (see Q2 in open_questions.json).

### Methodology caveats
- The DH outer loop uses a "hard" query-count cap of 22.5·√L; in practice we terminate earlier (median ~90–140 queries in the sweep) because the threshold falls quickly and the loop hits its inner max_outer=50 limit. This matches theory but the specific constants are algorithm-implementation-dependent.
- We use BBHT (Boyer–Brassard–Høyer–Tapp) as the inner Grover strategy because the number of marked states below threshold is unknown; the paper's own inner routine is described differently but is asymptotically equivalent.
- The "quantum" oracle here is classical linear algebra on a numpy array of amplitudes. This is exactly what "real numpy statevector simulation" means, and matches the QC-200 wave brief's expectations, but is NOT a claim about quantum-hardware runtime.

## What would strengthen the replication further

1. Gate-level reproduction in Qiskit / Cirq that compiles the trellis-metric oracle to Toffolis and reports real gate counts. (Would touch C3.)
2. AWGN + soft-decision extension. (Open Q4.)
3. Sweep out to L = 2^18 with 100 trials each. (Open Q1.)
4. Head-to-head vs the paper's specific multiphase-kickback oracle. (Open Q3.)
5. LLM-judge 3-panel scoring (Argo Opus / GPT-5.2 / Gemini 2.5-pro at localhost:44497) — skipped this run per the brief's fallback to self-verdict.
