# Brief

**What:** Independent replication of the analytic spoke-rotation-frequency prediction in the community E×B Penning-discharge benchmark (OSTI 3020556, Powis et al 2026, *Plasma Sources Sci. Technol.* **35** 025002).

**Why:** The paper reports a full 2D PIC benchmark whose central quantitative result is a spoke rotation frequency of **43.2 kHz** (mean period 23.1 µs), and states that collisionless-Simon-Hoh-instability (CSHI) theory — Eq. 4 of Ref [93] (Powis et al 2018, arXiv:1805.04438) — predicts **~53 kHz** from the discharge parameters. Rather than rerun the (expensive, multi-code) PIC simulation, we independently reimplemented the analytic CSHI formula from first principles, reproduced the 53 kHz scalar, verified the reported He-4 ion mass, confirmed the 1/√mᵢ mass-scaling law, and cross-checked the E×B drift kinematics against the measured 43.2 kHz. Reproduced 53.0 kHz to <1%; LLM judge (Argo gpt-5.2) scored **REPLICATED, 95%**.
