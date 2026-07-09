# Artifact harvest

## Paper PDF
- Title: "A Robust Finite Element Method for Darcy–Stokes Flow"
- Authors: K. A. Mardal, X.-C. Tai, R. Winther
- Journal/year: SIAM J. Numer. Anal. 40(5), 1605–1631, 2002
- DOI: 10.1137/S0036142901383910
- Canonical URL (publisher, paywalled): https://epubs.siam.org/doi/10.1137/S0036142901383910
- Semantic Scholar OA pointer: https://dr.ntu.edu.sg/bitstream/10356/90843/1/Mardal-Tai-Winther-RFE-02.pdf (blocked by AWS WAF at time of harvest)
- Successful source (Wayback snapshot 2024-05-03): http://web.archive.org/web/20240503211425/https://dr.ntu.edu.sg/bitstream/10356/90843/1/Mardal-Tai-Winther-RFE-02.pdf
- Local file: `work/paper_MTW2002.pdf`
- SHA1: `c9eee758318fd70b95134e6c772d20fc5c38396e`
- Size: 270,981 bytes
- Pages: 28

## Reference software (used to *reproduce paper's negative results* only)
- scikit-fem v12.0.1 (Python FEM library). Used for the P2-P0, Mini, CR sweeps that reproduce paper Tables 3.1–3.9. Standard elements only.
- No pre-existing MTW-element implementation used. The MTW element itself was implemented in this repl from the paper's Lemma 4.1 spec.

## Code written for this replication (all in `work/`)
- `mtw_element.py` — local V(T) basis construction (numeric null-space of 11 constraints on P₃²) plus DOF-inverse, ~340 lines.
- `mtw_solver.py` — global assembly + Dirichlet BCs + saddle-point solve + error norms, ~530 lines.
- `darcy_stokes_standard.py` — P2-P0, Mini, CR reproductions via scikit-fem, ~300 lines.

## Evidence files (in `report/evidence/`)
- `standard_elements_results.json` — full error table (rel L² velocity & pressure) for P2-P0, Mini, CR, across all (ε, h).
- `mtw_convergence.json` — full error table (rel L² velocity, rel L² pressure, rel energy, absolute div-error) for MTW element across all (ε, h), plus fitted rates.
- `run_standard.log` — driver stdout for standard-elements sweep.
- `run_mtw.log` — driver stdout for MTW sweep.
- `mtw_selftest.log` — MTW basis 9-DOF unisolvence self-test output (DOF-of-basis = 9×9 identity, div φᵢ = P₀).
