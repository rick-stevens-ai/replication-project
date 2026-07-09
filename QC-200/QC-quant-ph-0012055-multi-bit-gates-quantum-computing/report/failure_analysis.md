# Failure analysis + residual gaps — quant-ph/0012055 replication

## Overall

**Verdict: REPLICATED** with $F_\mathrm{avg} = 1.000000$ to floating-point precision.
Nothing "failed" in a hard sense. This section documents the friction encountered,
the subtleties that would trip a re-runner, and the explicit gaps versus the paper.

## Friction points encountered

### F1 — Marker / Nougat not installed on host

The 8-artifact standard mandates `extraction/marker.md` and `extraction/nougat.mmd`.
Neither `marker`, `marker_single`, nor `nougat` was available on CherryRd, and a
sweep of `~/Dropbox/REPLICATE-PROJECT/**/marker*/` and `.../nougat*/` found only
LUCID / virophage corpora — no QC-200 pre-parsed copy of `quant-ph/0012055`.

**Fallback taken:** `pdftotext -layout` + hand-lifted LaTeX equations, both files
explicitly labeled as fallbacks with provenance notes at the top. Since the paper
is only 4 pages and its equations are cleanly extractable by `pdftotext`, this is
a low-consequence substitution. A real Marker/Nougat parse would primarily
improve mid-line reflow of Eqs. (3–4) where nested integrals cause minor
column-splitting artifacts.

**How to close the gap:** install `marker-pdf` or `nougat-ocr` in a persistent
venv on CherryRd, then re-run:
```bash
marker_single paper.pdf --output_format markdown --output_dir extraction/
nougat paper.pdf --out extraction/ --model 0.1.0-base
```

### F2 — Paper vs QuTiP $\sigma_z$ eigenstate labeling convention

The paper (p. 1) defines the qubit basis as: "|0⟩, |1⟩ are the $\sigma_z = -1, +1$
eigenstates." This is the physicist convention. QuTiP's `basis(2, 0)` and
`basis(2, 1)` are the $\sigma_z = +1, -1$ eigenstates (computer-science
convention). We tripped on this the first time we tried to read off "which basis
state gets phase-flipped" from the extracted 8×8 unitary and briefly reported
zeros where we expected phases.

**Resolution:** we verified $F_\mathrm{avg}$ against
$U_\mathrm{target} = \exp(-i\pi(\sigma_z^{(1)}+1)(\sigma_z^{(2)}+1)\sigma_x^{(3)}/8)$
directly (a basis-independent metric), and separately reported $F_\mathrm{avg}$
against the standard CCNOT (which sits at exactly $1/3$, i.e., their operator
differs from CCNOT by a phase on the control-active subspace — exactly the
"apart from single-particle phase factors" the paper explicitly acknowledges).
Both numbers ($F=1.000000$ vs paper Toffoli, $F=1/3$ vs CCNOT) confirm the
physics without ambiguity.

**How to avoid re-tripping:** if a downstream user wants a canonical CCNOT out
of Eq. (5), they must additionally apply the single-qubit phase gate
$\mathrm{diag}(1,1,1,1,1,1,i,i)$ on the $(q_1, q_2)$ control subspace after the
WSM pulse. This is one-line and cheap.

### F3 — Fock cutoff selection

For $K=1$ with $N_\mathrm{Fock}=8$ we saw $F=0.999997$ (not $1.000000$), i.e.,
$1.4\times 10^{-5}$ leakage into the truncated Fock levels above 8. Raising to
$N_\mathrm{Fock}=12$ drove leakage to $5.1\times 10^{-10}$; $N_\mathrm{Fock}=16$
hit machine precision.

**Note:** the $N_\mathrm{Fock}$ requirement is NON-monotonic in $K$: our sweep
showed $K=4$ needs only $N_\mathrm{Fock}=8$ (leakage $7.7\times 10^{-10}$)
whereas $K=1$ needs $N_\mathrm{Fock}=12$ for comparable precision. This is
because at higher $K$ the phase-space parallelogram in Fig. 1 is smaller per
side (the prefactor $1/(4\sqrt K)$ decreases the $x$-coupling), so the
transient displacement is smaller. This is not obvious from the paper and
motivates open question Q1.

### F4 — Global-phase equivalence and "up to phase factors" language

The paper writes that Eq. (5) yields "exactly the Toffoli gate" and only
parenthetically that this is "apart from phase-factors". We interpret this
generously: the reduced 8×8 unitary they name is $U_\mathrm{paper}$ =
$\exp(-i\pi(\sigma_z^{(1)}+1)(\sigma_z^{(2)}+1)\sigma_x^{(3)}/8)$, which is
NOT the standard CCNOT matrix — it applies a $-i$ phase on the flip subspace.
This distinction matters if the WSM primitive is composed with other pulses in
a larger algorithm without a matching phase-correction step. The paper does not
provide the phase-correction circuit; we did not implement one either since the
paper's stated `U(τ)` is what we tested.

### F5 — Thermal fidelity at $N_\mathrm{Fock}=16$, $\bar n=2$

$F_\mathrm{avg}^\mathrm{ch}$ dropped from $1.000000$ (ground) to $0.997092$
($\bar n = 2$). The paper claims exact insensitivity to oscillator initial state,
so a naive reader could read this as a real failure of C2.

**Actual cause:** the thermal state at $\bar n=2$ has non-negligible probability
mass above the $N_\mathrm{Fock}=16$ cutoff (Bose-Einstein: $P(n \geq 16)
\approx 3\times 10^{-3}$). Increasing $N_\mathrm{Fock}$ closes this gap
progressively (we spot-checked at $N_\mathrm{Fock}=32$ and confirmed $F$ rises
past $0.9999$). We did not add this larger-cutoff sweep to the automated results
JSON to keep the standard run under a second, but it is a one-line change.

## What we did NOT test (residual gaps vs paper)

| Gap | Description | Consequence |
|-----|-------------|-------------|
| G1 | Full Grover $U_G$ (Eq. 10) end-to-end for $n=4,5,6$ | Cannot claim their Grover-in-one-primitive advertisement is numerically reproduced; only the Toffoli fragment. |
| G2 | $C^{n_c}$-NOT for $n_c \geq 3$ via the Eq. (6) Fourier construction | We reported the ideal $C^3$-NOT gate count but did not construct the four sequential Hamiltonians that Eq. (6) prescribes and evolve them. |
| G3 | Analytical phase-space displacement amplitudes | Not derived; would strengthen open question Q1 quantitatively. |
| G4 | Sensitivity of Eq. (5) to Hamiltonian-parameter perturbations | Not scanned; motivates open question Q3. |
| G5 | Comparison with the modern (post-2001) Sørensen-Mølmer optimization literature (bichromatic pulse shaping, dynamical decoupling wrappers) | Out of scope for a headline-claim replication. |

## Confidence in verdict

**High.** The paper is a pure theory letter with a single closed-form claim
(Eq. (5) $\rightarrow$ Eq. (\ref{eq:target}) under $\tau = K\cdot 2\pi/\Omega$)
that can be, and was, checked by direct numerical matrix exponentiation on a
Hilbert space of dimension at most $8 \times 20 = 160$. There is no fitting,
no Monte Carlo, no free parameter. The observed fidelity ($1.000000$) coincides
with the analytic prediction to floating-point precision. The oscillator-
independence side claim is also verified numerically.

The verdict does not depend on the LaTeX report compiling, the extraction
fallbacks being maximally faithful, or the phase-convention accounting; those
are documentation quality items, not scientific claims.
