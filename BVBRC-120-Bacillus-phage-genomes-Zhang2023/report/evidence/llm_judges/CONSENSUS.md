# LLM-judge consensus — BVBRC-120

Three independent free-endpoint LLM judges via the cherryrd LiteLLM aggregator (`<tailnet-aggregator>:4000/v1`), routed through the free Argo proxy.

| Judge model | Verdict | Coverage | Agreement | Faithful? |
|---|---|---|---|---|
| argo:gpt-5.2 | PARTIAL | 0.50 | 0.75 | true |
| argo:gpt-4.1 | PARTIAL | 0.75 | 1.00 | true |
| argo:gpt-4o | PARTIAL | 0.75 | 1.00 | true |

**Consensus:**
- Verdict: **PARTIAL** (3/3 judges)
- Faithful: **true** (3/3 judges — the report's own PARTIAL self-assessment is honest, not inflated)
- Mean coverage: **0.67** — most testable claims attempted; some (WebMGA COG cargo, PHASTER prophage set) genuinely out of scope
- Mean agreement: **0.92** — attempted claims agree strongly with paper's numbers

Raw JSON responses in this directory.
