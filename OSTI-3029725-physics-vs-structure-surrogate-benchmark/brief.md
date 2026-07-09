# Brief: OSTI 3029725 — Physics vs Structure: Systematic Benchmark of Learned Building-Thermal Surrogates

## Paper
- **Title**: Physics vs structure: systematic benchmark of learned building-thermal surrogates
- **OSTI ID**: 3029725
- **Domain**: Building energy modelling / data-driven surrogates for zone-temperature dynamics
- **File**: `work/paper.pdf`

## Central question
When we build a learned surrogate for a multi-zone building's thermal dynamics, what matters more — (a) the *physics prior* embedded in the model class (linear state-space, MLP, neural ODE, physics-informed PCNN, ...) or (b) the *structural inductive bias* about which zones are connected (a monolithic "whole-building model", **WBM**, vs an "interconnected-zone model", **IZM**, that only permits inter-zone couplings that physically exist)?

## Model zoo (paper)
- **LSSM** — linear state-space model
- **MLP** — one-step-ahead multilayer perceptron
- **NSSM** — nonlinear state-space model (MLP transition on latent state)
- **NODE** — neural ODE integrator
- **PCNN** — physics-consistent NN (energy-balance layer + learned residual)
- **LSSM-EncDec** — LSSM with encoder/decoder for hidden-state lifting

Each is trained in two variants:
- **-WBM**: one dense operator over the joint state (no structure prior)
- **-IZM**: sparsity mask enforcing only physically-adjacent zone couplings

## Key claims to check
1. Under WBM, LSSM ≥ MLP (linear structure prior beats overparameterised feedforward when structure is absent).
2. Adding IZM sparsity **helps** for every model class — dominant effect vs choice of model class.
3. LSSM-IZM is close to the overall best surrogate despite being the simplest (paper reports ~0.32 °C shoulder-MAE vs ~0.67 °C for LSSM-WBM).
4. PCNN's physics prior is not a free lunch: accuracy trade-off vs MLP-WBM.
5. LSSM-EncDec's hidden-state lifting improves over plain LSSM in the WBM regime.

## Approach (replication)
We use a small **2R2C-per-zone** RC-building proxy simulator (5 zones, 15-min timestep) as a stand-in for the paper's EnergyPlus co-simulation (we do not have the paper's dataset). We generate matched shoulder-season and cooling-season episodes, train each of the 11 (model × structure) combinations for 100 epochs (seed=0), and compare 6h/48h-horizon MAE. This tests **directional** claims, not absolute magnitudes.

Compute: single A100 on `uicgpu`. Framework: PyTorch. All endpoints used are FREE (Argo :44497 for LLM judge, no cloud training).
