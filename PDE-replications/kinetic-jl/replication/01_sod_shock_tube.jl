#!/usr/bin/env julia
# =============================================================================
# Replication 1: Sod Shock Tube via Kinetic.jl (BGK kinetic solver)
# =============================================================================
# This is the flagship example from Kinetic.jl: solving the Sod shock tube
# problem using the BGK kinetic equation with KFVS flux splitting.
# We compare against the exact Riemann solution.
#
# Paper: Xiao 2021, "Kinetic.jl: A portable finite volume toolbox..."
# Reference: Sod (1978) shock tube problem
# =============================================================================

using KitBase, Plots
using Printf

println("="^70)
println("REPLICATION 1: Sod Shock Tube (1D BGK Kinetic → Euler)")
println("="^70)

# ---- Setup using Kinetic.jl API ----
# Equivalent to the sod.txt config in the examples
set = Setup(
    case = "sod",
    space = "1d2f1v",
    flux = "kfvs",
    collision = "bgk",
    nSpecies = 1,
    interpOrder = 1,
    limiter = "vanleer",
    boundary = "fix",
    cfl = 0.3,
    maxTime = 0.2,
)

ps = PSpace1D(0.0, 1.0, 200, 1)
vs = VSpace1D(-5.0, 5.0, 28)

gas = Gas(
    Kn = 0.0001,
    Ma = 0.0,
    Pr = 1.0,
    K = 2.0,
    γ = heat_capacity_ratio(2.0, 1),
    ω = 0.81,
    αᵣ = 1.0,
    ωᵣ = 0.5,
    μᵣ = ref_vhs_vis(0.0001, 1.0, 0.5),
)

# Initial conditions: Sod problem
# Left state: ρ=1, u=0, p=1 → T = p/ρ = 1
# Right state: ρ=0.125, u=0, p=0.1 → T = p/ρ = 0.8
γ = gas.γ
primL = [1.0, 0.0, 0.5]   # [ρ, u, λ=1/(2T)]  where T=p/ρ=1, λ=1/(2*1)=0.5
primR = [0.125, 0.0, 0.625]  # ρ=0.125, u=0, T=p/ρ=0.8, λ=1/(2*0.8)=0.625

wL = prim_conserve(primL, γ)
wR = prim_conserve(primR, γ)

hL = maxwellian(vs.u, primL)
hR = maxwellian(vs.u, primR)
bL = hL .* gas.K ./ (2.0 * primL[end])
bR = hR .* gas.K ./ (2.0 * primR[end])

p = (x0 = 0.0, x1 = 1.0, wL = wL, wR = wR, primL = primL, primR = primR,
     hL = hL, hR = hR, bL = bL, bR = bR)

fw = function(x, p)
    x <= (p.x0 + p.x1) / 2 ? p.wL : p.wR
end
ff = function(x, p)
    x <= (p.x0 + p.x1) / 2 ? (p.hL, p.bL) : (p.hR, p.bR)
end
bc = function(x, p)
    x <= (p.x0 + p.x1) / 2 ? p.primL : p.primR
end

ib = IB2F(fw, ff, bc, p)
ks = SolverSet(set, ps, vs, gas, ib)
ctr, face = init_fvm(ks)

println("Grid points: $(ks.ps.nx)")
println("Velocity points: $(ks.vs.nu)")
println("Knudsen number: $(ks.gas.Kn)")
println("CFL: $(ks.set.cfl)")
println("Max time: $(ks.set.maxTime)")

# ---- Solve ----
println("\nRunning BGK kinetic solver...")
t_start = time()
t = solve!(ks, ctr, face, 0.0)
t_elapsed = time() - t_start
@printf("Completed in %.2f seconds\n", t_elapsed)
@printf("Final simulation time: %.6f\n", t)

# ---- Extract solution ----
nx = ks.ps.nx
x = [ks.ps.x[i] for i in 1:nx]
ρ = [ctr[i].prim[1] for i in 1:nx]
u = [ctr[i].prim[2] for i in 1:nx]
T = [1.0 / (2.0 * ctr[i].prim[3]) for i in 1:nx]  # T = 1/(2λ)
p_val = [ctr[i].prim[1] / (2.0 * ctr[i].prim[3]) for i in 1:nx]  # p = ρT = ρ/(2λ)

# ---- Exact Riemann solution for Sod problem at t=0.2 ----
# Standard Sod: (ρL,uL,pL)=(1,0,1), (ρR,uR,pR)=(0.125,0,0.1), γ=5/3
# Exact solution regions at t=0.2:
# Region 1 (left): ρ=1, u=0, p=1
# Region 2 (rarefaction fan): x/t from head to tail
# Region 3 (contact left): ρ*, u*, p*
# Region 4 (contact right): ρ**, u*, p*
# Region 5 (right): ρ=0.125, u=0, p=0.1

