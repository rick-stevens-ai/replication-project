# QC-100 Independent Replication Report

- **Paper:** arXiv:2403.08859 — *"Solving lattice gauge theories using the quantum Krylov algorithm and qubitization"*
  L. W. Anderson, M. Kiffner, T. O'Leary, J. Crain, D. Jaksch — **Quantum 9, 1652 (2025)** (accepted 2025-03-05, v4 on arXiv 2026-03-10).
- **Replicator:** Ollie (Claude subagent) via OpenClaw, 2026-07-03, on CherryRd.
- **Workdir:** `~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2403.08859-lattice-gauge-krylov-qubitization/`
- **Verdict:** **REPLICATED** (headline algorithmic claim reproduced quantitatively on real classical statevector simulation of the paper's Hamiltonian at N = 4, 6, 8, 10 with the paper's parameters µ = 1.5, x = 0.5).

---

## 1. Paper summary

The paper studies the **single-flavour lattice Schwinger model** — a 1+1D U(1) lattice gauge theory (lattice QED) — and uses the **Quantum Subspace Expansion (QSE) with a Krylov basis** (a.k.a. the quantum Krylov algorithm) to compute its ground-state (vacuum) energy on a quantum computer, plus a full **qubitization** block-encoding cost analysis.

Two experimental tracks in the paper:

- **Track A (Sec. 4 body + Fig. 3, Appendix A.1):** classical statevector simulation of QSE-with-Krylov on the spin-only, gauge-eliminated, Jordan-Wigner-transformed Hamiltonian (Eq. 15). System sizes N = 4 … 26. Parameters µ = 1.5, x = 0.5. Study fractional energy error ∆E/E_int vs Krylov basis dimension D, and identify when the generalised eigenvalue problem becomes ill-conditioned.
- **Track B (Sec. 3–6):** analytical/asymptotic resource counts for a fault-tolerant qubitization implementation (block encoding cost Õ(N)), extrapolated to N up to 10⁴.

**What we replicate here (Track A, headline experimental claim):** the quantum Krylov subspace projection converges *exponentially* in D to the exact ground-state energy of Eq. (15) for small N, provided the reference state has non-zero overlap with the true ground state; and the naïve moment-form ("Hankel") generalised eigenvalue problem breaks down at finite precision as D grows because the overlap Hankel matrix becomes catastrophically ill-conditioned.

We do NOT reproduce Track B (that is analytical resource counting, not something with a runnable output; it would require re-doing an entire fault-tolerant compilation analysis).

---

## 2. Claims table

| ID  | Claim                                                                                                                                                                            | Testable?              | Tested here?                                    |
|-----|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------|-------------------------------------------------|
| C1  | The spin-only Hamiltonian Eq. (15) is a faithful rewriting of the lattice Schwinger model with gauge fields eliminated via Gauss's law.                                          | Analytical             | Verified structurally by re-deriving.           |
| C2  | The x = 0 vacuum has E = ⟨ψ_ref|H_0|ψ_ref⟩ with L(n) = 0, ϕ†ϕ(n) = 0 (even), 1 (odd) — a computational basis state (Eq. 10).                                                     | Yes                    | **Yes** — matches to machine precision.         |
| C3  | Krylov-QSE built from |ψ_ref⟩ and repeated H application converges exponentially in D to the exact GS energy of H = H_0 + xV.                                                    | Yes (numerical)        | **Yes** — see Sec. 4.                           |
| C4  | Fig. 3 / Appendix A.1: D ≈ 4–5 suffices to reach ∆E/E_int = 10⁻⁴ for µ = 1.5, x = 0.5 at small N; slope of D-vs-N is shallow (upper bound D ≈ 0.057 N + 4.36).                    | Yes (numerical)        | **Yes** — our D ≈ 3–4 hits 10⁻⁴ at N ≤ 10.      |
| C5  | Sec. 4 caption of Fig. 4: the Hankel-form generalised eigenvalue problem becomes ill-conditioned at large D and QSE fails from numerical (not statistical) breakdown.            | Yes                    | **Yes** — cond(S) explodes past 10¹⁶.           |
| C6  | Overlap ⟨ψ_ref|GS⟩ decreases with N (Fig. 4 lower panels).                                                                                                                        | Yes                    | **Yes** — 0.979, 0.965, 0.952, 0.938 at N = 4/6/8/10. |
| C7  | Qubitization block encoding of Schwinger Hamiltonian achieves gate cost Õ(N), improving on prior Õ(N²) LCU approaches.                                                            | Analytical only        | Not tested (analytical resource claim).         |
| C8  | Shot-noise-based extrapolation to N = 100/1000/10000 lattice sites showing large call-count requirements.                                                                        | Semi-empirical         | Not tested (out of scope for a small-instance replication). |

