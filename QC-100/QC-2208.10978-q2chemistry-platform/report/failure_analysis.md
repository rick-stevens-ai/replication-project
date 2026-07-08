# Failure Analysis — QC-2208.10978 Q²Chemistry

**Honest critique of what this replication does and does not verify.**
Required by Rick Stevens' 2026-07-05 backfill directive: genuine failure/limitation analysis for every replication, no whitewash.

## TL;DR
- ✅ **C1 (headline sanity check) genuinely reproduced** — VQE-UCCSD on H₂ reproduces PySCF FCI to floating-point roundoff (≤10⁻¹² mHa) across 5 bond lengths.
- ❌ **The Q²Chemistry pipeline itself was NOT independently re-implemented or installed.**
- ❌ **The paper's actual Fig 6 configuration (40 qubits / ccj-pVDZ) was NOT reproduced** — a strictly weaker STO-3G basis was used.
- ❌ **The claimed integration / speedup was NOT quantitatively verified.**
- ❌ **C3, C4 (scale, silicon bands) not reproduced.**
- ❌ **C5 (public installability) is a NEGATIVE finding.**

## 1. Q²Chemistry pipeline: not reimplemented, not installed

**Fact:** The replication uses OpenFermion + PySCF as a functional stand-in, not the Q²Chemistry Python/C++ code itself. The QC-100 wave brief permits this when a paper's software is not publicly installable, but it means:

- **Q²Chemistry-specific bugs are not caught.** If the group's ansatz-builder or MPS backend has a subtle numerical error, this replication would not surface it.
- **The MPS backend (Julia, distributed) is entirely bypassed.** The paper's core novelty on the simulator side — the tensor-network circuit backend — is not exercised at all.
- **The classical-quantum interface layer** (Hamiltonian construction → OpenMPI dispatch → circuit evaluation → parameter update) is not tested. Only its input-output contract is (via a different implementation).

**Root cause of the stand-in:** as of 2026-07-03 we could not locate:
- a pip / conda package
- a public GitHub / GitLab / Gitee repo
- a downloadable source tarball
for Q²Chemistry. The only artifact reachable was the group's project page `zpy2001.github.io/Q2Chemistry` describing the software. This is a **negative finding on C5** — the paper describes a platform that a peer cannot obtain and install without contacting the authors.

## 2. Molecule / basis: strictly weaker test

**Fact:** The paper's Fig 6 uses H₂ in **ccj-pVDZ (40 qubits, 53 UCCSD parameters, 560 CPU cores, 24 h/geometry)**. This replication uses H₂ in **STO-3G (4 qubits, 2 UCCSD parameters, 1 core, ~1.6 s/geometry)**.

**Why the downshift is not a fatal flaw for C1's spirit:** UCCSD on H₂ tests the same algorithmic content — Jordan-Wigner encoding of a PySCF Hamiltonian, UCCSD generator, gradient-free VQE, PySCF FCI reference.

**Why the downshift IS a real limitation:**
- **STO-3G / H₂ is analytically trivial.** UCCSD spans the entire 4-qubit CI space, so the variational minimum is *by construction* the FCI energy. The 10⁻¹² mHa agreement is the expected trivial outcome, not a stress test of the ansatz.
- **At ccj-pVDZ, double excitations into virtual orbitals matter.** Whether the paper's symmetry-reduced 53-parameter ansatz actually spans the physically important subspace — and how gracefully BOBYQA finds the minimum on 40-parameter × 40-qubit landscape — is exactly what a scale replication would test, and is not tested here.
- **Optimizer difference (BOBYQA vs COBYLA+BFGS) is untested at scale.** Both are gradient-free trust-region methods, but their behavior on the paper's actual landscape is not established by a 2-parameter H₂ run.

## 3. Integration / speedup: not verified

**Fact:** The paper makes performance claims (Fig 5: 72-qubit Cr₂ MPS scaling on 768 cores; Fig 6: 40-qubit H₂ on 560 cores). This replication does **zero** performance measurement.

**What we did NOT do:**
- Measure Q²Chemistry wall-clock on any workload.
- Measure MPI scaling as a function of rank count.
- Measure MPS bond-dimension × wall-clock behavior.
- Measure classical-quantum interface latency.
- Compare Q²Chemistry against a canonical baseline (Psi4, PySCF-VQE, OpenFermion + Cirq, Qiskit-Nature) on a matched workload.

Any claim in the paper about the platform being "efficient", "scalable", or "faster than X" is trusted only on the paper's own report.

## 4. C3, C4: not reproduced

**C3 (72-qubit Cr₂ MPS on 768 cores):** requires the group's own code + a large HPC allocation. Out of scope for a single-node QC-100 replication. Not tested.

**C4 (silicon EOM-ADAPT-C bands, 0.047 eV MAD vs EOM-CCSD):** EOM-ADAPT-C is a Q²Chemistry-specific implementation. No open equivalent was substituted. Not tested.

## 5. C5: negative finding

**Fact:** No public pip / conda package. No public GitHub / GitLab / Gitee repo located. Only a project description page.

**Implication:** the paper's platform-availability claim (whether stated explicitly or implied by the term "platform") is not verifiable by a third party without contacting the authors. This is a real limitation of the paper's reproducibility posture, independent of anything this replication did.

## 6. Baseline comparison: what would strengthen the replication

To upgrade this from **REPLICATED (spot-check scale)** to **REPLICATED (full scale)**, one would need:
1. Access to the Q²Chemistry source code (blocker: not obtainable at time of writing).
2. HPC allocation of ~500 CPU cores × 24 h per geometry for the 40-qubit ccj-pVDZ H₂ run (blocker: not in QC-100 budget).
3. A DMRG / CASPT2 reference for C3 (Cr₂) — currently the paper reports only wall-clock, not accuracy, so even at HPC scale the accuracy claim is not falsifiable in isolation.
4. An open EOM-CCSD reference on the paper's silicon supercell for C4.

## 7. Overall honesty statement

The verdict **REPLICATED** is defensible **for C1 only**, and only under the "headline-exercised" rule where the sanity-check claim that lets a third party trust the platform's core VQE pipeline is genuinely reproduced. It is **NOT** a claim that:
- the Q²Chemistry software has been independently validated as bug-free,
- the platform's scale / performance claims have been confirmed,
- the paper's Fig 6 has been reproduced at its own scale (40 qubits, ccj-pVDZ),
- Q²Chemistry is publicly obtainable.

The 5 open questions in `open_questions.json` are precisely the probes that would close these gaps.
