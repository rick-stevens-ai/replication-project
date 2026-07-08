"""ERA5 — diagnosis (no re-pass possible without real data).

The prior pass documented three failed data acquisition routes:
  - WeatherBench 1.0 (TUM Nextcloud): HTTP 401 Unauthorized
  - WeatherBench 2 (Google Cloud Storage zarr): aiohttp / HTTPS_PROXY incompatibility
  - Copernicus CDS API: requires a registered Copernicus account

The prior pass used a clearly-labeled synthetic AR(1)+wave proxy.  The paper's
ERA5 claims (14-day forecasts beating persistence, stable 1-year climatology)
*cannot* be evaluated against this proxy because:
  - the AR(1) proxy is trivially predictable by *any* model
  - it has no real climatology to match
  - it has no real spectral characteristics

This script confirms the situation by:
  1. Reading prior pass metrics
  2. Listing the artifacts that would unblock a real re-pass
  3. Documenting what *was* shown (code path works end-to-end on synthetic data)

Outputs:
  - results/repass/era5/diagnosis.json
"""
import json, os, sys


def main():
    prior_metrics = os.path.join(
        os.path.dirname(__file__), "..", "..",
        "replication", "v2_faithful", "results", "era5", "metrics.json")
    out_dir = os.path.join(
        os.path.dirname(__file__), "..", "..", "results", "repass", "era5")
    os.makedirs(out_dir, exist_ok=True)

    with open(prior_metrics) as f:
        prior = json.load(f)

    rmse_model = prior.get("rmse_model_per_step", [])
    rmse_pers  = prior.get("rmse_persistence_per_step", [])
    rmse_clim  = prior.get("rmse_climatology_per_step", [])
    beats_pers = all((m < p for m, p in zip(rmse_model[1:], rmse_pers[1:])))

    diagnosis = {
        "paper_claims_assessed_against": "synthetic AR(1)+wave proxy (NOT real ERA5)",
        "paper_claims": [
            "14-day forecasts beat persistence model",
            "14-day forecasts beat vanilla NODE",
            "Stable 1-year climatology when started from random init in 2011-2016",
            "Reasonable spatial reconstruction of T,U,V,H at day 1 and day 14",
        ],
        "prior_pass_status": {
            "model_beats_persistence_on_proxy": bool(beats_pers),
            "n_steps": len(rmse_model),
            "rmse_model_final": rmse_model[-1] if rmse_model else None,
            "rmse_persistence_final": rmse_pers[-1] if rmse_pers else None,
            "rmse_climatology_final": rmse_clim[-1] if rmse_clim else None,
        },
        "what_proxy_proves": (
            "Code path is correct end-to-end. DilatedCNN-RHS NODE encoder/decoder "
            "pipeline runs, MP penalty schedule executes, rollouts produce finite "
            "stable predictions on the synthetic data. This is necessary but not "
            "sufficient -- nothing about the synthetic test exercises atmospheric "
            "physics, so no claim about real-ERA5 skill can be made."
        ),
        "what_proxy_does_NOT_prove": [
            "14-day forecast skill on real reanalysis data",
            "Long-term climatological stability of MP-NODE on chaotic 5-variable global flow",
            "Comparative skill vs. vanilla NODE on real ERA5",
            "Stability when started from out-of-sample (2011-2016) ICs vs. train (2000-2009)",
        ],
        "agreement_diagnosis_for_ERA5": (
            "Agreement cannot be diagnosed -- it is a data-availability question, "
            "not a method question. The prior pass got 'agreement N/A' for this "
            "section, which is the only honest score. There is no failure of "
            "MP-NODE here; there is failure to acquire the input data."
        ),
        "unblock_plan_smallest_path": [
            "Register free Copernicus CDS account (https://cds.climate.copernicus.eu)",
            "Get UID + API key, place in ~/.cdsapirc",
            "`pip install cdsapi`",
            "Use cds.retrieve('reanalysis-era5-pressure-levels', {...}) for t/q/u/v at sigma~0.95/0.51",
            "OR: identify a WeatherBench2 mirror reachable from CherryRd (not GCS)",
        ],
        "re_pass_action": (
            "No new run for ERA5 on this pass. The prior pass artifact is already the "
            "best the project can produce without one of the unblocks above. We update "
            "the agreement score to clarify it is 'data-blocked', not 'model failed'."
        ),
    }

    with open(os.path.join(out_dir, "diagnosis.json"), "w") as f:
        json.dump(diagnosis, f, indent=2)

    print("=== ERA5 diagnosis ===")
    print(json.dumps(diagnosis, indent=2))


if __name__ == "__main__":
    main()
