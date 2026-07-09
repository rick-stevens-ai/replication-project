# Marker parse — arXiv:1710.01022

**Source PDF:** `work/paper.pdf` (5.7 MB, 27 pages, PDF v1.5)
**Marker tool availability:** Marker (VikParuchuri/marker) was **not installed** in this environment at replication time (`which marker_single` returned not-found). The central corpus at `~/Dropbox/REPLICATE-PROJECT/corpus-parsed/` did not contain a pre-parsed copy for `1710.01022`.

**Fallback extraction used:** `pdftotext` (poppler) — the standard fallback per the QC wave brief when Marker is unavailable. The full extracted text is preserved in `work/paper.txt` (reflowed, 1808 lines) and `work/paper_layout.txt` (`-layout` mode, 1488 lines). Both were used to verify claims + extract coefficients.

## Paper metadata (verified from PDF)
- **Title:** Quantum optimization using variational algorithms on near-term quantum devices
- **Authors:** Nikolaj Moll, Panagiotis Barkoutsos, Lev S. Bishop, Jerry M. Chow, Andrew Cross, Daniel J. Egger, Stefan Filipp, Andreas Fuhrer, Jay M. Gambetta, Marc Ganzhorn, Abhinav Kandala, Antonio Mezzacapo, Peter Müller, Walter Riess, Gian Salis, John Smolin, Ivano Tavernelli, Kristan Temme
- **Affiliations:** IBM Research – Zurich (¹), IBM T.J. Watson Research Center (²)
- **arXiv:** 1710.01022v2 [quant-ph], 9 Oct 2017
- **Character:** Overview / review article — later published in Quantum Sci. Technol.

## Structure (verified against ToC on p.2 of PDF)
1. Introduction (p.2)
2. Quantum volume, a metric for near-term quantum devices (p.5)
3. Exploring Hilbert space with the variational quantum eigensolver (p.7)
   3.1 Variational quantum eigensolver method
4. Quantum chemistry with qubits (p.10)
   4.1 Mapping fermions to qubits
   4.2 Coupled cluster trial wavefunctions
   4.3 Hardware-efficient trial states suitable for near-term quantum hardware
   4.4 Small molecules calculated with the variational quantum eigensolver
5. Classical optimization with qubits (p.15)
   5.1 Quantum approximate optimization algorithm with short depth
   5.2 Variational quantum eigensolver applied to the MaxCut problem
6. Classical robust optimizers for measured expectation values (p.18)
7. Prospects of fighting decoherence without full error correction (p.19)
8. Conclusion (p.21)

## Reproducible-claim excerpts (verbatim locations in `work/paper.txt`)

### QAOA for MaxCut (§5.1, lines ~980–1050)
The paper introduces QAOA (Farhi-Goldstone-Gutmann 2014) with cost Hamiltonian
```
H_C = Σ_α h_α ⊗_{iα} σ^z_{iα}     (Eq. 17)
```
and mixer `H_M = -Σ σ^x_i`, then defines
```
U(β, γ) = Π_{l=1..D} e^{-i β_l H_M} e^{-i γ_l H_C}    (Eq. 18)
```
The paper cites Farhi-Goldstone-Gutmann 2014 (ref [41,42]) for the QAOA formulation. The **0.6924 approximation-ratio guarantee for QAOA p=1 on 3-regular graphs** is the FGG2014 baseline result that the paper builds on — it is the concrete testable number extracted for the QAOA half of this replication.

### VQE for small molecules (§4.4, lines ~830–905)
The 4-qubit STO-3G H₂ Hamiltonian is written explicitly (verbatim from paper):
```
H_{H2} = f0 · 1⊗1 + f1 · σz⊗σz + f2 · σz⊗1 + f3 · 1⊗σz + f4 · σx⊗σx    (Eq. after §4.4)
```
The paper discusses achieving **chemical accuracy** (~1 mHa / kcal-mol⁻¹ / 1.6 mHa) with hardware-efficient ansatz depths (D≈8 for H₂, D=28 for LiH/BeH₂). The **VQE-H₂ within chemical accuracy** claim is the concrete testable number extracted for the VQE half of this replication.

## Notes on parse quality
- `pdftotext` produced clean linear text; math notation is Unicode/ASCII (e.g. `σz`, `⊗`, `Σ`) — good enough for extracting coefficients and section structure.
- Figures + tables lost — see original PDF for Fig. 4 (H₂/LiH/BeH₂ dissociation curves) and Fig. 5 (QAOA MaxCut on 5-qubit device).
- Bibliography intact (95 refs); Farhi-Goldstone-Gutmann 2014 QAOA papers are refs [41], [42].

**Verdict:** parse quality is sufficient for the replication; a full Marker parse would additionally preserve equation LaTeX + figure crops but would not change the extracted testable numbers.
