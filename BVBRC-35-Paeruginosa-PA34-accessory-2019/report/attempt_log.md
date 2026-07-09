# Attempt Log — BVBRC-35 (PA34 accessory genome)

**2026-07-01, Ollie**

1. Dedup check: `ls REPLICATE-PROJECT | grep -iE pseudomonas|aeruginosa|PA34` → no match. Proceeded.
2. Read WAVE_BRIEF_2026-07-01.md + BVBRC-17 exemplar REPORT.md for structure.
3. Resolved paper: DOI 10.1371/journal.pone.0215038, PMC6464166. Fetched printable PDF + Europe PMC full-text XML (free).
4. **PDF tool routed to paid Anthropic (credit-balance error)** → pivoted to parsing the free Europe PMC XML directly with Python/regex to extract accessions, tool list, and all headline numbers. (Lesson: for OA papers, use Europe PMC fullTextXML, not the paid `pdf` tool.)
5. Extracted claims: pangenome 7,643 / core 5,078 / accessory 1,213 / unique 543 / no-ortholog 886/737/946 / PA34∩VRFPA04 124 / ST1284 / exoU / AAC(3)-IId / 6 plasmid AMR genes; tools Roary 3.12, Prokka, ResFinder, MAUVE.
6. **Accession resolution snag:** naive `GCA_003812505.1` guess for PA34 returned an unrelated *Staphylococcus hominis* record; VRFPA04 `GCF_000496935.1` also wrong. Fixed via NCBI esearch: PA34 = GCF_003332705.2 (chromosome CP032552), VRFPA04 = GCF_000473745.2. PAO1/PA14 confirmed by dataset_report organism field.
7. Downloaded 4 genomes (NCBI Datasets REST) + 2 PA34 plasmids (nuccore efetch). Verified plasmid sizes 95,404 / 26,862 bp and GC 57.2 / 61.0 = **exact** paper match.
8. **uicgpu env discovery:** no standalone prokka/roary in PATH, but existing `bvbrc28` env (from prior waves) has **prokka 1.12 + roary 3.12.0**, and `bvbrc14` has abricate + mlst. Reused them (no new installs needed).
9. **First job launch failed silently:** `set -euo pipefail` + `source ~/env.sh` killed the scripts before first echo (0-byte output). Fixed by dropping `set -e` and sourcing conda directly; relaunched with `setsid ... < /dev/null`.
10. Noted a concurrent BVBRC-29 (B. anthracis) Roary job on the same box using bvbrc28 — 255 cores, load ~45, ample headroom, no conflict.
11. Prokka ran on all 4 (PA34 6246, PAO1 5671, PA14 5901, VRFPA04 6129 CDS). Roary completed: core 5,079 / total 7,639.
12. AMR job also died silently on first pass; reran abricate steps inline → ResFinder 16, CARD 60, VFDB 300; MLST ST1284; exoU + aac(3)-IId confirmed.
13. `analyze_roary.py` on the presence/absence matrix reproduced the Fig-1 Venn: unique 543 (exact), no-ortholog 886/737/945, PA34∩VRFPA04 124 (exact).
14. Copied evidence back to report/evidence. LLM-judge (free argo:gpt-5.2) → **REPLICATED, ~92% coverage, VERY HIGH agreement.**
15. Wrote REPORT.md, brief.md, artifact_harvest.md.

**Result:** REPLICATED — near-exact numerical reproduction of the paper's pangenome/accessory analysis on real public data.
