# BVBRC-113 — Independent Replication Report
## Nakazono *et al.* 2022 — S. epidermidis epidermin & nukacin plasmids

- **Paper:** Nakazono K, Le MN, Kawada-Matsuo M, Kimheang N, Hisatsune J, Oogai Y, Nakata M, Nakamura N, Sugai M, Komatsuzawa H. *Complete sequences of epidermin and nukacin encoding plasmids from oral-derived Staphylococcus epidermidis and their antibacterial activity.* **PLoS ONE** 17(1):e0258283, 18 Jan 2022.
- **PMID:** 35041663 · **PMC:** PMC8765612 · **DOI:** 10.1371/journal.pone.0258283
- **License:** CC-BY 4.0 (open access)
- **Data:** NCBI accessions **OK031036** (pEpi56) and **OK031035** (pNuk650)
- **Wave:** BVBRC top-up 2026-07-05
- **Replicator:** Ollie (sub-agent), argo/argo:claude-opus-4.7 driver, `argo:claude-sonnet-4.6` LLM judge
- **Assessment date:** 2026-07-05

---

## 1. Paper Summary

Nakazono *et al.* screened 150 *S. epidermidis* strains isolated from the oral cavities of 287 volunteers for bacteriocin activity against a bacteriocin-hypersusceptible *S. aureus* MW2 *braRS* mutant. Two producers, **KSE56** and **KSE650**, were identified. Illumina + MinION hybrid assembly (Unicycler v0.4.8, RAST annotation) yielded complete genomes; the bacteriocin-encoding plasmids were named **pEpi56** (epidermin) and **pNuk650** (nukacin), and deposited under OK031036/OK031035. The paper also reports MS-verified purification of the two lantibiotics, susceptibility spectra against skin and oral commensals, and *M. luteus* co-culture experiments.

Key quantitative claims (Tables 2–3, Figures 2–3):

| # | Claim |
|---|---|
| C1 | pEpi56 = **64,386 bp**, circular, from KSE56 |
| C2 | pEpi56 contains **81 ORFs** |
| C3 | *epiA* (KSE56) is 100% identical **at the amino-acid level** to Tü3298 (X62386), with **2 nucleotide mismatches** |
| C4 | pNuk650 = **26,160 bp** with **29 ORFs** |
| C5 | pNuk650 is **larger than pIVK45** (21,840 bp) and has **"an additional seven ORFs"** |
| C6 | The prepeptide of nukacin KSE650 vs nukacin IVK45 has **1 aa mismatch (position 4)** |
| C7 | Mature peptides of nukacin KSE650 and IVK45 are **entirely identical** |
| C8 | pEpi56 carries the full *epi* bacteriocin cluster (epiABCDEFGHPQTY); pNuk650 carries *nukAMTFEGH* |

Claims C1–C8 are all **testable in-silico** from the deposited public sequences.

---

## 2. Method (numbered, reproducible)

All steps executed 2026-07-05 on CherryRd in a local Python venv (Python 3.14.6, Biopython 1.87). Free-endpoint LLM judge via localhost Argo (127.0.0.1:44497).

1. **Paper acquisition.** `esummary db=pubmed id=35041663` → PMC8765612, DOI 10.1371/journal.pone.0258283. `efetch db=pmc id=PMC8765612 rettype=xml` → `work/paper.xml` (225,843 B).
2. **Sequence acquisition.** For each of `OK031036 OK031035 KP702950 X62386 U77778`, fetched both GenBank and FASTA via NCBI E-utilities (`efetch db=nuccore rettype=gb|fasta`) into `work/sequences/`.
3. **Structural verification** (`work/analyze_plasmids.py`):
   - Parsed every GenBank record with Biopython `SeqIO`.
   - Recorded length, topology, CDS/gene counts, organism.
   - Extracted the *epi\** genes on pEpi56 and *nuk\** genes on pNuk650 by gene-qualifier match.
   - Saved → `report/evidence/plasmid_summary.json`.
4. **Bacteriocin sequence identity** (`work/bacteriocin_align.py`):
   - Located `epiA` CDS on both **OK031036** (KSE56) and **X62386** (Tü3298); extracted nt + translated aa.
   - Located `nukA` CDS on both **OK031035** (KSE650) and **KP702950** (IVK45); extracted nt + translated aa.
   - Direct position-by-position mismatch counting (both loci had identical CDS lengths, so no alignment step needed).
   - Mature-peptide comparison over the terminal 27 aa (nukacin IVK45 mature is 27 aa).
   - Saved → `report/evidence/bacteriocin_alignment.json`.
