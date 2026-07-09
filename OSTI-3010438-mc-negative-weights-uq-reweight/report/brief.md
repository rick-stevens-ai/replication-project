# Brief — OSTI 3010438 replication

Palmer & Kronheim (Phys. Rev. D 113, 012003, 2026) propose a general MC reweighting method for
samples containing negatively-weighted events: define g(x) = 2·P+(x) - 1 (per Eq. 5) and multiply
each event's weight by g(x), turning a signed sum into a positive sum with equal expectation
and reduced variance. Two uncertainty-quantification methods (event-by-event vs. PCA on
ensemble histograms) are developed for the case when g must be learned by a DNN. This replication
independently verifies the mathematical claims (C1-C3, C6) and the fully-controlled double-slit MC
demonstration (C4-C5) via a clean-room NumPy implementation with an LLM judge (Argo Claude
Opus 4.8) confirming reproducibility. The Sherpa/ATLAS V+jets HEP demonstration (Sec. V, C7) was
not replicated because it requires ATLAS OpenData PhysLite samples + DNN training beyond this
window; verdict is therefore PARTIAL (solid) rather than REPLICATED.
