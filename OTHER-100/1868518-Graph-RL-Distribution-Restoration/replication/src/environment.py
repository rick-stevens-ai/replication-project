# Suppress pandapower numba warnings before any pandapower import
import os
os.environ['NUMBA_DISABLE_JIT'] = '1'
import warnings
warnings.filterwarnings('ignore')
import logging
logging.disable(logging.WARNING)

# Monkey-patch pandapower to suppress numba check
import importlib
import sys
# Create a fake numba module
class _FakeNumba:
    __version__ = '0.0.0'
    def jit(self, *a, **kw):
        def decorator(func):
            return func
        if a and callable(a[0]):
            return a[0]
        return decorator
    def __getattr__(self, name):
        return lambda *a, **kw: None
sys.modules['numba'] = _FakeNumba()
sys.modules['numba.core'] = _FakeNumba()
sys.modules['numba.core.types'] = _FakeNumba()

"""
Distribution System Restoration Environment
============================================
Replication of Zhao & Wang (2021): "Learning Sequential Distribution System Restoration 
via Graph-Reinforcement Learning" (OSTI 1868518)

This module implements the power distribution system restoration environment using 
pandapower for power flow simulation. The environment models:
- IEEE 123-node and IEEE 8500-node test feeders
- Distributed generators (DGs) at specified buses
- Remotely controlled switches (sectionalizing + tie switches)
- Sequential restoration after a blackstart event
"""

import numpy as np
import pandapower as pp
import pandapower.networks as pn
import networkx as nx
from typing import Dict, List, Tuple, Optional
import copy
import warnings
warnings.filterwarnings('ignore')


