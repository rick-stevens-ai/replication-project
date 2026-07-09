# Brief — OSTI 3012815 (MOOSE ProbML, Dhulipala et al. 2025)

The paper documents the design and demonstration of massively parallel
probabilistic ML / uncertainty-quantification capabilities inside the MOOSE
finite-element / finite-volume framework (INL), and applies them to five
computational-energy problems (TRISO fission-product release, HP microreactor
rare-events analysis, additive-manufacturing MOGP + PCA, lid-driven cavity
DGP, TMAP8 tritium batch-BO). Because MOOSE + BISON + TMAP8 is a
multi-hour multi-repo C++ build and the paper's specific application decks
were not attached to the OSTI PDF, we performed an *independent
implementation* of the paper's central quantitative claim (active-learning
subset-simulation dramatically reduces expensive-model evaluations vs.
crude MC for rare-event failure probabilities) in Python on a standard
2D four-branch series-system benchmark, and additionally verified that
every algorithm class the paper claims (`ParallelSubsetSimulation`,
`ActiveLearningGaussianProcess`, `BayesianActiveLearner`, `LMC` for
multi-output GP, `AffineInvariantStretch`, `PMCMCDecision`, etc.) is
actually present in the released MOOSE `stochastic_tools` module.
