# Workflow — QC-200 Replication of arXiv:1701.05052

**Paper.** Ananda Roy and David P. DiVincenzo, *"Topological Quantum Computing"*, Lecture Notes of the 48th IFF Spring School (Chapter **D7**), Forschungszentrum Jülich, 2017. arXiv:1701.05052v1 [quant-ph], 18 Jan 2017. 18 pages.

**Critical framing correction.** The wave-brief target description referred to "D_7 topological quantum computing" using the D_7 dihedral modular tensor category (F/R matrices, pentagon/hexagon, Kitaev–Solovay compilation of a Hadamard). This is a **misidentification**: the "D7" in the title is the **chapter number** in the IFF Spring School lecture-note proceedings, not the dihedral group D_7. The paper is a **pedagogical review of Majorana-fermion-based topological quantum computing** — abelian anyons in the Kitaev honeycomb model, non-abelian Ising-type Majorana braiding, and magic-state distillation for the non-Clifford π/8 and controlled-phase gates. The replication was retargeted to the paper's **actual** testable equations.

---

## Timeline & tools

| Step | Time (approx.) | Tool / command | Notes |
|------|----------------|----------------|-------|
| 1. Fetch PDF | <1 s | `curl` from `arxiv.org/pdf/1701.05052` | 998 KB, 18 pp, v1, PDF/1.5 |
| 2. `pdftotext` sanity read | <1 s | `pdftotext paper.pdf work/paper.txt` | poppler `pdftotext` |
| 3. Realize "D7" is chapter no., re-scope | ~2 min | (reading Sec. 4 title + IFF Spring School header) | ← key correction |
| 4. Kick Marker + Nougat on uicgpu | started ~18:15 CDT | `marker_single` (marker env) + `nougat` (nougat env) via ssh | uicgpu A100, `/gpustor/stevens/anaconda3/envs/{marker,nougat}` |
| 5. Write and run numpy simulator | ~4 min author + <1 s exec | `python3 report/evidence/sim_majorana_braiding.py` | numpy only, dim=2^n exact |
| 6. Plot Kitaev phase diagram | ~30 s | `matplotlib` | `figures/kitaev_phase_diagram.png` |
| 7. Pull Nougat + Marker outputs | ~1 min | `scp` back to `extraction/` | |
| 8. Write REPORT.tex + open_questions.json + failure_analysis.md + artifacts_summary.md | ~10 min | editor | this pass |

**Total effective wall-clock:** ~30 min for driver work + parser wait; simulation itself is <1 s CPU on CherryRd (Intel MBP).

## Tools + versions

| Tool | Version | Where | Purpose |
|------|---------|-------|---------|
| `python3` | 3.13.7 (system) on macOS | CherryRd host | driver |
| `numpy` | (system numpy on macOS) | CherryRd | dim=16 exact linear algebra for Majorana Clifford algebra & braid ops |
| `matplotlib` | (system, Agg backend) | CherryRd | phase-diagram figure |
| `pdftotext` | poppler 25.x, `/usr/local/bin/pdftotext` | CherryRd | quick text extraction |
| `marker_single` | marker-pdf (conda env `marker` @ uicgpu) | uicgpu A100 | high-fidelity markdown parse |
| `nougat` | nougat-ocr 0.1.x (conda env `nougat` @ uicgpu) | uicgpu A100 | equation-preserving `.mmd` parse |
| `curl`, `scp`, `ssh` | standard | CherryRd ↔ uicgpu | file transfer |

**LLM inference:** none required. All numeric claims are checked with exact linear algebra + closed-form Kitaev honeycomb dispersion. Free-endpoint policy trivially satisfied.

## What was actually simulated

The paper contains **no numerical simulation of its own** — it is a review. The replication therefore takes each concrete equation/algebraic claim and verifies it directly on the finite-dimensional Fock space of the referenced Majorana operators.

Encoding used (matches paper Eq. 15–17):
- 2n Majorana operators `γ_1 … γ_{2n}` implemented on a `2^n`-dim Hilbert space via **Jordan–Wigner** (Kitaev–style JW string):
  - `γ_{2j-1} = Z⊗…⊗Z⊗X⊗I⊗…` (X at site j)
  - `γ_{2j}   = Z⊗…⊗Z⊗Y⊗I⊗…` (Y at site j)
- Verified `{γ_i, γ_j} = 2 δ_{ij}` and hermiticity to machine precision.

Tests, each pinned to a specific numbered equation of the paper:

| Check | Paper eq. | What is checked | Numeric result |
|------|-----------|-----------------|----------------|
| **C1** | Eq. 30 | `B_{i,i+1} = (I − γ_i γ_{i+1})/√2` is unitary; `B B⁻¹ = I` | max err **2.23 × 10⁻¹⁶** |
| **C2** | Eqs. 20–21 | far commutation `[B_i, B_j] = 0` for `|i−j|>1`; Yang–Baxter `B_i B_{i+1} B_i = B_{i+1} B_i B_{i+1}` | max err **4.47 × 10⁻¹⁷** (both n=4 & n=6) |
| **C3** | text below Eq. 32 | `B² = −γ_i γ_{i+1}`, `B⁴ = −I` (operator level), `B⁴ · γ_k · B⁻⁴ = γ_k` (conjugation level, which is what the paper's "identity operation" statement means) | max err **6.66 × 10⁻¹⁶** |
| **C4** | Eq. 33 | `[B_{i-1,i}, B_{i,i+1}] = γ_{i-1} γ_{i+1}` | max err **2.22 × 10⁻¹⁶** |
| **C5** | Eqs. 39–41 + Gottesman–Knill argument | Each braid maps logical Paulis to logical Paulis (up to ±1 phase) → braids ⊂ Clifford. Explicit table given in `results.json`. | 9/9 mappings clean |
| **C5b** | Non-universality argument | Exhaustive enumeration of the group `⟨B_{1,2}, B_{2,3}, B_{3,4}⟩` on the parity-+1 code subspace (BFS to word length 8, canonicalised up to global phase) yields **exactly 24** distinct 2×2 unitaries — the single-qubit Clifford group order. This *quantitatively* confirms Roy–DiVincenzo's motivation (their Sec. 4) for magic-state–distilled π/8 and controlled-phase gates. | 24 = 24 ✓ |
| **C6** | Eq. 11 (Fig. 3) | Kitaev honeycomb gap: gapless ⇔ triangle inequalities `|Jx| ≤ |Jy|+|Jz|` (and cyclic). Tested via analytic minimum of `|Jx e^{ia} + Jy e^{ib} + Jz|` on 7 points spanning all four phases. | 7/7 match |

All checks pass; JSON summary in `report/evidence/results.json`.

## Estimate of work done

- ~30 min wall-clock end-to-end.
- ~250 lines of numpy simulator; ~40 lines matplotlib.
- 1 real GPU-backed Marker parse + 1 GPU-backed Nougat parse, driven from CherryRd via ssh.
- 6 concrete claims from the paper checked at machine precision. No fabricated numbers, no LLM-judged results, no approximations beyond IEEE-754 double.
