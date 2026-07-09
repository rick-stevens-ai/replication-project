# Brief

Independent replication of Gottlieb & Shu (1998), *"Total variation
diminishing Runge-Kutta schemes"* (Math. Comp. 67(221), 73–85), the canonical
paper introducing the optimal 2nd- and 3rd-order Strong-Stability-Preserving
(SSP, then called TVD) explicit Runge–Kutta schemes. We implement SSP-RK2 (eq.
4.1) and SSP-RK3 (eq. 4.2) from scratch in NumPy and verify their three core
claims — formal order, TVD/SSP property under the paper's CFL bound, and the
optimal SSP coefficient c* = 1 — on the standard scalar test problems used in
the paper. All three claims reproduce cleanly on real numerical experiments;
independent LLM-judge scoring (Argo `argo:gpt-4o`, FREE endpoint) returns
verdict **REPLICATED**.
