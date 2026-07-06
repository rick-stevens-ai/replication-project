# Failure Analysis — Sivakumar et al. 2023 Replication

Rick's brief: honest failure analysis, evidence-strength critique, no
rubber-stamping. Even for a REPLICATED verdict, document friction, partial
mismatches, and assumptions.

## Executive summary

The replication reproduced every **genome-count**, **MLST/CC**, and
**presence/absence gene count** claim in the paper, at 41/41 strain scope, and
did not contradict any claim. But five substantive things went wrong or were
skipped, and the ``REPLICATED'' verdict deserves a discount. Each failure
below is paired with (a) root cause, (b) workaround used, (c) residual gap,
(d) what would close it.

---

## Failure 1 — We never re-ran the paper's pipeline

**What failed:** Instead of re-executing SPAdes v3.11.1 + RAST + Prokka +
Roary + CSI Phylogeny + CARD-RGI + VFanalyzer against the raw Illumina reads,
we compared the paper's numbers to BV-BRC's *pre-computed annotations for the
same 41 accessions*.

**Root cause:** Raw Illumina reads for these 41 accessions were not fetched.
The paper's pipeline includes tool versions from 2017 (SPAdes 3.11.1) that
would take substantial re-plumbing effort. The replication was designed as a
cross-source consistency check, not a raw-reads-up re-run.

**Workaround:** Rely on BV-BRC's independent annotation of the same accessions
as an *independent-enough* source. This is defensible for high-level claims
(strain count, ST composition, MSSA status, gene presence) but is not
end-to-end pipeline replication.

**Residual gap:** We cannot distinguish "paper is right and BV-BRC agrees"
from "paper and BV-BRC share upstream assembly errors that cancel." This is
the largest single caveat on the REPLICATED verdict.

**To close:** Pull raw reads from SRA (all 41 accessions have paired SRA
runs), run SPAdes → Prokka → Roary → CARD RGI → VFanalyzer at the paper's
versions, and compare. Estimated effort: ~ 24 CPU-hours + storage for ~ 100
GB reads. Trivial on Polaris/UICGPU; not attempted here.

---

## Failure 2 — Phylogeny is a topology proxy, not a replication

**What failed:** The paper's tree is an SNP-based ML tree (CSI Phylogeny v1.4,
2,293,099 SNPs, K5 reference). Our tree is a gene-content Jaccard UPGMA on
PLFam presence vectors. These are fundamentally different methods.

**Root cause:** SNP-based ML requires reads mapped to a reference; we did not
run BWA/SAMtools/FastTree.

**Workaround:** Report that we observe "6 major clusters" in the UPGMA tree,
matching the paper's clade count. Note that this is topology-count agreement
only, not membership-level verification.

**Residual gap:** We did **not** verify sub-clade assignments — Clade II =
ST580+ST243, Clade III = ST5, Clade IV = ST6+ST672, VIA = ST4968, VIB =
CC97 — at the strain level. Getting 6 clusters is far weaker than getting
6 clusters *with the right strains in each*.

**To close:** (a) Cluster-membership audit: for each of our UPGMA-derived
clusters, list the strains in it, compare to Fig. 2 of the paper. Report
membership Rand index. (b) Actually re-run CSI Phylogeny with the paper's
parameters (min depth 10×, SNP quality 30, map Q 25) against K5 and rebuild
the ML tree with FastTree 2.

---

## Failure 3 — Tooling deltas were shrugged off, not decomposed

**What failed:** Three claims marked "PARTIAL" have quantitative deltas
we handwaved:
- Pan-genome 4360 → 3412 ("PLFam clusters more aggressively than Roary")
- AMR 17 → 37 raw ("BV-BRC includes intrinsic genes")
- VF 108 → 131 ("VFDB version drift")

**Root cause:** We produced no *audit set* backing up any of these
explanations. We did not, for example, run Roary locally to demonstrate that
Roary's clustering *does* produce 4360 families on these assemblies.

**Workaround:** Wrote directional explanations in REPORT.md/REPORT.tex.

**Residual gap:** The "PARTIAL" verdicts are soft. In particular:
- The claim "~17 comparable AMR genes" in the raw 37 is an assertion, not a
  demonstration. No intersection-set audit was performed against the paper's
  Fig. 5 gene list.
- The VF total delta could be entirely VFDB drift, entirely BV-BRC threshold
  differences, or some mix — we don't know.

**To close:** (a) AMR intersection audit: parse Fig. 5 gene list from the
paper's PDF, compute exact overlap with our 37-gene set, report the delta
per gene. (b) Pin VFDB to the ~ 2021 release and re-annotate; compare
per-gene deltas. (c) Actually run Roary v3.13.0 at the paper's parameters
and report the pan-genome numbers.

---

## Failure 4 — Two claims were skipped, not deferred

**What failed:**
- **Claim 31 — 16 spa types + 8 untypeable.** Not tested. BV-BRC does not
  provide spa typing.
- **Claim 33 — Pan-genome closure power-law fit b=0.0817389.** Not tested.
  Requires Roary's gene-family accumulation curve.

