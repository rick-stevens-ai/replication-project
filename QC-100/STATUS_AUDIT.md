# QC-100 Replication — Status Audit

Owner: Ollie. Verdicts per AUDIT_PROTOCOL.md. Every result independently disk-verified (code re-run or numerics re-checked), not trusted from subagent self-report.

## Wave 1 (5 papers) — closed 2026-06-26

| # | Paper | Verdict | Cov/10 | Agr/10 | Notes |
|---|-------|---------|--------|--------|-------|
| 1 | Shor — Polynomial-Time Prime Factorization & Discrete Log (1997) | SPOT-CHECK | 5 | 9 | QFT order-finding factors N=15/21/35; P(recover r) 3–7.5× above φ(r)/3r bound. Re-run verified. §6 DL descoped. |
| 2 | Temme/Bravyi/Gambetta — Error mitigation (ZNE), PRL 2017 | PARTIAL | 6 | 9 | Density-matrix sim + Richardson/linear extrap; ~22× error reduction (linear). PEC + HW experiment out of scope. Subagent timed out; finished inline. |
| 3 | Peruzzo et al. — Variational eigenvalue solver (original VQE), NatComm 2014 | PARTIAL (algorithm REPLICATED) | 6 | 9 | UPDATED: subagent's PennyLane HeH+ version finished after 38min and SUPERSEDES my H2 inline fallback. Real HeH+ STO-3G, VQE=FCI <2e-6 mHa, R_eq 97.97pm vs paper 92.3pm, Nelder-Mead exact. Absolute-energy convention gap (paper's Supp Table 2 tapered H not in corpus). My H2 version kept as REPORT.ollie-h2-inline.md.bak. |
| 4 | Campbell — qDRIFT random compiler, PRL 2019 | REPLICATED | 8 | 9 | 1/N scaling + L-independence confirmed, all under 2λ²t²/N bound. Subagent did numerics (verified), timed out before writeup; report written from real results.json. |
| 5 | Costa/Jordan/Ostrander — Quantum algorithm for the wave equation, PRA 2019 | PARTIAL (REPLICATED core) | 7 | 10 | L=BBᵀ → Hamiltonian; matches analytic + leapfrog (E1 6.3e-4 … E4 2.0e-3), Q-factor 3.985 vs ~4. Independently re-run, all numbers match. Higher-order/Maxwell/Klein-Gordon untested. |

**Wave 1 tally (revised):** 1 REPLICATED, 3 PARTIAL, 1 SPOT-CHECK. 0 NO-GO, 0 CONTRADICTED.
All 5 are pure classical-simulator replications (no hardware, no paywall). Mean Agreement 9.4/10.
(VQE revised REPLICATED→PARTIAL when the subagent's superior HeH+ version landed late and replaced the H2 inline fallback — HeH+ is the paper's real molecule but the absolute-energy convention gap caps coverage.)

**Process note:** 3/5 subagents hit the Argo writeup timeout but completed the computation and left real artifacts (code/results/plots) on disk; salvaged by auditing numerics + writing the REPORT directly. No wasted work.

## Wave 2 (5 papers) — closed 2026-06-26

| # | Paper | Verdict | Cov/10 | Agr/10 | Notes |
|---|-------|---------|--------|--------|-------|
| 6 | Suzuki et al. — Amplitude estimation without phase estimation (2020) | REPLICATED | 8 | 9 | MLE-AE scaling exponents re-run independently: classical −0.48, LIS −0.75, EIS −0.96 vs paper −0.50/−0.76/−0.95. EIS recovers a to ~1e-5. |
| 7 | Bravyi et al. — Low-rank stabilizer decompositions (2019) | PARTIAL | 4 | 8 | Gottesman-Knill ✓, |S_n|=6/60/1080 exact, χ(|T>^t) t=1,2 match (t=3 found 4 vs 3, heuristic limit), Clifford+T prob exact. ⚠️ staged paper.md was WRONG (Kim 2023, cites Bravyi); subagent replicated from knowledge + flagged. Numerics verified vs literature. |
| 8 | Cade/Mineh/Montanaro — Fermi-Hubbard on near-term QC (2020) | REPLICATED (strategy) | 7 | 10 | VQE+HV ansatz across 5 lattices (4-12 qubits); energy error falls monotonically with depth to ~1e-4 (chemical accuracy). E_exact values verified (1x2=-1.236068 analytic). Subagent did numerics+code, timed out before writeup; report from verified results.json. |
| 9 | Romero et al. — Quantum autoencoders (2017) | PARTIAL | 6 | 8 | Recon fidelity 0.977/0.873/0.781 as latent k=3/2/1 — degradation-under-compression claim reproduced. Subagent timed out pre-code; done inline. Molecular states substituted; max-compression ansatz-limited. |
| 10 | Griffiths & Niu — Semiclassical Fourier Transform (1996) | REPLICATED | 9 | 10 | Measured-QFT ≡ coherent iQFT to TV ~1e-15 across 8 phases, k=3-5. ⚠️ subagent AND my first cut hit a bit-ordering bug → false DISAGREEMENT; fixed via exact-phase diagnostic → exact equivalence. Disk-verify caught a would-be false CONTRADICTED. |

