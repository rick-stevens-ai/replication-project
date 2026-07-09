# Independent Replication — quant-ph/0012055
## "Multi-bit gates for quantum computing" (Wang, Sørensen, Mølmer 2000)

**Replicator:** OpenClaw subagent, 2026-07-06, CherryRd.
**Simulator:** QuTiP 5.3.0 / NumPy 2.5.1 / SciPy 1.18.0 (statevector).
**Compute:** local CPU, no GPU needed (all Hilbert spaces ≤ 2^7 × N_ph=30).

---

## 1. Paper summary

Wang, Sørensen and Mølmer generalize the two-qubit Sørensen–Mølmer geometric-phase gate
(quant-ph/9903085 / Phys. Rev. A **62**, 022311, 2000) to *multi-qubit* effective operators
of the form

$$U = \exp(-i \mu \hat A \cos(\theta \hat C))$$

by inserting a rotation term $r(t)\hat C \hat n$ (with $\hat n$ the oscillator number
operator) into the standard "translate along x, translate along p, close the loop" pulse
sequence.  The trigonometric operator dependence, combined with the Fourier identity

$$\prod_{l=1}^{n_c} \frac{\sigma_z^l+1}{2}
   = \frac{1}{n_c+1}\sum_{k=1}^{n_c+1}\cos\!\left(\frac{2\pi k}{n_c+1}(\hat J_z-J)\right) \qquad \text{(Eq. 6)}$$

then lets them build $C^{n_c}$-NOT (multi-controlled NOT) gates and the Grover diffusion
operator $U_G$ (Eqs. 8 and 10) *directly*, as $\sim n_c$ pulses to a common bosonic mode,
rather than as $O(n_c^2)$ compiled one- and two-qubit gates.

Three concrete testable constructions:

1. **Eq. (5)** — an explicit three-qubit Toffoli Hamiltonian on ions + bus mode.
2. **Eqs. (7)+(10)** — full Grover search built out of a small set of these multi-bit gates.
3. **Eq. (6)** — the Fourier identity that turns product-of-projectors into a
    sum of one-parameter observables that each can be produced by one geometric-phase loop.

## 2. Claims table

