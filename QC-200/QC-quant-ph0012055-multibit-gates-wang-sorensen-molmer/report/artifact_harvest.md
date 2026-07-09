# Artifact Harvest

## Public resources pulled

| URL | Description | Size | Checksum (SHA-256) |
|-----|-------------|------|--------------------|
| `https://arxiv.org/pdf/quant-ph/0012055` | arXiv v2 PDF of "Multi-bit gates for quantum computing" | 113,185 B | (see below) |

```bash
$ sha256sum ~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph0012055-multibit-gates-wang-sorensen-molmer/paper.pdf
$ shasum -a 256 paper.pdf  # macOS
```

## Related public reference (not pulled, cited)
- **Journal version:** Wang, Sørensen, Mølmer, *Multi-bit gates for quantum computing*, **Phys. Rev. A 64, 062309** (2001). DOI: 10.1103/PhysRevA.64.062309. Not pulled (paywalled behind APS; arXiv version is scientifically identical). Would be worth checking whether Eq. (5) constant term was corrected between arXiv and journal (see Open Question Q1).
- **Cited building block:** Sørensen & Mølmer, *Entanglement and quantum computation with ions in thermal motion*, **Phys. Rev. A 62, 022311** (2000). arXiv:quant-ph/0002024. Not pulled.
- **Cited experimental confirmation of Mølmer-Sørensen gate:** Sackett et al., *Nature* **404**, 256 (2000). Not pulled.

## Reused corpus artifacts

| Path in this dir | Origin | Provenance |
|---|---|---|
| `extraction/marker.md` | copied from `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-0012055-multi-bit-gates-quantum-computing/extraction/marker.md` | Same paper, previously parsed. Untouched in sibling. |
| `extraction/nougat.mmd` | copied from `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-0012055-multi-bit-gates-quantum-computing/extraction/nougat.mmd` | Same paper, previously parsed (hand-typed nougat-style). Untouched in sibling. |

## Not pulled (out of scope for this replication)
- Any GitHub reference implementation of the Wang-Sørensen-Mølmer scheme — none is cited in the paper; the paper is a theory letter.
- Actual ion-trap experimental data — the paper is a proposal, not an experimental report.
- Errata files from APS — not checked (see Open Question Q1).

## Machine-readable outputs (produced by this replication)
All under `report/evidence/`:
- `eq5_toffoli_results.json` — full K × N_ph × oscillator-state sweep of Eq. (5) fidelities
- `eq5_target_comparison.json` — literal-target vs Toffoli vs corrected-Toffoli fidelity
- `eq5_typo_hypothesis.json` — confirmation that `-σx3/(32K)` gives exact Toffoli
- `eq6_grover_results.json` — Eq. (6) identity + Eq. (10) UG + Grover search
- `grover_trajectory.json` — Grover P(x₀) vs iteration k for n=3..6
- `cnot_multibit_results.json` — Cⁿ-NOT fidelities
- `cnot_permutation_fidelity.json` — permutation-fidelity results
- `ghz_states.json` — GHZ generation via Jy²
- `llm_judge.txt` — LLM-judge verdict (Argo Opus 4.7)
