# PENDING — Marker parse

**Reason:** `paper.pdf` is not resolvable through free channels. Fraser 1995 *Science* is paywalled and Unpaywall reports zero OA locations (`is_oa=false`) for DOI 10.1126/science.270.5235.397.

**sha256:** N/A (no PDF)

**Central corpus resolution attempted:** No — no PDF to hash against the SCOUT/OSTI Eagle manifests.

## What is known about the paper without the PDF (all from public metadata + landmark literature)

**Title:** The Minimal Gene Complement of *Mycoplasma genitalium*
**Authors:** Fraser CM, Gocayne JD, White O, Adams MD, Clayton RA, Fleischmann RD, Bult CJ, Kerlavage AR, Sutton G, Kelley JM, Fritchman RD, Weidman JF, Small KV, Sandusky M, Fuhrmann J, Nguyen D, Utterback TR, Saudek DM, Phillips CA, Merrick JM, Tomb J-F, Dougherty BA, Bott KF, Hu P-C, Lucier TS, Peterson SN, Smith HO, Hutchison CA III, Venter JC.
**Journal:** *Science* **270**, 397–403.
**Publication date:** 20 October 1995.
**DOI:** 10.1126/science.270.5235.397
**PMID:** 7569993
**GenBank accession (1995):** L43967 (580,070 bp)
**Current RefSeq:** NC_000908.2 (580,076 bp)
**Assembly:** GCF_000027325.1
**BioProject:** PRJNA224116
**Confirming metadata source:** NC_000908.2 GenBank flat file, REFERENCE 2, bases 1..580076 — cites this paper directly.

## Public abstract (paraphrased/summarised — not verbatim)
Fraser et al. report the complete sequence of the *Mycoplasma genitalium* G37 genome (580,070 bp; ~470 predicted protein-coding genes; ~32% G+C; 1 rRNA operon; 36 tRNAs covering all 20 amino acids). At the time of publication it is the smallest known genome of any self-replicating organism. Comparative analysis with the previously sequenced *Haemophilus influenzae* Rd genome is used to identify a candidate minimal set of essential genes, launching the "minimal genome" research programme.

## Fields plausibly present in the full paper (from decades of citing literature and JCVI follow-ups) — not extracted, only listed for downstream nougat/marker verification
- Full ORF list (locus_tag MG_001…MG_486 in the original nomenclature) with functional category assignments.
- Table of tRNA species with anticodons + amino acid coverage.
- GC-skew figure (used for putative origin/terminus placement).
- Metabolic pathway inventory — glycolysis complete, no TCA cycle, limited biosynthetic capacity.
- Comparative-genomics table vs *H. influenzae* Rd producing the ~256-gene candidate minimal set (later revised).
- Discussion of gene functional categories using an early Riley/COG-like scheme.

## How to close this stub
Drop the real Fraser 1995 PDF into `<dir>/paper.pdf` (Rick has institutional Science access), then run Marker on it and overwrite this file with the resulting `.md`. Recompute sha256 and log at the top.
