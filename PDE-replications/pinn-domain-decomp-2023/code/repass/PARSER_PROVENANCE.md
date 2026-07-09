# Parser Provenance — PINN Domain-Decomposition Re-Pass

**Paper source:** existing copy at
`/Users/stevens/Dropbox/REPLICATE-PROJECT/PDE-replications/pinn-domain-decomp-2023/paper/paper.pdf`
(MD5 verified identical to arXiv 2306.17648v2 fetched in pass 1).

**Parser used (re-pass):** `pdftotext -layout` (Poppler, system `/usr/local/bin/pdftotext`).
Output saved to `/Users/stevens/.openclaw/workspace/.tmp/pinn-dd-repass/paper.txt`
(1,440 lines). This was the source for all PDE definitions, Table 1, Table 3,
and Algorithm 3.1 used in the re-pass below.

**Why pdftotext and not the `pdf` tool:** the standard `pdf` MCP tool was unavailable
in this subagent session (Anthropic credits exhausted; Gemini variant disabled;
OpenAI variant required the document-extract plugin). `pdftotext -layout` produced
clean Table 1/3 reconstructions and full equation+text bodies; this was sufficient
to canonicalize every claim used in the re-pass.

**Self-fetch from arXiv:** not required (existing local PDF matches the published
SIAM J. Sci. Comput. version, doi:10.1137/23M1583375, arXiv 2306.17648v2).

**Verification checks executed against parsed text:**
- Table 1 (architectures × n_sd × k_s) recovered cleanly.
- Table 3 (Erel + time-to-solution for L-BFGS / ASPQN / MSPQN on Burgers, KG,
  Allen-Cahn) recovered cleanly.
- Algorithm 3.1 (SPQN pseudocode) recovered cleanly.
- Sec 5.2.1 quote on line search recovered: *"we employ cubic backtracking
  line-search method with strong Wolfe conditions [Dennis & Schnabel,
  Algorithm A6.3.1, pages 325-327]"*.
- Sec 5: hardware = Piz Daint XC50 node, NVIDIA Tesla P100 16GB, single GPU.

No fabrication.
