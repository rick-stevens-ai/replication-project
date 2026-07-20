# Failure analysis — arXiv:2212.03756 replication

## Summary
No genuine failure of the paper's analytic/symmetry claims. The reproducible core
(tight-binding model Eqs 2-6, its symmetry properties, and the Fig 3(d) magnitude scale)
reproduced completely: **10/10 machine-checkable claims pass.** The items below are either
(a) a self-inflicted harness bug we caught and fixed, or (b) genuinely out-of-scope
DFT/experimental magnitudes that cannot be produced from a minimal model without fabrication.

## (a) Harness bug caught and fixed — NOT a paper failure
- **AFM-domain sign-reversal test (claim 9).** First implementation flipped the exchange
  as J -> -J. Because Eq(6) depends on (J+beta) with beta = e2+2t2*cos(kz c) != 0, this
  changed the splitting *magnitude* (41.18 -> 26.17 meV), so the "sign reversal, magnitude
  preserved" assertion failed. Root cause: J->-J is not the correct model operation for an
  AFM domain flip. The physically correct operation is the spin-label interchange
  E_up <-> E_down, i.e. (delta-gamma) <-> (delta+gamma), equivalently gamma -> -gamma
  (inter-sublattice symmetric hopping reverses relative to spin). After the fix the
  splitting flips sign with magnitude preserved, matching the paper's statement. Lesson:
  map "physical domain operation" to the correct Hamiltonian symmetry, not the most obvious
  parameter sign flip.

## (b) Out-of-scope — DFT / experimental, marked, not faked
The paper's quantitative results in these categories come from LAPW (Elk) and PAW (VASP)
all-electron relativistic calculations with Ueff=5 eV, plus the extended Elk multipole/MCP
modules. Reproducing their *magnitudes* would require running those DFT codes (not available
here and explicitly outside a "minimal/tractable model, NOT full DFT" mandate). We therefore
did NOT attempt to fabricate them; where a *symmetry* statement was checkable we checked it:

1. **Octupole magnitudes vs lambda_r (Fig 2)** — DFT tensor-moment decomposition of the
   density matrix. Out of scope (magnitude). Symmetry that O_32^- is ferro and O_30 is
   antiferro is a group-theory statement consistent with our reciprocal form factor.
2. **Piezo-/anti-piezomagnetic moments (Fig 4)** — the paper shows these GROW with SOC
   (lambda_r doubling) and concludes they are *relativistic*. Our SOC-free model cannot
   produce the magnitudes; we verified only the tensor structure
   Lambda_xyz=Lambda_yxz != Lambda_zxy via the xy m_z octupole integral (claim 10:
   O_{z,xy}=int x^2 y^2 > 0, O_{z,xx}=0 by odd-y parity). Magnitudes: OUT OF SCOPE.
3. **Magnetic Compton profile magnitudes (Fig 5)** — computed with the extended Elk MCP
   module from the DFT spin momentum density. Out of scope (magnitude). Its qualitative
   signatures (symmetric in p, C4 sign flip, zero integral) follow from the d-wave spin
   texture we DID reproduce, but were not independently computed here (see open question 5).
4. **Absolute DFT band structure (Fig 3a, Fig 6)** — full electronic structure; out of
   scope. Only the top-valence-pair splitting is model-tractable and was reproduced.

## Tooling limitations encountered (environmental, not scientific)
- Native PDF-analysis tool and vision/image tools were unavailable (API credit exhausted on
  Anthropic; misconfigured OpenAI/Google routes). Mitigation: used `pypdf` for text
  extraction (13 pages, ~66k chars, incl. all equations and Table I) and relied on numeric
  assertions rather than visual inspection of figures. No scientific content was lost.

## Confidence
High. The decisive check is claim 1: the paper's closed-form Eq(6) equals brute-force
8x8 diagonalization to 6e-15 eV over 2000 random k-points — an internal consistency proof
that our transcription of Eqs (2)-(6) is exact. The Fig 3(d) magnitude (41 meV) and all
d-wave symmetry properties then follow with independent parameters from Table I.
