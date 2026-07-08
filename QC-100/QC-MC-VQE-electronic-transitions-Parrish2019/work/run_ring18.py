import importlib.util, json, numpy as np, time
spec=importlib.util.spec_from_file_location('m','QC-MC-VQE-exciton.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
# monkeypatch optimize maxiter via run_case default; call run_case then cap inside
g,mt,md,dE=m.lh2_ring_geometry(N=18)
# patch MCVQE.optimize to cap iterations
orig=m.MCVQE.optimize
def capped(self, maxiter=25, restarts=0): return orig(self, maxiter=25, restarts=0)
m.MCVQE.optimize=capped
t=time.time()
r,_=m.run_case("N18_LH2_B850_ring", g,mt,md,dE, nstates=18, layers=1,
               neighbor_only=True, ring=True)
json.dump({"N18_LH2_B850_ring":r}, open("results_ring18.json","w"), indent=2)
print("DONE in", round(time.time()-t), "s")
print(json.dumps({k:r[k] for k in
    ['n_matched_mc','max_en_err_mc_matched_ueV','mean_en_err_mc_matched_ueV',
     'max_en_err_cis_matched_meV','max_mc_O_relerr_matched','max_cis_O_relerr_matched',
     'mean_cis_blueshift_meV','n_lbfgs_iters','nparam','c5_residual','runtime_s']}, indent=2))
