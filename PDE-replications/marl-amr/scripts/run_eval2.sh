#!/bin/bash
# Second-pass eval: multi-episode randomized ICs for both VDGN and heuristic; finer threshold sweep.
set -e
set -o pipefail

PROJDIR=/data/stevens/projects-active/marl-amr
LOG=$PROJDIR/eval2.log
exec > >(tee -a "$LOG") 2>&1
echo "=== $(date -Is) eval pass 2 ==="

source ~/env.sh 2>/dev/null || true
source ~/miniconda3/etc/profile.d/conda.sh
conda activate marlamr
cd "$PROJDIR/marl-amr/marl_amr/alg"
export CUDA_VISIBLE_DEVICES=""

# (A) Patch advection_test to use the *training* IC randomization + 20 episodes.
# Make a copy of the test config that randomizes ICs over the paper's training distribution.
cat > configs/advection_test_random.py <<'PYEOF'
from marl_amr.alg.configs.advection_test import get_config as base_get_config
import numpy as np

def get_config():
    config = base_get_config()
    # Override IC params to the paper's training distribution (per advection_vdgn.py)
    config.env.solver.initial_condition.params = type(config.env.solver.initial_condition.params)()
    config.env.solver.initial_condition.params.randomize = 'uniform'
    config.env.solver.initial_condition.params.theta_range = [0.0, 1.0]
    config.env.solver.initial_condition.params.u0_range = [0.0, np.sqrt(2*1.5**2)]
    config.env.solver.initial_condition.params.w_range = [100, 100]
    config.env.solver.initial_condition.params.x0_range = [0.5, 1.5]
    config.env.solver.initial_condition.params.y0_range = [0.5, 1.5]
    config.alg.n_test_episodes = 20
    config.main.dir_name = 'random_eval'
    return config
PYEOF

mkdir -p nx16_ny16_depth1_tstep0p25_vdgn_pretrained

echo ""
echo "----- (A) VDGN, 20 episodes, randomized IC (paper training distribution) -----"
python test.py tf --config_name=advection_test_random --write_csv --name_train=vdgn --name_test=random20 2>&1 | tee $PROJDIR/eval_vdgn_random20.log | grep -vE "(FutureWarning|np_q|np_resource|gradients_util|sparse Indexed|^      )" | tail -40

echo ""
echo "----- (A.1) VDGN, 1 episode, deterministic single-Gaussian (paper Fig5 setting) -----"
python test.py tf --config_name=advection_test --verbose --save_err_time 2>&1 | tee $PROJDIR/eval_vdgn_singleGauss.log | grep -vE "(FutureWarning|np_q|np_resource|gradients_util|sparse Indexed|^      )" | tail -30

# Copy VDGN error_vs_time to a stable location
cp nx16_ny16_depth1_tstep0p25_vdgn_pretrained/error_vs_time.csv $PROJDIR/vdgn_err_vs_time_singleGauss.csv 2>/dev/null || true

# (B) Heuristic baselines on the SAME randomized IC distribution, 20 episodes
echo ""
echo "----- (B) Heuristic DoubleThreshold sweep, 20 randomized episodes -----"
cd "$PROJDIR/marl-amr/marl_amr/scripts"
mkdir -p $PROJDIR/heuristic_out2

# Need a random-IC version of the JSON config too. Make one.
cat > $PROJDIR/marl-amr/marl_amr/envs/configs/advection_href_random.json <<'JSEOF'
{
  "env": {
    "agent_manager_use_tree": false,
    "agent_obs_type": "self",
    "debug": false,
    "dof_threshold": 1000000,
    "dimensionless": true,
    "edge_feature_is_relative": true,
    "enable_deref": true,
    "error_threshold": 5.0e-4,
    "log_obs": true,
    "max_depth": 1,
    "multi_objective": false,
    "obs_uses_true_error": true,
    "observation_type": "graph",
    "observe_depth": true,
    "observe_dof_and_time_balance": false,
    "overrefine_penalty_factor": 5.0,
    "penalize_dof_excess": true,
    "reward_type": "global",
    "reward_uses_true_error": true,
    "solver": {
      "aniso": false,
      "CFL": null,
      "dt": 0.002,
      "element_shape": "quad",
      "error_method": "projected",
      "initial_condition": {
        "coefficient": "Gaussian2DCoefficient",
        "params": {
          "randomize": "uniform",
          "theta_range": [0.0, 1.0],
          "u0_range": [0.0, 2.121320343559643],
          "w_range": [100, 100],
          "x0_range": [0.5, 1.5],
          "y0_range": [0.5, 1.5]
        }
      },
      "jit": true,
      "length": 2,
      "mesh_file": "",
      "nx": 16,
      "ny": 16,
      "nz": 1,
      "orbiting_velocities": false,
      "order": 1,
      "periodic": true,
      "ratio": 25,
      "refine_IC": true,
      "refinement_mode": "h",
      "single_step": false,
      "sx": 2.0,
      "sy": 2.0,
      "sz": 1.0,
      "t_step": 0.25
    },
    "solver_name": "advection",
    "stopping_criteria": "budget_or_time",
    "t_final": 0.75,
    "t_history": 1
  }
}
JSEOF

# Sweep a Pareto of thresholds with 20 episodes each
for HIGH in 1e-4 5e-4 1e-3 5e-3; do
  echo "  -- DoubleThreshold high=$HIGH (20 episodes) --"
  python evaluate_custom_strategies.py advection_href_random dt \
      --low_array=1e-5 \
      --high_array=$HIGH \
      --n_episodes=20 \
      --save_dir=$PROJDIR/heuristic_out2 \
      --name=ht_h${HIGH} 2>&1 | tail -8
done

# err_vs_time for both the deterministic single-Gaussian setting and one threshold
echo ""
echo "----- (C) Heuristic err_vs_time on DETERMINISTIC single Gaussian (matches VDGN A.1) -----"
python evaluate_custom_strategies.py advection_href err_vs_time \
    --thres_low=1e-5 --thres_high=5e-4 \
    --multipliers=125 \
    --save_dir=$PROJDIR/heuristic_out2 2>&1 | tail -8
mv $PROJDIR/heuristic_out2/true_error_t_step_125_dt.csv $PROJDIR/heuristic_err_vs_time_singleGauss.csv 2>/dev/null || true

echo ""
echo "----- (D) Fixed mesh baselines (coarse / fine) on 20 randomized episodes -----"
python evaluate_custom_strategies.py advection_href_random coarse \
    --n_episodes=20 --write_csv --save_dir=$PROJDIR/heuristic_out2 --name=fixed20 2>&1 | tail -5
python evaluate_custom_strategies.py advection_href_random fine \
    --n_episodes=20 --write_csv --save_dir=$PROJDIR/heuristic_out2 --name=fixed20 2>&1 | tail -5

echo ""
echo "----- summary listing -----"
ls -la $PROJDIR/heuristic_out2/
ls -la $PROJDIR/vdgn_err_vs_time_singleGauss.csv 2>/dev/null
ls -la $PROJDIR/heuristic_err_vs_time_singleGauss.csv 2>/dev/null
ls -la $PROJDIR/marl-amr/marl_amr/results/advection/random_eval/ 2>/dev/null
echo "=== $(date -Is) eval2 done ==="
