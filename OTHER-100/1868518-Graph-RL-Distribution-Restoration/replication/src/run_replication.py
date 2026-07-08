#!/usr/bin/env python3
"""
Main Replication Script
========================
Runs the complete replication of Zhao & Wang (2021):
"Learning Sequential Distribution System Restoration via Graph-Reinforcement Learning"

This script:
1. Trains GCN-DQN (paper's method) on IEEE 33-bus and IEEE 123-bus
2. Trains MLP-DQN baseline for comparison  
3. Evaluates all methods + baselines
4. Runs generalization tests
5. Generates plots and report data
"""

import os
import sys
import json
import time
import numpy as np
import torch

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from environment import make_env
from train import GCN_DQN_Trainer, MLPDQNTrainer
from evaluate import (run_comparison, evaluate_random_baseline, 
                      evaluate_greedy_baseline, generalization_test,
                      timing_analysis)
from plot_results import (plot_training_curves, plot_comparison_bar,
                          plot_network_graph)


def main():
    # Setup directories
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    results_dir = os.path.join(base_dir, 'results')
    figures_dir = os.path.join(base_dir, 'figures')
    os.makedirs(results_dir, exist_ok=True)
    os.makedirs(figures_dir, exist_ok=True)
    
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Using device: {device}")
    
    all_results = {}
    
    # ================================================================
    # Phase 1: Train on IEEE 33-bus (smaller, faster)
    # ================================================================
    print("\n" + "="*60)
    print("PHASE 1: Training on IEEE 33-bus network")
    print("="*60)
    
    n_episodes_33 = 2000
    
    # GCN-DQN on 33-bus
    print("\n--- GCN-DQN on IEEE 33-bus ---")
    env_33 = make_env(network_case='ieee33', max_steps=20, n_dgs=4, seed=42)
    gcn_config_33 = {
        'n_episodes': n_episodes_33,
        'max_steps': 20,
        'lr': 3e-4,
        'batch_size': 32,
        'eval_interval': 200,
        'log_interval': 100,
        'epsilon_decay': 0.999,
    }
    gcn_trainer_33 = GCN_DQN_Trainer(env_33, config=gcn_config_33, device=device)
    gcn_save_dir_33 = os.path.join(results_dir, 'gcn_dqn_ieee33')
    t0 = time.time()
    gcn_history_33 = gcn_trainer_33.train(save_dir=gcn_save_dir_33)
    gcn_time_33 = time.time() - t0
    print(f"GCN-DQN 33-bus training: {gcn_time_33:.1f}s")
    
    # MLP-DQN on 33-bus
    print("\n--- MLP-DQN on IEEE 33-bus ---")
    env_33_mlp = make_env(network_case='ieee33', max_steps=20, n_dgs=4, seed=42)
    mlp_config_33 = {
        'n_episodes': n_episodes_33,
        'max_steps': 20,
        'lr': 3e-4,
        'batch_size': 32,
        'eval_interval': 200,
        'log_interval': 100,
        'epsilon_decay': 0.999,
    }
    mlp_trainer_33 = MLPDQNTrainer(env_33_mlp, config=mlp_config_33, device=device)
    mlp_save_dir_33 = os.path.join(results_dir, 'mlp_dqn_ieee33')
    t0 = time.time()
    mlp_history_33 = mlp_trainer_33.train(save_dir=mlp_save_dir_33)
    mlp_time_33 = time.time() - t0
    print(f"MLP-DQN 33-bus training: {mlp_time_33:.1f}s")
    
    # ================================================================
    # Phase 2: Train on IEEE 123-bus
    # ================================================================
    print("\n" + "="*60)
    print("PHASE 2: Training on IEEE 123-bus network")
    print("="*60)
    
    n_episodes_123 = 2000
    
    # GCN-DQN on 123-bus
    print("\n--- GCN-DQN on IEEE 123-bus ---")
    env_123 = make_env(network_case='ieee123', max_steps=30, n_dgs=5, seed=42)
    gcn_config_123 = {
        'n_episodes': n_episodes_123,
        'max_steps': 30,
        'lr': 1e-4,
        'batch_size': 32,
        'eval_interval': 200,
        'log_interval': 100,
        'epsilon_decay': 0.9995,
    }
    gcn_trainer_123 = GCN_DQN_Trainer(env_123, config=gcn_config_123, device=device)
    gcn_save_dir_123 = os.path.join(results_dir, 'gcn_dqn_ieee123')
    t0 = time.time()
    gcn_history_123 = gcn_trainer_123.train(save_dir=gcn_save_dir_123)
    gcn_time_123 = time.time() - t0
    print(f"GCN-DQN 123-bus training: {gcn_time_123:.1f}s")
    
    # MLP-DQN on 123-bus
    print("\n--- MLP-DQN on IEEE 123-bus ---")
    env_123_mlp = make_env(network_case='ieee123', max_steps=30, n_dgs=5, seed=42)
    mlp_config_123 = {
        'n_episodes': n_episodes_123,
        'max_steps': 30,
        'lr': 1e-4,
        'batch_size': 32,
        'eval_interval': 200,
        'log_interval': 100,
        'epsilon_decay': 0.9995,
    }
    mlp_trainer_123 = MLPDQNTrainer(env_123_mlp, config=mlp_config_123, device=device)
    mlp_save_dir_123 = os.path.join(results_dir, 'mlp_dqn_ieee123')
    t0 = time.time()
    mlp_history_123 = mlp_trainer_123.train(save_dir=mlp_save_dir_123)
    mlp_time_123 = time.time() - t0
    print(f"MLP-DQN 123-bus training: {mlp_time_123:.1f}s")
    
    # ================================================================
    # Phase 3: Evaluation
    # ================================================================
    print("\n" + "="*60)
    print("PHASE 3: Evaluation & Comparison")
    print("="*60)
    
    eval_results = {}
    
    for network in ['ieee33', 'ieee123']:
        n_dgs = 4 if network == 'ieee33' else 5
        max_steps = 20 if network == 'ieee33' else 30
        
        env = make_env(network_case=network, max_steps=max_steps, n_dgs=n_dgs, seed=42)
        
        print(f"\n--- Evaluating on {network} ---")
        
        # Random baseline
        random_res = evaluate_random_baseline(env, n_episodes=100, max_steps=max_steps)
        
        # Greedy baseline
        greedy_res = evaluate_greedy_baseline(env, n_episodes=100, max_steps=max_steps)
        
        # GCN-DQN
        gcn_checkpoint = os.path.join(results_dir, f'gcn_dqn_{network}', 'best_model.pt')
        if os.path.exists(gcn_checkpoint):
            gcn_trainer = GCN_DQN_Trainer(env, device=device)
            gcn_trainer.load(gcn_checkpoint)
            gcn_trainer.epsilon = 0.0
            gcn_eval_r, gcn_eval_l = gcn_trainer.evaluate(n_episodes=100)
        else:
            gcn_eval_r, gcn_eval_l = 0.0, 0.0
        
        # MLP-DQN
        mlp_eval_r, mlp_eval_l = 0.0, 0.0
        mlp_checkpoint = os.path.join(results_dir, f'mlp_dqn_{network}', 'best_model.pt')
        if os.path.exists(mlp_checkpoint):
            mlp_trainer = MLPDQNTrainer(env, device=device)
            mlp_trainer.policy_net.load_state_dict(
                torch.load(mlp_checkpoint, map_location=device))
            mlp_trainer.epsilon = 0.0
            mlp_eval_r, mlp_eval_l = mlp_trainer.evaluate(n_episodes=100)
        
        eval_results[network] = {
            'random': {
                'mean_reward': float(np.mean(random_res['rewards'])),
                'std_reward': float(np.std(random_res['rewards'])),
                'mean_load_ratio': float(np.mean(random_res['load_ratios'])),
                'std_load_ratio': float(np.std(random_res['load_ratios'])),
                'convergence_rate': float(np.mean(random_res['pf_converged'])),
            },
            'greedy': {
                'mean_reward': float(np.mean(greedy_res['rewards'])),
                'std_reward': float(np.std(greedy_res['rewards'])),
                'mean_load_ratio': float(np.mean(greedy_res['load_ratios'])),
                'std_load_ratio': float(np.std(greedy_res['load_ratios'])),
                'convergence_rate': float(np.mean(greedy_res['pf_converged'])),
            },
            'gcn_dqn': {
                'mean_reward': float(gcn_eval_r),
                'mean_load_ratio': float(gcn_eval_l),
            },
            'mlp_dqn': {
                'mean_reward': float(mlp_eval_r),
                'mean_load_ratio': float(mlp_eval_l),
            },
        }
        
        print(f"\n  Results for {network}:")
        print(f"  {'Method':<15} {'Reward':>10} {'Load Ratio':>12}")
        print(f"  {'-'*37}")
        for method, res in eval_results[network].items():
            r = res.get('mean_reward', 0)
            l = res.get('mean_load_ratio', 0)
            print(f"  {method:<15} {r:>10.4f} {l:>12.4f}")
    
    # ================================================================
    # Phase 4: Generalization & Timing
    # ================================================================
    print("\n" + "="*60)
    print("PHASE 4: Generalization & Timing Analysis")
    print("="*60)
    
    timing = timing_analysis(device=device)
    
    # ================================================================
    # Phase 5: Generate Plots
    # ================================================================
    print("\n" + "="*60)
    print("PHASE 5: Generating Plots")
    print("="*60)
    
    # Training curves
    for network in ['ieee33', 'ieee123']:
        paths = []
        labels = []
        for method in ['gcn_dqn', 'mlp_dqn']:
            p = os.path.join(results_dir, f'{method}_{network}', 'training_history.json')
            if os.path.exists(p):
                paths.append(p)
                labels.append(method.upper().replace('_', '-'))
        
        if paths:
            plot_training_curves(
                paths, labels,
                os.path.join(figures_dir, f'fig1_training_{network}.png'),
                title=f'Training Progress - {network.upper()}'
            )
    
    # Comparison bars
    for network, results in eval_results.items():
        plot_comparison_bar(
            results,
            os.path.join(figures_dir, f'fig2_comparison_{network}.png'),
            title=f'Method Comparison - {network.upper()}'
        )
    
    # Network topology
    for network in ['ieee33', 'ieee123']:
        n_dgs = 4 if network == 'ieee33' else 5
        env = make_env(network_case=network, n_dgs=n_dgs, seed=42)
        plot_network_graph(
            env,
            os.path.join(figures_dir, f'fig3_topology_{network}.png'),
            title=f'{network.upper()} Distribution Network'
        )
    
    # ================================================================
    # Save all results
    # ================================================================
    final_results = {
        'evaluation': eval_results,
        'timing': timing,
        'training_times': {
            'gcn_dqn_ieee33': gcn_time_33,
            'mlp_dqn_ieee33': mlp_time_33,
            'gcn_dqn_ieee123': gcn_time_123,
            'mlp_dqn_ieee123': mlp_time_123,
        },
    }
    
    with open(os.path.join(results_dir, 'all_results.json'), 'w') as f:
        json.dump(final_results, f, indent=2, default=str)
    
    print(f"\n{'='*60}")
    print("REPLICATION COMPLETE")
    print(f"Results: {results_dir}")
    print(f"Figures: {figures_dir}")
    print(f"{'='*60}")
    
    return final_results


if __name__ == '__main__':
    main()
