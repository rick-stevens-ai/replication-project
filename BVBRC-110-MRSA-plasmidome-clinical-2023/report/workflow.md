# Workflow — BVBRC-110 replication

**Paper:** Al-Trad et al., *Antibiotics* 12(4):733 (2023) — MRSA plasmidome, Malaysia
**BioProject:** PRJNA722830
**Host:** CherryRd (macOS), local; sequence downloads via NCBI E-utilities.
**Verdict:** PARTIAL (8/8 tested claims reproduce; 2 dataset-scale claims reduced to data-availability spot-checks).

## 1. Pipeline overview

```
  ┌───────────────────────────────┐
  │ 1. Paper acquisition          │
  │   Semantic Scholar → PMC JATS │
  │   → paper_fulltext.txt        │
  └───────────────┬───────────────┘
                  │
  ┌───────────────▼───────────────┐
  │ 2. Data-availability audit    │
  │   E-utilities esearch         │
  │   bioproject / sra / assembly │
  │   / nuccore                   │
  └───────────────┬───────────────┘
                  │
  ┌───────────────▼───────────────┐
  │ 3. Sequence pulls             │
  │   efetch db=nuccore FASTA + GB│
  │   (8 accessions)              │
  └───────────────┬───────────────┘
                  │
        ┌─────────┴──────────┐
        │                    │
  ┌─────▼──────┐    ┌────────▼────────┐
  │ 4a. BLAST  │    │ 4b. Annotation  │
  │ makeblastdb│    │ GenBank grep    │
  │ blastn     │    │ RepL + ermCL +  │
  │ (C5,C6,C7) │    │ erm(C) (C3)     │
  └─────┬──────┘    └────────┬────────┘
        │                    │
        └─────────┬──────────┘
                  │
  ┌───────────────▼───────────────┐
  │ 5. Claim scoring              │
  │   compile claims × evidence   │
  │   → LLM judge (argo:gpt-5.2)  │
  │   → score 86, verdict PARTIAL │
  └───────────────────────────────┘
```

## 2. Step-by-step

### Step 1 — Paper text
- S2 API key from macOS Keychain (`semantic-scholar-api-key` / `rick-stevens-ai`).
- MDPI PDF + PMC PDF both cloudflare/PoW-gated for `curl` → **fallback**: pull JATS XML from PMC:
  ```
  efetch.fcgi?db=pmc&id=PMC10135026&rettype=xml
  → work/pmc_fulltext.xml (299 KB)
  → work/paper_fulltext.txt (184 paragraphs, Python ElementTree)
  ```
- Verified: Methods §3, Results §2.1–§2.6, and all accessions recovered verbatim.

### Step 2 — Data-availability audit (C1, C4-existence, C8)
```
esearch db=bioproject term=PRJNA722830   → 1 project
esearch db=sra        term=PRJNA722830   → 88 SRA runs
esearch db=assembly   term=PRJNA722830   → 92 assemblies
esearch db=nuccore    term="PRJNA722830[BioProject]" → 92 contigs
                                            (3 titled "plasmid":
                                             CP098728, CP098729, CP098730)
```

### Step 3 — Sequence pulls
`efetch db=nuccore rettype=fasta` for:

| Accession | What | Size (bp) |
|-----------|------|-----------|
| JAIVEH010000014.1 | pSauR23-1 | 58,422 |
| JAHMGZ010000022.1 | pSauR165-1 | 28,649 |
| SWED01000025.1 | pSAZ10A | 35,123 |
| GQ900430.1 | SAP078A reference | 35,508 |
| AF051917.1 | pSK41 reference | 46,445 |
| V01277.1 | pC194 reference | 2,910 |
| J01764.1 | pT181 reference | 4,439 |
| CP098730.1 | pSauR3-3 (RepL/ermC rep.) | 2,473 |

Also GenBank flat-file for CP098730.1.

### Step 4a — Comparative-genomics BLAST (C5, C6, C7)
`ncbi-blast+ 2.16.0` on CherryRd.

**C7 (pSAZ10A vs pSK41):**
```
makeblastdb -in AF051917.fasta -dbtype nucl -out pSK41_db
blastn -query SWED01000025.1.fasta -db pSK41_db -outfmt 6 \
  > work/blast_pSAZ10A_vs_pSK41.tsv
```
- 36 HSPs; merged intervals per subject and per query.
- **Query-side coverage = 87.6%** of 35,123 bp pSAZ10A.
- Length-weighted mean identity (≥500 bp / ≥95% id) = **99.29%**.
- (Paper: ~88% coverage, 99.9% identity. Gap explained by IS-mediated repeats + HSP-boundary choice; see failure_analysis.md.)

**C5 (pSauR165-1 → pC194 subregion):**
- Python slice `[11468:14220]` from JAHMGZ010000022.1 → 2,752 bp query.
- `blastn` vs pC194 (V01277.1).
- Top HSP: **99.782% id, 2753 bp, subject nts 162→2910** (paper: 99%, 2751 bp, subject 162–2910). Exact coordinate match.

**C6 (pSauR165-1 → pT181 subregion):**
- Slice `[18931:22762]` → 3,831 bp query.
- `blastn` vs pT181 (J01764.1).
- Top HSP: **99.597% id, 3725 bp** (paper: 99%, 3829 bp). Minor HSP-boundary offset, near-exact.

### Step 4b — RepL / ermC annotation (C3)
- Pulled GenBank flat-file for CP098730.1 (pSauR3-3, 2,473 bp).
- `grep` confirmed features:
  - `/product="replication/maintenance protein RepL"`
  - `/gene="ermCL"` → ErmCL leader peptide
  - `/gene="erm(C)"` → 23S rRNA (adenine(2058)-N(6))-methyltransferase
- `##Genome-Assembly-Data##` block: `Assembly Method :: Unicycler v. v0.4.8` (matches paper Methods §3.4).

### Step 5 — LLM-judge scoring
- Compiled claim/evidence table → `argo:gpt-5.2` via `http://127.0.0.1:44497/v1/chat/completions`.
- `temperature=0`, `max_tokens=600`, strict JSON output format.
- Return: `{"score":86,"verdict":"PARTIAL"}` → `report/evidence/judge_response.json`.
- **Note:** `argo:claude-opus-4.7` tried first, hit an upstream response-schema validation error → fell back to gpt-5.2 (also free).

## 3. What was NOT run (honesty gap)

- **NO re-assembly of 88 SRA runs** (est. 24 CPU-hr on uicgpu).
- **NO end-to-end PlasmidFinder / CARD / ResFinder / BacMet re-run** on all 92 assemblies.
- **NO MOB-typing re-computation** (60 MOBV + 1 MOBP claim accepted from paper).
- **NO wet-lab D-test, no filter-mating conjugation assay** (out of scope).
- **NO orthogonal-assembler cross-check** (deposited contigs accepted as ground truth).

These four omissions are what pull the verdict from REPLICATED to PARTIAL.

## 4. Provenance

- All commands run from CherryRd (macOS, `zsh`).
- No paywalled services; no proprietary tools.
- No network dependency on private CGE endpoints — BLAST run locally.
- Every sequence saved to `work/seqs/` and every BLAST TSV saved to `work/` for re-inspection.
- Judge response saved to both `/tmp/judge_resp.json` and `report/evidence/judge_response.json`.
