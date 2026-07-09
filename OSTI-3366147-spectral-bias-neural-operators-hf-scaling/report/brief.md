# Brief

Independent replication of Khodakarami, Oommen, Bora, Karniadakis (2026),
"Mitigating spectral bias in neural operators via high-frequency scaling for
physical systems" (Neural Networks 193:108027; OSTI 3366147). We
re-implemented the HFS latent-space scaling module (paper Eqs. 4-6) and the
band-partitioned spectral error metric (paper Eq. B.3) inside a ResUNet-style
convolutional neural operator (PyTorch) and evaluated it on a synthetic 2D
multiscale-field operator-learning task designed to preserve high-frequency
energy in the target (BubbleML / Kolmogorov datasets were out of scope on
free compute). Across 3 seeds on an A100, spectral bias (C1) and negligible
parameter overhead (C3) are cleanly confirmed; overall relative-L2
improvement (C4) is directional but small and inconsistent; the paper's
headline claim that HFS reduces the **high-frequency** spectral error (C2)
is **not** reproduced (F_high change is −0.4% to −0.5% in every seed).
Verdict: PARTIAL.
