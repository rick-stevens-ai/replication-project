# Attempt Log — BVBRC-33 (2026-07-01)

1. **Dedup check** — `ls ~/Dropbox/REPLICATE-PROJECT | grep -iE "kpneu|klebsiella|hypervirulent"` → only `BVBRC-14-HybridAssembly-Ecoli-Kpneu-Khezri2021` (a different paper: hybrid assembly, Khezri 2021). No dir for this hypervirulent/hypermucoviscous paper → proceeded.
2. **Read brief + BVBRC-17 exemplar** for structure & verdict vocabulary.
3. **Identified paper** via Semantic Scholar (S2 API key from keychain): exact title includes "…Strain **Lacking the Hypermucoviscous Regulators (rmpA/rmpA2)**" — DOI 10.3390/antibiotics11050596, PMID 35625240, PMC9137517.
4. **Fetched full text** — MDPI PDF bot-blocked (411 B HTML). Used Europe PMC `fullTextXML` (176 KB) + PMC HTML. Stripped to `work/paper.txt`.
5. **Located the study's genome from full text** — Data Availability: BioProject PRJNA767482, BioSample SAMN26332310, WGS JAKWFM000000000, strain 9KP.
6. **Resolved accession** — Datasets REST by biosample SAMN26332310 → **GCA_022511605.1** (K. pneumoniae 9KP). (BioProject alone is an umbrella project with many isolates incl. E. coli, so biosample was the correct key.)
7. **Downloaded** genome+protein+gff via `datasets download` (3.06 MB). Stats: 5,364,730 bp / 83 contigs / GC 57.33% / N50 220,979 — consistent with KpSC.
8. **Tooling** — kleborate/amrfinder/mlst absent locally and on uicgpu. Built a local stack: pip `kleborate`+`kaptive` in a venv; bioconda env `kleb` with minimap2+mash+ncbi-amrfinderplus+blast (kleborate deps). `amrfinder -u` → DB 2026-05-15.1. Ran kleborate from venv with kleb-env bin prepended to PATH so it finds minimap2/mash/amrfinder.
9. **Kleborate kpsc** on the assembly → K. pneumoniae, **ST14**, **KL2/K2** (99.83%, wzi2), **O1** (OL2α.1, 100%), **rmpA absent / rmpA2 absent**, ybt/clb/aerobactin/salmochelin absent, virulence_score 0; AMR: SHV-28(chr), OXA-1, sul2, aph(3'')-Ib, aph(6)-Id, aac(6')-Ib-cr, tet(A), GyrA S83Y, cipro nonwildtype R.
10. **AMRFinderPlus** (--organism Klebsiella_pneumoniae --plus) → confirmed above + fosA(FosA5 family), oqxA/oqxB. Hits map to study contigs JAKWFM01… confirming identity.
11. **Reconciled virulome vs paper** — PGAP product-name checks in protein.faa: **IroE present** (matches paper), **RcsA + RcsB present** (matches paper's alternative regulators), **T6SS** 32 components (matches "4 T6SS"), rich fimbriome (46 fimbrial/pilus products vs paper's 19). **iutA/aerobactin and iroN/salmochelin NOT confirmed** by curated Kleborate loci.
12. **blaCTX-M-15 blastn** vs deposited assembly → **NO hit** (fragments ≤44 bp, qcov ≤7%). Paper placed it on plasmid pMDR; plasmid content evidently not in the deposited draft assembly.
13. **LLM judge** — `argo:claude-opus-4.8` → HTTP 502 (proxy bug). Fell back to **`argo:gpt-5.2`** (free): **PARTIAL**, **15/18 = 0.83**, key discrepancy = missing plasmid-borne blaCTX-M-15.
14. Wrote report + evidence.

## What worked / failed
- ✓ Biosample→assembly resolution via Datasets REST was the crux (avoided the umbrella-BioProject trap).
- ✓ Kleborate + AMRFinderPlus reproduced the paper's core typing exactly on the authors' own genome.
- ✗ MDPI PDF direct download blocked → Europe PMC XML.
- ✗ argo opus judge 502 → gpt-5.2 fallback (both free, per rule).
- ⚠ Kleborate curated loci disagree with the paper's VFDB/RAST-based aerobactin(iutA)/salmochelin(iroN) calls — a genuine tool-dependent virulome discrepancy worth flagging; plasmid genes absent from deposited assembly.
