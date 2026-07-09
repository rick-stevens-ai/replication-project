# Brief

Wu et al. 2025 (OSTI 3000582, *Nuclear Science and Engineering*, DOI
10.1080/00295639.2025.2552500) is a **perspective/survey paper on uncertainty
quantification (UQ) of ML for nuclear engineering** that also presents a
concrete **Section IV.A "Analytical GP" demonstration** comparing MC Dropout,
Deep Ensemble, Bayesian NN, Gaussian Process, Split Conformal Prediction, and
Studentized-Residual CP on a heteroscedastic 1-D benchmark plus a SAFARI-1
research-reactor axial-flux case study (Section IV.B). We reproduced the fully
specified Section IV.A benchmark end-to-end on a fresh 8×A100 (uicgpu, PyTorch
2.12, Pyro 1.9, XGBoost 3.2, scikit-learn 1.9) using the paper's exact
data-generating process (μ(x)=x+0.02x²+5sinx, Matérn 5/2 ℓ=0.2, tent σ(x)
0.1→1.0→0.1, 1000 points from 10 GP realizations) and paper-specified
architectures. All six methods hit approximately-95% empirical coverage
(0.92–0.99), and the paper's qualitative ordering was recovered: SRCP-XGBoost
shows by far the strongest local adaptivity (Pearson r=+0.85 between predicted
band width and true σ(x)), Split-CP-DNN / GP-wrong-kernel produce
essentially-flat bands (width-range-ratio ≈ 1.0), MCD is near-flat (2.2×),
Deep Ensemble is adaptive (3.1×) but weaker than the paper claims, and BNN
produces the widest CIs with only weak adaptivity. The SAFARI-1 case study
was not reproduced (data not public). **LLM-judge verdict: PARTIAL** —
6/6 methods successfully run, 4/6 qualitative claims cleanly reproduced, 2/6
partially reproduced, and the Section IV.B real-reactor case out of reach.
