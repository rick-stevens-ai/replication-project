"""
Master runner for Zhang et al. 2019 replication.
Runs all three examples and collects results.
"""
import json
import os
import sys
import time

RESULTS_DIR = '../results'

def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)

    all_results = {}
    t_total_start = time.time()

    # Example 1: Stochastic Advection
    print("=" * 70)
    print("EXAMPLE 1: STOCHASTIC ADVECTION")
    print("=" * 70)
    from example1_advection import train_advection

    print("\n--- NN-DO ---")
    adv_do = train_advection(method='DO', save_dir=os.path.join(RESULTS_DIR, 'advection'))
    all_results['advection_DO'] = adv_do

    print("\n--- NN-BO ---")
    adv_bo = train_advection(method='BO', save_dir=os.path.join(RESULTS_DIR, 'advection'))
    all_results['advection_BO'] = adv_bo

    # Example 2: Stochastic Burgers
    print("\n" + "=" * 70)
    print("EXAMPLE 2: STOCHASTIC BURGERS")
    print("=" * 70)
    from example2_burgers import train_burgers

    print("\n--- NN-DO ---")
    burg_do = train_burgers(method='DO', save_dir=os.path.join(RESULTS_DIR, 'burgers'))
    all_results['burgers_DO'] = burg_do

    print("\n--- NN-BO ---")
    burg_bo = train_burgers(method='BO', save_dir=os.path.join(RESULTS_DIR, 'burgers'))
    all_results['burgers_BO'] = burg_bo

    # Example 3: Reaction-Diffusion
    print("\n" + "=" * 70)
    print("EXAMPLE 3: REACTION-DIFFUSION")
    print("=" * 70)
    from example3_reaction_diffusion import train_forward, train_inverse

    print("\n--- Forward Problem ---")
    rd_fwd = train_forward(save_dir=os.path.join(RESULTS_DIR, 'reaction_diffusion'))
    all_results['reaction_diffusion_forward'] = rd_fwd

    print("\n--- Inverse Problem ---")
    rd_inv = train_inverse(save_dir=os.path.join(RESULTS_DIR, 'reaction_diffusion'))
    all_results['reaction_diffusion_inverse'] = rd_inv

    total_time = time.time() - t_total_start
    print(f"\n{'='*70}")
    print(f"ALL DONE. Total time: {total_time:.1f}s ({total_time/3600:.2f}h)")
    print(f"{'='*70}")

    # Save summary
    summary = {
        'advection_DO': adv_do.get('errors', {}),
        'advection_BO': adv_bo.get('errors', {}),
        'burgers_DO': {k: v for k, v in burg_do.items() if k != 'total_training_time'},
        'burgers_BO': {k: v for k, v in burg_bo.items() if k != 'total_training_time'},
        'reaction_diffusion_inverse': {
            'a_predicted': rd_inv.get('a_predicted'),
            'b_predicted': rd_inv.get('b_predicted'),
            'a_true': rd_inv.get('a_true'),
            'b_true': rd_inv.get('b_true'),
        },
        'total_time': total_time,
    }

    with open(os.path.join(RESULTS_DIR, 'summary.json'), 'w') as f:
        json.dump(summary, f, indent=2, default=str)

    print("\nResults saved to", RESULTS_DIR)


if __name__ == '__main__':
    main()