**Wave 2 tally (5 closed):** 3 REPLICATED, 2 PARTIAL. 0 NO-GO, 0 CONTRADICTED. Mean Agreement 9.0/10.

**Running total (Waves 1+2, 10 papers):** 4 REPLICATED, 5 PARTIAL, 1 SPOT-CHECK. 0 NO-GO, 0 CONTRADICTED.

**Key audit catches this wave:**
- Semiclassical-QFT would have been falsely logged CONTRADICTED from a bit-ordering bug — caught by disk-verify + exact-phase sanity check. Paper is exactly correct (machine-precision equivalence).
- Stabilizer-rank had the WRONG paper.md staged (a citing paper, not Bravyi). Corpus hash→title mapping matched a citation line. Subagent handled correctly; flagged for corpus cleanup.

## Wave 3 (5 papers) — closed 2026-06-29 (Ollie-audited, disk-verified)

| # | Paper | Verdict | Cov/10 | Agr/10 | Notes |
|---|-------|---------|--------|--------|-------|
| 11 | Cleve/Ekert/Macchiavello/Mosca — Quantum Algorithms Revisited (1998) | REPLICATED | 9 | 10 | DJ P=1; BV hidden-string P=1; QPE min P(best m-bit)=0.4056 ≥ 4/π²=0.4053 (0/2000 below bound); Shor N=15 s/r exact, factors {3,5}@98.3%; Grover P_k 0.945–0.999. Independently re-run by Ollie — all numbers match. |
| 12 | Vedral/Barenco/Ekert — Quantum Networks for Elementary Arithmetic (1996) | REPLICATED | 8 | 10 | Exact NOT/CNOT/Toffoli adders; adder-mod-N exact (N=3,5,11,15); aˣ mod N orders exact; gate count O(n) R²=1.0; memory 7n+1/5n+2/4n+3 confirmed. Disk-verify caught+fixed a mod-N adder index overflow. |
| 13 | Seeley/Richard/Love — Bravyi-Kitaev transformation (2012) | REPLICATED | 9 | 10 | β₄/P/U/F sets exact; {a,a†}=δ exact both JW & BK; BK & JW H2 spectra match 4.4e-16, ground −1.851046; gate counts EXACT BK 30sq/44CX, JW 46sq/36CX; locality JW O(n) vs BK O(log n). Independently re-run by Ollie — exact match. |
| 14 | McCaskey et al. — Quantum chemistry benchmark VQE (2019) | PARTIAL | 6 | 9 | Table-1 hardware (IBM Tokyo/Rigetti Aspen) unreproducible w/o QPU → PARTIAL per hardware-blocker rule. Simulator backbone REPLICATED: ucc-1 VQE=FCI to 8.3e-10; PES tracks FCI <chem-acc at 6 bond lengths. Honest scoping confirmed. |
| 15 | Childs & Wiebe — Hamiltonian Simulation via LCU / multi-product formulas (2012) | REPLICATED | 8 | 10 | Lemma 2 failure prob to <1e-9 (9 cases); Thm3 κ=4.0 exact; MPF raises order S2 2.99→5.00; ΣC_q=1 exact; 2-qubit MPF 220× more accurate than S2. (Swapped in for a 5th to avoid overlap with done work.) |

**Wave 3 tally:** 4 REPLICATED, 1 PARTIAL. 0 NO-GO, 0 CONTRADICTED. Mean Agreement 9.8/10.
**Running total (Waves 1+2+3, 15 papers):** 8 REPLICATED, 6 PARTIAL, 1 SPOT-CHECK. 0 NO-GO, 0 CONTRADICTED.

**Audit note (Ollie, 2026-06-29):** Independently re-ran W3-bravyi-kitaev (exact 4.44e-16 spectra match, gate counts 30/44 & 46/36 confirmed) and W3-quantum-algorithms-revisited (QPE bound, Shor {3,5}@98.3%, Grover all >0.5 confirmed). VQE PARTIAL verdict is honestly scoped to the hardware-blocker rule, not inflated. All 5 dirs have paper.md + replicate.py + results.json + REPORT.md. No paid endpoints; pure local numpy/scipy simulation.