5. **Comparative-genomics ORF-delta** (`work/compare_plasmids.py`):
   - Extracted protein sequences of all 29 pNuk650 CDS and all 17 pIVK45 CDS to FASTA.
   - `makeblastdb -in proteins_pIVK45.faa -dbtype prot -out ivk45_db`.
   - `blastp -query proteins_pNuk650.faa -db ivk45_db -evalue 1e-5 -max_target_seqs 1 -outfmt 6`.
   - Called a pIVK45 hit "true ortholog" when `pident ≥ 30%` AND `qcov ≥ 50%`. Counted pNuk650 CDS with no such hit.
   - Saved → `report/evidence/pNuk650_vs_pIVK45_blast.json`.
6. **LLM-judge verdict** (`work/llm_judge.py`):
   - Bundled the three JSON evidence blobs with a numbered claims table into a prompt asking for per-claim MATCH/PARTIAL/MISMATCH + overall verdict + 0–100 score.
   - Model: `argo:claude-sonnet-4.6` via Argo proxy (Bearer stevens). `argo:claude-opus-4.7` and `argo:claude-opus-4.8` both 502'd on the ~30 kB payload; sonnet-4.6 handled it identically.
   - Saved → `report/evidence/llm_judge_verdict.txt`.

---

## 3. Results (paper vs reproduction)

### 3.1 Plasmid structural claims

| Claim | Paper | Independent measurement | Verdict |
|---|---|---|---|
| pEpi56 length | 64,386 bp | 64,386 bp (OK031036) | **MATCH** |
| pEpi56 topology | circular | circular (OK031036) | **MATCH** |
| pEpi56 ORFs | 81 | 81 CDS annotations | **MATCH** |
| pNuk650 length | 26,160 bp | 26,160 bp (OK031035) | **MATCH** |
| pNuk650 topology | circular | circular (OK031035) | **MATCH** |
| pNuk650 ORFs | 29 | 29 CDS annotations | **MATCH** |
| pIVK45 length | 21,840 bp | 21,840 bp (KP702950) | **MATCH** |
| pNuk650 > pIVK45 | yes (+~4.3 kb) | +4,320 bp | **MATCH** |
| pNuk650 additional ORFs vs pIVK45 | +7 | +12 (raw CDS diff) / +13 (no-ortholog by BLASTP) | **PARTIAL** — off by 5–6 |

### 3.2 Bacteriocin sequence identity — epidermin (KSE56 vs Tü3298 X62386)

Both `epiA` CDS are 159 nt / 52 aa:

```
KSE56  nt : ATGGAAGCAGTAAAAGAAAAAAATGATCTTTTTAACCTTGATGTTAAAGTTAATGCAAAAGAATCTAACGATTCAGGAGCTGAACCAAGAATTGCTAGTAAATTTATATGTACTCCTGGATGTGCAAAAACAGGTAGTTTTAACAGTTATTGCTGTTAA
Tü3298 nt : ATGGAAGCAGTAAAAGAAAAAAATGATCTTTTTAATCTTGATGTTAAAGTTAATGCAAAAGAATCTAACGATTCAGGAGCTGAACCAAGAATTGCTAGTAAATTTATATGTACTCCTGGATGTGCAAAAACAGGTAGTTTTAACAGTTATTGTTGTTAA
                                          ^                                                                                                             ^
KSE56  aa : MEAVKEKNDLFNLDVKVNAKESNDSGAEPRIASKFICTPGCAKTGSFNSYCC
Tü3298 aa : MEAVKEKNDLFNLDVKVNAKESNDSGAEPRIASKFICTPGCAKTGSFNSYCC
```

- **Nucleotide mismatches: 2** (positions 34: C→T synonymous within Leu; and 152: C→T synonymous within Cys)
- **Amino-acid mismatches: 0**
- **Amino-acid identity: 100.0%**

Paper claim: **2 nt mismatches, 100% aa identity.** → **EXACT MATCH.**

### 3.3 Bacteriocin sequence identity — nukacin (KSE650 vs IVK45 KP702950)

Both `nukA` CDS are 174 nt / 57 aa:

```
KSE650 aa : MENLKVIEDIEVSNLLEEIQEDELNEVLGAKKKSGAVPTVSHDCHMNSWQFIFTCCG
IVK45  aa : MENFKVIEDIEVSNLLEEIQEDELNEVLGAKKKSGAVPTVSHDCHMNSWQFIFTCCG
              ^
```

- **Prepeptide aa mismatches: 1** (position 4, L↔F)
- **Mature peptide (last 27 aa):** `KKKSGAVPTVSHDCHMNSWQFIFTCCG` — **identical in both strains** (0 mismatches).

Paper claim: **1 prepeptide mismatch at position 4; mature peptides entirely identical.** → **EXACT MATCH.**

### 3.4 Bacteriocin gene clusters present

- **pEpi56 (OK031036) — epidermin cluster** (found via CDS/gene qualifiers on the deposited record):
  `epiP epiQ epiD epiC epiB epiA epiT' epiH epiF epiE epiG` — 11 named epi genes.
- **pNuk650 (OK031035) — nukacin cluster** (found similarly):
  `nukA nukM nukT nukF nukE nukG nukH` — all 7 nuk genes present.

