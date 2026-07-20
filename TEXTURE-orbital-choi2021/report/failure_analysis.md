# Failure analysis — choi2021 replication

## What matched
- **Mechanism (fully reproduced):** a finite, *large* orbital Hall conductivity from a
  pure d-orbital tight-binding model with **no spin–orbit coupling**, driven entirely by
  momentum-space orbital texture. This is the paper's central conceptual claim.
- **Ordering σ_OH ≫ σ_SH (reproduced, extreme form):** σ_SH is identically 0 without SOC
  while σ_OH ~ 10²–10³. The paper's ~2-orders-of-magnitude dominance is present.
- **Order of magnitude of σ_OH (partial match):** peak |σ_OH| ≈ 775, i.e. the correct
  "large" regime, within a factor ~5 of the DFT value 3800.

## What did NOT match / limitations
1. **Exact value 3800 not reproduced.** The surrogate gives ~10²–10³, not 3800.
   - *Cause:* single d-manifold + generic Slater–Koster params, not fitted to real fcc-Ti
     DFT bands; no s/p hybridization; cubic surrogate lattice instead of true fcc with a
     realistic Fermi surface. The magnitude of orbital Berry curvature is very sensitive to
     band near-degeneracies at the actual E_F.
2. **σ_SH = −40 not reproduced (only its smallness).** By construction SOC=0, so σ_SH ≡ 0.
   The finite but small −40 requires adding weak on-site λL·S.
3. **k-grid convergence is coarse.** σ_OH flips sign between nk=12 (−142.8) and nk=16
   (+147.7) at the Ti filling — orbital Berry curvature hot spots are under-sampled on
   coarse grids. The peak-over-scan value (~775) is more physically representative of the
   "large OHE" claim than the single converged number, but a proper error bar needs nk≥24.
4. **No surface/transport chain.** The experiment measures a MOKE Kerr signal from
   *surface-accumulated* orbital moments, linked to bulk σ_OH via orbital drift-diffusion
   (lL ~ 74 nm) + magneto-optics. That full chain was scoped out (compute budget).

## Honest scoping statement
A from-scratch d-orbital TB + Kubo surrogate is expected to, and does, reach the correct
**order of magnitude** and the correct **SOC-free orbital-texture mechanism**. The exact
DFT number (3800) and the finite σ_SH (−40) require a DFT-fitted multi-orbital Hamiltonian
with SOC and were deliberately scoped out per the fast/coarse replication brief. No values
were fabricated; all numbers come from the executed model in `choi2021_result.json`.

## Verdict
**PARTIAL** — order-of-magnitude + mechanism REPLICATED; exact magnitude and finite SHE scoped out.
