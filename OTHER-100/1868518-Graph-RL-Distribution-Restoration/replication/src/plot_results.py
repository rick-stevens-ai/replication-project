"""
Plotting utilities for replication results.
Generates figures comparable to the original paper.
"""

import os
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')


def plot_training_curves(history_paths, labels, save_path, title="Training Progress"):
    """Plot training reward curves for multiple methods."""
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    colors = ['#2196F3', '#FF5722', '#4CAF50', '#9C27B0', '#FF9800']
    
    for i, (path, label) in enumerate(zip(history_paths, labels)):
        if not os.path.exists(path):
            continue
        with open(path) as f:
            history = json.load(f)
        
        color = colors[i % len(colors)]
        
        # Smooth with moving average
        window = 50
        
        # Episode rewards
        rewards = np.array(history.get('episode_rewards', []))
        if len(rewards) > window:
            smoothed = np.convolve(rewards, np.ones(window)/window, mode='valid')
            axes[0].plot(range(len(smoothed)), smoothed, color=color, label=label, alpha=0.8)
            axes[0].fill_between(range(len(smoothed)), 
                                smoothed - np.std(rewards[:len(smoothed)]),
                                smoothed + np.std(rewards[:len(smoothed)]),
                                alpha=0.15, color=color)
        
        # Load ratios
        load_ratios = np.array(history.get('episode_load_ratios', []))
        if len(load_ratios) > window:
            smoothed_lr = np.convolve(load_ratios, np.ones(window)/window, mode='valid')
            axes[1].plot(range(len(smoothed_lr)), smoothed_lr, color=color, label=label, alpha=0.8)
        
        # Eval rewards
        eval_rewards = history.get('eval_rewards', [])
        if eval_rewards:
            x_eval = np.linspace(0, len(rewards), len(eval_rewards))
            axes[2].plot(x_eval, eval_rewards, 'o-', color=color, label=label, markersize=4)
    
    axes[0].set_xlabel('Episode')
    axes[0].set_ylabel('Episode Reward')
    axes[0].set_title('Training Reward')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    axes[1].set_xlabel('Episode')
    axes[1].set_ylabel('Load Restoration Ratio')
    axes[1].set_title('Load Restoration Progress')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    axes[2].set_xlabel('Episode')
    axes[2].set_ylabel('Evaluation Reward')
    axes[2].set_title('Evaluation Performance')
    axes[2].legend()
    axes[2].grid(True, alpha=0.3)
    
    plt.suptitle(title, fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {save_path}")


def plot_comparison_bar(results, save_path, title="Method Comparison"):
    """Bar chart comparing methods across metrics."""
    methods = list(results.keys())
    metrics = ['mean_reward', 'mean_load_ratio', 'convergence_rate']
    metric_labels = ['Mean Reward', 'Load Restoration Ratio', 'PF Convergence Rate']
    
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    
    colors = ['#2196F3', '#FF5722', '#4CAF50', '#9C27B0', '#FF9800']
    
    for ax_idx, (metric, metric_label) in enumerate(zip(metrics, metric_labels)):
        values = []
        errors = []
        for method in methods:
            values.append(results[method].get(metric, 0))
            errors.append(results[method].get(f'std_{metric.replace("mean_", "")}', 0))
        
        bars = axes[ax_idx].bar(methods, values, color=colors[:len(methods)], 
                                 alpha=0.8, edgecolor='black', linewidth=0.5)
        if any(e > 0 for e in errors):
            axes[ax_idx].errorbar(methods, values, yerr=errors, 
                                  fmt='none', color='black', capsize=5)
        
        axes[ax_idx].set_ylabel(metric_label)
        axes[ax_idx].set_title(metric_label)
        axes[ax_idx].grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for bar, val in zip(bars, values):
            axes[ax_idx].text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.01,
                             f'{val:.3f}', ha='center', va='bottom', fontsize=9)
    
    plt.suptitle(title, fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {save_path}")


def plot_restoration_timeline(env, actions_sequence, save_path):
    """Plot restoration timeline showing load recovery over steps."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    load_ratios = []
    voltage_mins = []
    voltage_maxs = []
    dgs_active = []
    
    state = env.reset()
    
    for step, actions in enumerate(actions_sequence):
        state, reward, done, info = env.step(actions)
        
        load_ratios.append(info.get('restored_load_ratio', 0))
        
        if env.pf_converged and len(env.net.res_bus) > 0:
            vms = env.net.res_bus.vm_pu[env.net.res_bus.vm_pu > 0]
            voltage_mins.append(vms.min() if len(vms) > 0 else 0)
            voltage_maxs.append(vms.max() if len(vms) > 0 else 0)
        else:
            voltage_mins.append(0)
            voltage_maxs.append(0)
        
        n_active = sum(1 for i in env.dg_indices if env.net.sgen.at[i, 'in_service'])
        dgs_active.append(n_active)
        
        if done:
            break
    
    steps = range(1, len(load_ratios) + 1)
    
    # Load restoration
    axes[0, 0].plot(steps, load_ratios, 'b-o', markersize=4, linewidth=2)
    axes[0, 0].fill_between(steps, 0, load_ratios, alpha=0.2)
    axes[0, 0].set_xlabel('Restoration Step')
    axes[0, 0].set_ylabel('Load Restoration Ratio')
    axes[0, 0].set_title('Sequential Load Restoration')
    axes[0, 0].set_ylim(0, 1.1)
    axes[0, 0].axhline(y=1.0, color='g', linestyle='--', alpha=0.5, label='Full restoration')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # Voltage profile
    axes[0, 1].fill_between(steps, voltage_mins, voltage_maxs, alpha=0.3, color='orange')
    axes[0, 1].plot(steps, voltage_mins, 'r-', label='Min voltage')
    axes[0, 1].plot(steps, voltage_maxs, 'g-', label='Max voltage')
    axes[0, 1].axhline(y=0.95, color='r', linestyle='--', alpha=0.5, label='Lower limit')
    axes[0, 1].axhline(y=1.05, color='r', linestyle='--', alpha=0.5, label='Upper limit')
    axes[0, 1].set_xlabel('Restoration Step')
    axes[0, 1].set_ylabel('Voltage (p.u.)')
    axes[0, 1].set_title('Voltage Profile During Restoration')
    axes[0, 1].legend(fontsize=8)
    axes[0, 1].grid(True, alpha=0.3)
    
    # DGs active
    axes[1, 0].bar(steps, dgs_active, color='#4CAF50', alpha=0.8)
    axes[1, 0].set_xlabel('Restoration Step')
    axes[1, 0].set_ylabel('Active DGs')
    axes[1, 0].set_title('DG Activation Sequence')
    axes[1, 0].grid(True, alpha=0.3)
    
    # Cumulative reward
    cumulative = np.cumsum([info.get('reward_breakdown', {}).get('load', 0) 
                           for _ in load_ratios])
    axes[1, 1].plot(steps, load_ratios, 'b-o', markersize=4, linewidth=2, label='Load ratio')
    axes[1, 1].set_xlabel('Restoration Step')
    axes[1, 1].set_ylabel('Metric')
    axes[1, 1].set_title('Restoration Metrics')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.suptitle('Distribution System Restoration Timeline', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {save_path}")


def plot_network_graph(env, save_path, title="Network Topology"):
    """Visualize the distribution network topology."""
    try:
        import networkx as nx
        
        G = env.get_graph()
        
        fig, ax = plt.subplots(1, 1, figsize=(12, 10))
        
        pos = nx.spring_layout(G, k=2.0/np.sqrt(len(G.nodes())), iterations=50, seed=42)
        
        # Color nodes by type
        node_colors = []
        for node in G.nodes():
            if node == 0:
                node_colors.append('#FF0000')  # Substation
            elif node in env.dg_buses:
                node_colors.append('#00FF00')  # DG bus
            else:
                node_colors.append('#87CEEB')  # Regular bus
        
        nx.draw(G, pos, ax=ax, node_color=node_colors, node_size=50,
               with_labels=False, edge_color='gray', alpha=0.7, width=0.5)
        
        # Highlight DG buses
        dg_nodes = [n for n in G.nodes() if n in env.dg_buses]
        nx.draw_networkx_nodes(G, pos, nodelist=dg_nodes, node_color='#00FF00',
                              node_size=150, ax=ax, edgecolors='black', linewidths=1.5)
        
        # Highlight substation
        nx.draw_networkx_nodes(G, pos, nodelist=[0], node_color='red',
                              node_size=200, ax=ax, edgecolors='black',
                              linewidths=2, node_shape='s')
        
        ax.set_title(title)
        
        # Legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='red', edgecolor='black', label='Substation'),
            Patch(facecolor='#00FF00', edgecolor='black', label='DG Bus'),
            Patch(facecolor='#87CEEB', edgecolor='black', label='Load Bus'),
        ]
        ax.legend(handles=legend_elements, loc='lower left')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close()
        print(f"Saved: {save_path}")
    except Exception as e:
        print(f"Could not plot network: {e}")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--results_dir', type=str, default='../results')
    parser.add_argument('--figures_dir', type=str, default='../figures')
    args = parser.parse_args()
    
    os.makedirs(args.figures_dir, exist_ok=True)
    
    # Plot training curves if histories exist
    for network in ['ieee33', 'ieee123']:
        paths = []
        labels = []
        for method in ['gcn_dqn', 'mlp_dqn']:
            p = os.path.join(args.results_dir, f'{method}_{network}', 'training_history.json')
            if os.path.exists(p):
                paths.append(p)
                labels.append(f'{method.upper()}')
        
        if paths:
            plot_training_curves(
                paths, labels,
                os.path.join(args.figures_dir, f'training_{network}.png'),
                title=f'Training Progress - {network.upper()}'
            )
    
    # Plot comparison if evaluation results exist
    eval_path = os.path.join(args.results_dir, 'evaluation_results.json')
    if os.path.exists(eval_path):
        with open(eval_path) as f:
            eval_results = json.load(f)
        
        for network, results in eval_results.get('comparison', {}).items():
            plot_comparison_bar(
                results,
                os.path.join(args.figures_dir, f'comparison_{network}.png'),
                title=f'Method Comparison - {network.upper()}'
            )
    
    # Plot network topology
    for network in ['ieee33', 'ieee123']:
        env = make_env(network_case=network, n_dgs=5, seed=42)
        plot_network_graph(
            env,
            os.path.join(args.figures_dir, f'topology_{network}.png'),
            title=f'{network.upper()} Network Topology'
        )