function exact_sod(x, t; γ=5.0/3.0)
    # Left and right states
    ρ1, u1, p1 = 1.0, 0.0, 1.0
    ρ5, u5, p5 = 0.125, 0.0, 0.1

    # Sound speeds
    c1 = sqrt(γ * p1 / ρ1)
    c5 = sqrt(γ * p5 / ρ5)

    gm1 = γ - 1.0
    gp1 = γ + 1.0
    
    # Solve for p* via Newton iteration
    p_star = 0.3
    for _ in 1:200
        # Left rarefaction function
        fL = (2*c1/gm1) * ((p_star/p1)^(gm1/(2γ)) - 1.0)
        dfL = (1.0/(ρ1*c1)) * (p_star/p1)^(-(gp1)/(2γ))
        
        # Right shock function
        A5 = 2.0 / (gp1 * ρ5)
        B5 = gm1/gp1 * p5
        fR = (p_star - p5) * sqrt(A5 / (p_star + B5))
        dfR = sqrt(A5 / (p_star + B5)) * (1.0 - (p_star - p5) / (2.0 * (p_star + B5)))
        
        f_val = fL + fR + u5 - u1
        df_val = dfL + dfR
        dp = -f_val/df_val
        p_star += dp
        abs(dp/p_star) < 1e-14 && break
    end

    # Contact velocity
    fL_star = (2*c1/gm1) * ((p_star/p1)^(gm1/(2γ)) - 1.0)
    u_star = 0.5 * (u1 + u5 + fL_star - (2*c1/gm1)*((p_star/p1)^(gm1/(2γ)) - 1.0))
    # Actually: u_star = u1 - fL_star (by definition)
    u_star = u1 - fL_star

    # Post-shock density (right side of contact)
    ρ4 = ρ5 * ((p_star/p5 + gm1/gp1) / (gm1/gp1 * p_star/p5 + 1.0))
    
    # Post-rarefaction density (left side of contact)
    ρ3 = ρ1 * (p_star/p1)^(1.0/γ)
    
    # Sound speed behind rarefaction
    c3 = c1 * (p_star/p1)^(gm1/(2γ))
    
    # Shock speed (Rankine-Hugoniot)
    S = u5 + c5 * sqrt((gp1/(2γ)) * (p_star/p5) + gm1/(2γ))
    
    # Wave positions
    x_head = 0.5 + (u1 - c1) * t    # rarefaction head (left-going)
    x_tail = 0.5 + (u_star - c3) * t # rarefaction tail
    x_contact = 0.5 + u_star * t     # contact discontinuity
    x_shock = 0.5 + S * t            # shock front

    @printf("  Exact Riemann: p*=%.6f, u*=%.6f\n", p_star, u_star)
    @printf("  ρ3=%.6f, ρ4=%.6f\n", ρ3, ρ4)
    @printf("  Waves: head=%.4f, tail=%.4f, contact=%.4f, shock=%.4f\n",
        x_head, x_tail, x_contact, x_shock)
    
    n = length(x)
    ρ_ex = zeros(n)
    u_ex = zeros(n)
    p_ex = zeros(n)
    
    for i in 1:n
        xi = x[i]
        if xi <= x_head
            ρ_ex[i] = ρ1; u_ex[i] = u1; p_ex[i] = p1
        elseif xi <= x_tail
            # Rarefaction fan (self-similar)
            c_fan = (2.0/gp1) * (c1 + gm1/2.0 * (xi - 0.5)/t)
            u_fan = (2.0/gp1) * (c1 + (xi - 0.5)/t)
            ρ_ex[i] = ρ1 * (c_fan/c1)^(2.0/gm1)
            u_ex[i] = u_fan
            p_ex[i] = p1 * (c_fan/c1)^(2γ/gm1)
        elseif xi <= x_contact
            ρ_ex[i] = ρ3; u_ex[i] = u_star; p_ex[i] = p_star
        elseif xi <= x_shock
            ρ_ex[i] = ρ4; u_ex[i] = u_star; p_ex[i] = p_star
        else
            ρ_ex[i] = ρ5; u_ex[i] = u5; p_ex[i] = p5
        end
    end
    
    T_ex = p_ex ./ ρ_ex
    return ρ_ex, u_ex, p_ex, T_ex
end

ρ_ex, u_ex, p_ex, T_ex = exact_sod(x, 0.2; γ=γ)

# ---- Compute errors ----
# Global errors (includes discontinuities — expected to be O(1) there)
L2_ρ = sqrt(sum((ρ .- ρ_ex).^2) / nx)
L2_u = sqrt(sum((u .- u_ex).^2) / nx)
L2_p = sqrt(sum((p_val .- p_ex).^2) / nx)
L2_T = sqrt(sum((T .- T_ex).^2) / nx)

