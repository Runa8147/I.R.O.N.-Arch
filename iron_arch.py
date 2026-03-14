#!/usr/bin/env python3
"""
IRON Arch: Interference-Reduced Optimized Network Architecture with DVFS
Main simulation driver
"""
import numpy as np
import json
from config import *
from models.access_point import AccessPoint
from models.user import User
from models.channel import ChannelModel
from models.scheduler import TDMAScheduler
from utils.clustering import cluster_access_points, assign_frequencies_to_clusters, get_interfering_aps
from utils.visualizer import plot_topology, plot_energy_comparison, plot_sinr_cdf
from utils.metrics import compute_network_metrics

def generate_topology():
    """Create random AP and user placements"""
    np.random.seed(RANDOM_SEED)
    
    aps = [AccessPoint(i, 
                      np.random.uniform(0, AREA_SIZE), 
                      np.random.uniform(0, AREA_SIZE)) 
           for i in range(NUM_APS)]
    
    users = [User(np.random.uniform(0, AREA_SIZE),
                  np.random.uniform(0, AREA_SIZE)) 
             for _ in range(NUM_USERS)]
    
    # Simple association: user connects to nearest AP
    for user in users:
        min_dist = float('inf')
        nearest_ap = None
        for ap in aps:
            dist = np.sqrt((user.x - ap.x)**2 + (user.y - ap.y)**2)
            if dist < min_dist:
                min_dist = dist
                nearest_ap = ap
        user.serving_ap = nearest_ap
    
    return aps, users

def run_iron_arch_simulation():
    """Main simulation loop for IRON Arch"""
    print("🚀 Starting IRON Arch Simulation...")
    
    # 1. Generate topology
    aps, users = generate_topology()
    
    # 2. Apply IRON Arch: Clustering + FDMA assignment
    cluster_access_points(aps)
    assign_frequencies_to_clusters(aps)
    
    # 3. Initialize scheduler
    scheduler = TDMAScheduler()
    scheduler.allocate_slots(users, aps)
    
    # 4. Simulation state tracking
    iron_energy = []
    traditional_energy = []
    sinr_iron = []
    sinr_traditional = []
    
    # 5. Time-stepped simulation
    for t in range(TIME_STEPS):
        # Update traffic loads (random walk with inertia)
        for ap in aps:
            # Load evolves with some temporal correlation
            new_load = np.clip(ap.traffic_load + np.random.normal(0, 0.1), 0, 1)
            ap.update_load(new_load)
        
        # === IRON ARCH MODEL ===
        total_energy_iron = 0
        for ap in aps:
            # DVFS-adjusted energy consumption
            energy = ap.step_energy()
            total_energy_iron += energy
            
            # Calculate SINR for associated users (only in their assigned slot)
            interfering = get_interfering_aps(ap, aps)
            for user in users:
                if user.serving_ap == ap:
                    sinr = ChannelModel.calculate_sinr(ap, user, interfering)
                    sinr_iron.append(sinr)
        
        iron_energy.append(total_energy_iron)
        
        # === TRADITIONAL MODEL (Baseline) ===
        total_energy_trad = 0
        for ap in aps:
            # No DVFS: always at max voltage/frequency
            load = ap.traffic_load  # Same traffic pattern
            power = 5.0 * load  # Simplified: fixed max power * load
            total_energy_trad += power
            
            # No clustering: all APs on same channel → more interference
            for user in users:
                if user.serving_ap == ap:
                    # All other APs interfere
                    all_other_aps = [a for a in aps if a.ap_id != ap.ap_id]
                    sinr = ChannelModel.calculate_sinr(ap, user, all_other_aps)
                    sinr_traditional.append(sinr)
        
        traditional_energy.append(total_energy_trad)
    
    # 6. Generate visualizations
    print("📊 Generating plots...")
    plot_topology(aps, users)
    plot_energy_comparison(iron_energy, traditional_energy)
    plot_sinr_cdf(sinr_iron, sinr_traditional)
    
    # 7. Compute summary metrics
    metrics = compute_network_metrics(iron_energy, traditional_energy, sinr_iron, sinr_traditional)
    
    # 8. Save results to JSON
    with open("results/metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)
    
    print("✅ Simulation complete! Check results/ folder")
    print(f"📈 Key Result: {metrics['energy_savings_percent']:.1f}% energy savings")
    
    return metrics

if __name__ == "__main__":
    run_iron_arch_simulation()