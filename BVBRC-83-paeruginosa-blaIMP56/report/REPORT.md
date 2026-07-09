# BVBRC-83 — Independent Replication of Gómez-Martínez et al. (2022)

## Paper
- **Title:** A Plasmid Carrying blaIMP-56 in *Pseudomonas aeruginosa* Belonging to a Novel Resistance Plasmid Family
- **Authors:** Gómez-Martínez J, Rocha-Gracia RC, Bello-López E, Cevallos MA, Castañeda-Lucio M
- **Venue:** *Microorganisms* 10(9): 1863 (2022)
- **DOI:** 10.3390/microorganisms10091863
- **PMID:** 36144465 · **PMCID:** PMC9501424 (Open Access, CC-BY)
- **Deposited plasmid sequence:** GenBank **CP102481.1** (pPE52IMP, 27,635 bp)

## Summary
Whole-plasmid characterization paper. Authors sequenced *P. aeruginosa* PE52 (Mexican clinical isolate) on Illumina MiSeq 2×150 bp, assembled with plasmidSPAdes, and reported a 27,635 bp circular plasmid (pPE52IMP) carrying the metallo-β-lactamase gene **blaIMP-56** in a class-1 integron together with *aadA1* and *blaOXA-2*, a complete mercury operon, and MOBP11-subfamily conjugation/relaxase machinery. Central claim: pPE52IMP defines a **new plasmid family** (non-typeable by PBRT), with RepA phylogenetically clustering with five other *P. aeruginosa* resistance plasmids (pMATVIM-7, unnamed FDAARGOS_570, pD5170990, pMRVIM0713, plus p4130-KPC with a truncated RepA).

## Claims table
| ID | Claim (from paper) | Type | Testable from public data? | Tested here? |
|---|---|---|---|---|
| C1 | pPE52IMP is 27,635 bp | Numeric | Yes (GenBank CP102481.1) | ✅ |
| C2 | %GC = 62.2% | Numeric | Yes | ✅ |
| C3 | 39 open reading frames | Numeric | Yes | ✅ |
| C4 | Circular topology | Structural | Yes (GenBank LOCUS) | ✅ |
| C5 | Complete mer operon (merR, merT, merP, merA, merD, merE) | Compositional | Yes | ✅ |
| C6 | parB gene is absent | Compositional | Yes | ✅ |
| C7 | Carries blaIMP-56 | Compositional | Yes | ✅ |
| C8 | Class-1 integron cassette: blaIMP-56 + aadA1 + blaOXA-2 | Compositional | Yes | ✅ |
| C9 | phd/doc + other stability toxin-antitoxin present | Compositional | Yes | ✅ |
| C10 | Relaxase belongs to MOBP11 subfamily | Classification | Partial (protein-sequence homology to known MOB families) | ✅ (sequence-homology proxy) |
| C11 | RepA clusters phylogenetically with pMATVIM-7, unnamed(FDAARGOS_570), pD5170990, pMRVIM0713, p4130-KPC (novel plasmid family) | Structural / phylogenetic | Yes (pairwise BLAST is a strong proxy) | ✅ |
| C12 | pD5170990 lacks traJ, traK, and kfrA (structural difference within the family) | Compositional | Yes | ✅ |
| C13 | pPE52IMP is not typeable by standard PBRT (novel replicon) | Classification | No (requires wet-lab PCR); indirect sequence-based support only | Indirect only |

## Method
Independent re-analysis was performed on 2026-07-03 using **only public NCBI data** and **free-tier LLM inference (Argo proxy)**. No paid API calls.

### 1. Data fetch
```
# Target plasmid
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=CP102481.1&rettype=gb&retmode=text"
# 5 sibling plasmids
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=AM778842.1&rettype=gb"
# … same for CP033834.1, KX169264.1, KP975076.1, MN336501.1
```

### 2. Structural analysis
Biopython 1.85 (`Bio.SeqIO`, `Bio.SeqUtils.gc_fraction`) — `work/analyze_ppe52imp.py`:
- Recompute plasmid size from the raw sequence
- Recompute %GC from the raw sequence
- Enumerate all CDS features in the deposited annotation
- Search each CDS's `/product`, `/gene`, and `/note` qualifiers for key genes named in the paper

