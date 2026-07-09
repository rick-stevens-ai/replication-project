# Brief

Independent replication of Wang, Zong, McCreight, Hughes, Fienen & Tartakovsky
(2025), "Karhunen–Loève deep learning method for surrogate modeling and
approximate Bayesian parameter estimation," *Advances in Water Resources* 203:
105024 (OSTI 2570716). We reimplemented the KL-DNN forward-surrogate pipeline
end-to-end (Gaussian random log-K field with exponential covariance,
finite-volume elliptic PDE reference, empirical KL expansion, and a
2×3000-neuron SiLU DNN trained in the reduced KL latent space) on a synthetic
5 km × 10 km, 20×40-cell Freyberg-analog aquifer and swept the paper's Case 1/2/3
training-set sizes (168, 472, 2000). The method reproduces qualitatively:
KL truncation ranks match within ~30 %, head-covariance eigenvalues decay much
faster than log-K eigenvalues, and surrogate error decreases monotonically with
Ntrain. Absolute rel-L2 (3.8×10⁻³ at Ntrain=2000) is ~10× larger than the
paper's 3.5×10⁻⁴, attributable to substituting a linear elliptic PDE for
MODFLOW-6's nonlinear unconfined-aquifer solver and skipping the paper's
hyperparameter search. LLM-judge verdict: **PARTIAL**.
