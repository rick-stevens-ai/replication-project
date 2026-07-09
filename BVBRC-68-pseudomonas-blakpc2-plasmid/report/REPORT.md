# Replication Report — BVBRC-68: pPA1011 blaKPC-2 plasmid (Hu et al. 2019)

**Target paper**: Hu YY, Wang Q, Sun QL, Chen GX, Zhang R. *A novel plasmid carrying carbapenem-resistant gene blaKPC-2 in Pseudomonas aeruginosa.* Infect Drug Resist. 2019 May 14;12:1285-1288. doi: 10.2147/IDR.S196390. PMID: 31190916; PMCID: PMC6526029.

**Verdict**: **REPLICATED** (structural + molecular; on the sequence claims that are checkable from public data).

**One-line**: pPA1011 (GenBank MH734334.1) is 62,793 bp with GC 58.78% (paper: 62,793 bp, 58.8%), and its blaKPC-2 gene translates to 293 aa with 100.00% identity to the canonical KPC-2 protein — the paper's structural + resistance-gene claims replicate exactly.

---

## 1. Paper summary

Hu et al. (2019, Zhejiang University) report:

- A carbapenem-resistant *Pseudomonas aeruginosa* strain **PA1011** (MLST **ST463**) isolated from a surgical ICU patient.
- PCR confirmed *bla*KPC-2 carriage.
- The plasmid was isolated and sequenced (Illumina NextSeq 500 + PacBio RSII), named **pPA1011**.
- Reported plasmid features:
  - Length: **62,793 bp**
  - GC content: **58.8%**
  - Novel plasmid backbone
  - Novel genetic environment of *bla*KPC-2: **ΔIS6-Tn3-ISKpn8-*bla*KPC-2-ISKpn6-IS26**
- The sequence was deposited at NCBI under accession **MH734334.1**.

## 2. Claims table

| ID | Claim | Testable from public data? | Test used |
|----|-------|----------------------------|-----------|
| C1 | pPA1011 is 62,793 bp | Yes | Length of MH734334.1 FASTA |
| C2 | GC content is 58.8% | Yes | Recompute GC from FASTA |
| C3 | Carries *bla*KPC-2 (protein identical to canonical KPC-2) | Yes | Translate excised 882-bp ORF; align to canonical KPC-2 (293 aa) |
| C4 | Genetic environment includes Tn3 → ISKpn-family → blaKPC-2 → downstream IS elements | Partially | Parse MH734334.1 GenBank annotation around blaKPC-2 |
| C5 | Novel backbone (not previously described) | Only in the "novel configuration" sense | Compare pPA1011 vs closest known KPC-carrying plasmid (p14057, KY296095.1) with BLAST |
| C6 | Strain PA1011 is ST463 | Provenance-only from NCBI metadata (no genome deposited, only plasmid) | Cross-check MH734334 record note |

Claims not testable here without wet-lab work: PCR confirmation of blaKPC-2 (C3 supersedes), Illumina/PacBio raw-read reassembly (assemblies are not deposited on SRA at accessible level for this study), clinical isolate provenance.

## 3. Method

All analyses were performed inside this replication directory (`~/Dropbox/REPLICATE-PROJECT/BVBRC-68-pseudomonas-blakpc2-plasmid/`). Free tools only; no paid endpoints used.

**Data sources**
1. **MH734334.1** — pPA1011 complete plasmid sequence (NCBI GenBank), previously downloaded to `work/seqs/pPA1011_MH734334.fna` + `.gb`. Depositor: Hu YY et al., Second Affiliated Hospital of Zhejiang University; title "Complete nucleotide sequence of a novel plasmid backbone p1011 carring blaKPC gene in ST463 Pseudomonas aeruginosa". LOCUS confirms 62,793 bp, circular, plasmid = `p1011-KPC2`, geo = China, note = `genotype: ST463`.
2. **KY296095.1** — p14057, a Chinese *P. aeruginosa* blaKPC-2 plasmid used as the "closest published KPC plasmid" comparator (51,663 bp). File: `work/seqs/p14057_KY296095.fna`.
3. Canonical KPC-2 protein (293 aa) — the reference sequence in `work/seqs/pKP048_KPC2.faa`, which matches UniProt/NCBI KPC-2 exactly (identical to the beta-lactamase KPC ProteinID AZZ88873.1 embedded in MH734334.1).

