# Attempt Log — BVBRC-44 (2026-07-01, night wave)

1. **Dedup check.** `ls ~/Dropbox/REPLICATE-PROJECT/ | grep -iE "baumannii|pCl107|acinetobacter"` → only BVBRC-24 (AbGRI4, Chan2020 — a *different* A. baumannii paper). No pCl107 dir. Proceeded.
2. **Read brief + exemplar.** WAVE_BRIEF_2026-07-01.md and BVBRC-17 (E. coli B2/IBD) REPORT.md for structure/depth.
3. **Located paper.** Europe PMC search → PMC10117892, DOI 10.1093/femsmc/xtac027, CC BY, OA. Pulled full-text XML (172 KB) → work/fulltext.xml.
4. **Mined accessions from full text.** Data-availability section: **CP098521 = chromosome, CP098522 = pCl107**; SRR20613520 (Illumina), SRR20613519 (MinION). Reference plasmids in text: KU744946 (pA297-3), CP012005 (pAB3), KT779035 (pD4), MF399199 (pD46-4), MK531536 (pMC1.1).
5. **Extracted 11 testable claims** from Results/Methods (sizes, ST typing, resistance genes, AbGRI1 relatedness, BREX, ptx, uric-acid, P450, MPF, chromosomal determinants, plasmid family).
6. **uicgpu setup.** `ssh uicgpu; source ~/env.sh` (proxy). Tools: bvbrc28 env (prokka/datasets/blast/mafft/FastTree), amr micromamba env (AMRFinderPlus 3.12.8), bvbrc14 env (mlst + abricate). Workdir `/data/stevens/scratch/bvbrc44-pCl107`.
7. **Downloaded sequences** via NCBI eutils efetch (through proxy). Verified exact lengths: chromosome 4,056,235 bp ✓, plasmid 198,716 bp ✓ (both EXACT to paper). Pulled plasmid gbff (197 CDS).
8. **Resistance genes — 3 independent callers.** AMRFinderPlus (--organism Acinetobacter_baumannii), abricate/ResFinder, and RefSeq annotation. All agree: sul2, tet(B), aph(3'')-Ib+aph(6)-Id (=strAB), aac(3)-IIe (=aacC2), aac(6')-Ian (=aacA1) — all 100% cov/id. Plus mer operon.
9. **Host typing.** `mlst` Pasteur → **ST25**, Oxford → **ST229**. Both EXACT to paper.
10. **Module coordinates** mined from gbff: BREX (brxL/pglZ/pglX/brxC, start 125,913 = paper's stated start), ptx (phnC/D/E + ptxD ~149-152 kb), uric acid (puuE/uraD/uraH present; **urate oxidase absent → incomplete, matches paper**), cytochrome P450, MPF (DotA/TraY, DotD/TraH).
11. **Comparative / "missing link".** blastn of pCl107 resistance region (75-90 kb) vs pA297-3 = 100% id over ~12.3 kb; vs pAB3 = 100/96%. Whole-plasmid relatedness ranked MK531536 (pMC1.1) closest — matches paper.
12. **Chromosome determinants.** AMRFinderPlus on chromosome → blaOXA-64, blaADC-26, gyrA_S81L, parC_S84L — all match paper exactly.
13. **LLM judge (free Argo gpt-5.2).** coverage 9/10, agreement 10/10, verdict **REPLICATED**. Saved to evidence/llm_judge_argo_gpt5.2.json.
14. **Wrote report + evidence.** All evidence in report/evidence/; lean artifacts in work/.

## What worked
- Deposited assemblies exactly match paper sizes; multiple independent AMR callers unanimous; MLST exact; module coordinates match to the base.

## Not done (gap to a hypothetical "beyond REPLICATED")
- De-novo hybrid reassembly from raw SRA (SRR20613520/19); 90-taxon BREX phylogeny; Kaptive KL14/OCL6 capsule typing; exhaustive 616-plasmid comparative panel. None affect the tested core claims.
