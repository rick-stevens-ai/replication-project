# LLM judge output

**Model**: argo:gpt-5.2

---

{
  "coverage": 0.62,
  "agreement": 0.78,
  "verdict": "PARTIAL",
  "confidence": 0.63,
  "one_line": "Numerical pseudospectral runs for Burgers–Hilbert, fKdV (α=-0.6), and Whitham show bounded u with rapid negative-slope growth and T* roughly ∝1/A, consistent with Saut–Wang wave-breaking predictions, but only a narrow slice of parameter/initial-data conditions and no quantitative check of theorem constants were exercised.",
  "reasoning": "What was testable here are qualitative PDE consequences of the analytical theorems: (i) finite-time wave breaking in the sense of bounded u but unbounded u_x, and (ii) scaling of breaking time with initial negative slope/amplitude (and, more broadly, dependence on dispersion family/α). The replication exercised three equation families (Burgers–Hilbert, one fractional exponent α=-0.6 within the stated range, and classical Whitham) plus Burgers as a control, using smooth mean-zero sinusoidal data and an amplitude sweep.\n\nAgreement: For A≥1, all three dispersive families show the expected wave-breaking signature: max|u| stays O(A) while min u_x becomes very negative (thresholded at -500), with breaking times around 0.5–1.2. The observed monotone decrease of T* with A and near-constancy of A·T* (~1.05–1.18) is consistent with the paper’s O(1/(-inf φ′)) scaling discussion. The one non-breaking run (Burgers–Hilbert A=0.5 up to t=5) is not a contradiction because the theorems require sufficiently steep negative slope; however, the replication did not explicitly verify the theorem’s sufficient-condition inequalities for the chosen φ.\n\nLimitations lowering coverage/agreement: (1) Only one initial-data shape (A sin x) was used; the theorems’ hypotheses involve more detailed pointwise/Sobolev constraints, not just amplitude. (2) Fractional KdV was tested at a single α value; no sweep across α∈(-1,-2/5) or near-endpoint behavior. (3) “Breaking time” is defined by an arbitrary diagnostic threshold (min u_x<-500) with coarse sampling, so quantitative comparison of constants (or Theorem 2.7’s explicit bound) is not really tested. (4) No ε-rescaled Whitham experiments were run to directly probe the Section 7 long-time scaling regime.\n\nOverall, the numerics provide a plausible and consistent spot verification of the main qualitative wave-breaking scenario across the three model classes, but they do not comprehensively test the parameter ranges or the theorem-level quantitative bounds/conditions."
}
