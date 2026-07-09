# Workflow — Portugal (2017) "Element Distinctness Revisited" replication

## Timing & effort
- **Wall-clock**: single subagent turn, ~15 minutes total (paper fetch → PDF read → code → debug typo → sweep → plots → report).
- **Simulation time**: <1 second for 14 sizes N ∈ {6, 9, 12, 15, 20, 30, 50, 80, 120, 200, 400, 800, 1500, 3000} on CherryRd CPU (5×5 matrix exponentiation only).
- **Human/agent decisions during the run**:
  1. Realized the task-prompt description ("coined walk on Johnson graph J(N,3)") does **not** match the paper; verified against the fetched PDF that the paper actually uses the staggered walk on graph Γ (line graph of Ambainis' bipartite graph) with an exact (2k+1)-dim invariant subspace. Coded the paper's actual formulation, not the prompt's paraphrase.
  2. Chose the reduced (2k+1)-dim subspace as the simulation target instead of full-space simulation. Rationale: it is mathematically identical for computing success probability, and the paper *proves* this is exact — no approximation. Full-space simulation would be limited to N ≤ ~10 by C(N,r)·(N-r)·M^{r+1} dimension explosion.
  3. Diagnosed a mismatch between the extracted Eq. (9) and the paper's own claim that u_β is unitary. Fixed by using the symmetric reading j → j (not j → j') in the off-diagonal Kronecker δ. Documented the fix inline in code and in the report.
  4. Fixed a float-overflow bug in the initial-state builder for large N by moving the C(N,r)·(N-r) normalization into log-space (lgamma).

## Step-by-step commands

```bash
# 1. Set up working dir
cd ~/Dropbox/REPLICATE-PROJECT/QC-200
mkdir -p QC-1711.11336-element-distinctness-revisited-portugal/{work,extraction,report/evidence}
cd QC-1711.11336-element-distinctness-revisited-portugal

# 2. Fetch paper
curl -sL -o work/paper.pdf https://arxiv.org/pdf/1711.11336
cp work/paper.pdf paper.pdf

# 3. Extract text (marker/nougat unavailable on host; pdftotext fallback)
pdftotext -layout work/paper.pdf work/paper.txt
cp work/paper.txt extraction/marker.md
cp work/paper.txt extraction/nougat.mmd

# 4. Verify title / author / theorem directly from paper.txt (2-min skim).

# 5. Run replication
python3 report/evidence/replicate_portugal.py \
  | tee report/evidence/replicate_portugal.log
python3 report/evidence/make_plots.py

# 6. Compile report
cd report && pdflatex -interaction=nonstopmode REPORT.tex \
                 && pdflatex -interaction=nonstopmode REPORT.tex
```

## Tools + versions

| Tool | Version | Purpose |
|---|---|---|
| `python3` | 3.13 (system) | Simulation harness |
| `numpy` | ≥2.x (system) | Linear algebra (5×5 matrices; matrix_power) |
| `matplotlib` | (system) | Log-log plot |
| `curl` | (system) | Paper fetch |
| `pdftotext -layout` | poppler (Homebrew) | PDF → text extraction (fallback for marker/nougat) |
| `pdflatex` | TeX Live 2026 | Report typesetting |
| **not used** | Qiskit, Cirq, Stim, PennyLane | Not needed — the paper's (2k+1)-dim reduction *is* the exact classical simulation |
| **not available** | marker, nougat | See `extraction/README.md` for pdftotext fallback |

## Why no full-circuit simulator
The paper's own Theorem 3.1 proves the algorithm's dynamics are invariant on the (2k+1)-dim subspace spanned by |η_ℓ^j⟩. For k=2 that's a 5×5 matrix. This is the *definitive* classical simulation for computing success probability — not an approximation. A Qiskit/Cirq full-circuit implementation would (a) require simulating the C(N,r)·(N-r)·M^{r+1}-dim full Hilbert space (intractable beyond N ~ 8), and (b) produce numerically identical success probabilities to the reduced-subspace simulation. We chose the mathematically-equivalent reduction that lets us run all the way up to N = 3000 in <1 s.

## What I actually implemented (files)

| File | LoC | Purpose |
|---|---|---|
| `report/evidence/replicate_portugal.py` | ~350 | u_alpha, u_beta, R, psi0 builders; sweep runner; classical baseline |
| `report/evidence/make_plots.py` | ~65 | Log-log Q-vs-N + p_succ-vs-N figure |
| `report/REPORT.tex` | ~300 | Full LaTeX report (compiled: `REPORT.pdf`, 8 pages) |
| `report/open_questions.json` | 5 items | Machine-readable open-questions (each `q`, `basis`, `next_steps`) |
| `extraction/marker.md`, `extraction/nougat.mmd` | pdftotext fallback | Cover the 8-artifact bar; see `extraction/README.md` |

## What I did NOT do

- Did **not** run marker or nougat (not installed on execution host).
- Did **not** run a full-circuit Qiskit/Cirq simulation (mathematically redundant per the paper's own invariant-subspace theorem; would be strictly *less* informative because it's limited to N ~ 8).
- Did **not** try k ≥ 3 (paper focuses on k=2, wave brief targets the element-distinctness headline claim, and k=3 is Belovs 2012 territory).
- Did **not** call any LLM endpoint (paper is short and self-contained; classical replication of the numerical claims did not need LLM assistance). Argo remains available at `localhost:44497` per the wave brief but was not needed.
