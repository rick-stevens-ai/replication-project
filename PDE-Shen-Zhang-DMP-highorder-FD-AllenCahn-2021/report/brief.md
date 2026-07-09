# Brief

Independent complementary-angle replication of Shen & Zhang (CMS 20(5), 2022;
arXiv:2104.11813), "Discrete Maximum Principle of a High Order FD Scheme for a
Generalized Allen–Cahn Equation." From-scratch numpy/scipy solver for
uₜ = μΔu − ε⁻¹(u³−u) on Ω=[-1,1]^d, d∈{1,2}, using 2nd-order and compact
4th-order sparse Laplacians and stabilized IMEX backward-Euler. We independently
verify (a) the paper's 2nd-order companion scheme achieves O(h²) with observed
rates → 2.00 (1D) and (b) the discrete maximum principle holds empirically in
six real time-stepping runs at ε∈{0.01,0.1} with peak max|u|=0.997 (well
under 1). The paper's exact Q2 4th-order alternating stencil and Thm 3.9
monotonicity bound are handled by the sibling dir
`PDE-allen-cahn-maxprinciple-shen-zhang-2021`; this angle instead exercises the
DMP in real dynamics — complementary evidence, not duplication. LLM-judge
verdict (argo:gpt-5.4 via LiteLLM aggregator): **PARTIAL** — C2/C3 reproduced,
C1/C4 out-of-scope for this angle.
