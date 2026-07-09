# LLM-judge scoring (free endpoints only)

Two independent judges, both free CELS endpoints (no Anthropic/OpenAI/OpenRouter).

## Judge 1 — llama70 (Llama-3.3-70B-Instruct on CELS chicago-2)
VERDICT: REPLICATED
SCORE: 98
JUSTIFICATION: The replication report successfully reproduces all central quantitative claims, including assembly-level statistics, BGC count, and the presence of the pfa cluster, with exact or near-exact matches to the original paper.
COVERAGE: 8/11
AGREEMENT: HIGH

## Judge 2 — nemotron-3-ultra (NVIDIA Nemotron-3-Ultra-NVFP4 on CELS chicago-4)
VERDICT: REPLICATED
SCORE: 95
JUSTIFICATION: All central quantitative claims (genome length, CDS count, strand distribution, exact BGC count of 47, pfa cluster locus tags and architecture) are independently reproduced with matching numbers.

## Consensus
Both judges: REPLICATED. Mean score = (98+95)/2 = **96.5** → conservative reported = **96**.
