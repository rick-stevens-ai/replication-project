# PROGRESS — PARTRAC analytical-formulas replication

## Paper identification

- **Source markdown:** `/data/stevens/lucid-corpus-extracted/LUCID-papers/2e71b349ed26bcca.md` (uicgpu)
- **Actual paper in MD:** Kundrát P, Friedland W, Becker J, Eidemüller M, Ottolenghi A, Baiocco G. *Analytical formulas representing track-structure simulations on DNA damage induced by protons and light ions at radiotherapy-relevant energies.* Sci Rep 10:15775 (2020). DOI 10.1038/s41598-020-72857-z
- **Note on task DOI:** task gave DOI `10.3390/cancers11020205`, which is McMahon & Prise 2019 (Cancers) — a review cited as ref [3] in the Kundrát paper. The markdown file content is unambiguously the Kundrát 2020 *Scientific Reports* paper. Proceeding with the markdown-as-truth and flagging the DOI mismatch as a friction tag.

## Replication classification

This is **NOT** a re-run of PARTRAC (no public PARTRAC binary, proprietary code at Helmholtz Zentrum München).
This **IS** an **analytical / figure replication**: re-implement the published analytical formulas (Eqs. 1 & 2) with the published fitted parameters (Tables 1 & 2), then:
1. Numerically reproduce the LET-dependent yield curves shown in Figs. 1–5
2. Confirm the paper's stated quantitative claims (low-LET yields, peak DSB-site values, RBE behavior, etc.)
3. Verify the qualitative trends discussed in Results & Discussion

## Timeline

- **2026-05-29 16:31** Spawned. Read source paper, set up project tree.
- **2026-05-29 16:35** Identified paper / DOI mismatch (flagged).
- **2026-05-29 16:40** Drafted formulas module and parameter tables in `code/`.

## Blockers / friction

- DOI in task differs from actual paper content (resolved by using markdown content).
- No raw PARTRAC simulation output is in the markdown; we can only compare the analytical fits against the **reported** ranges and headline numbers (e.g. "~64 direct SB per Gy per Gbp at low LET", "~7 DSB per Gy per Gbp at low LET", "~15 DSB sites per Gy per Gbp peak at 100-200 keV/µm"). Underlying PARTRAC numerical tables (the symbols in Figs 1–5) are not in the supplement we have access to. So claim-by-claim agreement is limited to (a) self-consistency at the universal low-LET parameter p1 and (b) headline yield ranges quoted in prose.

- **2026-05-29 17:10** Main agent took over after v2/v3 empty completions. Added `code/run_replication.py`, generated JSON/CSV results and four PNG figures, then wrote `README.md` and `REPORT.md`.
- **2026-05-29 17:10** Final local verdict: PARTIAL / analytical-figure replication. Full PARTRAC rerun and raw symbol comparison blocked by unavailable proprietary simulator/raw tables.
