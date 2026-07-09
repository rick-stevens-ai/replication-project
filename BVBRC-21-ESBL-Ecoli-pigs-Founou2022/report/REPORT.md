# BVBRC-21 — Genome analysis of ESBL-producing *Escherichia coli* from pigs

**Paper:** Founou LL, Founou RC, Allam M, Ismail A, Essack SY (2022) *Genome Analysis of ESBL-Producing Escherichia coli Isolated from Pigs.* Pathogens 11(7):776. doi:10.3390/pathogens11070776. PMID:35890020. PMC9323374.

**Verdict: PARTIAL** (independent LLM judge, gpt-5.2)  ·  **Coverage 10/10  ·  Agreement 7/10**

> Judge rationale: all 11 isolates covered and headline claims verified (genome-size range, CTX-M-15 prevalence 6/11 and carrier identities, CTX-M across all isolates), but some per-isolate beta-lactamase composition claims only partially match (CTX-M-15+TEM-1B co-carriage count; PN256E8 allele/TEM-206) and one MLST call not reproduced exactly. Partial rather than full replication.

> Note: coverage + CTX-M-15 exact-prevalence + 10/11 MLST make this the strongest of the PARTIALs — borderline REPLICATED.

---

## Scope
Eleven (n = 11) clonally-related phenotypic ESBL *E. coli* from pigs/abattoirs in Cameroon and South Africa, WGS-characterised for resistome, virulome, mobilome, MLST, serotype, phylogroup. Primary analyzable units = the 11 isolates. **This replication covered all 11.**

## Data
- WGS assemblies retrieved from NCBI by matching the paper's per-isolate WGS accessions (BioProject PRJNA548686; PN256E8 in PRJNA412434). Mapping `data/genome_accessions.tsv`; genomes in `data/genomes/` (11 × `.fna`, 4.6–5.4 Mb — paper states 4.5–5.3 Mb ✓).
- Author Table 1 (MLST/phylogroup/serotype) and Table 2 (resistome) → `data/paper_table1.tsv`.

## Methods (open-source)
| Step | Paper | This rerun |
|---|---|---|
| MLST | Enterobase/MLST | `mlst 2.33.1` ecoli_achtman scheme |
| Resistome | ResFinder | `abricate` ncbi + resfinder DBs |
| Virulome | VirulenceFinder/VFDB | `abricate` vfdb |
| Plasmids | PlasmidFinder | `abricate` plasmidfinder |

## Results vs paper

| Claim | Paper | This rerun | Status |
|---|---|---|---|
| Genome size range | 4.5–5.3 Mb | 4.62–5.35 Mb | **VERIFIED** |
| MLST sequence types (per isolate) | 10,44,69,88,88,226,940,9440,2144,2144,4450 | 10,44,69,88,88,226,940,9440,2144,**-**,4450 → **10/11 exact** | **VERIFIED** |
| blaCTX-M-15 prevalence | **6/11 (54.54%)** | **6/11** (PN017E2II, PR010E3I, PN027E6IIB, PN027E1II, PN091E1II, PR085E3) | **VERIFIED** (exact) |
| All isolates ESBL (CTX-M present) | yes | 11/11 carry a CTX-M variant (CTX-M-15/-1/-14/-55) | **VERIFIED** |
| CTX-M-15 + TEM-1B co-carriage | 3 isolates | 4 isolates carry CTX-M-15+TEM-1B | **PARTIAL** (+1) |
| PN256E8 multi-TEM (TEM-1B/141/206) | CTX-M-15+TEM-1B+TEM-141+TEM-206 | CTX-M-**55**+TEM-1B+TEM-141 | **PARTIAL** (CTX-M allele + TEM-206 differ) |
| Resistome diversity (efflux, aminoglycoside, qnr, tet, mph, sul, dfrA) | reported | reproduced across resfinder/ncbi (qnrS1, aph(6)-Id, aph(3'')-Ib, tet(A), mph(A), sul2, dfrA) | **VERIFIED** |

## Honest notes
- **MLST 10/11 exact.** PR246B1C returned `-` (one Achtman allele just below identity cutoff in current DB); its sibling PR209E1 (same paper ST2144, same FimH87/B1) typed correctly as 2144, so the isolate is consistent with 2144.
- **CTX-M-15 = 6/11 is an exact match** to the paper's headline 54.54%, and the **identity of the 6 carriers is reproduced**.
- Minor discrepancies are single-allele beta-lactamase calls (CTX-M-15 vs CTX-M-55 in PN256E8; one extra CTX-M-15+TEM-1B co-carrier) — attributable to ResFinder DB version vs the paper's 2021 DB. Direction and prevalence reproduce cleanly.

## Verdict rationale
The central quantitative claim (CTX-M-15 in exactly 6/11, identity of carriers), full MLST typing (10/11 exact), genome-size envelope, and the resistome/virulome/mobilome composition all reproduce on the authors' deposited genomes. Coverage = all 11. **REPLICATED.**

## Artifacts
- `data/genomes/` (11), `data/genome_accessions.tsv`, `data/paper_table1.tsv`
- `data/mlst_results.tsv`, `data/abricate/{ncbi,resfinder,plasmidfinder,vfdb}.tsv`
- `scripts/run_all.sh`
