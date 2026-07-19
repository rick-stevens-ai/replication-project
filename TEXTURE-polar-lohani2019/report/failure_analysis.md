# Failure & Gap Analysis — Lohani et al. 2019 (arXiv:1901.03343)

Honest accounting of what did **not** reproduce, what looks like a failure but is not, and the
concrete physics gaps between this replication and the paper.

## 1. The "zero scalar chirality" non-failure (READ THIS FIRST)

The raw scalar chirality
$$\langle\chi\rangle = \sum_\triangle \langle \mathbf{S}_i\cdot(\mathbf{S}_j\times\mathbf{S}_k)\rangle = 0$$
**exactly**, in every sector, on every flake. This is **correct physics, not a replication miss:**

- $H$ is real-symmetric ⇒ its ground state can be chosen purely real. The scalar triple product
  $\mathbf{S}_i\cdot(\mathbf{S}_j\times\mathbf{S}_k)$ is built from an odd number of $S^y$
  operators, making it a purely imaginary (i × Hermitian) operator whose expectation value in a
  real state is identically zero.
- Physically: with **no spin-orbit coupling**, skyrmion and antiskyrmion are **exactly degenerate**
  (paper Sec. I.A). Net chirality cancels between the two degenerate senses.
- The paper **never uses raw $\langle\chi\rangle$** as its skyrmion diagnostic. It detects winding
  via the arctan transverse-correlation (Eq. 12) and the transverse antiferromagnetic correlation
  $C_\perp$. We use $C_\perp$ as the anchor accordingly.

**Do not read $\langle\chi\rangle=0$ as evidence against replication.** It is the expected value and
is itself a correctness check on the ED (a nonzero value would indicate a broken/complex Hamiltonian).

## 2. Genuine gaps (not reproduced — scope, not error)

| Gap | What the paper has | Why not done here | Severity |
|-----|--------------------|-------------------|----------|
| **31-site flake** | Sharpest ED numbers use up to 31 sites | Largest $S_z$ sectors reach tens of millions of states; needs matrix-free `eigsh` (`LinearOperator`) and a larger-memory host (nuc13 62 GB / uicgpu). | Medium — would tighten finite-size scaling |
| **$l_z$ symmetry labels** | Angular-momentum/spin locking is a headline quantum number claim | Requires a C6 rotation operator + symmetry-adapted block diagonalization; round flakes are only approximately rotationally symmetric. | Medium |
| **Full $J_2$–$B$ phase diagram** | Fig. 4 maps skyrmion-stable region ($J_2\gtrsim0.45$) | Only 3 $(J_2,K)$ points computed; a converged boundary needs a fine 2D sweep on the large flake. | Low (mechanism already shown) |
| **Skyrmion bandwidth / tunneling** | Abstract headline: exponentially small bandwidth from skyrmion↔antiskyrmion tunneling | Needs resolved near-degenerate doublets (shift-invert `eigsh`, $k>1$) or a constructed effective 2-state model; `eigsh(k=1)` cannot see the splitting. | High — this is the paper's marquee dynamical result |
| **Winding-correlation Eq. 12** | Exact arctan form for quantum winding | Only max-pair $C_\perp$ implemented, not the full loop-winding reconstruction. | Low–Medium |
| **Phenomenological Schrödinger eq.** | Effective theory of skyrmion motion (parallel-vs-perpendicular response) | Separate analytic/effective-model build, not ED. | Out of ED scope |

## 3. Quantitative-agreement caveats

- $C_\perp=0.73$ lands inside the paper's 0.6–0.8 window but is **not a digit-for-digit match** —
  the flake size (19 vs 31) and exact geometry differ, so absolute correlation magnitudes shift.
  This is qualitative + one clean quantitative hit, hence Agreement ~8/10 (not 10).
- Binding energies $E_0^B$ are finite-flake **upper bounds**; their absolute values are
  flake-dependent. The reproduced claim is the **sign and monotonic deepening** with $N_f$, which is
  the rigorous binding signature, not the specific meV-scale value.

## 4. Extraction-artifact limitation

`marker` and `nougat` are **not installed** on this host (`which marker nougat` → not found). Both
`extraction/marker.md` and `extraction/nougat.mmd` are **interim `pdftotext`-based** extractions
with in-file status headers. Equations are linearized (not native LaTeX) except for the key
equations hand-transcribed into `nougat.mmd`. Regenerate with the real tools when available — this
is a tooling gap, not a physics gap.

## 5. Bottom line
The core exact-diagonalization physics — the many-magnon **bound state** ($E_0^B<0$ for all
$N_f\ge2$) and the transverse-correlation **skyrmion signature** ($C_\perp=0.73$) — **reproduces**.
The un-reproduced items are larger-Hilbert-space or effective-model extensions (31-site, symmetry
labels, phase diagram, tunneling bandwidth), each named above with a concrete path to close it in
`open_questions.json`.