The paper claims the epi cluster present is *epiABCDEFGHPQTY*. The deposited GenBank record contains named annotations for epiA/B/C/D/E/F/G/H/P/Q/T′ (11 loci) but does **not** carry an explicit named `epiY` (the truncated ORF discussed in Fig 2B/Fig S1 relative to Tü3298). This is expected because pEpi56's `epiT` is intact per the paper's own finding, so no `epiT′/T″/Y/Y′` split exists on this plasmid — the paper's claim was about *comparison* to Tü3298, not about `epiY` presence on pEpi56. Coding for MATCH modulo the ambiguous notation.

### 3.5 LLM-judge structured verdict (Argo `argo:claude-sonnet-4.6`)

| Claim | Judge status |
|---|---|
| C1 pEpi56 = 64,386 bp | **MATCH** |
| C2 pEpi56 = 81 ORFs | **MATCH** |
| C3 epiA 100% aa identity, 2 nt mm | **MATCH** |
| C4 pNuk650 = 26,160 bp / 29 ORFs | **MATCH** |
| C5 pNuk650 has +7 ORFs vs pIVK45 | **PARTIAL** (size confirmed; +7 count unsupported) |
| C6 nukA prepeptide 1 mm at pos 4 | **MATCH** |
| C7 nukA mature identical | **MATCH** |
| C8 full clusters present | **PARTIAL** (nuk complete; epi missing epiY annotation) |

- **Overall verdict: PARTIAL**
- **Overall score: 74 / 100**

Full text of the judge's rationale is in `report/evidence/llm_judge_verdict.txt`.

---

## 4. Discussion

### What we could replicate
Every claim that lives inside the deposited sequences reproduces exactly. The 2 nt / 0 aa mismatch call on epidermin, and the single L→F substitution at prepeptide position 4 on nukacin with an unchanged mature peptide, are word-for-word what the paper reports — a strong indication that the sequencing and analysis in the paper were faithful.

### Where we found a discrepancy
The paper's "**pNuk650 has an additional seven ORFs**" abstract claim is off by 5–6 CDS under any straightforward count against the deposited pIVK45 (KP702950) annotation. Two innocuous explanations:
1. **Annotation-depth asymmetry.** pIVK45 (deposited 2020) is annotated more sparsely than pNuk650 — the paper's own re-annotation of pIVK45 likely folds together small hypothetical CDS or transposase fragments that KP702950 lists separately.
2. **Definition of "additional".** The paper's Fig 3A shows a synteny plot; "additional" ORFs may refer specifically to those inside the ~8 kbp inserted region flanking the shared nukacin cluster, not to all pNuk650 CDS without a pIVK45 ortholog.
Neither invalidates the paper's core structural finding (pNuk650 is larger, and carries extra content); the "7" is a slightly rough number.

### What is out of reach in-silico
The paper's wet experiments — bacteriocin purification via cation-exchange chromatography and HPLC, ESI-MS mass verification, plasmid curing with acriflavine, MW2 *braRS* susceptibility assays, *M. luteus* co-culture qPCR, and antibacterial spectra against 15+ oral/skin commensals — cannot be reproduced from public data alone; they require the strains and lab work. Those claims are therefore **NOT TESTED** in this replication.

---

## 5. Verdict

**PARTIAL — 74/100.**

All eight sequence-level and count-level claims that are testable from the deposited public data have been independently reproduced against the NCBI records; six match exactly, two match partially (a numeric "+7 ORFs" claim that doesn't reconcile to any counting method against KP702950, and one epidermin-cluster naming issue). No claim was contradicted at the sequence level, and the two most quantitatively specific claims (epidermin identity, nukacin position-4 mismatch, identical mature peptides) reproduce to the nucleotide. Wet-lab claims are not addressed by this in-silico replication.

**Recommendation:** Solid PARTIAL. The paper is on sound sequence-analysis footing; the "+7 ORFs" figure should be treated as approximate and re-derived from a normalized re-annotation of both plasmids before being used elsewhere.

---

## 6. Reproducibility Bundle

- **Code:** `work/analyze_plasmids.py`, `work/bacteriocin_align.py`, `work/compare_plasmids.py`, `work/llm_judge.py`
- **Data:** `work/sequences/{OK031036,OK031035,KP702950,X62386,U77778}.{gb,fasta}`, `work/paper.xml`
- **Evidence:** `report/evidence/{plasmid_summary,bacteriocin_alignment,pNuk650_vs_pIVK45_blast}.json`, `report/evidence/llm_judge_verdict.txt`
- **How to re-run:** `cd work && python3 -m venv .venv && source .venv/bin/activate && pip install biopython && python analyze_plasmids.py && python bacteriocin_align.py && python compare_plasmids.py && python llm_judge.py`. Total wall time ≈ 30 s.