**Root cause:** For Claim 31, we assumed BV-BRC lack of spaTyper was
show-stopping; it isn't — we could have run spaTyper locally or via CGE
webserver on the 41 assemblies. For Claim 33, we didn't run Roary.

**Workaround:** None. Marked NT (not tested) in the claims table.

**Residual gap:** Two of the paper's more distinctive claims are un-audited.
The spa-typing claim is especially load-bearing for the paper's
epidemiological narrative (spa types t7286, t7867, t10760 dominant).

**To close:** (a) Fetch the 41 assemblies from BV-BRC (`.fna`), push through
`spaTyper` (Bitbucket) or the CGE webserver, tabulate. (b) Same 41
assemblies through Roary v3.13.0, extract the accumulation curve, refit the
power law.

---

## Failure 5 — cgMLST 198-genome analysis was not touched

**What failed:** The paper's cgMLST minimum-spanning tree of 198 Indian
*S. aureus* (Fig. 3–4), which produces two of its most novel epidemiological
claims — (i) MUF256 (a diabetic-foot-ulcer strain) is the common ancestor of
all Indian *S. aureus*, and (ii) CC97 is exclusively bovine among Indian
sequenced *S. aureus* — was not touched by this replication at all.

**Root cause:** cgMLST was run in Bionumerics v8.0 (proprietary) and requires
building the 198-genome comparison set. Non-trivial and out of scope for the
BV-BRC-only replication design.

**Workaround:** None.

**Residual gap:** Two of the paper's most cited claims are entirely
unaudited by this replication.

**To close:** Pull all Indian *S. aureus* WGS from NCBI/BV-BRC (should now
be > 250 as of 2026), run cgMLST via a free tool (chewBBACA, PHYLOViZ, or
BV-BRC's cgMLST if enabled for *S. aureus*), rebuild the MST, and test both
the MUF256-root claim and the CC97-bovine-exclusivity claim.

---

## Failure 6 — Central Marker/Nougat corpus unreachable

**What failed:** Backfill step for `extraction/marker.md` and
`extraction/nougat.mmd` normally pulls from
`/eagle/projects/AuroraGPT/stevens/scout_corpus/` on Polaris via sha256
lookup. From this subagent context, Polaris SSH returned "Permission denied
(keyboard-interactive,hostbased)" — subagent lacks interactive Duo prompt.

**Root cause:** Polaris requires Duo 2FA; automated subagent SSH cannot
handle keyboard-interactive.

**Workaround:** Fell back to `pdftotext -layout` for marker.md; wrote a
pending stub for nougat.mmd with the PDF sha256 pinned so a later corpus
sweep can resolve it automatically.

**Residual gap:** `extraction/marker.md` is not a real Marker parse (no table
extraction, no equation preservation); `extraction/nougat.mmd` is a stub.

**To close:** From a Polaris-interactive session (or a Kukla-side automated
job), sha256-lookup this paper (e8ff50da7e228d69c2f1fab9b277fbddeae939ebd5580108d8ed94bfdf40dde9)
against scout_corpus/{md,mmd} and copy resolved files into place.

---

## Paper-internal inconsistencies we noticed but did not flag as errata

1. **blaZ count:** Abstract-region says 14; Fig. 5 narrative says 15. BV-BRC
   gives 14. Almost certainly a paper typo.
2. **ST467 vs ST4967:** The paper's narrative reports ST467 (n=2) at one
   point but describes ST4967 in CC97 elsewhere. BV-BRC gives ST4967 (n=2).
   Almost certainly a paper typo (also missing digit in a subclade
   description that says "ST4967 2459" without a comma).
3. **CC1 members:** Text says CC1 = ST5360 + ST5098, but the STs table
   suggests only ST5360 was represented — Sivakumar's ST5098 attribution
   would need cross-check.

None of these were formally raised; the replication's job is not to author
errata, but they should be noted for downstream users of the paper.

---

## Evidence-strength critique (summary)

| Category | Evidence strength |
|---|---|
| Strain-count, ST/CC composition | **Strong** — direct BV-BRC MLST agreement, no ambiguity |
| MSSA status | **Strong** — 41/41 confirmed at the AMR-gene absence level |
| Per-gene presence counts (blaZ, sak, tet(K), PVL, ica operon, hemolysins) | **Strong** — exact matches on well-conserved genes |
| Pan-genome counts | **Moderate** — direction agrees, magnitude untested at Roary parameters |
| Phylogeny (6 clades) | **Weak-to-moderate** — cluster count matches, membership unverified |
| AMR gene *set* | **Moderate** — count differs, per-gene intersection with Fig. 5 not audited |
| VF count | **Moderate** — VFDB version delta not controlled |
| Spa typing | **None** — not tested |
| cgMLST-198 / MUF256-ancestor / CC97-bovine-exclusivity | **None** — not tested |
| Pan-genome power-law closure (b=0.0817) | **None** — not tested |

The REPLICATED verdict rests on the top four rows. The bottom five are
untested or weak. Any paper-critical downstream claim relying on rows 5–10
should not treat this replication as evidence for or against.
