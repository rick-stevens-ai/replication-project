# Brief — QC-quant-ph9602016 (Beckman, Chari, Devabhaktuni, Preskill 1996)

**What.** Independently reproduced the Sec. VII "factor 15 with 6 qubits and 38 laser pulses" claim of Beckman-Chari-Devabhaktuni-Preskill 1996 by building the paper's Eq. (7.5) EXP_N(x=7, N=15) network gate-for-gate in Qiskit, running the full 6-qubit circuit on a statevector simulator, and cross-checking with a generic 12-qubit Shor QPE.

**Why.** This paper is the foundational proof-of-principle-scale resource-estimate for Shor's algorithm on ion traps, and its Sec. VII 6-qubit circuit is the canonical "small enough to demonstrate" benchmark that shaped the entire 1996-2001 experimental Shor-factoring push. Verifying that the paper's Eq. (7.6) [6, 0, 4] gate count and 38-pulse budget hold up 30 years later on modern simulator infrastructure closes a very old loop.

**Result.** REPLICATED — all six tested claims (C1-C6) reproduced exactly. Free-endpoint LLM judge (`argo:gpt-5.4`) confirms.
