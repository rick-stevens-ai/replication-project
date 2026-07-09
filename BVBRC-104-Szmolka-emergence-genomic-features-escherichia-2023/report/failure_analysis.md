# Failure Analysis — BVBRC-104

Honest analysis (per Rick's 2026-07-05 hard rule) of what failed, why, workarounds, residual gaps,
and what would be needed to close them. This is deliberately not a rubber-stamp — the verdict is
REPLICATED but the evidence has real edges that should be documented.

## A. Things that failed during the original run + workarounds

### A1. MDPI direct HTML fetch (Access Denied)
- **What failed.** `curl` against `https://www.mdpi.com/2079-6382/12/10/1519` from CherryRd and via
  uicgpu proxy both returned MDPI's anti-bot Access-Denied page.
- **Root cause.** MDPI runs Cloudflare + JS-challenge on their HTML endpoint; unattended `curl`
  looks like a bot to their WAF.
- **Workaround.** Pivoted to NCBI E-utilities `efetch db=pmc id=10604428 rettype=xml` which
  returns the full JATS XML (124 KB, no gate). Parsed with Python `ElementTree` to plain text.
- **Residual gap.** Figures + Supplementary Tables S1/S2 are not in the JATS XML (PMC ingests
  text only). We never read Table S1 (BV-BRC 504-strain sampling) or Table S2 (full AMR gene
  list per plasmid) directly. For C10 this matters — Table S1 is the input to the cgMLST tree.
- **To close.** MDPI's supplementary ZIP is at
  `https://www.mdpi.com/article/10.3390/antibiotics12101519/s1` and might be fetchable with a
  browser session (not `curl`). Or use a headless browser (Playwright) with a real User-Agent.

### A2. First-pass BLAST returned junk hits
- **What failed.** First IncX4/mcr-1 reference esearch was unfiltered and pulled a Culex virus
  and a Trametes fungal mRNA on term ambiguity. First BLAST attempt against those 3 refs gave
  2–18% qcov and would have looked like a *failed* replication of the "highly conserved backbone"
  claim if we hadn't caught it.
- **Root cause.** Unfiltered NCBI Nuccore search terms — `"mcr-1" "IncX4" plasmid` matches any
  record with those tokens anywhere, including virus databases that got contaminated by mcr-1
  keyword papers.
- **Workaround.** Added size filter `30000:40000[SLEN]` and `"complete sequence"` to force real
  33 kb-range plasmids → 17 clean IncX4/mcr-1 references.
- **Residual gap.** Manual filter is subjective. A different curator might have picked a
  different 17-subset from the ~20 candidate accessions, which would slightly shift the
  pident distribution (see critique §4).
- **To close.** Use the Enterobase / PLSDB plasmid-typed reference set (curated by plasmid
  community) rather than raw NCBI Nuccore esearch.

### A3. Argo Opus 4.7 502-flap on LLM judge
- **What failed.** 4 consecutive HTTP 502 (transient Argo Vertex issue) on the 7.5 KB judge
  prompt to `argo:claude-opus-4.7`.
- **Root cause.** Argo backend Vertex passthrough hiccup (not our issue, comes and goes).
- **Workaround.** Fallback to `argo:gpt-5.2` which returned on first call.
- **Residual gap.** Single-model, single-shot judge after fallback. No cross-model quorum.
- **To close.** Standardize a 3-model judge quorum (Opus + GPT-5 + Gemini 2.5 Pro) and require
  2/3 agreement for verdicts near the REPLICATED / DID-NOT-REPLICATE boundary. Overkill for
  this clean call, essential for marginal ones.

## B. Things this replication chose not to do (declared out-of-scope)

### B1. cgMLST across 504 BV-BRC mcr-1 E. coli (C10)
- **Why skipped.** ~500 assemblies × chewBBACA runtime + proprietary Ridom SeqSphere+ dependency
  (the paper's actual tool) does not fit a 15-minute free-endpoint replication budget.
- **Consequence.** The paper's central epidemiological claim (Hungarian duck ST162 clusters with
  Chinese human strains, not with Chinese duck strain) is untested here.
- **To close.** Follow-up wave: chewBBACA + Enterobase E. coli cgMLST v1 (2513 loci) on uicgpu with
  BV-BRC re-harvested strains, bootstrap 100×. This is Q2 in `open_questions.json`.

### B2. Wet-lab conjugation transferability (C11)
- **Why skipped.** Not testable in silico.
- **Consequence.** The paper's most anomalous finding (an IncX4/mcr-1 plasmid that isn't
  conjugative) is left completely unaddressed by the replication.
- **To close.** Requires wet-lab work. This is Q1 in `open_questions.json`.

### B3. Ab initio reassembly from Illumina + ONT SRA reads
- **Why skipped.** Would only re-derive the same deposited assembly. The added value is
  small vs the disk + compute cost (~20 GB SRA + hours of Unicycler + Nanopolish).
- **Consequence.** We validated the deposited assembly, not the paper's assembly workflow.
  If the deposited FASTA has assembly errors (mis-scaffolding of the 190 kb hybrid where
  duplicated cassettes could create scaffolding ambiguity, mis-polished Nanopore homopolymer
  indels), our rerun silently inherits them.
- **To close.** Second-wave: pull SRA reads, re-run Unicycler 0.5.0 + Nanopolish 0.14.0 on
  uicgpu, hash-compare final contigs to the deposited FASTA.

