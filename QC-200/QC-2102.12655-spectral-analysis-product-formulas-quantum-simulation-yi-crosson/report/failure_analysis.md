# Failure analysis / friction / residual gaps

## What we did NOT reproduce, and why

### 1. QPE step-size improvement (Theorem 1: ε → √ε)
The paper's headline analytical claim is that for real-matrix-element
Hamiltonians the QPE Trotter step to reach precision ε improves from
~ε to ~√ε (a quadratic improvement in gate count). This is an
**asymptotic scaling** claim proved via effective-Hamiltonian
perturbation theory. Directly demonstrating it in a small-n
end-to-end QPE simulation is possible but requires a much larger
apparatus (ancilla register, phase-kickback circuit, sweep of the
precision target ε across a few orders of magnitude). At n=4..6 the
finite-dimensional overhead terms swamp the asymptotic scaling, so
we did not attempt it in this pass. Classified as *analytical, not
tested* rather than "replicated" or "failed."

### 2. DAS Trotter improvement (Theorem 3: M⁻¹ → M⁻²)
Same class as above — an asymptotic claim in the total gate count M
for digital adiabatic simulation. Reproducing it needs a full
Trotterized adiabatic sweep with schedule fitting and separation of
Trotter error from adiabatic error via extrapolation. Explicitly
called out as "not attempted" in the claims table (C6).

### 3. QAOA ↔ diabatic-annealing similarity
An interpretive/case-study claim (C7). Requires running QAOA + a
digitized annealer on a common problem instance and comparing their
error profiles. Out of scope for a one-hour replication of the
foundational scaling laws.

## Friction / adaptations
- **Marker + Nougat not installed on this host.** The brief allows
  pulling from the central corpus if pre-parsed, else running the
  parsers locally. Neither `marker_pdf` nor `nougat` is on the CherryRd
  Python environment, and no pre-parsed 2102.12655 copy exists in the
  REPLICATE-PROJECT corpus. To keep the 8-artifact contract honest, we
  produced fallback extractions from `pdftotext` and `pdftotext -layout`,
  each clearly banner-marked as "FALLBACK — parser not installed." A
  future pass on a Marker/Nougat-equipped host can drop in real parses.
- **numpy 2.4.3 quirks.** No issues in practice; `numpy.linalg.lstsq`
  needs `rcond=None` to suppress the deprecation warning — handled.
- **Suzuki-4 sign check.** The Yoshida recursion uses
  s = 1/(4 - 4^{1/3}) ≈ 0.4145 and a central weight (1 - 4s) ≈ -0.6579,
  which is negative — reverse-time evolution. Not a bug; correct
  Suzuki construction. We double-checked by verifying the slope came
  out to 4 in op-norm.

## Residual gaps
| Gap | Impact | Cheapest fix |
|---|---|---|
| No Marker/Nougat parses | Downstream tools that consume mmd/marker markdown lose ~5% of the paper's math typography fidelity. | `pip install marker-pdf nougat-ocr` on a GPU box + re-run parse. |
| No QPE end-to-end sim | We couldn't numerically corroborate the ε→√ε claim. | Build a Qiskit QPE at n=4 (a day of work). |
| Single-model TFIM only | Universality of the ~3.1 op-bound/actual ratio (Open Question Q1) untested. | Add Heisenberg + Fermi-Hubbard sweeps to `trotter_scaling.py` (30 min). |

## Honest summary
The **foundational scaling** the paper builds on is cleanly and
crisply reproduced (slopes 1.03 / 2.04 / 3.98 vs. expected 1 / 2 / 4).
The paper's **central qualitative message** — that a state-fidelity
error measure on a specific initial eigenstate is a much tighter
Trotter error bound than the operator-norm bound — is directly
demonstrated by our factor-of-~29 gap between the op-norm bound and
the actual state infidelity at δt = 1/32 on TFIM n=6. The specific
asymptotic **theorems** (QPE ε→√ε, DAS M⁻¹→M⁻²) are analytical
statements we did not attempt to verify numerically; they are labeled
as such rather than misclassified.
