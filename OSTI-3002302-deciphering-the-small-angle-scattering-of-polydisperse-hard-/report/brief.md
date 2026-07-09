# Brief

Ding & Do (ORNL, APL Machine Learning 3, 036112, 2025; DOI 10.1063/5.0290589)
introduce a VAE-based deep-learning framework that (i) generates the small-angle
scattering function I(Q) from system parameters (volume fraction η,
polydispersity σ) and (ii) inversely infers those parameters from a measured
I(Q), for a polydisperse hard-sphere fluid. Ground truth comes from LAMMPS MD
of 23,328 truncated-shifted-LJ particles for three size distributions (uniform,
normal, log-normal). Traditional Percus-Yevick + β-correction is the baseline.
We independently replicated the paper's two headline claims by loading the
authors' released MD test set (1,000 points per distribution) and released
trained weights, and evaluated both the neural-network inferrer/generator and a
freshly implemented Wertheim-PY + β-correction baseline. We also re-trained
the model from scratch on the released training data (pdType=1) to verify the
recipe is reproducible.