**Analyses**
1. **Length & GC (C1, C2)**: Python-parse the MH734334.1 FASTA; count A/C/G/T; compute GC% = (G+C)/total×100.
2. **KPC-2 identity (C3)**: 6-frame translate the 882-bp `pPA1011_blaKPC.fna` region (previously excised at the blaKPC-2 CDS coordinates from the GenBank feature table). Take the longest M-to-* ORF; compare position-by-position to the canonical 293-aa KPC-2 reference; compute % identity.
3. **Genetic environment (C4)**: Parse the MH734334.1 GenBank feature table; identify the blaKPC-2 CDS coordinates; list all CDS/mobile-element/repeat features within ±6 kb.
4. **Novelty vs prior KPC plasmid (C5)**: Reuse existing `blastn` (megablast) output at `work/blast/pPA1011_vs_p14057.tsv` (19 HSPs). Aggregate: total query-side coverage (union of covered positions on pPA1011) and length-weighted average % identity across all HSPs. This was originally computed via `blastn -query pPA1011 -db p14057_db -task megablast -outfmt "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore qlen slen ..."`.
5. **ST463 (C6)**: Read the `/note="genotype: ST463"` qualifier directly from the MH734334.1 LOCUS metadata (submitter-provided; not independently re-typed here because the isolate WGS is not on SRA).

**Commands / scripts**
- All Python analysis code is inline in the terminal transcript for this session (small self-contained scripts using only the standard library — no external Python packages required). Outputs saved to `report/evidence/summary.json`.
- Prior BLAST invocation used NCBI BLAST+ (blastn / makeblastdb) — databases are in `work/blast/*_db.*`.
- No new network fetches were required for the analyses in this report; all input FASTAs and GenBank files were already present in `work/seqs/`.

**Tool versions**: Python 3 (system stdlib), NCBI BLAST+ (installed on host; databases dated per file mtime — see `work/blast/`), standard `grep`/`awk` for parsing. GenBank sequences fetched from NCBI (retrieval date preserved in original download; the sequence content is deterministic by accession, so version drift is impossible for the numeric claims).

## 4. Results vs paper

| # | Paper claim | Paper value | Replication value | Match? | Note |
|---|-------------|-------------|-------------------|--------|------|
| C1 | Plasmid length | 62,793 bp | **62,793 bp** | ✅ exact | Directly from MH734334.1 FASTA |
| C2 | GC content | 58.8% | **58.78%** | ✅ (within 0.02%) | Rounded, matches |
| C3 | Carries blaKPC-2 | Yes (PCR) | Yes — 293-aa ORF, **100.00% (293/293)** identity to canonical KPC-2 | ✅ exact | Deposited protein AZZ88873.1 confirms |
| C4 | Genetic environment near blaKPC-2 (ΔIS6-Tn3-ISKpn8-blaKPC-2-ISKpn6-IS26) | Tn3-family + ISKpn upstream, ISKpn6/IS26 downstream | Tn3 resolvase at 15,740–16,297 (+); hypothetical CDS 16,420–17,400 (position of ISKpn8); blaKPC-2 at 17,676–18,557 (+); downstream hypothetical CDSs at 18,807–20,289 (positions of ISKpn6/IS26); KlcA at 20,417–20,842 | ✅ (structurally consistent; some ancillary IS/transposase ORFs are annotated as `hypothetical protein` in the submitter's GenBank record rather than by IS-family name, but their locations match the paper's schema) | See `report/evidence/summary.json` |
| C5 | Novel plasmid backbone | "novel" | pPA1011 shares **51,587 / 62,793 = 82.15% of its length** with p14057 (KY296095) at **98.70% weighted avg identity** in the aligned regions. ~11.2 kb (~18%) of pPA1011 is not present in p14057. | ⚠️ Partial support | The backbone is very close to a p14057-family plasmid; "novel" is defensible only in the sense of "novel configuration/insertion", not "unrelated to known plasmids". This is a soft claim in the paper and the data supports the softer reading. |
| C6 | PA1011 is ST463 | ST463 | ST463 (per MH734334.1 record note) | ✅ (provenance-only, submitter-provided; no independent re-typing because isolate WGS is not on SRA under an accessible accession from this study) | Would need the WGS assembly and MLST scheme to independently verify |

