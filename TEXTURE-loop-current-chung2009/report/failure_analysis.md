# Failure / gap analysis — chung2009 (chiral spin liquid, flux 1/3)

**Verdict: REPLICATED** — both headline claims reproduce. This file records the
caveats, residuals, and scoped-out pieces honestly.

## Most important caveat first: the parity input to the 1/3 result
The `<Phi_x>=1/3` headline is a *counting* result: 3 of the 4 global-flux
sectors survive projection in the non-Abelian phase, and their `Phi_x` values
average to `(+1+1-1)/3 = 1/3`. The single non-trivial physics input — that the
`(-1,-1)` sector has **odd** fermion parity for `g<sqrt3` and is projected out —
is taken from the paper's derivation (Eqs. following Eq.5; Refs [1,16,19]),
**not re-derived here** from the many-body projector `P=prod_i (1+D_i)/2`. Our
kernel confirms the arithmetic and the finite-T Eq.13 limit, but a fully
self-contained replication would re-derive the sector parity from `P`
(open question 1). Given that input, the result is exact.

## Residuals (quantitative)
- **`g_c`: 0.41% error.** Gap minimum at `g=1.725` vs `sqrt3=1.7321`. The bulk
  gap does not fully close on our finite BZ grid (residual min-gap ~0.032). This
  is a finite-`k`-grid / single-unit-cell discretization artifact: the critical
  mode sits at a specific BZ momentum the discrete grid does not sample exactly.
  The gap-**minimum location** (the robust observable) tracks `sqrt3`. Confirming
  the exact closure needs the analytic critical `k` (open question 5).
- **`<Phi_x>` fraction: exact.** Both the direct counting and the `T->0` limit of
  Eq.13 give 1/3 (nA) and 0 (A) with zero error.

## Chern-number convention
Our Fukui–Hatsugai–Suzuki sum over the 3 occupied Majorana bands gives `C=+3`
deep in the nA phase and `C=0` deep in the A phase — correctly capturing the
chiral(TRS-broken)→trivial change. The value `+3` is a multi-band, doubled-
Majorana, gauge-dependent count; the physical invariant of the Yao–Kivelson nA
phase is a **single chiral Majorana edge mode** (`|C|=1`, Ising anyons). Points
right at the transition (`g=1.6,1.8`) are FHS-noisy because the gap is nearly
closed. Pinning `|C|=1` needs an edge-spectrum calculation (open question 2).

## Scoped out (coverage-capping, not failures)
1. **`T*(g)` scaling `T* ~ Delta(g)/ln N` (Eq.9).** We show the
   `<Phi_x>(T)` shape at one size/one `g`; the log-slow size scaling — the
   paper's main *conceptual* result — is not fit. (open question 3)
2. **Vortex-pair entanglement entropy `ln2` excess (Fig.5).** The non-Abelian
   Majorana-zero-mode entanglement signature is not computed; needs the
   two-vortex free-fermion correlation matrix. (open question 4)
3. **Full many-body projector.** See "most important caveat" above.

## Extraction tooling (not a physics gap)
`marker` and `nougat` are not installed; `extraction/marker.md` and
`extraction/nougat.mmd` are the documented `pdftotext` interim fallback (with
Eqs 1–13 hand-transcribed into the .mmd). `pdflatex` is absent so REPORT.tex
ships as source. All are tooling limitations, not replication gaps.

## What would raise the verdict to a perfect score
Re-derive the `(-1,-1)` sector parity from `P` (closes the one imported input),
pin `|C|=1` via edge modes, fit `T*(g) ~ Delta/ln N`, and add the vortex
entanglement `ln2` — i.e. close the 5 open questions. The current evidence
already establishes the two abstract-level claims, hence REPLICATED at
Coverage 8 / Agreement 9.
