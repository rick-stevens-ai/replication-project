# Brief

Independent from-scratch replication of **Shen & Zhang, "Discrete Maximum principle of a
high order finite difference scheme for a generalized Allen-Cahn equation"** (arXiv:2104.11813,
Comm. Math. Sci. 20(5), 2022). The paper proposes a fourth-order finite-difference scheme —
derived from the Q2 spectral-element method with 3-point Gauss-Lobatto quadrature — for a
generalized Allen-Cahn equation with passive incompressible convection, and proves it satisfies
a **discrete maximum principle** (operator inverse-positivity) under mesh/time-step constraints,
notably a *lower* bound on the time step that 2nd-order schemes do not require. We reimplemented
the D1/D2 stencils and 2D operator from the equations (no paper code), validated on an analytic
steady problem (recovering 4th-order superconvergence), then reproduced accuracy Tables 6.1
(Allen-Cahn, manufactured exact solution) and 6.2 (stream-vorticity, periodic BC) to <6% on
every entry with matching convergence orders, and directly verified Theorem 3.9 by showing the
backward-Euler operator's inverse is entrywise non-negative exactly when the constraints hold and
loses positivity when the novel lower time-step bound is violated. Three independent free-endpoint
LLM judges (Argo gpt-5.2, gemini-2.5-pro, gpt-4.1) unanimously scored the result REPLICATED.
