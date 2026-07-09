# Brief — OSTI 3007459 (Kolmogorov-Arnold Wavefunctions)

Independent reimplementation of a variational Monte Carlo (VMC) study that uses
**Kolmogorov-Arnold Network (KAN)** wavefunction ansätze for 1D many-boson quantum
systems and compares them to feed-forward MLP ansätze. We rebuilt the bosonic KAN
(spline/RBF line-functions, Eq. 2/5/9–11), a bosonic MLP baseline, a Metropolis-VMC
engine, and validated against two references: the paper's **solvable model** (exact
E₀, Eq. 7) and the **delta+harmonic model** (Busch analytic N=2 + Tonks-Girardeau
limits). The method's rigorous cores reproduce to machine precision (exact-wavefunction
zero-variance local energy; non-interacting E = N/2 for N = 2,3,4), and the KAN's
parameter-frugality is confirmed (≈2.9× fewer params than MLP). However, our
interacting-case KAN VMC did not converge robustly across seeds/regularization, and we
could not confirm the paper's headline ~10× walltime efficiency (our KAN was slower and
less accurate than our MLP on the interacting problem). Verdict: **PARTIAL**.
