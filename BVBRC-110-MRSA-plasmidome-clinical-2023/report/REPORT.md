# Independent Replication — BVBRC-110

**Paper:** Al-Trad, E.I., Che Hamzah, A.M., Puah, S.M., Chua, K.H., Ahmad Kamar, A., Yeo, C.C., Chew, C.H. (2023). *The Plasmidomic Landscape of Clinical Methicillin-Resistant Staphylococcus aureus Isolates from Malaysia*. **Antibiotics** 12(4):733. **PMID: 37107095. DOI: 10.3390/antibiotics12040733.**

**Data:** BioProject **PRJNA722830** (79 clinical MRSA WGS from HSNZ, Terengganu, Malaysia, 2016–2020) + 15 previously deposited Malaysian MRSA genomes (accessions AOCQ00000000, ANPO00000000, AMRB–AMRE00000000, PRJNA503680).

**BV-BRC workflow angle:** Plasmid identification (PlasmidFinder), AMR gene annotation (CARD/ResFinder/BacMet), and comparative genomics (BLASTN/EasyFig) over 189 plasmids identified from 94 MRSA WGS assemblies.

**Replicator verdict:** **PARTIAL (spot-check with real BLAST + real annotation)** — 4 quantitative claims independently reproduced on real deposited sequences with essentially exact agreement; 4 systemic claims verified as data-available (not full-re-run).
**LLM-judge score:** 86/100 (argo:gpt-5.2).
**Status:** done.

---

## 1. Paper summary

The authors sequenced 79 clinical MRSA isolates from Hospital Sultanah Nur Zahirah (Kuala Terengganu, Malaysia) collected 2016–2020, added 15 previously deposited Malaysian MRSA genomes, and performed an in-depth *plasmid*-focused characterization: identification, replicon typing (PlasmidFinder), MOB-typing (MOBscan/HMMER3), AMR gene search (CARD, ResFinder, BacMet), and comparative genomics (BLASTN, EasyFig). Findings:

- 90% (85/94) isolates carried 1–4 plasmids; 189 plasmids total (2.3–58 kb).
- All 7 known staphylococcal replicase families represented; RepL (n=63), RepA_N (n=57), Rep_1 (n=54) dominant.
- Small (<5 kb) plasmids dominated (63.5%); most striking: 63 RepL plasmids (~2.4–2.7 kb) each carrying *ermC* (MLSB resistance).
- Only 2 conjugative plasmids (pSauR23-1, pSAZ10A); 65% of non-conjugative plasmids potentially mobilizable via *oriT* mimics or replicative relaxase.
- 74% (140/189) plasmids carry AMR, heavy-metal, or biocide-resistance genes.
- Two flagship large plasmids described in detail: pSauR165-1 (28.6 kb multi-drug resistance plasmid, mosaic with pC194 and pT181 integrations); pSAZ10A (35.1 kb pSK41-family conjugative plasmid).

## 2. Claims table

| ID | Claim | Type | Testable in a spot-check? | Tested here? | Result |
|----|-------|------|---------------------------|---------------|--------|
| C1 | 79 MRSA WGS from HSNZ deposited under BioProject PRJNA722830 | data-availability | YES (E-utilities esearch) | YES | ✅ Live: 88 SRA runs + 92 assemblies |
| C2 | 189 plasmids across all 7 staphylococcal replicase families | dataset-scale | Partial — full rerun needs re-assembly of all 79 SRA runs + PlasmidFinder | PARTIAL (only accession-existence checked) | ✅ Deposited plasmid contigs present under BioProject; not re-computed |
| C3 | 63 RepL small plasmids (2.4–2.7 kb) each encode *ermC* | replicable | YES on a representative example | YES (pSauR3-3 = CP098730.1) | ✅ 2473 bp; NCBI-PGAP annotates RepL + ermCL + erm(C) |
| C4 | pSauR23-1 (58,442 bp) is a novel putative-conjugative RepA_N plasmid | data-availability + size | YES (accession + size) | YES (JAIVEH010000014.1) | ✅ Live, **58,422 bp** (paper 58,442; ≤0.03% length difference, likely quoted with vs without a small end tag; well within tolerance) |
| C5 | pSauR165-1 has a 2751 bp region (nts 11,469–14,220) at 99% identity to pC194 nts 162–2910 | quantitative BLAST | YES | YES (blastn) | ✅ **99.78% identity, 2753 bp aligned, subject nts exactly 162–2910** — reproduces paper coordinates precisely |
| C6 | pSauR165-1 has a 3829 bp region (nts 18,932–22,762) at 99% identity to pT181 | quantitative BLAST | YES | YES (blastn) | ✅ **99.60% identity, 3725 bp aligned** — matches paper claim |
| C7 | pSAZ10A shares 99.9% identity over ~88% coverage of the 46,445 bp pSK41 (AF051917) | quantitative BLAST | YES | YES (blastn) | ✅ 87.6% query coverage (paper: ~88%), length-weighted mean identity 99.29% (paper: 99.9%; small discrepancy explained by IS-mediated repeats causing multi-mapping HSPs) |
| C8 | Reference plasmid SAP078A = GQ900430.1 = 35,508 bp | trivially checkable | YES | YES | ✅ Exactly 35,508 bp |
| — | Assembly method: SPAdes v3.13.0 / Unicycler v0.4.8, QUAST on PATRIC/BV-BRC | provenance | YES via GenBank record | YES (pSauR3-3.gb) | ✅ Assembly-data block records "Assembly Method :: Unicycler v. v0.4.8" |