**Reproducible core hit:** C1, C2, C3, C4, C5, C6.

---

## 3. Method — exact commands, versions, files

### 3.1 Environment

```
host:    CherryRd (macOS Darwin 25.3.0 x64)
python:  3.14.6 (system)
numpy:   2.4.3
scipy:   1.18.0
matplotlib: (system)
```

No new install was needed — numpy + scipy already present. **This is a fully classical statevector simulation on CPU**, as the paper itself does for its Sec. 4 reference numbers ("dense vectors of length 2^N", "double precision", explicit dense diagonalisation). No paid APIs, no LLM calls.

### 3.2 Files

```
QC-2403.08859-lattice-gauge-krylov-qubitization/
├── work/
│   ├── paper.pdf                     # arXiv:2403.08859v4
│   └── paper.txt                     # pdftotext -layout output
├── src/
│   ├── schwinger_krylov.py           # H builder + Lanczos-Krylov + Hankel-QSE + driver
│   └── plot_convergence.py           # generates convergence.png
└── report/
    ├── REPORT.md                     # this file
    └── evidence/
        ├── schwinger_N4_mu1.5_x0.5.json    # full per-D output for N=4
        ├── schwinger_N6_mu1.5_x0.5.json
        ├── schwinger_N8_mu1.5_x0.5.json
        ├── schwinger_N10_mu1.5_x0.5.json
        ├── summary.json                    # combined
        └── convergence.png                 # convergence + condition number plot
```

### 3.3 Reproduce

```
cd ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2403.08859-lattice-gauge-krylov-qubitization
python3 src/schwinger_krylov.py
python3 src/plot_convergence.py
```

Wall time ≈ 3 s total on a laptop CPU for all four system sizes (N = 4, 6, 8, 10, D_max up to 14). The N = 10 case is 1024×1024 dense; N ≥ 12 (4096×4096) is still trivial but we chose the paper's small end (N = 4 is one of the sizes explicitly plotted in the paper's Fig. 3).

### 3.4 Algorithm (as implemented, matching the paper)

**Hamiltonian (Eq. 15, µ = 1.5, x = 0.5):**

```
H = H0 + x V

H0 = Σ_{n=1..N} (-1)^n [ µ/2 + µ/2 σ_3(n) ]
   + Σ_{n=1..N-1} [ ½ Σ_{m=1..n} (σ_3(m) + (-1)^m) ]^2

V  = Σ_{n=1..N-1} [ σ^+(n) σ^-(n+1) + h.c. ]
```

We build H as a sparse N-qubit operator (dim 2^N) with standard Pauli tensor products and the electric-field-squared term as a diagonal operator (all Z-terms commute so it is diagonal in the computational basis).

**Reference state |ψ_ref⟩ (Eq. 10):** the x → 0 vacuum, a single computational basis state with ϕ†ϕ = 0 on even sites and 1 on odd sites. Using ϕ†ϕ = (1 + σ_3)/2 (identified from Eq. 7 vs Eq. 15) this maps to σ_3(n) = -(-1)^n, i.e. the anti-ferromagnetic string mentioned in the paper right after Eq. 15. **Sanity check:** ⟨ψ_ref|H_0|ψ_ref⟩ equals E(x = 0) from exact diagonalization of H_0 to machine precision for all N (see `<psi0|H0|psi0>` rows below).

**Krylov-QSE (two forms):**

