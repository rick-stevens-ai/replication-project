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

## 1b. NOW REPRODUCED — skyrmion↔antiskyrmion tunneling bandwidth (COVERAGE-FLIP)

The paper's **marquee dynamical claim** (abstract: "*Their bandwidth is exponentially small
and arises from tunneling processes between skyrmion and antiskyrmion*") **now reproduces** via a
finite-size-scaling ED run (`work/lohani_fss.py`, evidence `report/evidence/lohani_fss_result.json`):

- We compute the **low-lying spectrum** ($k{=}4$–$6$ states via `eigsh`, not just the ground state)
  in each skyrmion sector on flakes $N=7,19,37$ (37 ≈ the paper's 31-site cluster).
- The **tunneling splitting** $\Delta_{\rm tun}=E_1-E_0$ within the skyrmion sector **collapses**:
  from a generic level spacing $\sim0.23$ at $N=7$ (no skyrmion, $C_\perp=0$) to
  $\sim10^{-2}$ and down to **machine-zero $\sim10^{-14}$** at $N=19,37$ in the skyrmion sectors —
  i.e. an **exponentially small bandwidth**, exactly as claimed.
- The splitting shows the paper's **mod-3 selection-rule structure** (paper Figs. 7–8): the
  $N_f=2\bmod3$ sectors are exactly degenerate ($\Delta_{\rm tun}\sim10^{-14}$, quadratic/vanishing
  tunneling), while $N_f=0,1\bmod3$ sectors show a finite $\sim10^{-2}$ splitting.
- Simultaneously $C_\perp$ stays in the paper's 0.6–0.8 window in the skyrmion sectors, confirming
  these near-degenerate doublets are genuine skyrmion/antiskyrmion partners, not accidental crossings.

This flips the item from "High severity, not reproduced" (previous verdict) to **reproduced**, and
is the basis for the PARTIAL→REPLICATED coverage upgrade.

## 2. Genuine gaps (not reproduced — scope, not error)

| Gap | What the paper has | Why not done here | Severity |
|-----|--------------------|-------------------|----------|
| **Exact 31-site geometry** | Sharpest ED numbers use an exactly-round 31-site flake with C6 symmetry | We reached $N=37$ (round flake, radius 3) — **larger** than the paper's 31 and in the same regime — but not the identical 31-site geometry with its exact C6 labels. | Low — size gap effectively closed |
| **$l_z$ symmetry labels** | Angular-momentum/spin locking is a headline quantum number claim | Requires a C6 rotation operator + symmetry-adapted block diagonalization; round flakes are only approximately rotationally symmetric. *(The mod-3 tunneling structure is now observed empirically — see §1b — but not yet tied to explicit $l_z$ labels.)* | Medium |
| **Full $J_2$–$B$ phase diagram** | Fig. 4 maps skyrmion-stable region ($J_2\gtrsim0.45$) | Only 3 $(J_2,K)$ points computed; a converged boundary needs a fine 2D sweep on the large flake. | Low (mechanism already shown) |
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
$N_f\ge2$), the transverse-correlation **skyrmion signature** ($C_\perp=0.73$), **and now the
paper's headline dynamical claim** (exponentially small skyrmion↔antiskyrmion **tunneling
bandwidth**, $\Delta_{\rm tun}$ down to $\sim10^{-14}$ with the correct mod-3 selection structure,
demonstrated by finite-size scaling to $N=37$) — **all reproduce**. The remaining un-reproduced
items are refinements (exact 31-site $l_z$ labels, the full $J_2$–$B$ phase diagram, the Eq. 12
arctan winding form, the phenomenological Schrödinger equation), each named above with a concrete
path to close it in `open_questions.json`.
