# Paper Provenance

- Target: OSTI 3022804 — "Physics-informed machine learning exploration of Na storage mechanisms in disordered carbon"
- Full citation (confirmed via web search of DOI): Nikhil Rampal, Stephen E. Weitzner, Fredrick Omenya, Marissa Wood, David M. Reed, Xiaolin Li, Jonathan R.I. Lee, Liwen F. Wan. *Energy Storage Materials* **2026**, 86, 104967. DOI: 10.1016/j.ensm.2026.104967.
- Corresponding author affiliations (typical for this group): LLNL / PNNL.

## PDF acquisition
- `https://www.osti.gov/servlets/purl/3022804` — unreachable from this subagent host (curl exit 28 timeout; alternate OSTI URLs also 000). No PDF SHA-256 available.
- `web_fetch` of DOI resolver returned 406; OSTI biblio page timed out.
- Substitution/basis for method-level replication: publicly indexed metadata (title, authors, journal) plus canonical PIML-for-battery-anode workflow (MLIP fit to DFT + MD sampling + PIML relationships between local coordination and adsorption/insertion energies) as reported in this paper family (see e.g. related work JACS 2021 PDF/NMR hard-carbon studies, Energy&Fuels 2022 ReaxFF hard-carbon studies).
- No PDF was hallucinated. The claims table below is stated at method/family level and the replication is an honest synthetic-toy test of the PIML relationship kernel, not a bit-for-bit reproduction.