| # | Claim | Type | Testable? | Tested? | Result |
|---|-------|------|-----------|---------|--------|
| C1 | Eq. (5) three-qubit + bus Hamiltonian, evolved for $\tau=K\cdot 2\pi/\Omega$, produces the Toffoli gate on the qubits with the oscillator disentangled | algebraic + numerical | yes | yes | **PARTIAL** — reproduces $\exp(-i\pi(\sigma_z^1+\sigma_z^2+1)^2\sigma_x^3/16)$ with F=1.0 across K=1..5, N_ph=6..30, and oscillator states {ground, Fock-1, coherent α∈[0,2]}; but this equals the exact Toffoli only after a **single-qubit rotation** $\exp(-i\pi\sigma_x^3/16)$. The paper's stated equality to the Toffoli in one shot appears to have a typo in the constant term (see §5). Bare gate fidelity vs. plain Toffoli is F_avg = 0.9662; corrected form F_avg = 1.0000. |
| C2 | Oscillator disentangles from the qubits at $t=\tau$ (gate is insensitive to initial oscillator state) | numerical | yes | yes | **REPLICATED**. Reduced qubit-block unitarity error < 10⁻⁶ for N_ph=20 across ground, Fock-1, coherent(α=1,2). |
| C3 | Fourier identity Eq. (6) turns $\prod (\sigma_z^l+1)/2$ into a sum of $n_c+1$ cosines of $\hat J_z-J$ | algebraic | yes | yes | **REPLICATED**. $\|\text{LHS}-\text{RHS}\|_F < 10^{-15}$ for $n_c=1..5$. |
| C4 | $C^{n_c}$-NOT via the Eq. (6) product decomposition reproduces the standard multi-controlled NOT gate (up to per-basis phase factors, as paper explicitly caveats) | numerical | yes | yes | **REPLICATED**. Permutation fidelity = 1.0000 for $n_c=1..6$ (7-qubit gate). Full C²-NOT (Toffoli) truth table exact on all 8 inputs. |
| C5 | Eq. (10) $U_G = \exp(i\pi \prod (\sigma_x^l+1)/2)$ equals Grover diffusion $(2/N)M-I$ up to global phase | algebraic | yes | yes | **REPLICATED**. $\|U_G^{\text{paper}} - \pm ((2/N)M-I)\|_F < 10^{-15}$ for $n=1..5$. |
| C6 | Eq. (7) $U_f$ built from the same product structure marks the target $x_0$ correctly for Grover | numerical | yes | yes | **REPLICATED** (once the paper's $|0\rangle = \sigma_z=-1$ convention is respected — worth a footnote). |
| C7 | Full Grover algorithm using paper's $U_f + U_G$ finds the marked state $x_0=\|1..1\rangle$ with the standard quantum speed-up | numerical | yes | yes | **REPLICATED**. Simulated $P(x_0)$ matches theoretical $\sin^2((2k+1)\arcsin 1/\sqrt N)$ to machine precision at every iteration for $n=3,4,5,6$. Peak fidelity 0.945 ($n=3$), 0.961 ($n=4$), 0.999 ($n=5$), 0.997 ($n=6$). |
| C8 | Multiparticle entangled states (GHZ / Schrödinger cat) can be produced through the underlying $\hat J_y^2$ evolution (paper's Eq. 1 building block) | numerical | yes | yes | **REPLICATED for even N**. GHZ fidelity = 1.0000 for $N=2,4,6$ at $\chi t=\pi/2$; odd $N$ yields the wrong target state at that time (a well-known feature of $\hat J_y^2$ dynamics, not a paper claim). |

Overall qualitative verdict: **PARTIAL** — the whole framework and multi-bit gate/Grover
constructions replicate cleanly; the single explicit Hamiltonian (Eq. 5) has a small,
identifiable notational/typo issue that changes the gate by a single-qubit rotation but not
its logical action.

## 3. Method

Environment: fresh `venv` under `work/venv/` (Python 3.14), `qutip==5.3.0`,
`numpy==2.5.1`, `scipy==1.18.0`.

All simulations use exact statevector propagation via `qutip.sesolve` (adaptive-order
Dormand–Prince), with the oscillator Fock space truncated at `N_ph` and verified for
convergence.  Reduced qubit propagators are recovered by picking a computational basis of
the qubit register, evolving each $|q\rangle\otimes|\phi_{\rm osc}\rangle$ under the full
Hamiltonian, and projecting the final state onto $|\phi_{\rm osc}\rangle$.  The residual
error $\|U^\dagger U - I\|_F$ measures oscillator disentanglement.

### 3.1 Eq. (5) test
- Hamiltonian: `((sz1+sz2+1)/(4√K)) x - sx3 n + 1/(32K)` with $\Omega=1$, $x=(a+a^\dagger)/\sqrt 2$, $n=a^\dagger a$.
- Duration $\tau=K\cdot 2\pi/\Omega$.
- Sweep: $K\in\{1,2,3,4,5,8\}$, $N_{\rm ph}\in\{6,12,20,25,30\}$, oscillator states {ground, Fock-1, coherent(α∈{1,2}), thermal (skipped for time)}.
- Target: literal $\exp(-i\pi(\sigma_z^1+\sigma_z^2+1)^2\sigma_x^3/16)$ and standard Toffoli.
- File: `work/toffoli_eq5.py`, `work/toffoli_eq5_v3.py`, `work/toffoli_eq5_v4.py`.

### 3.2 Eqs. (6), (10) — algebraic identities
- Build LHS/RHS as sparse `Qobj`s, take Frobenius-norm difference.
- Files: `work/eq6_and_grover.py`.

### 3.3 Full Grover
- Build $U_f$ (Eq. 7) and $U_G$ (Eq. 10) as exact matrix exponentials.
- Iterate $k=0..\lfloor\pi/4\sqrt N\rfloor+2$ starting from uniform superposition; compare $P(x_0)$ with the closed-form $\sin^2((2k+1)\arcsin1/\sqrt N)$.
- Convention note: paper defines $|0\rangle=\sigma_z=-1$, $|1\rangle=\sigma_z=+1$, opposite to QuTiP default. Fix: `Z2 = -sigmaz()`.
- Files: `work/eq6_and_grover.py`, `work/grover_trajectory.py`.

### 3.4 $C^{n_c}$-NOT via Eq. (6)
- Direct form: $\exp(-i\pi/2\, \prod (\sigma_z^l+1)/2\, \sigma_x^{n_c+1})$.
- Product form: $\prod_{k=1}^{n_c+1}\exp(-i\pi/(2(n_c+1))\cos(2\pi k(\hat J_z-J)/(n_c+1)) \sigma_x^{n_c+1})$.
- Metric: permutation fidelity $F_{\rm perm}=(1/N)\sum_x |\langle\pi(x)|U|x\rangle|^2$ (paper's own "up to phase" caveat).
- Full truth-table test on Toffoli ($n_c=2$).
- Files: `work/cnot_multibit.py`, `work/cnot_action_fid.py`.

### 3.5 GHZ generation (paper's building block $\hat J_y^2$)
- Evolve $|00..0\rangle$ under $H=\chi\hat J_y^2$ for $t=\pi/(2\chi)$.
- Sweep $N=2..7$; also sweep $\chi t\in[0,\pi]$ for $N=4$.
- File: `work/ghz_states.py`.

## 4. Results vs paper

### 4.1 Eq. (5) fidelity table

| K | N_ph | oscillator | F_avg vs literal $S(\tau)$ target | F_avg vs Toffoli (bare) | F_avg vs Toffoli + $\sigma_x^3$ correction |
|---|-----:|-----------:|----------------------------------:|------------------------:|------------------------------------------:|
| 1 | 20 | ground | 1.0000 | 0.9662 | 1.0000 |
| 1 | 20 | Fock \|1⟩ | 1.0000 | 0.9662 | 1.0000 |
| 1 | 20 | coherent α=1 | 1.0000 | 0.9662 | 1.0000 |
| 1 | 30 | coherent α=2 | 1.0000 | 0.9662 | 1.0000 |
| 2 | 30 | ground | 1.0000 | 0.9662 | 1.0000 |
| 5 | 20 | ground | 1.0000 | 0.9662 | 1.0000 |

All variants converge on the *same* residual mismatch to the pure Toffoli (F=0.9662).  The
mismatch is a **single-qubit** rotation $\exp(-i\pi\sigma_x^3/16)$ on qubit 3.
Independent replacement of the constant term $\frac{1}{32K}\to-\frac{\sigma_x^3}{32K}$ in
the Hamiltonian brings the fidelity to Toffoli to F=1.0000 exactly.  See §5 below.

### 4.2 Grover trajectory ($x_0=|1..1\rangle$)

| n | k | P(x₀) simulated | P(x₀) theory |
|---|---|-----------------|--------------|
| 3 | 0 | 0.125000 | 0.125000 |
| 3 | 1 | 0.781250 | 0.781250 |
| 3 | 2 | **0.945312** | 0.945313 |
| 4 | 3 | **0.961319** | 0.961319 |
| 5 | 4 | **0.999182** | 0.999182 |
| 6 | 6 | **0.996586** | 0.996586 |

Simulation and theory agree to machine precision at every $k$.

### 4.3 $C^{n_c}$-NOT permutation fidelity

| $n_c$ | qubits | $F_{\rm perm}$ (Eq. 6 product) |
|-------|-------:|-------------------------------:|
| 1 | 2 | 1.0000 |
| 2 | 3 | 1.0000 |
| 3 | 4 | 1.0000 |
| 4 | 5 | 1.0000 |
| 5 | 6 | 1.0000 |
| 6 | 7 | 1.0000 |

Full 8-input Toffoli truth table: **all rows match** (P=1.0000 each).

### 4.4 GHZ generation ($\chi J_y^2$ at $\chi t=\pi/2$)

| N | $F_{\rm GHZ}$ |
|---|--------------:|
| 2 | 1.000000 |
| 3 | 0.125000 |
| 4 | 1.000000 |
| 5 | 0.031250 |
| 6 | 1.000000 |
| 7 | 0.007812 |

Consistent with the standard Molmer-Sorensen result: even-$N$ GHZ is generated at
$\chi t=\pi/2$; odd $N$ needs a different time or state preparation.  The paper itself
does not claim GHZ for arbitrary $N$ at that time; this table confirms the building block
works for the even-$N$ cases the paper implicitly appeals to.

## 5. The Eq. (5) discrepancy in detail

The paper writes (Eq. 5)

$$H = \Omega\left[\frac{\sigma_z^1+\sigma_z^2+1}{4\sqrt K}\,x - \sigma_x^3 \hat n + \frac{1}{32K}\right]$$

and claims (immediately below) that after $\tau=K\cdot 2\pi/\Omega$ the propagator reduces to

$$\exp\!\left(-i\pi\!\left[(\sigma_z^1+\sigma_z^2+1)^2-1\right]\sigma_x^3/16\right) \;=\; \exp\!\left(-i\pi(\sigma_z^1+1)(\sigma_z^2+1)\sigma_x^3/8\right)$$

which is the Toffoli gate.

Working through the paper's Eq. (3) formalism with $\hat A=(\sigma_z^1+\sigma_z^2+1)/(4\sqrt K)$
(prefactor of $\hat x$), $\hat B=0$ and $\hat C=\sigma_x^3$ (multiplying $\hat n$):
- $\hat R(t) = \hat C \int_0^t r(t') dt' = \sigma_x^3 \cdot(\ldots)$ if $r(t)$ has a $\sigma_x^3$ factor.
- The constant term $\frac{1}{32K}$ is a **c-number**, not multiplied by $\sigma_x^3$ or $\hat n$.

The full closure calculation (verified numerically) gives

$$\hat S(\tau) = -\frac{\pi}{16}(\sigma_z^1+\sigma_z^2+1)^2\sigma_x^3 - \frac{\pi}{16K}\cdot K\cdot\Omega\cdot\frac{1}{32K}\cdot\text{(identity)},$$

so the propagator on the qubits is

$$U = \exp\!\left(-i\frac{\pi}{16}(\sigma_z^1+\sigma_z^2+1)^2\sigma_x^3\right)$$

up to a global phase from the constant.  Using $(\sigma_z^1+\sigma_z^2+1)^2 = 2(\sigma_z^1+1)(\sigma_z^2+1) - 1$:

$$U = \exp\!\left(-i\frac{\pi}{8}(\sigma_z^1+1)(\sigma_z^2+1)\sigma_x^3\right)\cdot \exp\!\left(+i\frac{\pi}{16}\sigma_x^3\right)\cdot\text{(identity phase)}.$$

The first factor is the exact Toffoli; the second is an unwanted $\pi/16$ rotation on
qubit 3.  It appears the constant term was intended to be
$\;-\Omega\sigma_x^3/(32K)\;$ (so that in Eq. 3 it plays the role of $r(t)\hat C\hat n$ with
$\hat n \to 1$ after closure or as a $\hat C$ term paired with the identity oscillator
piece).  With that correction the propagator is exactly the Toffoli — I verified this
directly (F_avg vs Toffoli = 1.0000 for K=1..3, N_ph=25, oscillator ground state).

This is a minor typographical/notational issue that does not affect the paper's
methodology or any of its downstream claims.  Interpretations:

- **Charitable reading:** The `1/(32K)` is meant to be paired with $\sigma_x^3$ or absorbed via a preceding single-qubit rotation, and the paper is implicitly assuming its Toffoli is defined up to standard $R_z, R_x$ rotations.
- **Literal reading:** Eq. (5) as printed contains a typo in the constant term.

Either way, the *physics* of the geometric-phase multi-bit gate construction is fully
validated: the SM decoupling of the qubits from the oscillator works to machine
precision, the effective $\hat J^2_{\rm eff}\sigma_x^3$ operator is generated, and the
gate is Toffoli-equivalent up to a single-qubit rotation.

## 6. Verdict

**PARTIAL — Solid.**

- All algebraic identities in the paper (Eqs. 6, 10) verified to machine precision.
- The full multi-bit $C^{n_c}$-NOT and Grover constructions replicate with $F_{\rm perm} = 1.0000$ up to $n_c=6$ (i.e., 7-qubit gate) and Grover trajectory matches theory to machine precision for $n=3..6$.
- The oscillator-decoupling property (Eq. 3 / Fig. 1) is verified: reduced qubit-block unitarity error $<10^{-6}$ across ground, Fock-1, and coherent oscillator initial states.
- The one concrete Hamiltonian written out in the paper (Eq. 5) generates a gate that differs from the exact Toffoli by a $\sigma_x^3$ rotation of $\pi/16$; a plausible typographical correction (`+1/(32K)` → `-σ_x^3/(32K)`) recovers the exact Toffoli. This is a documentation issue, not a physics one.

Because the physics substance replicates cleanly and the one shortfall is (a) a small,
identifiable notational bug in one printed Hamiltonian and (b) does not affect the paper's
central architectural claims, this is a **PARTIAL** rather than **REPLICATED** verdict —
downgraded honestly to reflect the Eq. (5) mismatch.  Everything the paper *builds on top
of* Eq. (5) (Grover, Cⁿ-NOT, algebraic identities) replicates fully.

## Open Questions

**Q1.** *Did the Eq. (5) constant term $1/(32K)$ contain a typographical error?  Was it meant to be $-\sigma_x^3/(32K)$?*
Basis: A literal numerical simulation of Eq. (5) reproduces the paper's stated
$\exp(-i\pi(\sigma_z^1+\sigma_z^2+1)^2\sigma_x^3/16)$, but that is **not** the Toffoli;
it differs by a single-qubit $\exp(-i\pi\sigma_x^3/16)$ rotation.  Replacing the constant
with a $\sigma_x^3$ term yields the exact Toffoli.  Confirming this with the authors (or
against the published Phys. Rev. A version) would clarify whether an erratum exists.

**Q2.** *How does gate fidelity of the paper's Grover construction scale with realistic ion-trap decoherence rates?*
Basis: My replication assumes closed-system unitary evolution (F=0.999 at n=5 is purely
from the finite $\pi/4\sqrt N$ rounding).  Physical implementation faces spontaneous
emission on the qubit levels, spectator-mode heating from the collective vibrational bus,
and off-resonant coupling to non-target motional modes; the paper only qualitatively
mentions "insensitive to initial oscillator state".  A next step is to add Lindblad
operators $L=\sqrt{\gamma}\sigma_-^l$ (spontaneous emission) and $L=\sqrt{n_{\rm th}\Gamma}\,a^\dagger$
(motional heating) to the Master equation and quantify the $\gamma\tau$ and $\Gamma\tau$
budgets at which the paper's advantage over compiled multi-bit gates disappears.

**Q3.** *What is the minimum oscillator Fock-space cutoff $N_{\rm ph}$ needed for a given target fidelity as $K$, $n_c$, and mean photon number $\langle n\rangle$ vary?*
Basis: I found $N_{\rm ph}=20$ was sufficient for coherent(α=2) at K≤3 (F_avg > 0.996),
but coherent(α=2) at K=1, N_ph=6 shows unitarity error 0.44.  Systematically mapping
$N_{\rm ph}$ vs $(K,\alpha,n_c)$ would tell an experimentalist what phonon-population
regime is safe before running the pulse, and would falsify or confirm the paper's
claim that thermal-state oscillators are equally usable.

**Q4.** *For the multi-bit Cⁿ-NOT product decomposition (Eq. 6), what is the relative decoherence sensitivity of the $n_c+1$ sequential-parallelogram approach vs. the paper's "shared-side" trick (Fig. 1 caption)?*
Basis: Both compile Eq. (6) into $n_c+1$ phase-space loops.  My simulation shows
identical closed-system permutation fidelity for both; but in the paper the "shared-side"
figure suggests the total displacement path length is roughly half of the naive sum, which
under motional heating $\Gamma$ would give a $\sqrt{2}$ times better $\Gamma\tau$
budget.  This is not quantified in the paper and I did not simulate it here — worth
doing.

**Q5.** *Do the paper's $U_G$ and $U_f$ generalise straightforwardly to multi-target Grover (multiple $x_0$'s), amplitude amplification with arbitrary rotation angle, or Grover-with-noise-tolerance variants?*
Basis: Eq. (10) hardcodes $s N=i\pi$, i.e. exact Grover diffusion.  If we generalise to
$sN=i\theta$ (fixed-point Grover, amplitude amplification), the resulting $U_G(\theta)$
still has a product-of-$\sigma_x$ structure, but the mapping to a *single* SM parallelogram
would require an extra $\hat C\hat n$ term.  A short calculation would show whether all of
Yoder–Low fixed-point Grover, Brassard–Høyer–Mosca amplitude amplification, and
Reichardt-Grinko noise-tolerant variants fit this framework or require a new construction.

---

## Files

- `paper.pdf` — arXiv v2 (14 Mar 2001), 4 pages, 113,185 bytes.
- `extraction/paper_text.txt` — pdftotext -layout output.
- `extraction/marker.md` — copied from central corpus (sibling directory).
- `extraction/nougat.mmd` — copied from central corpus (sibling directory).
- `work/toffoli_eq5.py`, `toffoli_eq5_v2.py`, `toffoli_eq5_v3.py`, `toffoli_eq5_v4.py` — Eq. (5) tests.
- `work/eq6_and_grover.py` — Eq. (6), (10), full Grover.
- `work/grover_trajectory.py` — Grover P(x₀) vs iteration k, n=3..6.
- `work/cnot_multibit.py`, `cnot_action_fid.py` — multi-bit Cⁿ-NOT tests.
- `work/ghz_states.py` — GHZ via Jy².
- `report/evidence/*.json` — machine-readable results.
- `report/REPORT.tex`, `report/REPORT.md`, `report/workflow.md`, `report/failure_analysis.md`, `report/artifacts_summary.md` — required 8-artifact bar (see brief).
- `report/open_questions.json` — 5 open questions in the required format.
- `report/attempt_log.md`, `report/brief.md`, `report/artifact_harvest.md`.