## C. Critique of evidence strength (Rick 2026-07-05 hard requirement)

This is the same critique as REPORT.tex §5, restated as a failure/gap analysis for completeness.

### C1. Confirmation is against tool panels, not against biology
AMRFinderPlus 4.2.7's VF panel does not include `fyuA`, `hlyE`, or `hlyF` (all named by the
paper). Our confirmation of C7 ("101 kb + 5 kb plasmids carry no AMR/VG") is a confirmation
*only against the AMRFinderPlus curated panel* — not a confirmation that these two plasmids are
biologically inert. Col156 plasmids commonly carry colicins; p0111 plasmids are implicated in
APEC virulence. See Q5.

### C2. LLM-judge coverage number is arithmetic, not epistemic
The judge counted 8 of the tested claims (C1–C9) as covered and said 100% agreement on those.
But C10 and C11 — the two claims the paper's Discussion spends the most words on — are the
ones we didn't test. The "85% coverage / 100% agreement" is systematically biased toward the
easily-testable claims. The claims we skipped are the most interesting.

### C3. BLAST reference set was hand-curated → identity distribution biased upward
We stripped 20 esearch hits to 17; the paper's set of 26 likely includes broader IncX4
diversity. Our 99.70–99.95% identity is *expected* to be tighter than the paper's 93–98%
because our filter is stricter. Don't read our higher-identity number as "even stronger
evidence" — it's the same evidence on a narrower reference set. The rerun corroborates
the qualitative claim ("highly conserved backbone") but not more strongly than the paper.

### C4. 100 bp chromosome length discrepancy dismissed too fast
Paper says chromosome is 4,966,963 bp; NCBI record is 4,967,063 bp. We wrote this off as
"likely paper typo" without checking:
- the paper's supplementary materials (Table S2 may enumerate)
- the NCBI record version history (record could have been re-polished after submission)
- the actual assembly version tag vs the paper's Materials & Methods statement of assembly version
"Typo" is a plausible guess, not a verified conclusion.

### C5. No MD5-parity check with any secondary source
We did not check the deposited FASTA MD5 sums against any secondary NCBI mirror or the paper's
supplementary FASTA. NCBI Nuccore records can be silently updated post-publication for polished
Nanopore assemblies; our "exact size match" on 5 of 6 replicons could be a match to a *revised*
record, not the record as it stood when the paper was written.

### C6. No wet-lab or expression evidence
Every claim we tested is sequence-based. The paper's most clinically loaded claims — colistin
MIC 8 µg/mL (Q4), non-transferability under conjugation (Q1) — cannot be touched by this pipeline.
The REPLICATED verdict does not extend to these claims; they remain untested.

### C7. Duplicated blaTEM-135-sul2-tet cassette not analyzed for mechanism
Both the paper and our rerun report the duplication as bare fact. Neither extracted the flanking
IS/Tn architecture to distinguish recent duplication (within-strain event) from independent
acquisition (two separate horizontal transfers into the same cell). This is Q3.

## D. What is needed to close the residual gaps

| Gap | Closure work |
|---|---|
| C10 cgMLST tree | Reharvest 504 BV-BRC strains → chewBBACA + Enterobase cgMLST → GrapeTree + bootstrap. ~1 day uicgpu compute. |
| C11 non-transferability | Wet-lab conjugation + oriT localization + plasmid curing + transformation. Weeks of wet lab. |
| Ab initio reassembly | Pull SRA → Unicycler 0.5.0 + Nanopolish 0.14.0 on uicgpu → hash-compare. ~2 days including reads download. |
| Full ORF annotation of "AMR-free" plasmids | Prokka + Bakta on CP134086, CP134090; screen for colicins + mobilization. ~1 hour uicgpu. |
| Chromosomal colistin-mutation panel | Extract mgrB/phoP/pmrAB, align to CLSI/EUCAST panel. ~1 hour. |
| MDPI supplementary Tables S1/S2 | Headless browser fetch of MDPI supplementary ZIP. ~30 min. |
| Marker + Nougat central corpus resolution | sha256(paper.pdf) → Eagle manifest lookup → rsync. Blocked on Polaris auth + queue. |

## E. What was NOT actually a failure but is worth logging

- The 100 bp chromosome discrepancy is *known* and dismissed as "likely typo". This is honest
  labelling; the residual gap is that we did not verify.
- The paper's "hlyE"/"fyuA" not showing in AMRFinderPlus VF panel is a *tool-panel gap*, not
  a real disagreement — the yersiniabactin operon subunits `ybtP`+`ybtQ` we did detect are on
  the same pathway as `fyuA`.
- The paper's "IncH" vs our "IncHI1A + IncHI1B(R27) + IncFIA(HI1)" for the 254 kb plasmid is
  a *refinement* not a disagreement — modern PlasmidFinder subtypes IncH into IncHI1A/B, the
  paper used the parent group.

## Bottom line

The REPLICATED verdict is defensible for the sequence-based claims we tested (C1–C9). But the
report should be honest that (a) we tested against curated tool panels not against biology,
(b) the two most epidemiologically-loaded claims (C10, C11) were not touched, and (c) we
validated the deposited assembly not the paper's assembly workflow. The "85% coverage / 100%
agreement" LLM-judge number is arithmetic; the epistemic coverage is meaningfully lower once
you weight claims by their importance to the paper's conclusions.
