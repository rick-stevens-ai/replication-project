# Artifact Harvest

| Artifact | Source URL | Type | Size | Notes |
|---|---|---|---|---|
| Primary paper PDF | https://arxiv.org/pdf/1902.00374v1 | PDF (OA preprint of PNAS 2019) | 322 KB, 7 pp | Gopal & Trefethen, "New Laplace and Helmholtz solvers". `work/paper_gopal_trefethen_1902.00374.pdf` |
| Paper text extract | (pdftotext -layout of above) | txt | 25 KB | `work/paper_text.txt` |
| Companion paper | https://arxiv.org/pdf/1905.02960v2 | PDF (OA) | 676 KB, 21 pp | Gopal & Trefethen, "Solving Laplace problems with corner singularities via rational functions", SINUM 57(5):2074–2094 (2019). Used for algorithmic detail (pole clustering, Arnoldi). |

## Access notes
- AMS Math. Comp. and Taylor & Francis / PNAS publisher PDFs returned HTTP 403 / Cloudflare to curl and headless browser. The **arXiv OA preprints** of both the primary and companion papers downloaded cleanly and contain the full method and the challenge specification, so no paywalled source was needed.
- No external datasets required — this is a self-contained analytic-PDE replication (canonical L-shape geometry + closed-form boundary data + known reference value).

## Key extracted specification (from primary paper, Section 1)
- **PDE:** Laplace `Δu = 0` in Ω, Dirichlet `u=h` on polygon boundary P.
- **Representation:** `u(z)=Re r(z)`, `r(z)=Σ_{j=1}^{N1} a_j/(z−z_j) + Σ_{k=0}^{N2} b_k z^k`, poles `z_j` fixed outside Ω, clustered exponentially near each corner.
- **Solve:** poles fixed ⇒ linear; least-squares fit `Re r(z)=h(z)` on ~3N boundary points; increase N until tolerance met; max-principle accuracy guarantee.
- **Challenge (C1):** L-shape, `h(z)=(Re z)²=x²`, exact `u(0.99,0.99)=1.02679192610…`.
- **Convergence (C2):** root-exponential `‖error‖ = O(exp(−C√N))`; N≈1000 DOF ⇒ ~10 digits.
