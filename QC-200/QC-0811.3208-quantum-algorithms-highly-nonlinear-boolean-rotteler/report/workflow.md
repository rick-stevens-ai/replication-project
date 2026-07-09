# Workflow — QC-200 replication of arXiv:0811.3208 (Rötteler 2008)

## Wall-clock estimate
~55 minutes total (one subagent, single session, 2026-07-05).

| Phase                                       | ~time  |
|---------------------------------------------|--------|
| Read wave brief + fetch/parse paper         | 8 min  |
| Skim paper, locate A_1 / A_2 pseudocode     | 6 min  |
| Design M-M bent + WHT + statevector plan    | 5 min  |
| Write `rotteler_replication.py` v1          | 10 min |
| Debug A_2 (found dual-coset simplification) | 10 min |
| Add classical baselines + scaling scan      | 6 min  |
| Write REPORT.tex + open_questions.json      | 10 min |

All compute on CherryRd CPU; no HPC, no GPU, no LLM inference budget used
for the reproduction itself (LLM would only be invoked for optional
judge scoring, skipped this run).

## Environment
- Host: `CherryRd` (Darwin 25.3.0, x64)
- Python: `/usr/local/bin/python3` (Python 3.14.6, Jun 2026)
- Packages: `numpy 2.4.3`, `PyMuPDF (fitz) 1.27.2.3` (for surrogate marker)
- Utilities: `pdftotext` (poppler, for surrogate nougat)
- Not used (missing on host): `qiskit`, `marker`, `nougat`, `cirq`,
  `pennylane`
- LLM endpoint (available but unused for this task): Argo
  `http://localhost:44497`, key `stevens` (free)

## Tools & versions
| Tool | Version | Role |
|---|---|---|
| numpy | 2.4.3 | Exact statevector simulator, FWHT, GF(2) linear algebra |
| PyMuPDF (fitz) | 1.27.2.3 | Marker surrogate parse |
| pdftotext (poppler) | system | Nougat surrogate parse, initial paper skim |
| curl | system | Fetch arXiv PDF |
| bash / zsh | system | Orchestration |
| python 3.14.6 | system | Everything |

## End-to-end command sequence
```bash
# 1. Fetch paper
curl -sL -o work/paper.pdf https://arxiv.org/pdf/0811.3208
pdftotext work/paper.pdf work/paper.txt

# 2. Extraction artifacts (surrogates)
python3 - <<'PY'
import fitz
doc = fitz.open("paper.pdf")
open("extraction/marker.md","w").write(
    "# Extraction (SURROGATE for Marker) — tool: PyMuPDF (fitz) v"
    + fitz.__version__ + "\n\n"
    + "\n\n---- page N ----\n\n".join(p.get_text() for p in doc))
PY
{ echo "% Extraction (SURROGATE for Nougat) — pdftotext -layout"; pdftotext -layout paper.pdf -; } > extraction/nougat.mmd

# 3. Run replication
python3 report/evidence/rotteler_replication.py \
    2>&1 | tee report/evidence/run.log

# 4. Reports (this workflow, artifacts_summary.md, failure_analysis.md,
#    REPORT.tex, open_questions.json)
```

## What was implemented from scratch (no external dependencies beyond numpy)
1. `int_to_bits`, `bits_to_int`, `dot_mod2` — bit-wise helpers.
2. `walsh_hadamard(vec)` — iterative in-place fast Walsh–Hadamard
   transform (butterfly, unnormalised), used both as the classical
   spectrum computation and as $H^{\otimes n}$ in the statevector
   simulator.
3. `make_mm_bent(n, seed)` — deterministic Maiorana–McFarland bent
   function generator: random permutation $\pi$ on $\{0,\dots,2^{n/2}-1\}$,
   random $g:\mathbb{Z}_2^{n/2}\to\mathbb{Z}_2$; returns $f$, closed-form
   dual $\tilde f$ (Lemma 4), $\pi$, $g$, $\pi^{-1}$.
4. `walsh_flatness_check(f, n)` — validates $|\hat f(w)|=2^{-n/2}$ to
   machine precision, and reconstructs $\tilde f$ from
   $2^{n/2}\hat f = (-1)^{\tilde f}$.
5. `hadamard_all`, `apply_phase_oracle` — statevector primitives.
6. `algorithm_A1(f, fe, n, s)` — literal transcription of Rötteler's
   6-step $A_1$ circuit as a numpy statevector; returns
   $(\arg\max_x |\psi(x)|^2, |\psi(s)|^2)$.
7. `algorithm_A2_one_sample(f, n, s)` — one HSP measurement round;
   samples uniformly from the proven dual coset
   $\{a:b_0\oplus\langle s,a_{\mathrm{rest}}\rangle=0\}$.
   `verify_A2_statevector` additionally simulates the quantum-function
   hiding step directly for auditability (see failure_analysis.md).
8. `algorithm_A2(f, n, s, num_queries)` — takes $O(n)$ samples, builds
   a GF(2) linear system $A\!\cdot\!s=b_0$ and Gaussian-eliminates.
9. `classical_shift_finder_ml`, `classical_min_T_to_identify`,
   `classical_distinguish_shift_vs_random` — three classical baselines
   to probe (and explicitly caveat) Theorem 8.

## Deliverables (all under this directory)
- `paper.pdf`
- `extraction/marker.md` + `extraction/nougat.mmd` + `extraction/README.md`
- `work/paper.pdf` (mirror), `work/paper.txt` (pdftotext)
- `report/REPORT.tex` (compile-optional: `pdflatex` present on host but
  not required to reproduce the raw numbers)
- `report/open_questions.json`
- `report/workflow.md` (this file)
- `report/artifacts_summary.md`
- `report/failure_analysis.md`
- `report/evidence/rotteler_replication.py` (single-file, self-contained)
- `report/evidence/results.json` (headline numbers)
- `report/evidence/scaling.json` (classical-vs-quantum queries by n)
- `report/evidence/run.log` (verbatim tee of the final run)
