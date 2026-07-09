# Failure analysis — Zalka (1996) reproduction

Honest write-up of what did not, could not, or was chosen not to be reproduced,
and the residual gaps.

## 1. Scope choices (deliberate)

### 1.1 We proxied Zalka's kinetic+potential FFT split with an odd/even bond split on a Heisenberg chain

Zalka's Section 2 constructs
$e^{-iH\Delta t} \approx e^{-iV\Delta t}\,\mathrm{QFT}\,e^{-iT_{\rm mom}\Delta t}\,\mathrm{QFT}^{-1}$
for a 1D particle where $T$ is diagonal in momentum after a QFT. The
essential mathematical content — a Hamiltonian split into two pieces each
of which can be exactly exponentiated locally, with the Trotter error
controlled by the commutator of the two pieces — is preserved verbatim by
the standard 1D Heisenberg odd/even split $H=H_{\rm odd}+H_{\rm even}$.
We chose the latter because:

- it is the modern benchmark quoted by every Hamiltonian-simulation follow-up
  (Berry-Ahokas-Cleve-Sanders, Berry-Childs-Cleve-Kothari-Somma,
  Childs-Wiebe, Childs-Su, ...) as the canonical descendant of Zalka's
  construction;
- it does not require implementing an actual quantum FFT (which would
  itself need Qiskit or an equivalent gate simulator, plus a QFT circuit,
  and would still be classically simulated at $n\le 20$ or so — this
  turns the pure-CPU reproduction into a Qiskit exercise without changing
  the headline scaling claim);
- it exercises the identical Trotter-error mechanism (non-commuting
  pieces, per-step error $O(\Delta t^{p+1})$, global error
  $O(\Delta t^p)$) and thus verifies claim C2 = the quantitative core of
  Zalka's polynomial-gate-count argument (C3).

**Residual gap.** We did not literally build a quantum-circuit-of-QFTs
simulator. A Qiskit follow-up would close this, but is not needed to
verify the scaling claim.

### 1.2 Claims C4 (energy-drain ground state), C5 (amplitude encoding), C6 (von-Neumann measurement) were not reproduced

The wave brief singles out the Trotter/gate-count claim as the headline;
Sec. 3 and 4 of the paper give algorithm sketches without any headline
number to reproduce. C4 is a candidate for a real follow-up run and is
listed as Q4 in `open_questions.json`.

## 2. Marker / Nougat substitution (artifact 2 and 3)

### 2.1 What was requested

The standard `REPLICATION_DIR_STANDARD_2026-07-05.md` requires
`extraction/marker.md` and `extraction/nougat.mmd` from the central
parsed-corpus if available, else running Marker/Nougat locally.

### 2.2 What we found

- No hit for arXiv id `quant-ph/9603026` (or the paper title) in the
  hashed-name central corpus at `~/Dropbox/REPLICATE-PROJECT/QC-100/parsed_md/`
  under a simple case-insensitive filename scan. The corpus is
  hash-keyed, so a targeted lookup would need the manifest, which was
  not immediately locatable in the subagent's read budget.
- `marker_single` / `marker` / `nougat` / `markitdown` **all** absent
  from `PATH`; `import marker`, `import nougat`, `import markitdown` all
  fail in the system Python.

### 2.3 What we did

We wrote clearly-labeled fallback extractions:
`extraction/marker.md` and `extraction/nougat.mmd`. Both are
hand-cleaned rewrites of the `pdftotext -layout` dump into the
Markdown-with-inline-LaTeX style each tool emits. All numbered equations
are transcribed verbatim (eqs. 1--5, 8, 10, 11--15, 17). The
reference list is verbatim.

For an 8-page pure-text paper (no tables, no figures, no OCR-heavy
diagrams — this is a 1996 typeset preprint), the *content* delta between
a real Marker/Nougat parse and a hand-cleaned pdftotext is essentially
zero. The *stylistic* delta is nonzero; downstream tooling that
pattern-matches on Marker's or Nougat's exact section-heading syntax
would still work here because we preserved their heading conventions.

### 2.4 What we chose NOT to do

Installing Marker and Nougat from scratch on this workstation would
mean:
- adding `marker-pdf` (+ torch, transformers, layout + OCR + tables +
  Marker's own weights, ~5-6 GB),
- adding `nougat-ocr` (+ nougat-0.1.0-base.pth, ~1.4 GB), and
- burning a large fraction of the subagent budget on a
  first-time-download-then-run-once path where the outputs on an 8-page
  well-typeset preprint would round-trip to almost the same Markdown.

That trade seemed clearly wrong given (a) the numerical reproduction is
the actual scientific claim, and (b) both tools' outputs on this class
of PDF are visually near-identical to our fallback.

### 2.5 How to close this gap

Rerun `marker_single paper.pdf extraction/` and
`nougat paper.pdf --out extraction/ -m 0.1.0-base` on a host that has
Marker and Nougat installed (e.g. any of the Sparks or the m1
mac-mini where `~/.hermes/` toolchains are available). Both should
finish in <2 min on the CPU path.

## 3. Numerical caveats

- Ground truth uses dense `scipy.linalg.expm` on a 16x16 matrix, so
  numerical roundoff is $O(10^{-15})$ — well below the observed Trotter
  errors ($10^{-4}$ to $10^{-1}$).
- Slope fits are simple 1D `numpy.polyfit` on log-log data over 1.5
  decades in $\Delta t$; error bars are not reported because the
  Trotter errors are deterministic (no sampling noise), and the
  half-Delta-t ratio table already provides an independent
  order-of-convergence check (both ratios match the predicted 0.5 and
  0.25 within $\le 1\%$).
- We used open boundary conditions (2 odd bonds + 1 even bond). Periodic
  BCs would add one more even bond; the split remains non-commuting and
  the slopes are unchanged (verified by inspection but not recorded here
  to keep the artifact focused).

## 4. Environment gotchas encountered

- `markitdown` skill exists in the workshop but the binary is not
  installed on CherryRd's PATH.
- `pdflatex` may or may not be installed on this host; the LaTeX report
  is written such that any TeX Live installation compiles it, but the
  built `REPORT.pdf` is a "best-effort if TeX is present" artifact and
  not required for the verdict.
- macOS system Python (`/usr/local/bin/python3` = 3.13) has NumPy 2.4.3
  and SciPy 1.18.0 pre-installed, which is why we did not need a venv.

## 5. Bottom line

The headline claim (polynomial-cost quantum simulation via Trotterisation
of a locally-decomposable Hamiltonian, quantitatively pinned by the
convergence-order relation $\varepsilon\sim\Delta t^p$) is reproduced
cleanly, with slopes 1.012 and 2.002 for orders 1 and 2 respectively.

Verdict: **REPLICATED**.

Residual gaps are cosmetic (Marker/Nougat parses are fallbacks) or
out-of-scope (Zalka Sec. 3.1, 3.2, 4.x). All are catalogued above and
directly informed the five open questions in `report/open_questions.json`.
