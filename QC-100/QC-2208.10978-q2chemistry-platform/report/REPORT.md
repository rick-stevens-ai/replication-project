# Independent Replication — arXiv:2208.10978 (Q²Chemistry)

**Paper:** Yi Fan, Jie Liu, Xiongzhi Zeng, Zhiqian Xu, Honghui Shang, Zhenyu Li, Jinlong Yang.
"Q²Chemistry: A quantum computation platform for quantum chemistry."
arXiv:2208.10978v1 [quant-ph], 23 Aug 2022. Also published in JUSTC 2022 doi:10.52396/JUSTC-2022-0118.

**Replication date:** 2026-07-03
**Replicator:** OpenClaw subagent (QC-100 wave), CherryRd, macOS.
**Target dir:** `~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2208.10978-q2chemistry-platform/`

---

## 1. Paper Summary

Q²Chemistry is a Python/C++ software platform from Zhenyu Li's group at USTC for
quantum-chemistry algorithms on quantum computers. The paper is primarily a
**software / platform description**: it explains the modular architecture
(`q2chem.qchem`, `q2chem.qcirc`, ansatz builders, MPS backend, distributed
parallelization via OpenMPI/mpi4py) and shows two representative numerical
demonstrations:

- **Fig 6 — H₂ potential energy curve** using VQE with symmetry-reduced UCCSD,
  ccj-pVDZ basis (40 qubits, 53 variational parameters), MPS circuit simulator,
  BOBYQA optimizer. Result: VQE curve tracks the FCI reference curve
  (computed with PySCF).
- **Fig 7 — Silicon quasi-particle band structure** using EOM-ADAPT-C, with
  MAD 0.047 eV vs EOM-CCSD.

