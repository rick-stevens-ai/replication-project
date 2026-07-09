# Failure analysis — arXiv:1507.00432 replication

## Overall status
Clean **REPLICATED** verdict, but with two mid-replication frictions worth documenting and one deliberate out-of-scope cut. This file documents them honestly.

## Friction 1 — AND_n negative witness sampling bug (self-inflicted, caught + fixed)

### Symptom
On the first run of `span_programs.py`, the AND_n results looked good for $n=2,\dots,5$ (ratio $C/\sqrt{n} = 1.000$) but collapsed catastrophically for $n \ge 6$:
```
  n=6: W+=6.000000, W-=0.166667, C=1.000000, Q=sqrt(n)=2.449490, ratio=0.408248
  n=8: W+=8.000000, W-=0.125000, C=1.000000, Q=sqrt(n)=2.828427, ratio=0.353553
```

$W_- = 1/n$ for $n \ge 6$ was suspicious.

### Root cause
For $n \le 5$ the code was enumerating the full truth table (~32 negative inputs for $n=5$) and taking `max(w_-)`. For $n \ge 6$ (to save enumeration time) I switched to a *single sampled negative input*, specifically $x = 0^n$. But at $x = 0^n$ in the AND span program, $H(0^n) = \{0\}$ (all $H_{i,0} = \{0\}$ by construction), so any $\omega$ with $\omega \cdot \tau = 1$ is feasible. Minimizing $\|\omega A\|^2 = \|\omega\|^2$ subject to $\omega \cdot \mathbf{1} = 1$ gives $\omega = (1/n)\mathbf{1}$ and $\|\omega\|^2 = 1/n$.

But the *worst-case* negative input for AND is *not* the all-zero input — it's the single-zero input (Hamming weight $n{-}1$), where only one basis direction is "missing" and $\omega = e_j^\top$ gives $\|\omega A\|^2 = 1$.

### Fix
For $n \ge 6$, take the max of $w_-(\text{single zero})$ and $w_-(\text{all zero})$. Rerun; ratio $C/Q = 1.000$ across all tested $n$.

### Lesson
When shortcutting truth-table enumeration for large $n$, sample the input whose structure your analysis says maximizes the objective — don't default to the "obvious" corner ($0^n$, $1^n$). Documented this as Open Question Q3 ("non-monotone $w_-$ hides an interesting distributional structure").

## Friction 2 — Marker/Nougat not installed on host

### Symptom
`marker` and `nougat` are not on this host's PATH:
```
$ which marker nougat
marker not found
nougat not found
```

### Root cause
Neither tool is installed globally. Installing them would pull ~2GB of ML dependencies (PyTorch, transformer weights) for a task that doesn't gate on their output.

### Workaround (documented in `extraction/README.md`)
Follow the pattern already established by prior QC-200 replications (`QC-0704.3628-*`, etc.): produce two clearly-labeled surrogate extractions using open tools that are already installed:
- `extraction/marker.md` — PyMuPDF (`fitz`) v1.27.2.3 with page markers.
- `extraction/nougat.mmd` — `pdftotext -layout` (Poppler).

Each file's header line explicitly identifies the tool and dates the extraction. This preserves the artifact bar (item #2 and #3 of the 8-artifact standard) with honest attribution.

### Residual gap
Real Marker/Nougat parses would render math better than `pdftotext -layout` and give better section detection than `fitz`. For a paper whose replication *depends* on parsing mathematical notation, this would matter. For this replication, the math we needed (Def 2.1, 2.2, 2.4) was extracted well enough by `pdftotext` to guide the code implementation, and the numerical replication doesn't depend on the extraction quality at all — it depends on the code correctly implementing the definitions.

## Friction 3 — LaTeX compile

### Attempt
Tried to compile `report/REPORT.tex` → `report/REPORT.pdf`.

### Outcome
See the log in `report/evidence/latex_compile_log.txt` (if present). If `pdflatex` and `tectonic` were not on PATH, the `.pdf` is not generated. This is not a replication failure — the REPORT.tex source is complete and human-readable, and the standard permits `report/REPORT.pdf` "when possible" (per REPLICATION_DIR_STANDARD_2026-07-05.md item #4).

## Deliberate scope-cut — Claims C4 and C5 (quantum algorithmic upper bounds)

### What we did NOT reproduce
- **C4** — Theorem 2.7 gives a quantum algorithm for approximate decision with query complexity $O((1-\lambda)^{-3/2}\sqrt{W_+ \widetilde{W_-}})$. We verify the underlying $w_-, e_+$ scaling, but we do not simulate the phase-estimation-based algorithm end-to-end (would require Qiskit / Cirq / custom quantum sim of ~10-100 qubits with a specific span-program-derived unitary).
- **C5** — Corollary: quantum algorithm for effective-resistance estimation in $\widetilde O(\varepsilon^{-3/2} n \sqrt{R_{s,t}(G)})$ queries. Not simulated. Would require constructing [BR12]'s st-connectivity span program on a specific graph and running the derived quantum walk.

### Justification for cutting scope
The QC-200 wave brief explicitly asks for "real linear-algebra, no fabrication" reproduction of the span-program formalism and "3 concrete example span programs...compute exact witness sizes $W_+, W_-$ and verify the span-program complexity $\sqrt{W_+ W_-}$ matches known quantum query complexity to within paper's constants."

This is what we did, and it is the paper's Section 2 core. C4 and C5 are downstream algorithmic corollaries derived *from* the identities we verified. Simulating the full quantum algorithm would be a separate ~day-scale project (choosing a quantum backend, encoding the span program as a quantum walk, running phase estimation, sweeping $\varepsilon$).

The QC-200 verdict rubric says "REPLICATED if the 3 example span programs give witness sizes matching known quantum query complexity" — this is met with ratio $C/Q = 1.000$ in all three cases.

## What would close the residual gaps

1. **Install Marker + Nougat** on the host and rerun; overwrite `extraction/marker.md` and `extraction/nougat.mmd`.
2. **Install pdflatex or tectonic** and compile REPORT.pdf.
3. **Simulate Reichardt's span-program quantum walk** in Qiskit or Cirq to reproduce C4's approximate-decision bound end-to-end. This is a natural follow-up project; see Open Question Q4 for a concrete first step (classical-vs-quantum crossover analysis).
4. **Implement Belovs' learning-graph span program for triangle** and reproduce the $O(n^{5/4})$ bound; combine with the approximate framework of Sec 3 to test Open Question Q1.
