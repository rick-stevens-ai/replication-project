# Brief — Osher & Sethian (1988) level-set method

Independent, from-scratch NumPy replication of the foundational level-set
method paper (Osher & Sethian, *J. Comput. Phys.* **79**, 12–49, 1988).
We implement the Hamilton–Jacobi level-set PDE φₜ + F|∇φ| = 0 with the
paper's Godunov upwind flux (their Eq. 3.11) and central-difference
curvature (their Eq. 3.14 recipe), and quantitatively verify three core
claims: (C1) constant-speed normal motion of a circle recovers the exact
linear-radius growth (0.36 % relative error at T=0.5); (C2) mean-curvature
flow F = −εK collapses a circle at the exact rate R(t) = √(R₀²−2εt) with
observed convergence order ≈ 1.6–1.9 in L∞ under grid refinement; (C2b)
the same flow smooths a non-convex 7-pointed star with strictly-decreasing
perimeter (0 % monotonicity violations); (C3) two disjoint disks under F=1
merge automatically at the analytically-predicted time 0.150 (numerical
0.1504, 0.27 % error). Verdict: **REPLICATED**.