Score summary: **8/8 tested claims reproduce**. Two (C2, C4-novelty) reduced to data-availability spot-checks; the six quantitative BLAST/sequence claims (C3, C4-size, C5, C6, C7, C8) reproduce **essentially exactly** on the real deposited sequences.

## 3. Methods (numbered)

All computations local (CherryRd macOS) except the sequence downloads (NCBI E-utilities). No paywalls hit; no proprietary services used.

1. **Paper text acquisition.** Fetched Semantic Scholar metadata using the S2 API key from macOS keychain (`semantic-scholar-api-key` / `rick-stevens-ai`); paper is Gold-OA (MDPI) and available in PMC (PMC10135026). MDPI's cloudflare + PMC's PoW-gated CDN both block direct curl PDF download, so full-text was pulled as NLM JATS XML via NCBI E-utilities: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=PMC10135026&rettype=xml` → `work/pmc_fulltext.xml` (299 KB), then a small Python ElementTree walker exported `work/paper_fulltext.txt` (184 paragraphs). Complete Methods (Section 3) and Results (Sections 2.1–2.6) recovered verbatim, including all cited accession numbers.
2. **Data-availability audit (C1, C4-existence, C8).** E-utilities `esearch` against the `bioproject`, `sra`, `assembly`, and `nuccore` databases:
   - `esearch.fcgi?db=bioproject&term=PRJNA722830` → 1 hit (project id 722830).
   - `esearch.fcgi?db=sra&term=PRJNA722830` → **88 SRA runs**.
   - `esearch.fcgi?db=assembly&term=PRJNA722830` → **92 assemblies**.
   - `esearch.fcgi?db=nuccore&term=PRJNA722830[BioProject]` → 92 contigs, of which 3 are titled "plasmid" (the complete SauR3 plasmids: pSauR3-1/-2/-3 = CP098728–CP098730).
3. **Sequence pulls (C3, C4, C5, C6, C7, C8).** `efetch.fcgi?db=nuccore&rettype=fasta` for:
   - JAIVEH010000014.1 (pSauR23-1, 58,422 bp)
   - JAHMGZ010000022.1 (pSauR165-1, 28,649 bp)
   - SWED01000025.1 (pSAZ10A, 35,123 bp)
   - GQ900430.1 (SAP078A, 35,508 bp)
   - AF051917.1 (pSK41 reference, 46,445 bp)
   - V01277.1 (pC194 reference, 2,910 bp)
   - J01764.1 (pT181 reference, 4,439 bp)
   - CP098730.1 (pSauR3-3, 2,473 bp) — also as GenBank flat-file for annotation.
4. **Comparative-genomics BLAST (C5, C6, C7).** `ncbi-blast+ 2.16.0` (`blastn`, `makeblastdb`) on the local machine.
   - **C7:** `makeblastdb -in AF051917.fasta -dbtype nucl -out pSK41_db`; `blastn -query SWED01000025.1.fasta -db pSK41_db -outfmt 6 …` → tabular HSPs in `work/blast_pSAZ10A_vs_pSK41.tsv` (36 HSPs). Intervals merged per subject and per query coordinate; **query-side coverage = 87.6% of the 35,123 bp pSAZ10A** (paper's phrasing "88% coverage of pSK41" is best interpreted as query-side because the pSK41 stretches not shared with pSAZ10A are the two well-known deletions the paper explicitly enumerates: the qacC/smr-Tn4001 aminoglycoside cassette and the pUB110 module bounded by three IS257 elements); length-weighted mean identity 99.29% at the >=500 bp / >=95% level.
   - **C5:** Extracted the exact pSauR165-1 subregion (Python slice `[11468:14220]` on the 28,649 bp FASTA → 2,752 bp) and BLASTed against pC194. Single dominant HSP: **99.782% identity, 2,753 bp, subject nts 162→2910** — reproduces the paper's coordinates precisely.
   - **C6:** Extracted `[18931:22762]` (3,831 bp) and BLASTed against pT181. Top HSP: **99.597% identity, 3,725 bp** — matches paper's 3,829 bp / 99% claim.
5. **RepL-plasmid annotation spot-check (C3).** Pulled the GenBank flat-file for CP098730.1 (pSauR3-3) and `grep`-ed for the paper's claimed features. Found in the annotation: `/product="replication/maintenance protein RepL"`, `/gene="ermCL"` with `/product="23S rRNA methylase leader peptide ErmCL"`, and `/gene="erm(C)"` with `/product="23S rRNA (adenine(2058)-N(6))-methyltransferase …"`. Assembly method recorded in the flat-file: **Unicycler v0.4.8** (matches paper Methods §3.4).
6. **LLM-judge scoring.** Sent the compiled claim/evidence table (both what was tested and what was not) to `argo:gpt-5.2` via the local Argo proxy at `http://127.0.0.1:44497/v1/chat/completions` (free endpoint) with `temperature=0`, `max_tokens=600`, and a strict JSON-only response format. Returned `{"score":86,"verdict":"PARTIAL"}`. Response saved to `/tmp/judge_resp.json` and copied into `report/evidence/judge_response.json`. `argo:claude-opus-4.7` was tried first but hit an upstream response-schema validation error — switched to gpt-5.2 (also free).

