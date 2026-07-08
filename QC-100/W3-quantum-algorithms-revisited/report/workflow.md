# Workflow — QC-100 W3 / Cleve, Ekert, Macchiavello, Mosca 1998

## 0. Environment
- Language: Python 3.11+
- Deps: `numpy` only. No Qiskit / Cirq / PennyLane — this is a deliberate
  independent reimplementation from first principles so bit-order and
  normalization conventions cannot be laundered through a library default.
- Seed: 12345 (set at top of `replicate.py`).
- Runtime: seconds; no GPU, no cloud. All simulator, all local.

## 1. Reproduce
```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-100/W3-quantum-algorithms-revisited/
python3 replicate.py            # writes results.json
```
Expect `results.json` to match the numbers in `REPORT.md` / `report/REPORT.tex`
to machine precision (DJ/BV/QPE-dyadic/Shor eigenphases are exact; Grover
and Shor factoring are Monte-Carlo but seeded).

## 2. What each artifact holds
- `paper.md` — source-text extraction of the paper's claims.
- `replicate.py` — the single-file numpy simulator; contains DJ, BV, QPE,
  Shor order-finding, Grover, plus a small library of unitary constructions
  (Hadamard, inverse QFT as an exact matrix, controlled-U^{2^j} by direct
  diagonal action).
- `results.json` — machine-readable numbers cited in the report.
- `REPORT.md` — top-level markdown replication report (Rick's canonical
  report format). Written first.
- `report/REPORT.tex` — LaTeX version of the same report, adds the honest
  critique + open-questions section for the QC-100 backfill standard.
- `report/open_questions.json` — 5 forward-looking open questions in the
  project's structured JSON schema.
- `report/open_questions_section.tex` — the same questions as a LaTeX
  section, `\input`-ed into `REPORT.tex`.
- `report/workflow.md` — this file.
- `report/artifacts_summary.md` — one-line-per-file manifest.
- `report/failure_analysis.md` — honest critique of what the replication
  did and did NOT cover.
- `extraction/nougat.mmd` — stub; no Nougat rerun. Semantic extraction
  is already captured in `paper.md`.

## 3. Reproduction checklist
- [x] Independent reimplementation (numpy, no framework wrapper).
- [x] DJ / BV / QPE / Shor / Grover all implemented against the same QPE
      core — the paper's unified network claim is verified operationally.
- [x] QPE bound $\ge 4/\pi^2$ checked at $m=8$ across 2000 random $\varphi$
      (0 violations, min 0.4056).
- [x] Shor: full classical + quantum loop for $N=15$, success rate 0.983
      over 300 trials.
- [x] Grover: $P_k$ measured for $n=3..8$, all $> 0.5$.
- [ ] Simon and discrete log NOT implemented (only qualitative in paper).
- [ ] Larger Shor $N$ ($N \in \{21, 33, 35, 39\}$) NOT run.
- [ ] Depolarizing / gate-error noise study NOT run.
- [ ] Second-source cross-check against Qiskit / Cirq NOT run.
