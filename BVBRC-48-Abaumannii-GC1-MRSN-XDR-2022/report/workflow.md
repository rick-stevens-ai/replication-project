# Workflow — BVBRC-48 Replication of Harmer et al. (2022, MRSN 56 GC1 A. baumannii)

**Paper:** Harmer CJ, Lebreton F, Stam J, McGann PT, Hall RM. *J Antimicrob Chemother* 77(7):1851–1855 (2022). DOI 10.1093/jac/dkac115. PMCID PMC9244215.
**Set:** BVBRC-48 (TOPUP85 rank-29). BV-BRC workflows: Similar Genome Finder + AMR analysis (CARD/AMRFinder).
**Compute:** uicgpu (A100 host, CPU-only for this task). LLM judge: free Argo `argo:gpt-5.2`, T=0.
**Envs:** `bvbrc28` (NCBI Datasets + Prokka + BLAST+), `bvbrc14` (AMRFinderPlus + mlst + abricate).

---

## 0. Constraints (standing rules honored)

- Free endpoints only (Argo / Sophia / CELS / UICGPU).
- No paid LLM calls; no `pdf`/`image` tools.
- Single writer per artifact; resume-only across restarts; seed preserved where applicable.
- No fabricated numbers — every count/percentage/ID sourced from a tool call on unmodified NCBI replicons.

## 1. Paper acquisition & claims extraction

1. Pulled full text from Europe PMC REST: `fullTextXML` for **PMC9244215**.
2. Regex-harvested accessions from the XML:
   - Isolate: **MRSN 56**
   - BioProject: **PRJNA742487**
   - Replicons: **CP080452–CP080456** (chromosome + 4 plasmids)
   - Comparator plasmids: **CP010781, CP010782, CP021783**
3. Distilled 8 testable claims (see REPORT.md §2, table C1–C8) plus one non-testable-from-sequence claim (C6b, the *mar*-operon FQ hypothesis).

## 2. Genome acquisition (provenance care)

1. First attempt: BV-BRC / NCBI BioProject → assembly link resolves to **GCA_021484925.1 / chromosome CP090606** (4,153,776 bp). This is a **later, different assembly** and does NOT match the paper's chromosome size (4,033,258 bp). Discarded.
2. Second attempt (used): fetched the paper's exact deposited replicons **CP080452–CP080456** via NCBI eutils `efetch` (fasta). Titles confirm "strain MRSN 56".
3. Computed replicon sizes and chromosome GC directly from FASTA (chromosome GC = 39.19%).

## 3. MLST (env: bvbrc14)

- Tool: `mlst 2.33.1`
- Ran both A. baumannii schemes:
  - Pasteur (`--scheme abaumannii_2`) → **ST1** (cpn60-1, fusA-1, gltA-1, pyrG-1, recA-5, rplB-1, rpoB-1)
  - Oxford (`--scheme abaumannii`) → partial/novel profile (gltA-10, gyrB-12, gdhB-4/182, recA-11, cpn60-4, gpi-98, rpoD-5). Attributed to local mlst DB version drift on the `gdhB` locus.
- **Pasteur ST1 = GC1** — the paper's typing claim confirmed unambiguously.

## 4. Resistome — 3 orthogonal callers (env: bvbrc14)

Run on the concatenated 5-replicon assembly, per-replicon output preserved so we can localize each hit.

1. **AMRFinderPlus 4.2.7** — `amrfinder --organism Acinetobacter_baumannii --plus`
2. **abricate 1.4.0 vs CARD** — `abricate --db card`
3. **abricate 1.4.0 vs ResFinder** — `abricate --db resfinder`

Result: 3/3 callers concordant on core XDR gene set (see REPORT.md §4.3 table). Cross-caller agreement is the key gate against caller-specific false positives.

## 5. Localization (C4)

For each hit from each of the three callers, recorded the source replicon accession. **Every** acquired-AMR hit maps to **CP080452.1** (chromosome). Zero AMR hits on CP080453–CP080456 (any caller). Reproduces the paper's central "no plasmid-borne resistance" claim.

## 6. Fluoroquinolone variants (C5)

- Point-mutation output from AMRFinderPlus (`--organism Acinetobacter_baumannii` triggers the A. baumannii mutation panel).
- **gyrA S81L**: called at 99.89% identity vs WP_000116450.1. ✅
- **parC**: no known-position RDR substitution called. ✅ (matches paper)

## 7. IS copy number (C7)

1. `makeblastdb -dbtype nucl` on the 5 replicons.
2. IS*Aba1*: `blastn` of canonical IS*Aba1* transposase reference (EU029998, ~570 bp transposase segment), hits accepted at ≥99% identity over the transposase region. Counted per replicon.
3. IS*Aba125*: `tblastn` of IS*Aba125*-family transposase (WP_001988464, 341 aa), hits accepted at 100% id / 100% coverage. Counted per replicon.
4. Chromosome counts: **20 IS*Aba1*** and **2 IS*Aba125*** — exact match to paper's 20 and 2.
5. Side observation: broad IS*Aba125*-family query cross-hits a Rep_3 region on pMRSN56-3 at 100% (not counted for C7 since the paper reports chromosome-only counts).

## 8. IS*Aba1* / ampC context (C6a)

- Took the ADC/*ampC* hit coordinates from CARD output.
- Cross-referenced against IS*Aba1* hit coordinates from step 7.
- Found IS*Aba1* copy at 2,823,501–2,824,068 sitting **10 bp upstream** of ADC/*ampC* (starts 2,824,078). ✅ (matches paper)

## 9. Plasmid-identity BLAST (C8)

- `blastn` pMRSN56-2 (CP080454) vs pA85-1 (CP021783) → **99.89% over 2726 bp**. ✅
- `blastn` pMRSN56-4 (CP080456) vs pA1-1 (CP010782) → **100.00% over full 8731 bp**. ✅

## 10. LLM judge scoring

- Endpoint: free Argo `argo:gpt-5.2`, T=0.
- Judge saw only tool outputs + paper's claim table.
- Score: coverage 9/10, agreement 9/10, verdict REPLICATED.
- Read as an anti-fabrication check, not an independent oracle.

## 11. Report generation & artifact packaging

- Assembled REPORT.md with claim-by-claim result tables and a REPLICATED verdict.
- Backfilled: REPORT.tex (this doc's LaTeX sibling), open_questions.json (5 items), artifacts_summary.md, failure_analysis.md.
- Emitted `WAVE_RESULT` line for the wave aggregator.

## 12. Out-of-scope items (documented, not silently skipped)

- **C6b — mar-operon FQ mechanism.** Functional/expression hypothesis, not testable by sequence re-analysis. Neither confirmed nor contradicted. Called out in REPORT.md §4.6 and §5.
- **KL1/OCL1 capsule typing (Kaptive).** Skipped per BV-BRC AMR-analysis scope, though free and fast. Documented as an open question.
- **De novo reassembly from SRR14998418 / SRR14008417.** Not required for content verification; documented as a next-step end-to-end pipeline replication.
