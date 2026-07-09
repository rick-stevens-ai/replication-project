# brief

Independent replication of J. A. Sethian (1996) "A fast marching level set
method for monotonically advancing fronts", *PNAS* 93(4):1591–1595. We
implement the Fast Marching Method (FMM) for the Eikonal equation
|∇T| F = 1 from scratch in Python/NumPy using the paper's upwind Godunov
scheme (Eqn. 8/9) and a heap-based narrow band (Sec. 4.1), then test
Sethian's three core claims on a local CPU: (C1) O(N log N) runtime scaling,
(C2) convergence of computed arrival times to the analytic point-source
distance function, and (C3) monotone front propagation with variable
speed F. All three are reproduced with real numerical measurements.
