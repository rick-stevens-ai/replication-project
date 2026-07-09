# Attempt Log — BVBRC-47 (2026-07-01)

Chronological. All times CDT.

1. **Dedup.** `ls ~/Dropbox/REPLICATE-PROJECT | grep -iE "variovorax|PAMC"` → only `BVBRC-04-Variovorax-trehalose-Shrestha2022`. Read its REPORT.md: BVBRC-04 = Shrestha 2022 **BMC Genomic Data** 23:4, DOI 10.1186/s12863-021-01020-y, single strain PAMC28711, trehalose *pathway prediction*. THIS task = Shrestha 2022 **Int J Microbiology**, DOI 10.1155/2022/5067074, three strains, *complete genome + comparative analysis*. Different journal/DOI/PMC/scope → NOT a dup. Proceeded.
2. Read wave brief + BVBRC-17 exemplar for structure.
3. Identified paper: web_search → PMC10232917, DOI 10.1155/2022/5067074, PMID 37275508. OA confirmed via Europe PMC (`isOpenAccess=Y`).
4. Pulled full-text XML from Europe PMC (`PMC10232917/fullTextXML`, 162 KB). Extracted abstract, Materials & Methods, and all 5 tables (regex tag-strip, free — no `pdf`/`image` paid tools).
5. Extracted testable claims: genome sizes/GC/CDS/genes/tRNA (Table 1), ANI/dDDH (Table 2), CAZyme counts (Table 3), trehalose pathway inventory (Table 1), "lowest GC among 19 Variovorax."
6. Resolved strain→assembly accessions: PAMC28711=GCF_001577265.1, PAMC26660=GCF_014302995.1, PAMC28562=GCF_014303735.1 (via NCBI esearch/esummary on nucleotide accessions CP014517/CP060295/CP060296). V. paradoxus NBRC15149T = GCF_050627025.1.
7. **Failure #1:** first two uicgpu download attempts hung with no output. Root cause = did NOT `source ~/env.sh`, so no HTTP proxy → NCBI unreachable from uicgpu. Verified: with env.sh, `http_proxy=http://<lan-host>:3128` and NCBI returns 200. Fix = always `source ~/env.sh` before any external fetch on uicgpu. (Logged to failure pattern.)
8. Downloaded all 4 assemblies (genome+protein+gff3) with `datasets` in env `bvbrc28`. All validated.
9. Computed genome stats → EXACT match on sizes (4.32/7.39/4.69 Mb), tRNA (46/52/47), GC% within 0.05%.
10. Ran fastANI all-vs-all. PAMC→Vpar ANI 81-86%, all <95% species threshold. (fastANI ≠ paper's ANIb/ANIm/dDDH, so numbers offset 1-3% but same conclusion.)
11. Trehalose pathway scan from RefSeq/PGAP product names. First otsA regex missed URL-encoded `%2C` in "alpha,alpha-trehalose-phosphate synthase"; fixed decode. Result: PAMC28711 & PAMC28562 = 3 pathways; PAMC26660 = OtsAB only. EXACT match to headline claim.
12. Proteome comparison (blastp best-hit orthology): 79-81% shared orthologs across the 3 PAMC strains.
13. Confirmed PAMC28562 GC (63.73%) is lowest of all 19 strains in Table 1.
14. Attempted Hindawi PDF archive → Cloudflare HTML block; discarded (Europe PMC XML is canonical source). No paid PDF tool used.
15. LLM-judge via free Argo `argo:gpt-5.2` → **REPLICATED**, Coverage 8/10, Agreement 9/10.
16. Wrote report/ + copied evidence JSON/TSV.

## Not done (out of feasible free scope this pass)
- CAZyme-family counts (Table 3) — needs dbCAN2 / `run_dbcan` (not in env). Product-name trehalase scan done as proxy.
- Exact ANIb/ANIm/dDDH numeric reproduction — used fastANI instead (OAT/GGDC pipelines not installed).
- AZCL wet-lab polysaccharide-degradation screening (Table 5) — experimental, not computationally reproducible.
