# Brief

Independent minimal replication of Lagaris, Likas, Fotiadis (1998) *"Artificial
Neural Networks for Solving Ordinary and Partial Differential Equations"*
(IEEE TNN 9(5):987-1000, preprint physics/9705023). We reimplemented the
trial-solution ANN method — Ψ_t = A(x) + F(x)·N(x,p) with A satisfying the BCs
and F vanishing on them — in PyTorch (double precision, CPU, L-BFGS), and
reproduced three of the paper's five worked examples: Problem 1 (1st-order ODE),
Problem 3 in its BVP form (2nd-order ODE, two Dirichlet BCs), and Problem 5 (2D
Poisson on [0,1]², Dirichlet). Max errors match the paper's reported accuracy
band to within a factor of ~2 in every case (2.7×10⁻⁵ vs paper ~1e-5 for P1;
3.5×10⁻⁶ vs paper ~1e-6 to 1e-5 for P3; 9.6×10⁻⁷ vs paper 5×10⁻⁷ for P5). The
paper's interpolation-superiority claim is confirmed on Problem 1: on a dense
200-point grid the ANN is 68.6× more accurate than a trapezoid-FD + cubic-spline
comparator solved on the same 10 training nodes. LLM judge (Argo `gpt-5`, no
regex): **REPLICATED**, coverage 10/10, agreement 9/10.
