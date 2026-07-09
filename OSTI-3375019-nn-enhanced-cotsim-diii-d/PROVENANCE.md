# PROVENANCE — OSTI 3375019

## Paper
- **Title:** Neural-Network-Enhanced COTSIM: Advancing Predictive Capabilities for Fast DIII-D Simulations
- **DOI:** 10.1109/TPS.2026.3695483
- **OSTI id:** 3375019
- **PDF (attempted):** https://www.osti.gov/servlets/purl/3375019

## PDF acquisition
- **Status:** FAILED to download.
- **Attempts (2026-07-05, host CherryRd):**
  - `curl --max-time 45 https://www.osti.gov/servlets/purl/3375019` → timeout (exit 28)
  - `curl --max-time 20 https://www.osti.gov/biblio/3375019` → HTTP 000 (no response, timeout)
  - `curl --max-time 20 https://doi.org/10.1109/TPS.2026.3695483` → no fetch (IEEE paywall + resolve failure)
- **Control test:** curl to google.com and arxiv.org from same host succeeded (HTTP 200) — confirms outbound Internet works, and that OSTI + doi.org are specifically unreachable / very slow / rate-limiting this host at this time.
- **SHA-256 / bytes:** N/A (no file obtained).
- **Substitution:** none — no substitute PDF used. Method context derived from public sibling papers by the same COTSIM group found via web_search:
  - OSTI 1836249 "Neural network model of the multi-mode anomalous transport module (MMMnet) for accelerated transport simulations" (Nucl. Fusion 61, 2021).
  - OSTI 2536775 "Enabling model-based scenario control in EAST by fast surrogate modeling within COTSIM" (Fusion Eng. Des., 2025).
  - OSTI 2586635 (NSTX-U variant, surrogate models for MMM / GENRAY-CQL3D / NUBEAM).
  - ScienceDirect S0920379625001693 (EAST COTSIM surrogate paper, open metadata).

## What this means for the replication
- The DIII-D-specific COTSIM 3375019 PDF was NOT read directly. The **core claim class** ("NN surrogate replaces an expensive transport-physics module inside COTSIM to give large speedup with tolerable accuracy loss on DIII-D-like scenarios") is well-attested by the sibling COTSIM papers listed above and is the standard published pattern for this group.
- The replication in `work/` therefore tests the METHOD (NN surrogate vs numerical diffusive-transport solve) on a reduced 1D synthetic plasma-transport analog. It cannot claim to reproduce DIII-D-specific numbers.
- Verdict is bounded to SPOT-CHECK (method-level plausibility check), not REPLICATED.
