# Marker parse (curated substitution) — arXiv:2007.11157

> Marker's full PyTorch pipeline was not run inside this subagent turn (model
> weights + install would exceed the wall-clock budget). Substituted with a
> targeted `pdftotext -layout` extraction of the paper's abstract, headline
> numbers, protocol description, and results tables. This file records the
> curated content that Marker would have produced for downstream consumers.

**Paper.** Valivarthi et al., "Teleportation Systems Towards a Quantum
Internet," arXiv:2007.11157v2 (2020), published as PRX Quantum 1, 020317.

**Authors (verified from PDF, first page):** Raju Valivarthi, Samantha Davis,
Cristián Peña, Si Xie, Nikolai Lauk, Lautaro Narváez, Jason P. Allmaras,
Andrew D. Beyer, Yewon Gim, Meraj Hussein, George Iskander, Hyunseong Linus
Kim, Boris Korzh, Andrew Mueller, Mandy Rominsky, Matthew Shaw, Dawn Tang,
Emma E. Wollman, Christoph Simon, Panagiotis Spentzouris, Neil Sinclair,
Daniel Oblak, Maria Spiropulu. Caltech / Fermilab / JPL / AT&T Foundry / U.
Calgary / Harvard.

## Abstract (verbatim)
> Quantum teleportation is essential for many quantum information technologies
> including long-distance quantum networks. Using fiber-coupled devices,
> including state-of-the-art low-noise superconducting nanowire single photon
> detectors and off-the-shelf optics, we achieve quantum teleportation of
> time-bin qubits at the telecommunication wavelength of 1536.5 nm. We measure
> teleportation fidelities of ≥ 90% that are consistent with an analytical
> model of our system, which includes realistic imperfections. To demonstrate
> the compatibility of our setup with deployed quantum networks, we teleport
> qubits over 22 km of single-mode fiber while transmitting qubits over an
> additional 22 km of fiber. Our systems, which are compatible with emerging
> solid-state quantum devices, provide a realistic foundation for a high-
> fidelity quantum internet with practical devices.

## Headline claims

| ID | Claim | Type | Testable in statevector reproduction? |
|----|-------|------|----------------------------------------|
| C1 | Time-bin qubit teleportation is performed using the standard BSM-based protocol at 1536.5 nm. | protocol-level | YES — reproduce the protocol as a 3-qubit circuit |
| C2 | Ideal-protocol fidelity is 1.0; hardware imperfections drive real F below unity. | analytical | YES — statevector run gives F=1 exactly |
| C3 | Average teleportation fidelity F_avg = 89 ± 1% without added fiber. | experimental (hardware) | NOT DIRECTLY — reproduce as an anchor for noise-model calibration |
| C4 | F_avg = 89 ± 1% with 22 km added fiber (i.e. no significant degradation). | experimental (hardware) | NOT DIRECTLY — anchor only |
| C5 | Decoy-state analysis: F_avg ≥ 89 ± 2%. | decoy method | analytical-only, out of scope for statevector sim |
| C6 | Entangled-Bell-state fidelity F_ent = 97.3 ± 0.2%. | experimental (hardware) | anchor only |
| C7 | The measured fidelities are consistent with an analytical model including realistic imperfections. | model consistency | partially — dephasing sweep reproduces the qualitative trend |

## Protocol summary (reconstructed for the reproduction)

1. **Alice** prepares an arbitrary time-bin qubit `|psi> = alpha|early> + beta|late>` (protocol-equivalent to any single-qubit state).
2. **Bob** generates an entangled Bell pair `|Phi+>_{AB} = (|00>+|11>)/sqrt(2)` and sends one half to the Bell-state-measurement station **Charlie**.
3. **Charlie** performs a Bell-state measurement (BSM) on Alice's qubit and Bob's half of the entangled pair. In the paper's optical implementation, this is a HOM interference + polarizing-beam-splitter projective measurement onto `|Psi->`.
4. **Classical channel:** Charlie announces the 2-bit BSM outcome to Bob.
5. **Bob** applies the corresponding Pauli correction (I, X, Z, or XZ) to his remaining qubit; the resulting state equals the input `|psi>`.

## Key numbers (locked from paper.txt for the reproduction target)

- Wavelength: 1536.5 nm (telecom C-band).
- Fiber length: 22 km single-mode (with an additional 22 km transmission arm).
- `F_avg = 0.89 ± 0.01` (without added fiber, quantum-state-tomography).
- `F_avg = 0.89 ± 0.01` (with added fiber).
- `F_ent = 0.973 ± 0.002` (Bell-state fidelity).
- Abstract-level headline: `F >= 0.90`.
- HOM visibility `V_+ ≈ 69.7 ± 0.91%` (without fiber).