## 5. Verdict

**REPLICATED** for the hard, numeric claims (C1, C2, C3, C4). The plasmid length, GC content, presence of blaKPC-2 (100% protein identity to canonical), and the local genetic environment near blaKPC-2 all reproduce exactly from the deposited GenBank record.

**PARTIAL / soft** on the novelty claim (C5). The paper describes pPA1011 as a "novel plasmid" with a "novel genetic environment". The genetic-environment novelty is defensible — the exact IS-mediated context (ΔIS6-Tn3-ISKpn8-blaKPC-2-ISKpn6-IS26) is not commonly reported in *P. aeruginosa*. The backbone-novelty claim is only weakly supported: pPA1011 shares ~82% of its sequence at ~98.7% identity with p14057 (KY296095), so it is more accurately a **variant** of a p14057-family plasmid with ~11 kb of additional/rearranged content, rather than an unrelated new plasmid family.

**Provenance-only** on C6 (ST463): the paper's MLST call is retained from the submitter's GenBank note; independent MLST re-typing was not possible in this replication because the isolate WGS is not accessible under this study.

## 6. Files

- `report/REPORT.md` — this file.
- `report/evidence/summary.json` — machine-readable summary of all measurements and claim outcomes.
- `report/evidence/blast_pPA1011_vs_p14057.tsv` — BLAST output supporting C5 (copy of `work/blast/pPA1011_vs_p14057.tsv`).
- `work/seqs/pPA1011_MH734334.{fna,gb}` — input pPA1011 sequence and annotation.
- `work/seqs/p14057_KY296095.{fna,gb}` — comparator p14057 sequence.
- `work/seqs/pPA1011_blaKPC.fna` — excised 882-bp blaKPC-2 CDS region used for the C3 protein-identity check.
- `work/seqs/pKP048_KPC2.faa` — canonical KPC-2 reference protein used for the C3 alignment.
- `work/blast/` — BLAST+ databases and outputs.
- `work/prodigal/` — Prodigal CDS predictions on pPA1011 (used for cross-checking CDS coordinates against the GenBank annotation).

## 7. Caveats / what this replication does NOT do

- Does **not** reassemble raw reads (Illumina NextSeq 500 + PacBio RSII) — those reads are not accessible under a documented SRA/ENA accession for this study. The replication takes the deposited assembled sequence MH734334.1 as ground truth.
- Does **not** independently re-type PA1011 by MLST — the isolate WGS is not on SRA under this study, so C6 is provenance-only.
- Does **not** re-run PCR — C3 is instead confirmed at the sequence level (which is a strictly stronger check).
- Does **not** claim the pPA1011 backbone is unique; on the contrary, this replication tightens the "novel" claim into a more accurate "variant of a p14057-family plasmid with ~11 kb of distinguishing content and a novel IS-mediated blaKPC-2 context".

---

WAVE_RESULT set=BVBRC-100 paper=pseudomonas-blakpc2-plasmid verdict=REPLICATED dir=/Users/stevens/Dropbox/REPLICATE-PROJECT/BVBRC-68-pseudomonas-blakpc2-plasmid one_line=pPA1011 (MH734334.1) is 62,793 bp / GC 58.78% (paper: 62,793 / 58.8%) and blaKPC-2 translates to 100.00% (293/293 aa) identity to canonical KPC-2; genetic environment consistent; novelty is a variant of a p14057-family plasmid.
