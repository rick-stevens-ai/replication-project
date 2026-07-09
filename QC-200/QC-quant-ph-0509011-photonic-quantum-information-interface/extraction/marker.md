# A Photonic Quantum Information Interface

**arXiv:** quant-ph/0509011v1 (1 Sep 2005)

**Authors:** S. Tanzilli¹, W. Tittel¹, M. Halder¹, O. Alibart¹, P. Baldi², Nicolas Gisin¹, and Hugo Zbinden¹

1. Group of Applied Physics, University of Geneva, 20 rue de l'École de Médecine, CH-1211 Geneva 4, Switzerland
2. Laboratoire de Physique de la Matière Condensée, Université de Nice–Sophia Antipolis, Parc Valrose, 06108 Nice Cedex 2, France

## Abstract

Quantum communication is the art of transferring quantum states, or quantum bits of
information (qubits), from one place to another. Photons represent the natural flying
qubit carriers for quantum communication, and the presence of telecom optical fibres
makes the wavelengths of 1310 and 1550 nm particularly suitable for distribution over
long distances. However, to store and process quantum information, qubits could be
encoded into alkaline atoms that absorb and emit at around 800 nm. Hence, future
quantum information networks made of telecom channels and alkaline memories will
demand interfaces able to achieve qubit transfers between these useful wavelengths
while preserving quantum coherence and entanglement. Here we report on a qubit
transfer between photons at 1310 and 710 nm via a nonlinear up-conversion process
with a success probability greater than 5%. In the event of a successful qubit transfer,
we observe strong two-photon interference between the 710 nm photon and a third
photon at 1550 nm, initially entangled with the 1310 nm photon, although they never
directly interacted. The corresponding fidelity is higher than 98%.

## Key equations

- Initial state (eq. 1):  |Ψ>_in = ( c1 |α1>_A ⊗ |β1>_B + c2 |α2>_A ⊗ |β2>_B ) ⊗ |0>_B'
- Desired transferred state (eq. 2):  |Ψ>_transfer = |0>_B ⊗ ( c1 |α1>_A ⊗ |β1>_B' + c2 |α2>_A ⊗ |β2>_B' )
- Effective Hamiltonian (eq. 3):  H = 1_A ⊗ [ g1 |0>_B<β1| ⊗ |β1>_B'<0| + g2 |0>_B<β2| ⊗ |β2>_B'<0| ] + h.c.
- Perfect transfer condition:  g1 = g2 ≡ g, |g| t = π/2 gives P_transfer = 1.
- Post-selected Franson state (eq. 7):  |Ψ>_post = (1/√2)( |s_A s_B> + e^{i(φ_A+φ_B)} |l_A l_B> )

## Key numeric claims

| # | Quantity | Value | Where in paper |
|---|----------|-------|----------------|
| C1 | Estimated QI-transfer success probability | ≈ 5 % (formula: 80%/W · 0.7W · 0.4² · 712/1312) | after eq. 6 |
| C2 | Net Franson visibility, source (before QI) | 97.0 ± 1.1 % | Fig. 2 caption |
| C2b | Raw Franson visibility, source | 87.4 ± 1.1 % | Fig. 2 caption |
| C3 | Net Franson visibility, after up-conversion | 96.2 ± 0.4 % | Fig. 3 discussion |
| C3b | Raw Franson visibility, after up-conversion | 86.4 ± 0.4 % | Fig. 3 discussion |
| C4 | Fidelity of the QI transfer | F = (1+V_net)/2 = 98.5 % (stated > 98 %) | Fig. 3 discussion |
| C5 | Pump laser coherence length | > 300 m | source description |
| C6 | Power reservoir (PR) power | 700 mW at 1560 nm | up-conversion stage |
| C7 | Classical up-conversion efficiency | 80 %/W of PR power | up-conversion stage |
| C8 | Waveguide coupling efficiency | 40 % | after-eq.-6 estimate |
| C9 | Single-photon coherence length | ≃ 150 μm (Δλ ≈ 15 nm) | Franson analyzer discussion |
| C10 | Interferometer path-length difference | ΔL ≈ 20 cm | Franson analyzer discussion |
| C11 | Bandpass filter around 712 nm | Δλ = 10 nm, > 30 dB rejection at 1550 nm | after up-conv stage |
| C12 | Bandpass filter on the 1555 nm arm | 1.5 nm | up-conv stage discussion |

## Extraction method

**Extractor:** *fallback: `pdftotext -layout paper.pdf`* (marker-pdf could not be installed
under Python 3.14 in the local venv: numpy build wheel unavailable). Body text was
manually reflowed to Markdown by the replication agent; equations transcribed by hand
from the source PDF; numeric claims cross-checked against the fetched arXiv PDF at
https://arxiv.org/pdf/quant-ph/0509011 (277 908 bytes, PDF v1.4, 7 pages).

See `report/failure_analysis.md` for the full note on the marker/nougat install issue.
