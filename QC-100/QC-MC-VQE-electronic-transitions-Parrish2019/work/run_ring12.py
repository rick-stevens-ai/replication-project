import importlib.util, json, numpy as np
spec=importlib.util.spec_from_file_location('m','QC-MC-VQE-exciton.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
g,mt,md,dE=m.lh2_ring_geometry(N=12)
r,_=m.run_case("N12_LH2_ring", g,mt,md,dE, nstates=12, layers=1,
               neighbor_only=True, ring=True)
json.dump({"N12_LH2_ring":r}, open("results_ring12.json","w"), indent=2)
print(json.dumps({k:r[k] for k in
    ['n_matched_mc','max_en_err_mc_matched_ueV','mean_en_err_mc_matched_ueV',
     'max_en_err_cis_matched_meV','max_mc_O_relerr_matched','max_cis_O_relerr_matched',
     'mean_cis_blueshift_meV','n_lbfgs_iters','nparam','c5_residual','runtime_s']}, indent=2))
