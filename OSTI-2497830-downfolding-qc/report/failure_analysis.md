# Failure Analysis — OSTI-2497830-downfolding-qc

Honest, self-critical audit of what this replication did **not** exercise, and why the verdict is legitimately PARTIAL rather than REPLICATED. This file is deliberately blunt.

## 1. What the paper actually claims

Alvertis, Khan, and Tubman (PRApplied 23:044028, 2025) make a three-material, two-step methodological claim:

1. **Ab-initio downfolding** (Wannier90 + cRPA) produces small, material-specific extended-Hubbard Hamiltonians that faithfully retain the low-energy physics of Ca$_2$CuO$_3$ (20 qubits), WTe$_2$ (32 qubits), and SrVO$_3$ (54 qubits).
2. **Tensor-network VQE** on these downfolded Hamiltonians produces energies and observables that agree with DMRG references (fidelities 99.3% / 96.2% / 31.8% respectively).

The unit of the paper is the joint demonstration across the three materials. A single-material reproduction is one third of the claim.

## 2. What this replication actually exercised

- **Independent from-scratch ED** of the Ca$_2$CuO$_3$ 10-site 1-band extended Hubbard using the paper's own Appendix C.1 parameters ($t=-0.491$, $U=3.578$, $V=0.903$ eV). Ground-state energy matched the paper's DMRG value 6.005 eV to $\sim 0.1$ meV. Fig 3b antiferromagnetic spin-correlation function reproduced in sign pattern.
- **Reduced-scale SrVO$_3$ sanity check** at 2×2 single-band. Not a reproduction of the paper's 3×3 3-band CDW; the reduced geometry forces $\Phi = 0$ by A/B sublattice symmetry.
- **Arithmetic cross-check** of Table II: $0.999^{290} = 0.7476 \approx 74.8\%$. Consistent.
- **LLM-judge verdict** (`argo:gpt-5.2`): PARTIAL.

## 3. What this replication did NOT exercise (and why it matters)

### 3.1 The full three-material demonstration
Only one of the three materials was reproduced at paper scale. The paper's argument stands on the diversity of the three cases (quasi-1D cuprate + excitonic insulator + correlated metal). Reproducing Ca$_2$CuO$_3$ alone confirms one point in that space; it does not confirm generalisation.

### 3.2 The VQE stack itself
The centerpiece method of the paper is the Khan–Clark–Tubman MPS-VQE with number-preserving and excitation-preserving ansätze. We reproduced the paper's DMRG denominator (via ED, which is exact and $\ge$ DMRG at any bond dimension), not the VQE numerator. The paper's headline VQE fidelities (99.3% / 96.2% / 31.8%) and the observation that fidelity degrades with correlation strength are **untested here**.

Consequence: this replication cannot say whether the VQE ansatz genuinely captures the physics or whether the fidelities are artifacts of chi=512 truncation. That gap is captured as Open Question #1.

### 3.3 The DFT→Wannier→cRPA→downfolded-H pipeline
We consumed the paper's Appendix C matrices as ground truth. Rebuilding the pipeline (Quantum ESPRESSO PBE run + Wannier90 projections + RESPACK / wan2respack cRPA) would be days of compute and was skipped. Any systematic in the paper's downfolding — cRPA window choice, active-orbital selection, projection convention — remains **untested**. This is Open Question #2.

### 3.4 No quantum hardware
The paper is a classical-simulation-of-quantum-algorithm paper (MPS-VQE); no real superconducting or trapped-ion hardware execution was performed by the authors, and none was performed here. The Table II fault-tolerant resource estimates ($\|H\|_1$, T-gate counts) are compiled from theory; whether the reported 74.8% ideal-model circuit fidelity actually predicts achievable ground-state accuracy on IBM Eagle/Heron or Quantinuum H2 is **untested** by both parties. Open Question #4.

### 3.5 No comparison against a non-downfolded reference
The internal ED-vs-DMRG agreement at 0.1 meV validates the compressed model against itself. It does NOT prove that the compressed model matches a non-active-space reference (AFQMC, full-basis DMRG, exact CI on a modest basis). If the compression itself is lossy at, say, 50 meV per Cu site, that error is invisible to this replication. Open Question #3.

### 3.6 No stress test outside the paper's chosen regime
All three of the paper's materials are near-insulating or moderately correlated. The workflow's behaviour in genuinely critical regimes (underdoped cuprate stripes, magic-angle twisted bilayer graphene, Kondo lattices) — where required MPS bond dimension can scale as $\chi \sim \exp(L)$ — is **untested**. Open Question #5.

### 3.7 No T-gate / resource-estimate audit beyond one arithmetic check
Table II reports T-counts, $\|H\|_1$, and $n_{2q,G}$ for each material. We spot-checked one arithmetic identity. The rest of the resource-estimate machinery (Hamiltonian block-encoding cost, T-gate compilation from arbitrary rotation gates, LCU coefficient estimation) was **not audited**. In particular, the C9 discrepancy ($\|H\|_1$ nearest-neighbour contribution $\approx$ 48.5 eV vs.\ paper's reported 267 eV) suggests long-range Wannier tails not tabulated in Appendix C.1 — consistent, but not verified.

## 4. Why the verdict is PARTIAL, not REPLICATED

**REPLICATED** would require independent reproduction of *all three* headline material demonstrations (Ca$_2$CuO$_3$ + WTe$_2$ + SrVO$_3$) at the paper's lattice size and band count, with matching DMRG and VQE energies + observables. That is out of reach of a 15-minute laptop replication.

**PARTIAL** honestly captures what was achieved: one of three material demonstrations reproduced at essentially machine precision on an independent code path, with the reproduced part being the paper's simplest and most publicly-verifiable case. This is a nontrivial confirmation of the paper's data-availability claim (Appendix C matrices are self-consistent and correct) and its DMRG-denominator claim for Ca$_2$CuO$_3$; it is not a confirmation of the paper's methodological breadth or its VQE ansatz's fidelity.

## 5. What would move the verdict

- **PARTIAL → REPLICATED**: reproduce WTe$_2$ ($E_0 = 115.029$ eV, $\Delta_{\text{exc}} = 0.640$) and SrVO$_3$ ($E_0 = -105.383$ eV, $\Phi = 0.12$) via ITensor DMRG on the downfolded Hamiltonians. Rough effort: 1–2 weeks and access to a moderate-memory workstation (256 GB) for the 54-qubit SrVO$_3$ DMRG.
- **REPLICATED → REPLICATED-EXTENDED**: rebuild the DFT→Wannier→cRPA pipeline from scratch, verify Appendix C matrices are what you get from the reported inputs. Effort: several weeks + a compute cluster.

## 6. Meta-note on this backfill (2026-07-06)

The backfill added LaTeX + JSON reporting artifacts to a REPORT.md that already made an honest PARTIAL case. No numerical claim in the original REPORT.md was changed; no additional simulation was run. The verdict is preserved at PARTIAL. If any of the open questions above become tractable on future compute, they should be executed as separate replications, not appended to this dir.