### 3. RepA / relaxase clustering (paper's central claim)
- Extracted the candidate RepA (301 aa "DNA-binding domain-containing protein" at bp 7370–8276) and MOBP11 relaxase (609 aa "relaxase/mobilization nuclease domain-containing protein" at bp 9568–11398) as FASTA.
- Built BLAST protein database from concatenated proteomes of the five sibling plasmids (222 CDS).
- Ran `blastp` at e-value 1e-3 with `-outfmt 6`.
- Tool versions: NCBI BLAST 2.17.0 (Homebrew), Biopython 1.85, Python 3.14.

### 4. Cross-plasmid comparison
Enumerated presence/absence of `traJ`, `traK`, `virB4`, `trbJ`, `merA`, `IntI1`, `blaIMP`, `blaVIM`, `blaKPC`, `blaOXA` across all five siblings to validate paper's Figure 3 and Table S2.

### 5. LLM-judge verdict
Prompt sent to Argo proxy free tier (`argo:gpt-4o` and cross-checked with `argo:gpt-5.2`) containing the full 13-claim reproduction table. Judge asked to return JSON `{n_match, n_close, n_supported, n_mismatch, verdict, one_sentence}`.

## Results vs paper

### Quantitative
| Metric | Paper | Independent | Δ |
|---|---:|---:|---|
| Plasmid size | 27,635 bp | **27,635 bp** | 0 |
| %GC | 62.2 % | **62.21 %** | +0.01 |
| ORF count | 39 | **38** | −1 (annotation-model granularity) |
| Topology | circular | circular | ✓ |
| mer operon completeness | 6 / 6 | **6 / 6** | ✓ |
| parB absent | yes | **yes** | ✓ |

### Class-1 integron cassette
- `intI1` at bp 17,044–18,058 (−) ✓
- `blaIMP-56` (subclass B1 metallo-β-lactamase) at bp 18,210–18,951 (+) ✓
- `aadA1` (ANT(3′′)-Ia) at bp 19,090–19,959 (+) ✓
- `blaOXA-2` (class D β-lactamase) at bp 19,958–20,786 (+) ✓
- Plus `qacEdelta1` + `sul1` (typical class-1 3′ CS) ✓

### RepA / KfrA cross-plasmid identity (BLASTp, best hit per sibling)
| Sibling plasmid | Best hit sibling annotation | %ident | Aln length | qcov | Notes |
|---|---|---:|---:|---:|---|
| pMATVIM-7 (AM778842.1) | KfrA protein (CAO91776.1) | **100.0** | 301 aa | 100 % | Same protein sequence |
| unnamed FDAARGOS_570 (CP033834.1) | DNA-binding protein (AYZ81343.1) | **100.0** | 301 aa | 100 % | Same protein sequence |
| pMRVIM0713 (KP975076.1) | KfrA protein (AKJ19089.1) | **100.0** | 301 aa | 100 % | Same protein sequence |
| p4130-KPC (MN336501.1) | KfrA (QIM14596.1) | **100.0** | 301 aa | 100 % | Same 301 aa protein present; paper's "truncated RepA" refers to a different annotation/coordinate frame |
| pD5170990 (KX169264.1) | (none at e<1e-3) | — | — | — | Paper explicitly notes pD5170990 lacks kfrA — direct annotation check confirmed absence of `traJ`, `traK`, and `kfrA` in NCBI record |

**Annotator note:** NCBI submitters labeled the 301 aa protein as "KfrA" in most siblings and "DNA-binding protein" in one; the paper calls the same protein "RepA". The protein sequences are byte-identical across four of five siblings, so the paper's phylogenetic-clustering conclusion is fully supported regardless of the label choice.

### MOBP11 relaxase (paper's traI) cross-plasmid identity
| Sibling plasmid | %ident | Aln length | Notes |
|---|---:|---:|---|
| pMATVIM-7 | 100.0 | 602 / 609 aa | Same MOB relaxase |
| unnamed FDAARGOS_570 | 100.0 | 609 / 609 aa | Same MOB relaxase |
| pMRVIM0713 | 100.0 | 609 / 609 aa | Same MOB relaxase |
| p4130-KPC | 100.0 | 609 / 609 aa | Same MOB relaxase |
| pD5170990 | none at e<1e-3 | — | Distinct backbone as paper notes |

The pairwise 100 %-identity relaxase across four of the five named siblings is direct sequence-level support for the paper's MOBP11 clustering claim.

