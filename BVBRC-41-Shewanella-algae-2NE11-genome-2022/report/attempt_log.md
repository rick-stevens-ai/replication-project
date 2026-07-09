# Attempt Log — BVBRC-41 (Shewanella algae 2NE11 genome, 2022)

Analyst: Ollie (OpenClaw AI subagent) · Date: 2026-07-01

1. **Dedup check** — `ls ~/Dropbox/REPLICATE-PROJECT/ | grep -iE "shewanella|2NE11"` → no existing dir. Proceeded.
2. **Read brief + exemplar** — WAVE_BRIEF_2026-07-01.md + BVBRC-17 REPORT.md (structure/verdict template).
3. **Located paper** — Europe PMC search → PMC8816663 / PMID 35145887. Pulled full-text XML (120 KB) via `europepmc/.../fullTextXML`. Extracted to plain text. ✅ free endpoint.
4. **Extracted claims** — from full text: genome length 5,030,813 bp, GC 52.98%, 1 circular contig, coverage 231.29×, feature counts (Table 2), decolorization genes (azoreductase HU689_20695, Dyp HU689_05310, Mtr operon, oxidoreductases), metal-resistance genes, carbohydrate genes, CRISPR-Cas, two genomic islands. Data-availability: **CP055159** / PRJNA547647 / SAMN15232066.
5. **Resolved assembly** — CP055159 → NCBI Assembly UID 7926261 → **GCF_014263185.1** (ASM1426318v1), coverage 231.29× (matches paper). ✅
6. **Downloaded genome** — `datasets download genome accession GCF_014263185.1 --include genome,protein,gff3,gbff,cds` (8.07 MB, md5-validated). ✅ free, no auth.
7. **Recomputed assembly stats** — Python: length **5,030,813 bp EXACT**, GC **52.98% EXACT**, 1 contig. ✅
8. **Feature counts** — parsed RefSeq GFF: protein-coding 4288 (EXACT vs paper), tRNA 110+1 pseudogenic = 111 (EXACT), rRNA 25 (EXACT), CDS 4343 (paper 4334). Assembly report (2026 re-annotation) shows minor drift (proteinCoding 4295, pseudo 48).
9. **Gene-content verification** — grep RefSeq GFF/faa by function + locus:
   - Azoreductase HU689_RS20690: 594 bp / **197 aa** (paper 594bp/197aa) EXACT.
   - Dyp peroxidase HU689_RS05305: 936 bp / **311 aa** (paper 936bp/311aa) EXACT.
   - Mtr operon HU689_RS08355–RS08390 (paper HU689_08360–08395); multiple OmcA/MtrC decaheme cytochromes → OmcA duplication confirmed.
   - Metal: cadA, corA/corC, zntB, arsA/arsB/arsC — all present.
   - Carbohydrate: L-lactate permease + lactate utilization; 6 Nag genes.
   - CRISPR-Cas: **Type I-F** (Cas1f, Cas3f, Cas6/Csy4) + CRISPR direct-repeat array.
   - Locus-tag mapping: paper HU689_XXXXX ≈ RefSeq HU689_RS(XXXXX−5), a known RefSeq re-index.
10. **Independent re-annotation (Prokka 1.12)** — scp genome to uicgpu, ran `prokka --genus Shewanella` in env `/data/stevens/envs/bvbrc28`. Result: bases 5,030,813 (exact), 1 contig, CDS 4385, tRNA 109, rRNA 25; azoreductase ×4, peroxidase, cadmium/CorA/CorC/ZntB/arsenic all present. Fully independent of paper's PGAP. ✅
    - Gotcha: prokka picked up system Perl (missing XML::Simple) unless the conda env is activated first (`conda activate` before invoking). Fixed.
11. **Genomic-island prediction** — wrote self-contained DIMOB-style predictor (dinucleotide relative-abundance bias + mobility-gene co-location). Found 7 mobility-associated atypical islands, largest ~48 kb/51 genes; T4SS/conjugative cluster located ~4.03–4.07 Mb. Qualitatively confirms HGT islands but exact GI-I/GI-II sizes/count not reproduced (IslandViewer 4 uses curated multi-method consensus).
12. **LLM judge (free Argo gpt-5.2)** — coverage 12/13, agreement 10/12, **FINAL_VERDICT: REPLICATED**.
13. Wrote report/ + evidence/ + work/.