# Smooth-region errors (away from discontinuities: left undisturbed + right undisturbed)
smooth_idx = vcat(1:40, 180:200)  # regions far from waves
L2_ρ_smooth = sqrt(sum((ρ[smooth_idx] .- ρ_ex[smooth_idx]).^2) / length(smooth_idx))
L2_u_smooth = sqrt(sum((u[smooth_idx] .- u_ex[smooth_idx]).^2) / length(smooth_idx))
L2_p_smooth = sqrt(sum((p_val[smooth_idx] .- p_ex[smooth_idx]).^2) / length(smooth_idx))

println("\n" * "="^50)
println("ERROR ANALYSIS (vs exact Riemann solution)")
println("="^50)
println("Global L2 errors (includes discontinuities):")
@printf("  density:     %.6e\n", L2_ρ)
@printf("  velocity:    %.6e\n", L2_u)
@printf("  pressure:    %.6e\n", L2_p)
@printf("  temperature: %.6e\n", L2_T)
println("\nSmooth-region L2 errors (undisturbed states):")
@printf("  density:     %.6e\n", L2_ρ_smooth)
@printf("  velocity:    %.6e\n", L2_u_smooth)
@printf("  pressure:    %.6e\n", L2_p_smooth)
println("\nNote: Global errors are dominated by numerical diffusion at")
println("discontinuities (contact, shock). This is expected for a")
println("1st-order kinetic scheme with Kn=0.0001.")

# Check key states
println("\n" * "="^50)
println("KEY STATE VERIFICATION")
println("="^50)
# Post-shock density
idx_contact = findfirst(x .> 0.5 + 0.2 * 0.9274) # approximate contact position
@printf("Post-shock region density:  computed=%.4f  exact=%.4f\n", 
    ρ[min(idx_contact+5, nx)], ρ_ex[min(idx_contact+5, nx)])
# Shock position (find steepest gradient)
dρ = diff(ρ)
shock_idx = argmax(abs.(dρ)) + 100  # search in right half
@printf("Approximate shock position: x ≈ %.4f\n", x[min(shock_idx, nx)])

# ---- Save plots ----
outdir = joinpath(@__DIR__, "..", "report", "figures")
mkpath(outdir)

# Density
p1 = plot(x, ρ, label="Kinetic.jl (BGK)", linewidth=2, color=:blue,
    xlabel="x", ylabel="Density ρ", title="Sod Shock Tube — Density (t=0.2)")
plot!(p1, x, ρ_ex, label="Exact Riemann", linewidth=2, linestyle=:dash, color=:red)
savefig(p1, joinpath(outdir, "sod_density.png"))

# Velocity
p2 = plot(x, u, label="Kinetic.jl (BGK)", linewidth=2, color=:blue,
    xlabel="x", ylabel="Velocity u", title="Sod Shock Tube — Velocity (t=0.2)")
plot!(p2, x, u_ex, label="Exact Riemann", linewidth=2, linestyle=:dash, color=:red)
savefig(p2, joinpath(outdir, "sod_velocity.png"))

# Pressure
p3 = plot(x, p_val, label="Kinetic.jl (BGK)", linewidth=2, color=:blue,
    xlabel="x", ylabel="Pressure p", title="Sod Shock Tube — Pressure (t=0.2)")
plot!(p3, x, p_ex, label="Exact Riemann", linewidth=2, linestyle=:dash, color=:red)
savefig(p3, joinpath(outdir, "sod_pressure.png"))

# Temperature
p4 = plot(x, T, label="Kinetic.jl (BGK)", linewidth=2, color=:blue,
    xlabel="x", ylabel="Temperature T", title="Sod Shock Tube — Temperature (t=0.2)")
plot!(p4, x, T_ex, label="Exact Riemann", linewidth=2, linestyle=:dash, color=:red)
savefig(p4, joinpath(outdir, "sod_temperature.png"))

# Combined 4-panel
p_all = plot(p1, p2, p3, p4, layout=(2,2), size=(1000,700),
    plot_title="Sod Shock Tube: Kinetic.jl BGK vs Exact Riemann (t=0.2)")
savefig(p_all, joinpath(outdir, "sod_combined.png"))

println("\nPlots saved to: $outdir")

# ---- Save CSV data ----
datadir = joinpath(@__DIR__, "data")
mkpath(datadir)
open(joinpath(datadir, "sod_results.csv"), "w") do io
    println(io, "x,rho,u,p,T,rho_exact,u_exact,p_exact,T_exact")
    for i in 1:nx
        @printf(io, "%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f\n",
            x[i], ρ[i], u[i], p_val[i], T[i], ρ_ex[i], u_ex[i], p_ex[i], T_ex[i])
    end
end
println("Data saved to: $(joinpath(datadir, "sod_results.csv"))")

println("\n✓ Sod shock tube replication complete")
