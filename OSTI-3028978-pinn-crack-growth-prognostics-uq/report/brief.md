# Brief — Independent replication of X-TFC for wind-turbine gearbox bearing crack prognostics

**Paper:** De Florio, Appleby, Keller, Eftekhari Milani, Zappalá, Sheng (2026),
_"Gearbox bearing crack growth prognostics and uncertainty quantification with
physics-informed machine learning"_, Wind Energy Science 11, 737–752
(doi:10.5194/wes-11-737-2026; OSTI id 3028978).

**What.** The paper introduces X-TFC (Extreme Theory of Functional Connections) —
a physics-informed random-projection single-layer neural network trained by
linear least-squares — to predict Remaining Useful Life (RUL) of high-speed
gearbox bearings from a noisy vibration-based Health Indicator (HI) stream. The
physics is Head's theory of fatigue crack growth (a Paris-law variant with
effective exponent m=6, giving ODE dN/da = N/(a·K1) with
K1 = 2·a_f − 2·√(a_0/a_f) ≈ 1.55 for their (a_0, a_f) = (0.05, 1.0)).
Epistemic UQ is done by Monte-Carlo ensembling ("MC X-TFC") over
independently-initialized networks trained on noise-perturbed data.

**Why replicate.** The raw HI dataset (Bechhoefer & Dubé 2020) is proprietary
and the paper's code is "available upon request". So we (a) re-implement X-TFC
from the paper's equations in pure Python/NumPy, (b) synthesize a
physics-consistent HI trajectory that satisfies Head's ODE with heteroscedastic
noise matching the paper's Fig. 2a description, and (c) reproduce Tables 1
(RUL error vs data availability × physics weight) and 2 (ensemble MC UQ:
ME, SDE, and 68/95/99.7% signed-error CIs).

**Verdict.** PARTIAL. Independent implementation reproduces the key qualitative
claims of the paper — monotonic error growth as physics weight decreases,
monotonic error growth as data availability decreases, calibrated CIs that
widen with less data, and millisecond-per-fit run time — but the exact
numerical magnitudes deviate because the underlying proprietary HI stream is
not available.
