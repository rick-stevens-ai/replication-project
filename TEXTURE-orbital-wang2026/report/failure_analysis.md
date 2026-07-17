# Failure Analysis — wang2026 (arXiv:2607.15228)

**Verdict:** PARTIAL. Two categories of gap: (A) one quantitative discrepancy in
a reproduced claim (spin-wave bandwidth), and (B) two claims out of self-contained
scope (C1/C2).

---

## A. The spin-wave bandwidth factor-~2 discrepancy (C5)

**Symptom:** reproduced LSWT bandwidth = **172.9 meV** vs paper's **~80 meV**,
a ratio of **2.16**.

**What is NOT wrong:** the spectrum *shape* is correct —
- two branches (acoustic + optical): MATCH
- acoustic branch softens to ~0.02 meV at Q=(0.509π,0.509π): MATCH
- optical branch spans ~164-173 meV (nearly flat), acoustic 0-19 meV.

Only the absolute energy scale is off, and by a factor ~2. That pattern is the
fingerprint of a **spin-normalization / Holstein-Primakoff convention** issue,
not a modelling error.

**Root-cause hypothesis (most likely):**
- In a Heisenberg model H = Σ J S_i·S_j, LSWT magnon energies carry a prefactor
  ~2S from the Holstein-Primakoff bosonization (E_magnon ~ 2 S J × structure factor).
- The paper reports couplings as **J·S products** (J_perpS=75, J1S=1.9, J3S=4.6,
  J1'S=1.38 meV). Our reproduce.py treats these J*S values directly as J (S=1
  absorbed), giving magnon energies ~ 2 × (J*S) — i.e. an extra factor of 2.
- To land at ~80 meV, the stated J*S values most plausibly must be interpreted as
  **already including the spin factor** in the magnon energy (E ~ J·S, not 2·J·S),
  or equivalently a factor-of-2 must be absorbed in the LSWT Hamiltonian
  definition (single- vs double-counting of bonds in Σ_{<ij>}).

**Why 2.16 and not exactly 2.0:** the optical branch is not perfectly flat
(164-173 meV), and "bandwidth" definition (top-of-optical vs optical-minus-acoustic
span) introduces a few-percent ambiguity. The dominant factor is 2×; the residual
0.16 is definitional/branch-dispersion.

**Resolution path:** obtain the exact LSWT Hamiltonian normalization from the
paper's Supplemental Material (the "approach detailed in the SM" cited alongside
the J*S values). That single convention (S vs 2S prefactor) determines the scale.
Re-running reproduce.py under the J*S-already-includes-spin interpretation is
expected to converge to ~80 meV. This is the diagnostic finding of the
reproduction, logged as Open Question Q1.

**Impact classification:** convention gap, not physics failure. The claim's
qualitative content (branch structure + softening) reproduces; the absolute
number does not, pending the SM normalization.

---

## B. Out-of-scope claims C1/C2 (correlated backbone)

**C1** — orbital-selective bad-metal/OSMP regime with Z_x >> Z_z.
**C2** — effective spin model = superexchange + RKKY (J^r(q) = -j_xz^2 χ(q)).

**Why not attempted:** both require the **DFT-derived tight-binding hoppings
t^{ab}_{il,jl'} and crystal-field levels ε_α of Ref[49]** (Liao et al., PRB 114,
045112). These are explicitly stated in the paper to be "taken from Ref. 49" and
are **not tabulated in wang2026 itself**. Without them:
- the slave-spin mean field has no bare Hamiltonian to renormalize → no Z_alpha(U);
- the Lindhard susceptibility χ(q) cannot be computed → no RKKY J1^r, J3^r;
- only the *downstream* consequences (given the paper's reported J values) are
  reproducible — which is exactly what C3/C4/C5 test.

**What a full reproduction needs:**
1. Import the Ref[49] bilayer two-orbital e_g TB parameters + crystal fields.
2. Implement the Yu-Si slave-spin solver (refs [66,67]) → Z_alpha(U), λ_alpha(U).
3. Build renormalized H_eff (t̃ = √(Z_α Z_β) t), diagonalize on a dense k-mesh.
4. Compute Lindhard χ_{ab;cd}(q;U), project to d_x2-y2, form even/odd channels.
5. FT the RKKY J^r_ll'(R) = -Σ_q e^{iq·R} j_xz^2 Re χ_ll'(q); confirm J3^r/J1^r>1
   peaking near U~4 eV.
6. Feed the derived J values into the C3/C4/C5 pipeline already implemented.

**Effort:** still CPU-bound, hours-scale, no GPU — but blocked on the external
Ref[49] hopping table, so it was correctly scoped out of this self-contained pass.

---

## Summary
| Gap | Type | Blocker | Status |
|---|---|---|---|
| C5 bandwidth 172.9 vs ~80 meV | quantitative (2.16x) | LSWT S vs 2S convention | diagnosed; needs SM normalization (Q1) |
| C1 slave-spin Z_alpha(U) | out of scope | Ref[49] DFT hoppings | not attempted (Q2) |
| C2 RKKY χ(q) derivation | out of scope | Ref[49] DFT hoppings | not attempted (Q2) |

The magnetic order, frustration mechanism, and spin-wave topology reproduce;
the absolute spin-wave energy scale and the correlated origin of the J values
do not (convention + external-dependency, respectively). Hence **PARTIAL**.
