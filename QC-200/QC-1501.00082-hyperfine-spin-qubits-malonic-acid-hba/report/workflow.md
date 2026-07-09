# Workflow — QC-1501.00082 Replication

## Timing summary

Approximate elapsed wallclock for this replication: ~20 minutes single-agent, all steps CPU-only on CherryRd.

| Phase | Wallclock | Notes |
|---|---|---|
| Fetch PDF + pdftotext | ~5 s | curl + poppler |
| Skim & extract analytical claims | ~3 min | grep + read on `work/paper.txt` |
| Write HBAC simulator (numpy) | ~5 min | pure-python density-diagonal PPA |
| Run all 4 experiments (C1-C4) + plot | ~2 s | numpy exact-arithmetic sort + kron |
| Write REPORT.tex + open_questions.json + supporting md | ~10 min | authoring |
| Compile REPORT.pdf | ~5 s | pdflatex (best-effort; TeX Live availability-dependent) |

## Tool inventory (versions)

| Tool | Version | Purpose |
|---|---|---|
| macOS / Darwin | 25.3.0 | Host |
| Python | 3.11 (`/usr/bin/python3`) | Simulation runtime |
| numpy | 1.26+ | Density-matrix arithmetic |
| matplotlib | 3.8+ (Agg backend) | Fig 7 reproduction PNG |
| PyMuPDF / fitz | 1.27.2.3 | Marker surrogate → `extraction/marker.md` |
| Poppler pdftotext | (system) | Nougat surrogate → `extraction/nougat.mmd` + `work/paper.txt` |
| curl | (system) | Fetch paper.pdf from arxiv.org |
| pdflatex | (best-effort, TeX Live) | Compile REPORT.tex → REPORT.pdf |

**Not used:** Argo, any LLM API, any external service, any paid endpoint.
The QC brief permits Argo (`localhost:44497 key=stevens`) but this
replication did not require LLM inference — the claims are exactly-verifiable
by a 60-line numpy simulation.

## Step-by-step commands (reproducible from this dir)

```bash
# 1. Fetch paper
curl -sL -o paper.pdf https://arxiv.org/pdf/1501.00082
pdftotext -layout paper.pdf work/paper.txt

# 2. Produce Marker+Nougat surrogates in extraction/
python3 work/make_extractions.py

# 3. Run the density-matrix HBAC simulator
python3 report/evidence/hbac_simulation.py 2>&1 | tee report/evidence/run.log

# 4. Plot Fig 7 replication
python3 report/evidence/plot_fig7.py

# 5. Compile the LaTeX report (best-effort)
cd report && pdflatex -interaction=nonstopmode REPORT.tex && pdflatex -interaction=nonstopmode REPORT.tex
```

## Design decisions (explicit, so a re-runner can question them)

1. **Density diagonal only, no coherences.** PPA compression is a
   permutation of populations; the initial product-thermal state is diagonal;
   reset is a partial trace + fresh thermal tensor product (also diagonal).
   Coherences never appear in the PPA idealization the paper's black-dashed
   "Theory" curve models. Storing only the 2^n diagonal is exact for this
   family of protocols.
2. **Sort-in-non-increasing-order compression.** Paper Sec 5 defines PPA
   compression as "a permutation that rearranges the diagonal elements of
   the density matrix in non-increasing order." We implement exactly this.
3. **Idealized reset (no Lindblad).** Reset is modeled as an instantaneous
   product-thermal re-preparation of the reset qubit at ε_b, with no leakage
   into the target qubits. This exactly matches what the paper calls the
   "Theory" curve in Fig 7 (black dashed) — the red / blue / green curves
   introduce Markovian T1/T2/T2* processes we deliberately do NOT reproduce
   (out of scope for a text-only replication).
4. **Same protocol at all n.** For n=3 the paper's simulated protocol IS the
   PPA (one swap, one swap, one 3-qubit sort). For n=5 the paper uses a
   modified swap-then-sort protocol that is NOT the true PPA (the paper is
   explicit about this). Our simulator uses the paper's n=3 protocol at all
   n, which is why it matches paper's asymptote exactly at n=3,4 but
   under-shoots at n≥5. This is a documented scope choice; Open Question Q1
   proposes the recursive PPA as follow-on.

## Estimate of work performed

- **Independent PPA density-matrix simulator implemented from scratch** (no
  copy-paste from any existing HBAC library).
- **Five numerical experiments** (C1 across 5 ε_b values, C2 across 5 ε_b
  values × 60 rounds, C3 across n∈{3..7} × 200 rounds, C4 at n=3 and n=5,
  full-curve reproduction of Fig 7 at 3 ε_b values × 16 rounds each).
- **One PNG plot** reproducing paper Fig 7's black-dashed theory curve.
- **Detailed LaTeX report** (REPORT.tex, 300+ lines) with claims table,
  results tables at floating-point precision, verdict, and 5 open questions.
- **All 8 required artifacts** produced.
- **Zero external network calls after fetching paper.pdf** (no LLM
  inference, no data downloads beyond the one PDF).