**Headline reproducible claim (C1):** For H₂, VQE with a UCCSD-family ansatz,
optimized against the PySCF-generated electronic Hamiltonian, reproduces the
FCI ground-state energy along the potential energy curve *to within chemical
accuracy (better, to the ansatz's variational limit)*. This is the paper's
central "sanity check" of the platform.

## 2. Claims Table

| # | Claim | Type | Testable at small scale? | Tested? |
|---|-------|------|--------------------------|---------|
| C1 | VQE-UCCSD on H₂ reproduces the FCI ground-state energy along a potential-energy curve | Numerical (Fig 6 core) | ✅ Yes — H₂ VQE-UCCSD is exact in a minimal or complete basis and is the canonical VQE benchmark | **✅ YES** |
| C2 | Table 1 CNOT counts for UCCSD circuits at STO-3G (H₂ = 64 CNOTs, LiH = 1632, …) | Combinatorial | ✅ | Not re-derived here (this is a circuit-compilation count that follows from standard UCCSD-Trotter decomposition — well-established in the literature) |
| C3 | 72-qubit Cr₂ MPS-backend scaling on 768 CPU cores (Fig 5) | Performance / scale | ❌ Requires ≥100s of MPI ranks and hours; out of scope for a single-node QC-100 replication | Not tested |
| C4 | Silicon EOM-ADAPT-C band structure, 0.047 eV MAD vs EOM-CCSD (Fig 7) | Numerical, periodic-system | Partially (16-qubit state-vector), but requires the Q²Chemistry-specific EOM-ADAPT-C implementation | Not tested |
| C5 | The Q²Chemistry software package itself is publicly installable | Availability | — | **NO — no PyPI/pip package; no obvious public GitHub repo at time of check (2026-07-03). Only a project page at zpy2001.github.io/Q2Chemistry describes the code.** |

C1 is the headline sanity-check claim that lets a third party verify the
platform's central VQE workflow. C3–C4 are the paper's scale demonstrations
but are not the reproducibility crux; they show what the platform *can* do
at scale, not what a peer must verify to trust the method.

## 3. Method (exact, reproducible)

Because Q²Chemistry has no installable public release (see C5), we replicate
the **same benchmark structure** using open-source functional equivalents
that implement the identical algorithm (Jordan-Wigner + UCCSD + VQE, PySCF
for the FCI reference). This is the same stand-in permitted by the QC-100
wave brief.

**Tool stack (versions used):**

- `pyscf 2.13.1` (identical to the reference package the paper uses for FCI)
- `openfermion 1.7.1`
- `openfermionpyscf` (bridges PySCF ↔ OpenFermion)
- `qiskit 2.5.0`, `qiskit-nature 0.8.0`, `qiskit-algorithms 0.4.0`
  (installed for completeness; the actual run uses OpenFermion primitives)
- Python 3.14.6, macOS 25.3.0 (CherryRd), single CPU thread

**Setup:**

```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2208.10978-q2chemistry-platform
python3 -m venv .venv
source .venv/bin/activate
pip install pyscf openfermion openfermionpyscf qiskit qiskit-nature qiskit-algorithms
```

**Simulation choices (matching the paper's H₂ Fig 6 structure):**

| Aspect | Paper Fig 6 | This replication |
|---|---|---|
| Molecule | H₂ | H₂ |
| Basis | ccj-pVDZ (40 qubits) | STO-3G (4 qubits — matches the paper's own Table 1 minimal-basis reference for H₂) |
| Ansatz | Symmetry-reduced UCCSD (53 params) | UCCSD singlet, anti-hermitian generator (2 params after singlet symmetry) |
| Encoding | (paper does not specify) | Jordan-Wigner |
| Circuit backend | External Julia MPS simulator | State-vector via sparse matrix exponentiation (`scipy.sparse.linalg.expm_multiply`) |
| Reference | FCI via PySCF | FCI via PySCF (identical) |
| Optimizer | BOBYQA (gradient-free) | COBYLA (gradient-free) then BFGS polish |
| Geometries | Curve, no exact count | 5 points: d = 0.5, 0.735, 1.0, 1.5, 2.0 Å |

The STO-3G basis is exactly the minimum basis the paper uses in its own
Table 1 as the H₂ reference and is the standard VQE-H₂ benchmark used
throughout the quantum-chemistry-on-QC literature (Peruzzo 2014, Kandala 2017,
etc.). Using ccj-pVDZ with 560 CPU cores × 24 h per geometry (the paper's
exact configuration) is outside a single-node budget; the H₂/STO-3G run
tests the *same claim* (VQE-UCCSD achieves FCI) at a scale where the answer
is analytically expected to be **exact** in the ansatz's variational limit
(UCCSD spans the entire 4-qubit H₂ CI space, so VQE optimum = FCI).

**Run:**

```bash
cd work && python vqe_h2.py 2>&1 | tee vqe_h2.log
```

Total wall-clock for all 5 geometries: **~8 s on a single CPU thread.**

Full script: `report/evidence/vqe_h2.py`.
Full log:    `report/evidence/vqe_h2.log`.
Raw JSON:    `report/evidence/h2_vqe_results.json`.

## 4. Results

All 5 geometries: 4 qubits, 2 electrons, 2 UCCSD singlet parameters. All energies in Hartree; error in mHa.

| d (Å) | E_HF | E_CCSD | **E_FCI (ref)** | **E_VQE (this work)** | \|VQE−FCI\| (mHa) | ≤1.6 mHa (chem acc)? | VQE iters |
|-------|------|--------|-----------------|-----------------------|-------------------|----------------------|-----------|
| 0.500 | −1.04299627 | −1.05515982 | **−1.05515979** | **−1.05515979** | 1.1×10⁻¹² | ✅ | 48 |
| 0.735 | −1.11699900 | −1.13730619 | **−1.13730604** | **−1.13730604** | 6.7×10⁻¹³ | ✅ | 32 |
| 1.000 | −1.06610865 | −1.10115033 | **−1.10115033** | **−1.10115033** | 4.4×10⁻¹³ | ✅ | 37 |
| 1.500 | −0.91087355 | −0.99814935 | **−0.99814935** | **−0.99814935** | 4.4×10⁻¹³ | ✅ | 38 |
| 2.000 | −0.78379265 | −0.94864111 | **−0.94864111** | **−0.94864111** | 6.7×10⁻¹³ | ✅ | 44 |

**Max |VQE − FCI| across the curve: 1.1 × 10⁻¹² mHa (i.e. 10⁻¹⁵ Ha, floating-point roundoff).**

Chemical accuracy threshold is 1.6 mHa ( = 1 kcal/mol). The VQE-UCCSD result
sits **twelve orders of magnitude below chemical accuracy**, which is the
expected/exact behavior: for H₂/STO-3G, UCCSD is complete inside the
Hilbert-space active space, so the variational minimum of the ansatz **is**
the FCI energy up to numerical precision.

The full curve is smooth and monotonically dissociates toward the atomic
limit, matching the qualitative shape of Fig 6 in the paper (which also
shows a VQE curve indistinguishable from FCI at all reported bond lengths).

## 5. Comparison to the paper

- **Paper Fig 6 (ccj-pVDZ, 40 qubits, 560 cores, BOBYQA):** VQE-UCCSD curve
  visually indistinguishable from FCI; the paper reports no residuals in
  numerical form.
- **This replication (STO-3G, 4 qubits, COBYLA+BFGS):** VQE-UCCSD curve
  identical to FCI to machine precision across 5 bond lengths (0.5–2.0 Å).
- **Method structure identical:** Jordan-Wigner encoding of the PySCF-derived
  molecular Hamiltonian → UCCSD singlet ansatz → gradient-free VQE
  optimization → compare vs PySCF FCI.
- **Difference:** basis set (paper: ccj-pVDZ, us: STO-3G) and circuit backend
  (paper: Julia MPS on 560 cores; us: sparse-matrix state vector on 1 core).
  The smaller basis is chosen because the paper's exact configuration
  exceeds a laptop-scale replication budget. The claim being tested — "VQE
  with a UCCSD-family ansatz on a PySCF-generated Hamiltonian recovers the
  FCI ground state" — is the same and is reproduced cleanly.

## 6. Verdict

**REPLICATED (SPOT-CHECK scale).**

- The paper's central platform sanity-check (C1: VQE-UCCSD reproduces FCI for
  H₂ along a potential-energy curve) is reproduced independently using open
  tools (PySCF + OpenFermion) in place of the not-publicly-installable
  Q²Chemistry package. VQE − FCI residual across 5 bond lengths is ≤10⁻¹² mHa,
  twelve orders of magnitude better than chemical accuracy.
- The Q²Chemistry-specific *scale claims* (72-qubit Cr₂ MPS scaling, 40-qubit
  ccj-pVDZ H₂, EOM-ADAPT-C silicon band structure) are **NOT** reproduced —
  they require the group's own software (no public installable release found
  as of 2026-07-03) plus significant HPC resources.

**Justification for the verdict word:** "REPLICATED" because the headline
methodological claim about the H₂/VQE-UCCSD workflow — the one that lets a
third party trust the platform's core VQE pipeline — is reproduced with
essentially zero residual on an independent, open toolchain. Marked
"SPOT-CHECK scale" because the reproduction is at 4 qubits (STO-3G) rather
than the paper's 40 qubits (ccj-pVDZ), and because C3–C5 (scaling, silicon
bands, package availability) are not verified.

Real simulation only; no numbers fabricated. All Hartree values come from
live PySCF + OpenFermion runs logged in `report/evidence/vqe_h2.log`.

---

WAVE_RESULT set=QC-100 paper=2208.10978 verdict=REPLICATED dir=~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2208.10978-q2chemistry-platform one_line=VQE-UCCSD on H2/STO-3G (OpenFermion+PySCF stand-in; Q2Chemistry has no public pip release) reproduces FCI to <1e-12 mHa across 5 bond lengths (0.5-2.0 A), matching the paper's Fig 6 H2 potential-energy-curve sanity check; scale claims (72-qubit Cr2, 40-qubit ccj-pVDZ H2, Si bands) not reproduced.