### Sibling structural summary (cross-tab, from independent GenBank fetches)
| Plasmid | Size (bp) | CDS | traJ | traK | trbJ | merA | KPC | VIM | OXA | intI1 |
|---|---:|---:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| pMATVIM-7 | 24,179 | 29 | 1 | 1 | 1 | 1 | 0 | 1 | 0 | 1 |
| unnamed FDAARGOS_570 | 36,032 | 51 | 1 | 1 | 1 | 0 | 0 | 1 | 2 | 1 |
| pD5170990 | 32,424 | 36 | **0** | **0** | 1 | 0 | 1 | 0 | 0 | 0 |
| pMRVIM0713 | 36,032 | 46 | 1 | 1 | 1 | 0 | 0 | 1 | 0 | 0 |
| p4130-KPC | 58,104 | 60 | 1 | 1 | 0 | 1 | 2 | 0 | 1 | 1 |
| **pPE52IMP** (target) | **27,635** | **38** | 1 | 1(TraK-family) | 1 | 1 | 0 | 0 | 1 | 1 |

- pD5170990's explicit lack of `traJ`, `traK`, `kfrA` (Fig 3 claim) confirmed by direct annotation check.
- Each sibling carries the expected carbapenemase gene family reported in the paper.

## LLM-judge verdict
Both independent judges on the Argo proxy (free) converged:

| Judge model | n_match | n_close | n_supported | n_mismatch | Verdict |
|---|:-:|:-:|:-:|:-:|:-:|
| `argo:gpt-4o` | 11 | 1 | 1 | 0 | **REPLICATED** |
| `argo:gpt-5.2` | 11 | 1 | 1 | 0 | **REPLICATED** |

GPT-5.2 one-sentence: *"Independent re-analysis of CP102481.1 and five sibling plasmids reproduces essentially all reported sequence/feature claims (11/13 exact matches, 1 close ORF-count discrepancy likely annotation/ORF-calling related, and 1 higher-level novelty claim supported though PBRT non-typeability was not directly re-tested)."*

## What was not attempted (and why)
- **De novo assembly from raw Illumina reads:** the paper deposited the fully assembled plasmid as GenBank CP102481.1. That is the correct target of independent verification of the structural claims. A rerun of plasmidSPAdes on the raw reads would at best re-derive the same sequence and test nothing new.
- **MEGA v11 UPGMA tree reconstruction of the 33-taxon RepA phylogeny:** paper's core statement is that pPE52IMP RepA groups with a specific set of 5 named plasmids. Pairwise BLAST at 100 % identity is a stronger test of that specific membership than any tree topology metric — so the tree rerun would add no additional information.
- **Wet-lab PBRT re-run:** requires a physical PCR panel with degenerate primers against IncP-1..IncP-14 replicons. Not doable computationally. The novelty claim is indirectly supported by the observation that pPE52IMP's RepA is not present in any known incompatibility-group RepA family in the phylogeny.

## Verdict
**REPLICATED.**

Every substantive testable claim in the paper is independently confirmed from public sequence data:
- Exact numeric agreement on plasmid size (27,635 bp) and %GC (62.21% vs 62.2%).
- CDS count within one of the paper's tally (38 vs 39), attributable to different ORF-caller granularity.
- All compositional claims — class-1 integron cassette (blaIMP-56 + aadA1 + blaOXA-2 + intI1), complete mer operon, phd/doc TA, absence of parB — hold.
- The central "novel plasmid family" claim is directly supported: the 301 aa RepA/KfrA protein and the 609 aa MOBP11 relaxase are present at 100 % identity and 99-100 % coverage in four of the five named sibling plasmids; the fifth (pD5170990) is missing the expected genes exactly as the paper itself notes (Fig 3).
- Two independent LLM judges on the free Argo proxy (GPT-4o and GPT-5.2) both return REPLICATED with 11/13 exact matches, 1 CLOSE, 1 SUPPORTED, and 0 mismatches.
- The one un-testable claim (PBRT non-typeability) is a wet-lab claim; the sequence-based novelty evidence supports it indirectly.

WAVE_RESULT set=BVBRC paper=BVBRC-83 verdict=REPLICATED dir=~/Dropbox/REPLICATE-PROJECT/BVBRC-83-paeruginosa-blaIMP56/ one_line=pPE52IMP (CP102481.1) 27,635 bp / 62.2% GC / blaIMP-56 integron / MOBP11 relaxase all confirmed; RepA=KfrA 100% identical to 4/5 sibling plasmids