class DistributionRestorationEnv:
    """
    Gym-like environment for distribution system restoration.
    
    The environment simulates a distribution network after a major outage (blackstart).
    Agents must sequentially operate switches and DGs to restore load while maintaining
    voltage and thermal constraints.
    
    State: Node features (voltage, load, generation) + edge features (switch status, flow)
    Actions: For each DG agent - which switch to operate or DG output to adjust
    Reward: Weighted combination of restored load, voltage violations, constraint violations
    """
    
    def __init__(self, network_case='ieee123', max_steps=30, 
                 n_dgs=5, fault_scenario='random', seed=None):
        """
        Args:
            network_case: 'ieee123' or 'ieee8500' or 'ieee33'
            max_steps: Maximum restoration steps per episode
            n_dgs: Number of distributed generators
            fault_scenario: 'random', 'fixed', or specific scenario dict
            seed: Random seed
        """
        self.network_case = network_case
        self.max_steps = max_steps
        self.n_dgs = n_dgs
        self.fault_scenario = fault_scenario
        self.rng = np.random.RandomState(seed)
        
        # Create base network
        self._create_network()
        
        # Setup DGs, switches, and loads
        self._setup_controllable_devices()
        
        # State/action dimensions
        self.n_buses = len(self.net.bus)
        self.n_switches = len(self.switch_indices)
        self.n_actions_per_agent = self.n_switches + 2  # switches + DG on/off + no-op
        
        # Episode tracking
        self.step_count = 0
        self.done = False
        self.total_load = 0.0
        self.restored_load = 0.0
        
    def _create_network(self):
        """Create the pandapower network for the specified test case."""
        if self.network_case == 'ieee123':
            self.net = self._create_ieee123()
        elif self.network_case == 'ieee8500':
            self.net = self._create_ieee8500()
        elif self.network_case == 'ieee33':
            self.net = self._create_ieee33()
        else:
            raise ValueError(f"Unknown network case: {self.network_case}")
        
        self.base_net = copy.deepcopy(self.net)
        
    def _create_ieee33(self):
        """Create IEEE 33-bus distribution test feeder with switches."""
        net = pn.case33bw()
        
        # Add tie switches (normally open) to create mesh options
        # Standard tie switches for IEEE 33-bus: (7,20), (8,14), (11,21), (17,32), (24,28)
        tie_pairs = [(7, 20), (8, 14), (11, 21), (17, 32), (24, 28)]
        for from_bus, to_bus in tie_pairs:
            if from_bus < len(net.bus) and to_bus < len(net.bus):
                new_line = pp.create_line(net, from_bus=from_bus, to_bus=to_bus,
                             length_km=1.0, std_type='NAYY 4x50 SE')
                pp.create_switch(net, bus=from_bus, element=new_line, 
                               et='l', closed=False, type='LBS')
        
        return net
    
    def _create_ieee123(self):
        """
        Create IEEE 123-node test feeder.
        Since pandapower doesn't have a native IEEE 123-bus case,
        we construct a representative 123-node radial distribution network.
        """
        net = pp.create_empty_network()
        
        # Create 123 buses
        for i in range(123):
            pp.create_bus(net, vn_kv=4.16, name=f'Bus_{i}')
        
        # External grid at bus 0 (substation)
        pp.create_ext_grid(net, bus=0, vm_pu=1.0)
        
        # Create main feeder topology (radial with laterals)
        # Main feeder: 0-1-2-...-17 (main trunk)
        main_trunk = list(range(18))
        for i in range(len(main_trunk) - 1):
            pp.create_line(net, from_bus=main_trunk[i], to_bus=main_trunk[i+1],
                         length_km=0.3 + self.rng.uniform(0, 0.2),
                         std_type='NAYY 4x150 SE')
        
        # Laterals branching off main trunk
        lateral_starts = [3, 5, 7, 9, 11, 13, 15, 17]
        bus_idx = 18
        for ls in lateral_starts:
            n_lateral = self.rng.randint(8, 16)
            prev_bus = ls
            for j in range(n_lateral):
                if bus_idx >= 123:
                    break
                pp.create_line(net, from_bus=prev_bus, to_bus=bus_idx,
                             length_km=0.2 + self.rng.uniform(0, 0.3),
                             std_type='NAYY 4x150 SE')
                prev_bus = bus_idx
                bus_idx += 1
                
                # Sub-laterals
                if self.rng.random() < 0.3 and bus_idx < 123:
                    pp.create_line(net, from_bus=prev_bus, to_bus=bus_idx,
                                 length_km=0.15 + self.rng.uniform(0, 0.15),
                                 std_type='NAYY 4x150 SE')
                    bus_idx += 1
        
        # Fill remaining buses
        while bus_idx < 123:
            parent = self.rng.randint(1, bus_idx)
            pp.create_line(net, from_bus=parent, to_bus=bus_idx,
                         length_km=0.2 + self.rng.uniform(0, 0.3),
                         std_type='NAYY 4x150 SE')
            bus_idx += 1
        
        # Add loads to most buses (skip substation)
        for i in range(1, 123):
            if self.rng.random() < 0.85:  # 85% of buses have loads
                pp.create_load(net, bus=i, 
                             p_mw=0.01 + self.rng.exponential(0.04),
                             q_mvar=0.005 + self.rng.exponential(0.02))
        
        # Add sectionalizing switches on some lines
        switch_lines = self.rng.choice(len(net.line), 
                                        size=min(20, len(net.line)//3), 
                                        replace=False)
        for sl in switch_lines:
            pp.create_switch(net, bus=net.line.at[sl, 'from_bus'], 
                           element=sl, et='l', closed=True, type='LBS')
        
        # Add tie switches (normally open)
        n_ties = 8
        all_buses = list(range(1, 123))
        for _ in range(n_ties):
            b1, b2 = self.rng.choice(all_buses, size=2, replace=False)
            new_line = pp.create_line(net, from_bus=b1, to_bus=b2,
                                    length_km=0.5 + self.rng.uniform(0, 0.5),
                                    std_type='NAYY 4x150 SE')
            pp.create_switch(net, bus=b1, element=new_line, 
                           et='l', closed=False, type='LBS')
        
        return net
    
    def _create_ieee8500(self):
        """
        Create a representative large-scale distribution network (8500-node scale).
        We use a scalable approach building from smaller feeders.
        """
        # For computational feasibility, we create a 500-bus representative network
        # that captures the key characteristics of the 8500-node system
        net = pp.create_empty_network()
        
        n_buses = 500  # Scaled version
        for i in range(n_buses):
            pp.create_bus(net, vn_kv=12.47, name=f'Bus_{i}')
        
        pp.create_ext_grid(net, bus=0, vm_pu=1.0)
        
        # Build tree topology with multiple feeders
        n_feeders = 5
        buses_per_feeder = (n_buses - 1) // n_feeders
        
        bus_idx = 1
        for f in range(n_feeders):
            feeder_root = bus_idx
            pp.create_line(net, from_bus=0, to_bus=feeder_root,
                         length_km=1.0, std_type='NAYY 4x150 SE')
            prev = feeder_root
            bus_idx += 1
            
            for j in range(buses_per_feeder - 1):
                if bus_idx >= n_buses:
                    break
                if self.rng.random() < 0.7:
                    parent = prev
                else:
                    parent = self.rng.randint(feeder_root, bus_idx)
                pp.create_line(net, from_bus=parent, to_bus=bus_idx,
                             length_km=0.1 + self.rng.exponential(0.3),
                             std_type='NAYY 4x150 SE')
                prev = bus_idx
                bus_idx += 1
        
        # Fill remaining
        while bus_idx < n_buses:
            parent = self.rng.randint(1, bus_idx)
            pp.create_line(net, from_bus=parent, to_bus=bus_idx,
                         length_km=0.2 + self.rng.uniform(0, 0.3),
                         std_type='NAYY 4x150 SE')
            bus_idx += 1
        
        # Add loads
        for i in range(1, n_buses):
            if self.rng.random() < 0.8:
                pp.create_load(net, bus=i,
                             p_mw=0.005 + self.rng.exponential(0.02),
                             q_mvar=0.002 + self.rng.exponential(0.01))
        
        # Switches
        n_switches = min(50, len(net.line) // 4)
        switch_lines = self.rng.choice(len(net.line), size=n_switches, replace=False)
        for sl in switch_lines:
            pp.create_switch(net, bus=net.line.at[sl, 'from_bus'],
                           element=sl, et='l', closed=True, type='LBS')
        
        # Tie switches
        for _ in range(15):
            b1, b2 = self.rng.choice(list(range(1, n_buses)), size=2, replace=False)
            new_line = pp.create_line(net, from_bus=b1, to_bus=b2,
                                    length_km=0.5 + self.rng.uniform(0, 1.0),
                                    std_type='NAYY 4x150 SE')
            pp.create_switch(net, bus=b1, element=new_line,
                           et='l', closed=False, type='LBS')
        
        return net
    
    def _setup_controllable_devices(self):
        """Setup DGs and identify controllable switches."""
        # Identify switches
        if len(self.net.switch) > 0:
            self.switch_indices = list(self.net.switch.index)
        else:
            self.switch_indices = []
        
        # Place DGs at strategic locations
        n_buses = len(self.net.bus)
        # Place DGs at roughly evenly spaced buses (avoiding substation)
        dg_buses = np.linspace(n_buses // (self.n_dgs + 1), 
                               n_buses - 1, self.n_dgs, dtype=int)
        
        self.dg_indices = []
        self.dg_buses = []
        for bus in dg_buses:
            bus = int(bus)
            if bus >= n_buses:
                bus = n_buses - 1
            idx = pp.create_sgen(self.net, bus=bus,
                                p_mw=0.1 + self.rng.uniform(0, 0.2),
                                q_mvar=0.05 + self.rng.uniform(0, 0.1),
                                in_service=False)
            self.dg_indices.append(idx)
            self.dg_buses.append(bus)
        
        self.base_net = copy.deepcopy(self.net)
        
    def _generate_fault_scenario(self):
        """Generate a random fault scenario (lines out of service)."""
        n_lines = len(self.net.line)
        if self.fault_scenario == 'random':
            # Random number of faulted lines (10-30% of network)
            n_faults = self.rng.randint(max(1, n_lines // 10), 
                                         max(2, n_lines // 3))
            self.faulted_lines = sorted(self.rng.choice(n_lines, size=n_faults, 
                                                          replace=False))
        elif self.fault_scenario == 'fixed':
            # Fixed scenario for reproducibility
            n_faults = max(1, n_lines // 5)
            self.faulted_lines = list(range(0, n_faults))
        elif isinstance(self.fault_scenario, dict):
            self.faulted_lines = self.fault_scenario.get('faulted_lines', [])
        else:
            self.faulted_lines = []
    
    def reset(self) -> Dict:
        """
        Reset environment for new episode.
        Returns initial state dictionary.
        """
        # Restore base network
        self.net = copy.deepcopy(self.base_net)
        
        # Generate fault scenario
        self._generate_fault_scenario()
        
        # Apply faults: open switches on faulted lines, disable lines
        for line_idx in self.faulted_lines:
            if line_idx < len(self.net.line):
                self.net.line.at[line_idx, 'in_service'] = False
        
        # Start with all DGs off and all controllable switches in initial state
        for dg_idx in self.dg_indices:
            self.net.sgen.at[dg_idx, 'in_service'] = False
        
        # Close sectionalizing switches, open tie switches
        for sw_idx in self.switch_indices:
            if self.net.switch.at[sw_idx, 'type'] == 'LBS':
                # Check if this is a tie switch (normally open)
                self.net.switch.at[sw_idx, 'closed'] = self.net.switch.at[sw_idx, 'closed']
        
        self.step_count = 0
        self.done = False
        
        # Calculate total possible load
        self.total_load = self.net.load.p_mw.sum()
        
        # Run initial power flow
        self._run_power_flow()
        
        return self._get_state()
    
    def _run_power_flow(self):
        """Run pandapower power flow with error handling."""
        try:
            pp.runpp(self.net, algorithm='nr', max_iteration=30, 
                    init='flat', enforce_q_lims=False, 
                    calculate_voltage_angles=True)
            self.pf_converged = True
        except pp.powerflow.LoadflowNotConverged:
            self.pf_converged = False
        except Exception:
            self.pf_converged = False
    
    def _get_state(self) -> Dict:
        """
        Get current state representation.
        
        Returns dict with:
            - node_features: (n_buses, n_node_features) array
            - edge_index: (2, n_edges) connectivity
            - edge_features: (n_edges, n_edge_features) array
            - global_features: global state vector
            - adjacency: adjacency matrix
        """
        n_buses = len(self.net.bus)
        
        # Node features: [voltage_pu, voltage_angle, active_load, reactive_load, 
        #                  has_dg, dg_active, dg_p, is_slack]
        node_features = np.zeros((n_buses, 8), dtype=np.float32)
        
        if self.pf_converged and len(self.net.res_bus) > 0:
            for i in range(n_buses):
                if i in self.net.res_bus.index:
                    node_features[i, 0] = self.net.res_bus.at[i, 'vm_pu']
                    node_features[i, 1] = self.net.res_bus.at[i, 'va_degree'] / 180.0
                else:
                    node_features[i, 0] = 0.0
                    node_features[i, 1] = 0.0
        else:
            node_features[:, 0] = 1.0  # Assume nominal voltage
        
        # Load information
        for idx in self.net.load.index:
            bus = self.net.load.at[idx, 'bus']
            if bus < n_buses:
                node_features[bus, 2] = self.net.load.at[idx, 'p_mw']
                node_features[bus, 3] = self.net.load.at[idx, 'q_mvar']
        
        # DG information
        for i, dg_idx in enumerate(self.dg_indices):
            bus = self.dg_buses[i]
            if bus < n_buses:
                node_features[bus, 4] = 1.0  # has DG
                node_features[bus, 5] = float(self.net.sgen.at[dg_idx, 'in_service'])
                node_features[bus, 6] = self.net.sgen.at[dg_idx, 'p_mw']
        
        # Slack bus
        for idx in self.net.ext_grid.index:
            bus = self.net.ext_grid.at[idx, 'bus']
            if bus < n_buses:
                node_features[bus, 7] = 1.0
        
        # Edge index and features
        edge_list = []
        edge_features_list = []
        
        for idx in self.net.line.index:
            if self.net.line.at[idx, 'in_service']:
                from_bus = self.net.line.at[idx, 'from_bus']
                to_bus = self.net.line.at[idx, 'to_bus']
                edge_list.append([from_bus, to_bus])
                edge_list.append([to_bus, from_bus])  # Undirected
                
                # Edge features: [in_service, loading_pct, p_flow, q_flow]
                feat = np.zeros(4, dtype=np.float32)
                feat[0] = 1.0
                if self.pf_converged and idx in self.net.res_line.index:
                    feat[1] = self.net.res_line.at[idx, 'loading_percent'] / 100.0
                    feat[2] = self.net.res_line.at[idx, 'p_from_mw']
                    feat[3] = self.net.res_line.at[idx, 'q_from_mvar']
                edge_features_list.append(feat)
                edge_features_list.append(feat)  # Same for reverse edge
        
        if len(edge_list) > 0:
            edge_index = np.array(edge_list, dtype=np.int64).T
            edge_features = np.array(edge_features_list, dtype=np.float32)
        else:
            edge_index = np.zeros((2, 0), dtype=np.int64)
            edge_features = np.zeros((0, 4), dtype=np.float32)
        
        # Build adjacency matrix
        adjacency = np.zeros((n_buses, n_buses), dtype=np.float32)
        for idx in self.net.line.index:
            if self.net.line.at[idx, 'in_service']:
                f = self.net.line.at[idx, 'from_bus']
                t = self.net.line.at[idx, 'to_bus']
                adjacency[f, t] = 1.0
                adjacency[t, f] = 1.0
        # Add self-loops
        np.fill_diagonal(adjacency, 1.0)
        
        # Global features
        global_features = np.array([
            self.step_count / self.max_steps,
            self.restored_load / max(self.total_load, 1e-6),
            float(self.pf_converged),
            len(self.faulted_lines) / max(len(self.net.line), 1),
            sum(1 for i in self.dg_indices if self.net.sgen.at[i, 'in_service']) / max(self.n_dgs, 1)
        ], dtype=np.float32)
        
        # Switch states
        switch_states = np.zeros(len(self.switch_indices), dtype=np.float32)
        for i, sw_idx in enumerate(self.switch_indices):
            switch_states[i] = float(self.net.switch.at[sw_idx, 'closed'])
        
        return {
            'node_features': node_features,
            'edge_index': edge_index,
            'edge_features': edge_features,
            'adjacency': adjacency,
            'global_features': global_features,
            'switch_states': switch_states,
            'n_buses': n_buses
        }
    
    def step(self, actions: Dict[int, int]) -> Tuple[Dict, float, bool, Dict]:
        """
        Execute one restoration step.
        
        Args:
            actions: Dict mapping agent_id (DG index) to action index
                     Action space per agent:
                       0 to n_switches-1: toggle switch i
                       n_switches: toggle own DG
                       n_switches+1: no-op
        
        Returns:
            state, reward, done, info
        """
        self.step_count += 1
        info = {'violations': [], 'actions_taken': []}
        
        # Execute actions for each agent
        for agent_id, action in actions.items():
            if action < self.n_switches:
                # Toggle switch
                sw_idx = self.switch_indices[action]
                current = self.net.switch.at[sw_idx, 'closed']
                self.net.switch.at[sw_idx, 'closed'] = not current
                info['actions_taken'].append(
                    f"Agent {agent_id}: Toggle switch {sw_idx} -> {'closed' if not current else 'open'}")
            elif action == self.n_switches:
                # Toggle DG
                dg_idx = self.dg_indices[agent_id]
                current = self.net.sgen.at[dg_idx, 'in_service']
                self.net.sgen.at[dg_idx, 'in_service'] = not current
                info['actions_taken'].append(
                    f"Agent {agent_id}: Toggle DG {dg_idx} -> {'on' if not current else 'off'}")
            else:
                # No-op
                info['actions_taken'].append(f"Agent {agent_id}: No-op")
        
        # Run power flow
        self._run_power_flow()
        
        # Calculate reward
        reward, reward_info = self._calculate_reward()
        info.update(reward_info)
        
        # Check termination
        if self.step_count >= self.max_steps:
            self.done = True
        
        state = self._get_state()
        
        return state, reward, self.done, info
    
    def _calculate_reward(self) -> Tuple[float, Dict]:
        """
        Calculate restoration reward.
        
        Reward = w1 * load_restored_ratio + w2 * voltage_quality - w3 * violations
        
        Following the paper's approach: maximize load restoration while maintaining
        voltage within [0.95, 1.05] pu and line loading within limits.
        """
        info = {}
        
        if not self.pf_converged:
            info['pf_converged'] = False
            info['restored_load_ratio'] = 0.0
            info['voltage_violations'] = 1.0
            info['thermal_violations'] = 1.0
            return -1.0, info  # Heavy penalty for non-convergence
        
        # Load restoration ratio
        total_load_served = 0.0
        if len(self.net.res_load) > 0:
            total_load_served = self.net.res_load.p_mw.sum()
        
        self.restored_load = max(0, total_load_served)
        load_ratio = self.restored_load / max(self.total_load, 1e-6)
        load_ratio = np.clip(load_ratio, 0, 1)
        
        # Voltage quality
        voltage_violations = 0.0
        n_energized = 0
        if len(self.net.res_bus) > 0:
            for idx in self.net.res_bus.index:
                vm = self.net.res_bus.at[idx, 'vm_pu']
                if vm > 0:
                    n_energized += 1
                    if vm < 0.95:
                        voltage_violations += (0.95 - vm) ** 2
                    elif vm > 1.05:
                        voltage_violations += (vm - 1.05) ** 2
        
        voltage_quality = 1.0 - min(voltage_violations * 10, 1.0)
        
        # Thermal violations
        thermal_violations = 0.0
        if len(self.net.res_line) > 0:
            for idx in self.net.res_line.index:
                loading = self.net.res_line.at[idx, 'loading_percent']
                if loading > 100:
                    thermal_violations += (loading - 100) / 100.0
        
        thermal_quality = 1.0 - min(thermal_violations * 0.5, 1.0)
        
        # Combined reward (paper uses weighted combination)
        w_load = 0.6
        w_voltage = 0.25
        w_thermal = 0.15
        
        reward = (w_load * load_ratio + 
                  w_voltage * voltage_quality + 
                  w_thermal * thermal_quality)
        
        # Bonus for significant load increase
        if load_ratio > 0.8:
            reward += 0.1
        if load_ratio > 0.95:
            reward += 0.2
        
        info['pf_converged'] = True
        info['restored_load_ratio'] = load_ratio
        info['voltage_quality'] = voltage_quality
        info['thermal_quality'] = thermal_quality
        info['voltage_violations'] = voltage_violations
        info['thermal_violations'] = thermal_violations
        info['n_energized_buses'] = n_energized
        info['reward_breakdown'] = {
            'load': w_load * load_ratio,
            'voltage': w_voltage * voltage_quality,
            'thermal': w_thermal * thermal_quality
        }
        
        return reward, info
    
    def get_graph(self):
        """Get networkx graph representation of current network state."""
        G = nx.Graph()
        for idx in self.net.bus.index:
            G.add_node(idx)
        for idx in self.net.line.index:
            if self.net.line.at[idx, 'in_service']:
                G.add_edge(self.net.line.at[idx, 'from_bus'],
                          self.net.line.at[idx, 'to_bus'])
        return G
    
    def get_action_mask(self, agent_id: int) -> np.ndarray:
        """Get valid action mask for an agent."""
        mask = np.ones(self.n_actions_per_agent, dtype=np.float32)
        # All actions are valid (switches can be toggled, DG can be toggled, no-op always valid)
        return mask
    
    def render(self):
        """Print current state summary."""
        print(f"\n=== Step {self.step_count}/{self.max_steps} ===")
        print(f"Power flow converged: {self.pf_converged}")
        print(f"Total load: {self.total_load:.4f} MW")
        print(f"Restored load: {self.restored_load:.4f} MW " 
              f"({self.restored_load/max(self.total_load,1e-6)*100:.1f}%)")
        print(f"Faulted lines: {len(self.faulted_lines)}")
        
        n_dgs_on = sum(1 for i in self.dg_indices 
                       if self.net.sgen.at[i, 'in_service'])
        print(f"DGs active: {n_dgs_on}/{self.n_dgs}")
        
        n_closed = sum(1 for sw in self.switch_indices 
                       if self.net.switch.at[sw, 'closed'])
        print(f"Switches closed: {n_closed}/{len(self.switch_indices)}")


def make_env(network_case='ieee123', **kwargs):
    """Factory function for creating environments."""
    return DistributionRestorationEnv(network_case=network_case, **kwargs)
