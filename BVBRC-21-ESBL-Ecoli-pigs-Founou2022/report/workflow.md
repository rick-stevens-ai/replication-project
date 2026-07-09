# Workflow — BVBRC-21 (Founou et al. 2022, ESBL *E. coli* from pigs)

**Paper:** Founou LL, Founou RC, Allam M, Ismail A, Essack SY (2022).
*Genome Analysis of ESBL-Producing Escherichia coli Isolated from Pigs.*
Pathogens 11(7):776 · doi:10.3390/pathogens11070776 · PMID:35890020 · PMC9323374.

**Verdict:** PARTIAL (borderline REPLICATED) — Coverage 10/10, Agreement 7/10 (LLM judge gpt-5.2).

---

## 0. Scope

- Replication target: the 11 clonally-related ESBL *E. coli* isolates (Cameroon + South Africa pig/abattoir sources) characterised by Founou et al. 2022.
- Primary analyzable unit: per-isolate WGS assembly.
- **Coverage this rerun: 11/11 isolates (100%).**

---

## 1. Data acquisition

1. **Enumerate WGS accessions** from the paper (Table 1 + Data Availability):
   - BioProject `PRJNA548686` (10 isolates)
   - BioProject `PRJNA412434` (isolate `PN256E8`)
2. **Fetch assemblies** from NCBI (`datasets download genome` / direct WGS `.fna` pull).
3. **Map accession ↔ paper isolate label** into `data/genome_accessions.tsv`.
4. **Land assemblies** in `data/genomes/` (11 × `.fna`, observed 4.62–5.35 Mb; paper: 4.5–5.3 Mb ✓).
5. **Transcribe paper ground truth** — Table 1 (MLST / phylogroup / serotype) and Table 2 (resistome) → `data/paper_table1.tsv`.

---

## 2. Analysis pipeline (all open-source, matched to paper tools where possible)

| Step | Paper tool | Replication tool | Output |
|------|------------|------------------|--------|
| MLST | Enterobase / MLST | `mlst 2.33.1` (scheme: `ecoli_achtman`) | `data/mlst_results.tsv` |
| Resistome | ResFinder | `abricate` vs NCBI DB | `data/abricate/ncbi.tsv` |
| Resistome | ResFinder | `abricate` vs ResFinder DB | `data/abricate/resfinder.tsv` |
| Plasmids | PlasmidFinder | `abricate` vs PlasmidFinder DB | `data/abricate/plasmidfinder.tsv` |
| Virulome | VirulenceFinder / VFDB | `abricate` vs VFDB | `data/abricate/vfdb.tsv` |

Driver: `scripts/run_all.sh` (iterates the 11 assemblies through the four abricate DBs plus `mlst`, writes per-tool merged TSVs).

---

## 3. Verification pipeline

For each paper claim, compare rerun table to `paper_table1.tsv`:

1. **Genome-size envelope** — min/max of `data/genomes/*.fna` sizes vs. paper's 4.5–5.3 Mb range.
2. **MLST per-isolate** — exact match on ST integer, per-isolate.
3. **CTX-M-15 prevalence** — count of isolates with a CTX-M-15 hit in abricate ncbi+resfinder; must match paper's 6/11 (54.54%) *and* the six carrier identities.
4. **Universal CTX-M** — every isolate carries some CTX-M variant.
5. **CTX-M-15 + TEM-1B co-carriage** — count isolates with both genes.
6. **PN256E8 multi-TEM composition** — allele-by-allele check.
7. **Resistome breadth** — presence of qnr, aph, tet, mph, sul, dfrA families.

---

## 4. Judging

Independent LLM judge (**gpt-5.2**) scores:

- **Coverage** — fraction of paper's analyzable units this rerun addresses. Here: **10/10**.
- **Agreement** — fraction of individual claims that match. Here: **7/10**.
- **Verdict** — one of `REPLICATED / PARTIAL / FAILED`. Here: **PARTIAL** (borderline REPLICATED — strongest of the PARTIALs in the batch).

Judge rationale: headline CTX-M-15 = 6/11 prevalence and carrier identities verified, genome-size envelope verified, MLST 10/11 exact; residual discrepancies in per-isolate β-lactamase composition (CTX-M-15+TEM-1B count +1; PN256E8 CTX-M allele + TEM-206) prevent a clean REPLICATED verdict.

---

## 5. Failure / partial-match handling

- **DB-vintage drift is the leading hypothesis** for every observed discrepancy. Not corrected in this rerun (pinned 2021 ResFinder snapshot would be the fix — see `open_questions.json`).
- **PR246B1C null MLST call** treated as an identity-cutoff artefact (sibling PR209E1, same paper ST2144 / same FimH87/B1, types cleanly).
- No isolates were dropped or excluded; all 11 flow through every step of the pipeline.

---

## 6. Artifacts produced

See `artifacts_summary.md` for the full artifact inventory and byte counts / row counts by file.

---

## 7. Reproducibility

- Fully re-executable via `scripts/run_all.sh` given `data/genome_accessions.tsv` and the four abricate DBs installed.
- Tool versions pinned: `mlst 2.33.1`, `abricate` (DB versions **not** pinned in this rerun — the single most impactful reproducibility improvement identified by the critique).
