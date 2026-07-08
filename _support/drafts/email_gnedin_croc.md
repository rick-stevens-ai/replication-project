# Draft email to Nick Gnedin re CROC source — for Rick's review

**To:** Nick Gnedin <gnedin@fnal.gov> (or <ngnedin@anl.gov>)
**Cc:** stevens@anl.gov
**Subject:** CROC code access for AI-replication study (OSTI 1275503)

---

Hi Nick,

I'm running an experiment on AI-assisted scientific replication — having an AI agent (with my close oversight) systematically reproduce ANL-authored OSTI papers end-to-end and score how faithfully it can reconstruct the methodology, data flow, and results. We're up to 35 papers across materials, nuclear, astro, ML, combustion, and bioinformatics.

One paper in our queue is OSTI 1275503 — "Cosmic Reionization on Computers: Properties of the Post-Reionization IGM" (Gnedin & Kaurov 2014/15ish, I think). The agent's first-pass replication scored 5/5 (out of 10) — capped not by the analysis methodology but by the lack of the actual CROC simulation source. We've been working with public hydro pieces (Healpix-3D RT, public ART pieces) but to do this paper proper justice we'd need access to the integrated CROC pipeline — the AMR + radiative-transfer + non-equilibrium chemistry stack you and the group have built up.

Would you be willing to share the source on a per-collaboration basis for this purpose? Specifically:

- The CROC executable / build scripts (the integrated AMR + RT + chemistry version)
- A small sample initial-conditions setup that matches one of the published runs (just enough to validate)
- Pointers to the analysis scripts you used for the paper's IGM property measurements

We'd run on Polaris (we already have time on `argonne_tpc` and `datascience` allocations), at a much smaller box size than your production runs (~25 Mpc/h, low resolution) — just enough to reproduce the paper's qualitative claims and one or two quantitative numbers. The agent has my supervision throughout, no autonomous publishing — anything we produce is internal benchmark data.

If sharing the full pipeline isn't feasible, even pointers to the right modules and a small working example would be a huge help. Happy to chat by phone or come by your office.

Thanks!
Rick

(P.S. The agent's name is Ollie. He's been running on a bunch of these replications overnight and it's been an interesting test of where AI helps and where it doesn't. Glad to share full results with you when this experiment wraps.)

---

## Notes for Rick

- I drafted this in your voice. Adjust as needed.
- If you'd rather write it yourself in 30 seconds, just hit reply with "I'd like to use CROC for an internal benchmark — can you share?" and Nick will probably just say yes.
- Either way: I'd rather have his blessing than try to reverse-engineer it.
- If he declines or wants formal MOU, we can mark 1275503 officially blocked and skip.
