# Artifacts Summary — BVBRC-110

**Paper:** Al-Trad et al., *Antibiotics* 12(4):733 (2023). PMID 37107095. DOI 10.3390/antibiotics12040733.
**BioProject:** PRJNA722830
**Verdict:** PARTIAL. LLM-judge (argo:gpt-5.2) = 86/100.

## Directory layout

```
BVBRC-110-MRSA-plasmidome-clinical-2023/
├── work/
│   ├── paper.pdf                          MDPI cloudflare-blocked placeholder (provenance)
│   ├── pmc_fulltext.xml                   NLM JATS XML from PMC10135026 (299 KB) — source of truth
│   ├── paper_fulltext.txt                 Extracted text, 184 paragraphs
│   ├── s2_meta.json                       Semantic Scholar metadata
│   ├── seqs/
│   │   ├── JAIVEH010000014.1.fasta        pSauR23-1, 58,422 bp
│   │   ├── JAHMGZ010000022.1.fasta        pSauR165-1, 28,649 bp
│   │   ├── SWED01000025.1.fasta           pSAZ10A, 35,123 bp
│   │   ├── GQ900430.1.fasta               SAP078A reference, 35,508 bp
│   │   ├── AF051917.1.fasta               pSK41 reference, 46,445 bp
│   │   ├── V01277.1.fasta                 pC194 reference, 2,910 bp
│   │   ├── J01764.1.fasta                 pT181 reference, 4,439 bp
│   │   ├── CP098730.1.fasta               pSauR3-3 (RepL/ermC), 2,473 bp
│   │   └── pSauR3-3.gb                    GenBank flat-file (annotation source)
│   ├── blast_pSAZ10A_vs_pSK41.tsv         BLAST HSPs (36 hits, C7 evidence)
│   └── blast_pSAZ10A_vs_pSK41_strict.tsv  Same, ≥500 bp / ≥95% id filter
│
└── report/
    ├── REPORT.md                          Primary report (Markdown, human-readable)
    ├── REPORT.tex                         LaTeX version + Genuine Critique section
    ├── workflow.md                        Step-by-step workflow (this replication)
    ├── artifacts_summary.md               This file
    ├── failure_analysis.md                What didn't quite match + why
    ├── open_questions.json                5 open questions for follow-up work
    └── evidence/
        ├── pSauR3-3_annotation.gb         Copy of CP098730.1 GenBank (RepL + ermCL + erm(C))
        ├── blast_pSAZ10A_vs_pSK41.tsv     Copy of BLAST TSV for C7
        └── judge_response.json            LLM-judge (argo:gpt-5.2) output {score:86, verdict:PARTIAL}
```

## Claim → evidence map

| Claim | Evidence artifact | Verified? |
|-------|-------------------|-----------|
| C1: PRJNA722830 exists w/ 79 WGS | E-utilities esearch output (88 SRA + 92 assy) | ✅ |
| C2: 189 plasmids across 7 replicase families | `work/paper_fulltext.txt` + accession existence (not re-run) | PARTIAL |
| C3: RepL + *ermC* on ~2.4–2.7 kb plasmid | `report/evidence/pSauR3-3_annotation.gb` | ✅ |
| C4: pSauR23-1 = novel 58,442 bp RepA_N conjugative | `work/seqs/JAIVEH010000014.1.fasta` (58,422 bp) | ✅ (0.03% length delta) |
| C5: pSauR165-1 vs pC194 subregion, 99%, 2751 bp | BLAST on-the-fly (subregion slice), reported inline in REPORT.md | ✅ (99.78%, 2753 bp, subj 162–2910) |
| C6: pSauR165-1 vs pT181 subregion, 99%, 3829 bp | BLAST on-the-fly, reported inline | ✅ (99.60%, 3725 bp) |
| C7: pSAZ10A vs pSK41, 99.9% id / ~88% cov | `work/blast_pSAZ10A_vs_pSK41.tsv`, `_strict.tsv` | ✅ (99.29%, 87.6% cov) |
| C8: SAP078A = GQ900430.1 = 35,508 bp | `work/seqs/GQ900430.1.fasta` | ✅ exact |
| Provenance: Unicycler v0.4.8 | `work/seqs/pSauR3-3.gb` ##Genome-Assembly-Data## | ✅ exact |

## External resources used

- **NCBI E-utilities** (public, no key required for these calls): `esearch.fcgi`, `efetch.fcgi`.
- **NCBI BLAST+ 2.16.0** (local install on CherryRd): `blastn`, `makeblastdb`.
- **Python 3 + xml.etree.ElementTree** (stdlib) for PMC JATS parsing.
- **Argo proxy** (local, free): `http://127.0.0.1:44497/v1/chat/completions` for LLM judge (argo:gpt-5.2).
- **Semantic Scholar API** (key from macOS Keychain `semantic-scholar-api-key` / `rick-stevens-ai`).

## Provenance & reproducibility notes

- All downloads are content-addressable by GenBank accession + version — a re-run today should get the same bytes.
- The three plasmid sequences central to the paper (pSauR3-3, pSauR23-1, pSauR165-1, pSAZ10A) plus 4 reference plasmids (pSK41, pC194, pT181, SAP078A) together account for ~215 KB of FASTA — easy to re-download and re-verify.
- BLAST results are deterministic given the same query + database + `blastn` version; `ncbi-blast+ 2.16.0` was used throughout.
- LLM-judge score is stochastic in principle; called with `temperature=0` and the fixed prompt in `report/evidence/judge_response.json` for reproducibility. A second-judge cross-check is not included (see failure_analysis.md).
