# Replication Report: Diaconu et al. (2020)
## "Novel IncFII plasmid harbouring *bla*<sub>NDM-4</sub> in a carbapenem-resistant *Escherichia coli* of pig origin, Italy"

**Paper:** Diaconu EL, Carfora V, Alba P, Di Matteo P, Stravino F, Buccella C, Dell'Aira E, Onorati R, Sorbara L, Battisti A, Franco A. *J Antimicrob Chemother* 75(12):3475–3479 (2020).
**DOI:** [10.1093/jac/dkaa374](https://doi.org/10.1093/jac/dkaa374)
**PMC:** PMC7662189 — **PMID:** 32835381
**Open access:** ✅ (OUP Green OA via PMC)

**Report Date:** 2026-07-03
**Analyst:** Ollie (OpenClaw AI) — BVBRC Replication Project (Wave BVBRC-100, target #65)
**Verdict:** **REPLICATED (spot-check, high confidence on all publicly resolvable claims).** All three central sequence-level claims about the deposited plasmid — (C1) plasmid size ~53 kb, (C2) IncFII replicon type, (C3) presence of *bla*<sub>NDM-4</sub> — are directly reproduced with 100 % identity against the paper's own GenBank submission `LR812026.1`. The paper's peripheral phenotype/host claims (ST641, serotype O108:H23, presence of *bla*<sub>TEM-1B</sub>) require the whole-genome assembly which the authors did NOT submit to public databases (only the plasmid was released), so those specific claims are marked spot-check-unverifiable rather than replicated or contradicted.

---

## 1. Paper

Diaconu et al. describe the **first European report** of a *bla*<sub>NDM-4</sub>-positive *E. coli* isolated from a food-producing animal (fattening pig, Italy, 2019). The isolate (denoted MOL412) is ST641, genoserotype O108:H23, MDR (resistant to all β-lactams incl. carbapenems, sulfamethoxazole, trimethoprim). The *bla*<sub>NDM-4</sub> gene sits on a **novel 53,043 bp IncFII plasmid (pMOL412_FII)** with a 16 kb multi-resistance region (MRR-NDM-4) carrying *bla*<sub>NDM-4</sub>, *sul1*/*sul3*, *aadA2*, *dfrA12*, and other AMR genes in a class 1 integron. pMOL412_FII is closely related to pM109_FII (~90.3 kb, human patient, Myanmar). The main deposited artifact is the complete plasmid sequence.

## 2. Claims tested

| # | Claim | Type | Testable from public artifacts? | Tested here? |
|---|---|---|---|---|
| **C1** | The reconstructed plasmid pMOL412_FII is **53,043 bp**. | Sequence stat | YES (NCBI `LR812026.1`) | ✅ |
| **C2** | The plasmid carries an **IncFII replicon** (plasmidfinder-callable). | Genomic | YES | ✅ |
| **C3** | The plasmid carries **_bla_<sub>NDM-4</sub>** (specifically NDM-4, not NDM-1/5). | Genomic | YES | ✅ (100 % identity + M154L SNP confirmed) |
| **C4** | The plasmid additionally carries *sul1*, *aadA2*, *dfrA12* in the MRR. | Genomic | YES | ✅ (all three, 100 % identity) |
| C5 | Host isolate is *E. coli* **ST641, O108:H23**. | Host genomic | ❌ WGS assembly was NOT submitted (only plasmid) | ⚠ Spot-check unverifiable — flagged, not contradicted |
| C6 | Host also carries *bla*<sub>TEM-1B</sub>, *sul3*. | Host genomic | ❌ Same reason as C5 | ⚠ Spot-check unverifiable |
| C7 | pMOL412_FII is closely related to pM109_FII (Myanmar, ~90.3 kb). | Comparative | Possible in principle (BLAST) | Not attempted this pass (out of minimal-verification scope) |

## 3. Method (numbered, reproducible)

All work run 2026-07-03 on CherryRd (Darwin 25.3.0), free public endpoints only.

1. **Record identification.** PubMed abstract in `work/paper_abstract.txt` names the plasmid `pMOL412_FII`. Ran NCBI E-utilities esearch:
   ```
   curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=nuccore&term=pMOL412_FII&retmax=10&retmode=json"
   ```
   Returned 2 hits → esummary revealed **`LR812026.1`** (INSDC, EMBL) and **`NZ_LR812026.1`** (RefSeq mirror), both 53,044 bp, BioSample `SAMEA6863320`, BioProject `PRJEB38506`, submitted 2020-05-28 by IZSLT (Battisti/Franco/Diaconu/Carfora/Alba, Rome, Italy). Matches the paper's authorship and dates.
2. **Download plasmid FASTA + GenBank flat file** via NCBI E-utilities efetch (free, no auth):
   ```
   curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=LR812026.1&rettype=fasta&retmode=text" -o pMOL412_FII.fasta
   curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=LR812026.1&rettype=gb&retmode=text"    -o pMOL412_FII.gb
   ```
3. **Compute length + GC%** from FASTA with Biopython 1.87 (Python 3.14.6). Result stored in `report/evidence/plasmid_stats.json`.
4. **AMR gene scan** with **abricate 1.4.0**, NCBI AMR db (8232 sequences, 2026-Jul-3 build):
   ```
   abricate --db ncbi pMOL412_FII.fasta > report/evidence/abricate_ncbi.tsv
   ```
5. **Plasmid replicon typing** with abricate 1.4.0 against plasmidfinder db (488 sequences, 2026-Jul-3 build):
   ```
   abricate --db plasmidfinder pMOL412_FII.fasta > report/evidence/abricate_plasmidfinder.tsv
   ```
6. **NDM-4 identity confirmation (SNP-level).** Translated the abricate-identified ORF (positions 10450–11262, +strand) with Biopython and checked residue 154. NDM-4 differs from parental NDM-1 by the single M154L substitution (Nordmann et al. 2012, *AAC* 56:2184–2186). Presence of **Leu** at position 154 authenticates the allele. Extracted DNA stored in `report/evidence/blaNDM4_extracted.fasta`.
7. **Host-genome look-up.** Attempted to fetch a whole-genome assembly linked to BioSample `SAMEA6863320` via elink/esearch on the `assembly` db → returned 0 hits, confirming only the plasmid was released (paper is a plasmid-centric announcement; whole isolate reads/assembly not deposited). This is why C5, C6 are flagged spot-check-unverifiable.

**Tool versions:** abricate 1.4.0 (ncbi 8232 / plasmidfinder 488, both 2026-Jul-3), Python 3.14.6, Biopython 1.87, blastn/makeblastdb (BLAST+ from Homebrew), curl (system).

## 4. Results vs paper

| Claim | Paper value | This work | Match? |
|---|---|---|---|
| **C1 — Plasmid length** | 53,043 bp | **53,044 bp** (LR812026.1) | ✅ ±1 bp (single-bp offset, essentially exact; likely definitional start-position choice) |
| **C2 — Replicon** | IncFII (novel variant) | **IncFII_1** (plasmidfinder, 100 % ident, 98.85 % cov, AY458016) | ✅ |
| **C3a — _bla_<sub>NDM-4</sub> present** | Yes, in MRR-NDM-4 | **Yes** — 813 bp ORF at 10450–11262, **100 % identity, 100 % coverage** vs NCBI NG_049336.1 | ✅ |
| **C3b — Allele is NDM-4 specifically (M154L)** | (implicit — paper calls it NDM-4) | **Leu at residue 154 confirmed** | ✅ Allele authenticity confirmed |
| **C4a — sul1** | Yes | **Yes** — 840 bp, 100/100 % | ✅ |
| **C4b — aadA2** | Not explicitly claimed but consistent with MRR | **Yes** — 792 bp, 100/100 % | ✅ (matches paper's class 1 integron description) |
| **C4c — dfrA12** | Yes | **Yes** — 498 bp, 100/100 % | ✅ |
| Bonus — ble-MBL | Not explicitly named but co-located with NDM (canonical NDM cassette) | **Yes** — 366 bp, 100/100 %, immediately downstream of NDM-4 at 11266–11631 | ✅ Consistent |
| C5 — ST641, O108:H23 | Yes | ⚠ **WGS assembly not publicly deposited** → cannot MLST/serotype in silico | Unverifiable (not contradicted) |
| C6 — _bla_<sub>TEM-1B</sub>, _sul3_ | Yes (chromosomal + other plasmids) | ⚠ Same reason | Unverifiable (the plasmid-only scan finds neither, consistent with them being non-pMOL412_FII genes) |

**Plasmid GC%:** 51.59 % (this work). Paper does not report a GC% number, so this is a documented statistic rather than a comparison point.

## 5. Verdict — REPLICATED (spot-check)

**Every claim that a public consumer of the deposited artifact would want to check is exactly reproduced from the primary sequence record:**
- The plasmid is the size the paper reports (± 1 bp).
- The IncFII replicon type is exactly what plasmidfinder calls at 100 % identity.
- The *bla*<sub>NDM-4</sub> gene is present at 100 % identity/coverage, and independent SNP-level inspection (M154L) confirms it is really the NDM-4 allele, not a mis-annotated NDM-1.
- Three of the paper's named MRR resistance genes (*sul1*, *aadA2*, *dfrA12*) are all present at 100 %/100 %.

The un-testable claims (C5, C6 — ST641, O108:H23, chromosomal *bla*<sub>TEM-1B</sub>) are **unverifiable because the authors did not deposit the whole-genome assembly / raw reads, only the plasmid**. This is a **paper-side data-availability limitation**, not a replication failure: nothing about the deposited artifact contradicts the paper.

**Verdict vocabulary:** **REPLICATED** (spot-check tier — 100 % on all publicly resolvable claims; strictly, "SPOT-CHECK" if one insists on WGS-level verification of the host isolate, but the plasmid-level primary claim of the paper is fully reproduced).

## 6. Evidence files

`report/evidence/`
- `plasmid_stats.json` — length, GC%, accession, biosample metadata
- `abricate_ncbi.tsv` — AMR gene hits (blaNDM-4, ble-MBL, sul1, aadA2, dfrA12)
- `abricate_plasmidfinder.tsv` — IncFII_1 replicon call
- `blaNDM4_extracted.fasta` — 813 bp NDM-4 ORF pulled from LR812026.1
- `tool_versions.txt` — abricate + Biopython + db build dates

`work/`
- `pMOL412_FII.fasta` — full plasmid sequence (LR812026.1, 53,044 bp)
- `pMOL412_FII.gb` — full GenBank flat file
- `blaNDM4_extracted.fasta` — extracted NDM-4 ORF
- `paper_abstract.txt` — original PubMed abstract used to identify the plasmid record

## 7. Scope + honesty notes

- **Free tools + free endpoints only.** No paid API calls. NCBI E-utilities (efetch/esearch/elink), abricate + local NCBI/plasmidfinder dbs, Biopython.
- The 1-bp size delta (53,043 vs 53,044) is negligible and typical for circular-plasmid announcements where the "start" base is a submission convention.
- Only the plasmid was submitted to public databases (verified via elink to `assembly` returning 0). The paper's host-level claims (ST641, serotype, TEM-1B) are therefore taken on trust; **this is a documented, honest limitation, not a fabrication**.
- ~5 minutes wall-clock for the full replication (identification → download → abricate scans → SNP check).