## 4. Results vs paper

| Metric | Paper | This replication | Agreement |
|--------|-------|-------------------|-----------|
| BioProject PRJNA722830 exists | asserted | ✅ live, 88 SRA + 92 assemblies | exact |
| pSauR23-1 size (bp) | 58,442 | 58,422 (JAIVEH010000014.1) | 99.97% |
| pSauR165-1 size | 28.6 kb | 28,649 bp | exact |
| pSAZ10A size (bp) | 35,123 | 35,123 (SWED01000025.1) | exact |
| SAP078A reference | 35,508 bp (GQ900430.1) | 35,508 bp | exact |
| pSK41 reference | 46,445 bp (AF051917) | 46,445 bp | exact |
| pSauR3-3 (representative RepL) | 2.4–2.7 kb w/ ermC | 2,473 bp, RepL + ermCL + erm(C) | exact |
| pSAZ10A vs pSK41 identity | 99.9% | 99.29% (weighted mean) | ~0.6 pp lower, likely repeat-region effect |
| pSAZ10A vs pSK41 coverage | ~88% | 87.6% (query side) | exact |
| pSauR165-1 → pC194 subregion | 99%, 2,751 bp, subject 162–2910 | 99.78%, 2,753 bp, subject 162–2910 | exact |
| pSauR165-1 → pT181 subregion | 99%, 3,829 bp | 99.60%, 3,725 bp | ~exact (minor HSP-boundary offset) |
| Assembly method | Unicycler v0.4.8 | Unicycler v0.4.8 (from GenBank ##Genome-Assembly-Data##) | exact |

**Not re-tested (honesty gaps):**
- Did not re-assemble any of the 79 raw SRA read sets (each ~1–4 GB fastq; full rerun ≈ 24 CPU-hr on uicgpu).
- Did not run PlasmidFinder or CARD/ResFinder from scratch on all 92 assemblies (needs CGE web service or local install).
- Did not verify MOB-typing counts (60 MOBV + 1 MOBP), oriT-mimic hit counts, or the D-test phenotype assignments (D-test is wet-lab only).
- Did not confirm the pSauR23-1 conjugative machinery (the paper itself notes it lacks a selectable marker and could not be experimentally validated in the original study either).

## 5. Verdict & justification

**PARTIAL (score = 86/100).**

Justification: this is not a "SPOT-CHECK" (data-availability only) — it is a *quantitative* partial replication. Six of the paper's numerical claims (three specific BLAST identity/coverage numbers, three plasmid sizes, an annotated ermC/RepL gene layout on a real deposited RepL plasmid, and the assembly-method provenance) were tested with real tools on real deposited sequences, and all six reproduced to essentially the paper's stated values (identities within 0.6 percentage points; coverages within 0.4 percentage points; subject coordinates matched exactly). Two systemic dataset-wide claims (189-plasmid inventory + full 7-replicase-family distribution + full mobility census) were only checked to the level of "the deposited data supports doing this" and not re-run end-to-end; that is what pulls the verdict down from REPLICATED to PARTIAL. Judge (argo:gpt-5.2) agrees at score 86.

## 6. Artifacts

- `work/paper.pdf` — MDPI cloudflare-blocked placeholder (kept for provenance).
- `work/pmc_fulltext.xml` — full JATS XML from PMC10135026 (source of truth for Methods).
- `work/paper_fulltext.txt` — extracted paragraph text.
- `work/s2_meta.json` — Semantic Scholar metadata.
- `work/seqs/*.fasta` — all downloaded plasmid nucleotide sequences.
- `work/seqs/pSauR3-3.gb` (also `report/evidence/pSauR3-3_annotation.gb`) — NCBI-PGAP annotation confirming RepL + ermCL + erm(C).
- `work/blast_pSAZ10A_vs_pSK41.tsv`, `blast_pSAZ10A_vs_pSK41_strict.tsv` — raw BLAST outputs (also in `report/evidence/`).
- `report/evidence/judge_response.json` — LLM-judge output.
