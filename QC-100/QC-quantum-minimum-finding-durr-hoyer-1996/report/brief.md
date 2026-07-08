# Brief — Dürr & Høyer 1996 (arXiv:quant-ph/9607014)

Independently replicated the Dürr–Høyer quantum minimum-finding algorithm from scratch in
pure NumPy statevector: Grover core (oracle+diffusion) + BBHT exponential-search subroutine
+ outer threshold-adopt loop. Over 300 trials at N∈{4,8,16,32,64}, empirical success
probability was 1.0 (paper's Theorem 1 requires ≥ 1/2) using the paper's exact iteration
budget ⌈22.5√N + 1.4·lg²N⌉. A separate BBHT t-sweep (N up to 128, t ∈ {1..N/2}) confirmed
the O(√(N/t)) expected-iteration scaling (measured mean/√(N/t) bounded < 0.81 across all
21 cells). Classical linear-scan baseline: exactly N probes always. LLM-judge (Argo
argo:gpt-5.2) verdict: PARTIAL — core claims reproduced but small-N range means the tight
≥1/2 bound isn't stress-tested.
