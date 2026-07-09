# Workflow — Replication of Yamaguchi et al. 2018 (NIES-2481 genome announcement)

**Paper:** *Complete Genome Sequence of Microcystis aeruginosa NIES-2481 and Common Genomic Features of Group G M. aeruginosa*, J. Genomics 6:30–33 (DOI 10.7150/jgen.24935).
**Analyst:** Ollie (OpenClaw AI) — bvbrc-99, 2026-07-04.
**Verdict driver:** All quantitative genome-level claims re-derivable from the deposited NCBI records (CP012375 chromosome + CP025929 plasmid for NIES-2481; CP011304 + CP026286 for sister strain NIES-2549) with a plain Biopython + BLAST+ toolchain.

---

## 0. Setup

- Host: laptop (macOS, Homebrew Python 3.13).
- Toolchain: Biopython 1.87, NCBI BLAST+ 2.17.0+, curl (for NCBI E-utilities REST).
- No auth needed, no institutional data access. All artifacts come from public NCBI + PMC.
- No LLM inference was used as evidence — this is a pure quantitative-agreement replication.

---

## 1. Paper acquisition

1. Fetch PMC full text of PMC5865083 with `curl` (CC BY-NC, open access).
2. Extract the numeric claims from Table 1 (genome overview) and the Results & Discussion paragraph comparing NIES-2481 to NIES-2549.
3. Enumerate the testable claims (C1–C15) — see `REPORT.md` §2.

---

## 2. Data acquisition (public NCBI, no auth)

Via NCBI E-utilities `efetch`:

| Accession | UID | Record | Purpose |
|---|---|---|---|
| CP012375 | 1052158287 | NIES-2481 chromosome (FASTA + GBK) | C1, C3, C5, C6, C7, C9, C10 |
| CP025929 | 1333047330 | NIES-2481 plasmid (FASTA + GBK)    | C2, C4, C8, C9 |
| CP011304 | –          | NIES-2549 chromosome (FASTA + GBK) | C11, C12, C10 (sister comparison) |
| CP026286 | –          | NIES-2549 plasmid (FASTA + GBK)    | plasmid comparison |
| BAG03679.1 (+2 WP orthologs) | – | Canonical McyA reference proteins (2,787 aa each) | C9 (microcystin absence, independent verification) |

All fetches used the pattern:
```
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=<UID>&rettype=gbwithparts&retmode=text" -o <ACC>.gbk
```

---

## 3. Genome-level statistics (Biopython 1.87)

For each FASTA/GBK record:

1. **Length:** `len(record.seq)` → tests C1, C2.
2. **GC%:** `(record.seq.count("G") + record.seq.count("C")) / len(record.seq) * 100` → tests C3, C4.
3. **Feature-type histogram:** iterate `record.features` and count `feature.type` → tests C5 (rRNA), C6 (tRNA), C7 (CDS), C8 (CDS on plasmid), C12 (NIES-2549 CDS).
4. Cross-check with the paper's Table 1 row-by-row.

---

## 4. 16S rRNA identity (C10)

1. Iterate every `rRNA` feature in both chromosomes.
2. Filter by product qualifier: `"16S ribosomal RNA"` for NIES-2481; also allow `"small subunit ribosomal RNA"` for the SEED-annotated NIES-2549 record.
3. Extract the 16S sequences via `feature.extract(record.seq)` (this respects strand automatically).
4. Confirm all 4 extracted copies are length 1,460 bp (they are).
5. Compute pairwise ungapped identity `sum(a==b) / L * 100` for all 4 NIES-2481 × NIES-2549 pairs. Test both orientations for safety.
6. Report the minimum, mean, and max identity across the 4 pairs (all three = 100.0%).

---

## 5. Microcystin (mcy) absence — independent verification (C9)

The paper's antiSMASH-based absence claim is re-checked by direct protein-vs-nucleotide homology search:

1. `makeblastdb -in CP012375_chromosome.fasta -dbtype nucl`
2. `makeblastdb -in CP025929_plasmid.fasta -dbtype nucl`
3. `tblastn -query mcyA_refs.fasta -db CP012375_chromosome -evalue 1e-5 -outfmt 6 -out mcyA_vs_chrom.tsv`
4. Same for the plasmid.
5. Apply the strict-orthology filter: keep rows with `pident >= 70 AND (alignment_length / query_length) >= 0.80`.
6. Count strict hits (must be 0 for a true absence claim) and total permissive hits (nonzero is expected — see step 7).
7. **Biological positive control:** the ~117 low-identity chromosome hits at ≤50% pid are the *expected* NRPS-module cross-hits to aeruginosin/micropeptin/microviridin (which the paper says ARE present). Their existence proves the tblastn search worked and is not silently null; their sub-threshold identity proves none of them is a true `mcyA` ortholog.

---

## 6. NIES-2481 vs NIES-2549 chromosome-size delta (C11)

1. `size_diff = len(CP012375.seq) - len(CP011304.seq)`
2. Compare against the paper's stated `+1,207 bp (NIES-2481 larger)`.
3. Magnitude matches exactly (1,207 bp). Sign is reversed on the deposited records — flagged as probable paper typo in the report.

---

## 7. Out-of-scope items (deliberately deferred)

- **C14 (28 antiSMASH clusters):** would need an antiSMASH v7+ run; deferred to a follow-up on uicgpu.
- **C15 (5 CRISPR loci):** would need CRISPRCasFinder / CRISPRCasTyper; also deferred.
- **Full Table 2 COG re-annotation:** the paper's COGNIZER pipeline was not redistributed exactly; spot-checked one enrichment (transposase-labeled CDS = 34), which is internally consistent.

---

## 8. Deliverables

- `report/REPORT.md`, `report/REPORT.tex` — narrative + genuine-critique replication report.
- `report/open_questions.json` — five biologically-grounded open questions for follow-up.
- `report/workflow.md` — this file.
- `report/artifacts_summary.md` — index of the input/derived artifacts.
- `report/failure_analysis.md` — post-mortem of the one direction-reversed comparison and the out-of-scope claims.
- `evidence/summary_stats.json` — raw JSON of every derived number (referenced from REPORT.md Appendix A).

---

## 9. Reproduction summary

Everything above completes in under 15 minutes on a laptop with Python 3, Biopython 1.87, and BLAST+ 2.17 (roughly: 2 min data fetch, 1 min feature stats, 30 s 16S identity, 5–10 min BLAST database build + tblastn on ~4.4 Mb genome vs three 2.8 kaa proteins).
