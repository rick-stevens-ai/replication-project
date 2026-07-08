# DRAFT — data request to Orly Alter (for Rick's approval, NOT yet sent)

**To:** Orly Alter <orly@sci.utah.edu>
**Cc:** Rick Stevens <stevens@anl.gov>, <rick.stevens@mac.com>
**From:** (decision needed — see options below)
**Subject:** Request: Datasets 1–3 + Mathematica Notebook 1 for reproducing your APL Quantum multitensor GSVD paper

---

Dear Orly,

Congratulations on the APL Quantum paper — "Quantum mechanics-based multitensor AI/ML uniquely able to discover, validate, and interpret predictors from small-cohort noisy high-dimensional multiomic data." It's a beautiful unification of the GSVD / HO-GSVD / tensor-GSVD framework, and the neuroblastoma result (the combined tumor-DNA predictors outperforming MYCN and the standard-of-care indicators, log-rank P = 2.3×10⁻⁵, HR = 4.0, concordance 0.80) is striking.

We'd like to reproduce the analysis end to end as part of a replication effort. Per your Data Availability statement, the following are available on request, and we'd be grateful to receive them:

- **Dataset 1** — discovery set (X = 101 NBL): clinical/sample/profile labels, the tumor and blood DNA profiles (log2 CG read counts, Z1 = 2,831,960 / Z2 = 2,831,959 1-kb hg19 bins, autosomal-median-centered), and the 71-patient tumor RNA profiles (Z3 = 15,393 transcripts).
- **Dataset 2** — validation set (Y = 419 NBL): labels + tumor/blood DNA profiles in the Z1 = 10,354 / Z2 = 10,475 shared bins.
- **Dataset 3** — genomic/segmentation/CNA labels of the CBS segments in the GSVD tumor-DNA-specific patterns u1,k (k = 1, 100, 101).
- **Mathematica Notebook 1** (PDF) — to follow your exact algorithm steps.

Our goal is a faithful, independent reproduction: rebuilding the GSVD / HO-GSVD decompositions, the u1,1 / u1,101 predictors, and Table I's survival statistics, then reporting coverage and agreement against your published numbers. Happy to share back our reproduction notebook/results and to credit the datasets exactly as you prefer.

Thank you again — and thanks for thinking of us.

Best,
[Rick / Ollie]

---

## SENDER DECISION (Rick, pick one):
- **(A) Rick sends it himself** from stevens@anl.gov — most natural; she's your contact and thanked you in the paper. I provide the text; you send.
- **(B) Ollie sends from ollie@kd9nwa.org**, cc you on both aliases, signed "Ollie (for Rick Stevens)" — keeps it in the agent-mail ledger, but introduces a new sender she doesn't know.
- I recommend **(A)** for a personal-contact data request; (B) is better for routine/agent-to-agent outreach.