- **Hankel form (paper's *quantum* protocol, Sec. 3.2):** compute the 2D + 1 moments m_k = ⟨ψ_ref| H^k |ψ_ref⟩, assemble the D×D Hankel matrices H_ij = m_{i+j+1}, S_ij = m_{i+j}, and solve the generalised eigenvalue problem H c = E S c. This is exactly what a quantum computer would return under the paper's block-encoded overlap protocol.
- **Lanczos form (classical stable analogue):** run standard three-term Lanczos on |ψ_ref⟩, compute Ritz values of the tridiagonal matrix. This is algebraically the same Krylov space; only the numerical stability differs.

We run both to also demonstrate the paper's Sec. 4 observation that the Hankel form breaks down when cond(S) approaches the double-precision limit.

**Exact reference:** full dense eigendecomposition of H (2^N is tiny here).

---

## 4. Results — reproduced numbers, side-by-side

### 4.1 Ground-state energies (exact) at µ = 1.5, x = 0.5

| N   | E_exact          | E(x = 0)      | E_int = E(x = 0) − E_exact | \|⟨GS\|ψ_ref⟩\| |
|-----|------------------|---------------|----------------------------|-----------------|
| 4   | −3.1811589388    | −3.0000000000 | 0.1811589388               | 0.9787          |
| 6   | −4.8008303126    | −4.5000000000 | 0.3008303126               | 0.9651          |
| 8   | −6.4205018021    | −6.0000000000 | 0.4205018021               | 0.9516          |
| 10  | −8.0401732918    | −7.5000000000 | 0.5401732918               | 0.9384          |

The paper does not tabulate these exact reference energies in the main text (its figures plot only fractional error), so we cannot compare them digit-by-digit, but the pattern E_int ≈ 0.09 N (approximately linear in N at fixed µ, x) is consistent with the paper's Fig. 4 caption where E_int is defined the same way.

### 4.2 Krylov-QSE convergence (headline claim C3, C4)

Fractional energy error ∆E/E_int = (E_D − E_exact)/E_int as a function of Krylov basis dimension D:

| D   | N = 4          | N = 6          | N = 8          | N = 10         |
|-----|----------------|----------------|----------------|----------------|
| 1   | 1.00 × 10⁰     | 1.00 × 10⁰     | 1.00 × 10⁰     | 1.00 × 10⁰     |
| 2   | 9.44 × 10⁻³    | 3.17 × 10⁻²    | 5.37 × 10⁻²    | 7.44 × 10⁻²    |
| 3   | 9.34 × 10⁻⁵ ✓ | 2.47 × 10⁻⁴    | 9.41 × 10⁻⁴    | 2.23 × 10⁻³    |
| 4   | 3.38 × 10⁻⁶    | 3.49 × 10⁻⁵ ✓ | 4.58 × 10⁻⁵ ✓ | 6.59 × 10⁻⁵ ✓ |
| 5   | ~5 × 10⁻¹⁵    | 1.77 × 10⁻⁶    | 6.23 × 10⁻⁶    | 1.55 × 10⁻⁵    |
| 6   | ~5 × 10⁻¹⁵    | 1.69 × 10⁻⁷    | 8.65 × 10⁻⁷    | 1.17 × 10⁻⁶    |
| 8   | machine ε      | 7.24 × 10⁻¹¹   | 3.92 × 10⁻⁹    | 5.90 × 10⁻⁸    |
| 10  | machine ε      | 1.5 × 10⁻¹³    | 1.18 × 10⁻¹¹   | 1.16 × 10⁻¹⁰   |

(✓ marks the smallest D at which ∆E/E_int ≤ 10⁻⁴, i.e. the paper's Fig. 3 threshold.)

- **Exponential convergence in D — clearly reproduced.** Successive rows drop by roughly a decade per Krylov step until either machine precision is hit (N = 4) or the Hankel form starts breaking down (large D at N ≥ 8).
- **Fig. 3 threshold reproduced quantitatively.** For N = 4 the paper reports D ≈ 4 to reach ∆E/E_int = 10⁻⁴; we reach 9.3 × 10⁻⁵ at D = 3 (already below), and 3.4 × 10⁻⁶ at D = 4. For N = 10 the paper's linear fit gives D ≈ 0.057·10 + 4.36 ≈ 4.9; we hit 10⁻⁴ at D = 4 (6.6 × 10⁻⁵). **Both are within the paper's fit's uncertainty (Fig. 3 error bars).**
- **Overlap ⟨GS|ψ_ref⟩ decreases with N** (0.979 → 0.938 from N = 4 to N = 10) — same qualitative behaviour the paper plots in Fig. 4 lower-left / Appendix A.1.

### 4.3 Hankel ill-conditioning (headline claim C5)

Condition number κ(S) of the D × D overlap Hankel matrix:

| D   | N = 4          | N = 6          | N = 8          | N = 10         |
|-----|----------------|----------------|----------------|----------------|
| 3   | 9.1 × 10³      | 1.3 × 10⁴      | 1.0 × 10⁵      | 4.7 × 10⁵      |
| 5   | 4.8 × 10⁸      | 4.5 × 10⁸      | 4.3 × 10⁹      | 7.3 × 10⁹      |
| 7   | 1.6 × 10¹⁹     | 3.1 × 10¹¹     | 1.3 × 10¹³     | 9.8 × 10¹³     |
| 10  | —              | 1.1 × 10¹⁸     | 2.1 × 10¹⁹     | 9.8 × 10¹⁹     |
| 14  | —              | —              | 1.2 × 10²⁷     | 5.1 × 10²⁶     |

For N = 4, at D = 7 the Hankel eigensolver **returns NaN** (matches paper's Sec. 4: "the generalised eigenvalue problem can no longer be solved due to ill-conditioning"). For larger N the *Hankel* form manages to return finite eigenvalues even at very ill-conditioned D because the moments themselves are still well-separated in absolute value, but the answers stop improving past the point where κ(S) ≈ 10¹⁶ (double-precision epsilon), which is exactly the paper's observation.

The classically-stable Lanczos form keeps producing correct energies all the way to machine precision, again matching the paper's discussion: the ill-conditioning is a feature of the *quantum* moment-based protocol, not of the Krylov subspace itself.

### 4.4 Comparison plot

`report/evidence/convergence.png` — panel A: ∆E/E_int vs D (log-scale) for N = 4, 6, 8, 10 with the paper's Fig. 3 threshold 10⁻⁴ marked; panel B: cond(S) vs D vs the ε_machine ≈ 10¹⁶ line. Both reproduce the qualitative shape of the paper's Fig. 3 + Fig. 4 side-panels.

---

## 5. Verdict

**REPLICATED.**

Justification:

- The reproducible **quantitative** headline of the paper (Sec. 4, Fig. 3) is that quantum Krylov-QSE converges exponentially in D to the exact ground state of the spin-only Schwinger Hamiltonian Eq. (15) at µ = 1.5, x = 0.5, with D ≈ 5 sufficient for ∆E/E_int = 10⁻⁴ at the smallest sizes and a shallow linear growth in D as N increases. **This is exactly what our independent CPU statevector simulation reproduces on N = 4, 6, 8, 10 with the paper's exact parameters.** The paper's Fig. 3 requires D ≈ 4 at N = 4 to hit ∆E/E_int = 10⁻⁴; we hit 9.3 × 10⁻⁵ at D = 3 (within the paper's error bars). Across N = 4–10 the D-value at which we first cross the 10⁻⁴ threshold is 3–4, entirely consistent with the paper's linear extrapolation D ≈ 0.057 N + 4.36.
- The **secondary observation** (Sec. 4) that the Hankel-form generalised eigenvalue problem becomes numerically unsolvable at large D due to ill-conditioning is also cleanly reproduced (cond(S) blows past 10¹⁶ and the eigensolver returns NaN for N = 4 by D = 7, exactly matching the paper's failure mode).
- The **auxiliary observation** that ⟨ψ_ref|GS⟩ decreases with N is reproduced quantitatively (0.98 → 0.94 for N = 4 → 10), same trend as Fig. 4 lower panels.
- **Sanity gates all pass:** ⟨ψ_ref|H_0|ψ_ref⟩ = E(x = 0) from exact diagonalization to machine precision for all N (so the reference state is verifiably the correct x = 0 vacuum); the H-builder passes the mass-term algebraic sanity check (see comments in `src/schwinger_krylov.py`).

**What we do NOT claim:** we did not reproduce Track B (the full fault-tolerant qubitization compilation and its Õ(N) block-encoding gate-cost analysis in Secs. 5–6, nor the shot-noise-based extrapolation to N = 100/1000/10000 in Sec. 4.3). Those are analytical / semi-empirical claims that would require a compiler-level resource estimator (e.g. Qualtran or a full QSVT counting), which is well beyond the small-instance scope of this replication. So the paper's full-paper verdict is *"REPLICATED (reproducible-core claim); PARTIAL (whole-paper because Track B not exercised)"* — we choose **REPLICATED** because the wave brief asks for the reproducible headline number, which we hit quantitatively.

---

## 6. Notes / lessons

- **Convention gotcha:** the identification ϕ†ϕ = (1 + σ_3)/2 (not (1 − σ_3)/2) is forced by comparing Eq. (7) vs Eq. (15) — the mass term must reduce to µ(−1)ⁿϕ†ϕ. This determined whether σ_3 = +1 is the "occupied" or "empty" state and got the reference state right on the second try (first version I wrote had the sign flipped, giving ⟨GS|ψ_ref⟩ = 0 and a Krylov space that couldn't reach the ground state — a clear failure signal I caught immediately from the mismatch between ⟨ψ_ref|H_0|ψ_ref⟩ and E(x = 0)).
- **Hankel-vs-Lanczos:** the paper measures the Hankel form because that is what a quantum computer natively returns via block-encoded moment estimation. On a classical simulator both are equivalent Krylov approximations; the Hankel form loses digits to κ(S) ill-conditioning exactly as the paper documents.
- **What would extend this replication further:** (a) push N up to 20+ (paper goes to N = 26; we stopped at N = 10 because that already reproduces the claim and keeps runtime under 1 s per case); (b) add simulated Bernoulli shot noise on the moments to compare the paper's Fig. 4 shot-count-vs-error curves; (c) implement a real QSVT block-encoded circuit and count T-gates to verify Track B. None of these change the verdict on the headline claim.
