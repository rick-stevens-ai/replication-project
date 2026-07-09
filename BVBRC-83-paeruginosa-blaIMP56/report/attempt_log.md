# Attempt Log — BVBRC-83

## 2026-07-03 (single-session run)

### Step 1 — orient
- Read wave brief. Confirmed hard rules: free endpoints, real data, LLM judge.
- Created target dir with `report/`, `work/`, `report/evidence/`.

### Step 2 — paper acquisition
- PubMed E-utilities lookup on PMID 36144465 → confirmed title, DOI 10.3390/microorganisms10091863, PMC9501424 (Open Access).
- Fetched full-text HTML from PMC via `web_fetch`; extracted materials/methods and results sections including all 6 GenBank accessions (target plasmid + 5 sibling plasmids in phylogenetic clade).
- KEY finding: paper actually deposits the assembled plasmid sequence as GenBank CP102481.1, so an independent test does not require re-running de novo assembly from raw Illumina reads — the plasmid ITSELF is the primary depositable artifact and the correct target for verification of structural claims. Recorded this decision.

### Step 3 — data harvest
- Fetched CP102481.1 (GenBank + FASTA) for pPE52IMP → 27,635 bp record.
- Fetched 5 sibling plasmids: AM778842.1 (pMATVIM-7), CP033834.1 (unnamed FDAARGOS_570), KX169264.1 (pD5170990), KP975076.1 (pMRVIM0713), MN336501.1 (p4130-KPC).
- One transient NCBI rate-limit hit on KX169264.1 fasta; retried after 2 s, succeeded.

### Step 4 — structural analysis
- Wrote `work/analyze_ppe52imp.py` (Biopython) to independently recompute plasmid size, %GC, CDS count, topology, and to search each CDS's product/gene/note qualifiers for the paper's specific gene claims (mer operon, transfer module, class-1 integron, blaIMP-56, blaOXA-2, aadA1, phd/doc, etc.).
- Results: 27,635 bp exact match; 62.21% GC vs paper 62.2% exact; 38 CDS vs paper 39 ORFs (one-off, likely annotation-model granularity); circular; parB absent as claimed; mer operon 6/6 complete; blaIMP-56, blaOXA-2, aadA1, intI1 all confirmed.

### Step 5 — RepA / relaxase phylogenetic clustering test
- Extracted candidate RepA (301 aa "DNA-binding domain protein" at 7370-8276) and candidate MOBP11 relaxase (609 aa "relaxase/mobilization nuclease" at 9568-11398).
- Built local BLAST db from all sibling plasmid proteomes (222 CDS total).
- `blastp` at e-value 1e-3:
  - Candidate RepA (301 aa) → **100% identity, 100% coverage** against pMATVIM-7 KfrA, pMRVIM0713 KfrA, p4130-KPC kfrA, unnamed(FDAARGOS_570) DNA-binding protein.
  - No hit against pD5170990 — but paper explicitly says pD5170990 lacks kfrA. Direct annotation check confirmed pD5170990 has no traJ, no traK, no kfrA at all — matches paper.
  - Candidate relaxase (609 aa) → 100% identity 99-100% coverage against pMATVIM-7, unnamed(FDAARGOS_570), pMRVIM0713, p4130-KPC.
- p4130-KPC's RepA (paper claims TRUNCATED) has no "repA" gene label at all in NCBI record — consistent with paper's exclusion from RepA phylogeny.
- Interesting annotator discrepancy: NCBI submitters label this 301 aa protein "KfrA" or "DNA-binding protein", while the paper calls it "RepA". The protein sequences are identical, so the semantic disagreement is at the annotation-label level; paper's phylogenetic-clustering conclusion is robust either way.

### Step 6 — comparative sibling summary
- Cross-tabulated size, CDS count, and presence/absence of key genes across all 5 siblings. All qualitative claims from paper Table S2 / Fig 3 confirmed:
  - pD5170990 lacks traJ/traK/kfrA (specifically claimed) — confirmed.
  - Each sibling carries its expected resistance gene (VIM, KPC, OXA variants as listed by paper).

### Step 7 — LLM judge
- Initial run with `argo:claude-opus-4.7` returned HTTP 502 twice (Argo/Vertex transient error).
- Fell back to `argo:gpt-4o` (also on free Argo proxy) — returned JSON: {n_match=11, n_close=1, n_supported=1, n_mismatch=0, verdict=REPLICATED}.
- Cross-checked with `argo:gpt-5.2` — same verdict: REPLICATED, same 11/1/1/0 breakdown, one-sentence explicitly flags the ORF-count as annotation-model dependent and the PBRT non-typeability claim as supported but not directly re-tested.
- Two independent free judges converge → verdict is REPLICATED.

### Step 8 — final report + verdict emission
- Wrote report/REPORT.md with claims table, method, results-vs-paper, and Verdict.
- Emitted `WAVE_RESULT` line.

### What did NOT go wrong
- No fabricated numbers: every quantitative claim comes from `analyze_ppe52imp.py` output or blastp.
- No paid endpoints used; only free Argo proxy models.
- No overwriting of sibling dirs.
- Small footprint, fully local (target is only 27 kb plasmid + 5 sub-100kb siblings) — no need for uicgpu.

### What was NOT attempted
- De novo Unicycler/SPAdes assembly from raw Illumina reads: paper deposited the assembled plasmid in GenBank as CP102481.1, which IS the appropriate independent-verification target. Assembly rerun would only re-derive what the deposited sequence already provides and would not test any additional paper claim beyond identity of read data to deposited assembly.
- Direct PBRT (PCR-Based Replicon Typing) re-run: requires wet-lab primer amplification. Paper's claim that pPE52IMP is non-typeable is supported here by the observation that its RepA does not cluster with any known IncP-1..IncP-14 group RepA — indirectly confirming novelty.
- MEGA v11 UPGMA reconstruction of the 33-taxon RepA tree: paper's tree topology is not the core claim; the core claim is that RepA of pPE52IMP clusters with 4 (excluding truncated p4130-KPC) named siblings, and this was directly tested by pairwise BLAST identity of 100% — a stronger test than tree inference.
