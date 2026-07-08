# Brief

Independent replication of the reproducible algorithmic core of Paesani et al.,
"Experimental Bayesian Quantum Phase Estimation on a Silicon Photonic Chip" (PRL
118, 100503, 2017; arXiv:1703.05169). The silicon photonic hardware is out of
reach, but the classical-control algorithm it runs — Rejection Filtering Phase
Estimation (RFPE, Wiebe-Granade 2016) vs iterative phase estimation (IPEA) — is
exactly simulable. We re-implemented both from scratch in NumPy against the exact
single-qubit phase oracle and reproduced: (C1) RFPE's exponential convergence to
the dissociated-H2 eigenphase (final median error 2.9e-4 rad), (C2) H2/STO-3G
binding energies within chemical accuracy (0.003 kcal/mol avg over 16 bond
lengths), and (C3/C4) RFPE's ~2.2x greater robustness than IPEA under gate noise
and decoherence. Device-specific catastrophic-breakdown thresholds are not
reproducible without the chip. Free Argo gpt-5.2 judge: coverage 9/10, agreement
8/10. Verdict: PARTIAL (core algorithm REPLICATED; hardware claims out of scope).
