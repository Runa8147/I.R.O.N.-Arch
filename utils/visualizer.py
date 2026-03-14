import matplotlib.pyplot as plt
import numpy as np
from config import AREA_SIZE

def plot_topology(aps, users, save_path="results/topology_plot.png"):
    """Scatter plot of APs colored by cluster, users in gray"""
    plt.figure(figsize=(10, 8))
    
    # Plot users
    user_x = [u.x for u in users]
    user_y = [u.y for u in users]
    plt.scatter(user_x, user_y, c='gray', s=10, alpha=0.3, label='Users', zorder=1)
    
    # Plot APs colored by cluster (FIXED: collect all clusters first)
    ap_x = [ap.x for ap in aps]
    ap_y = [ap.y for ap in aps]
    ap_clusters = [ap.cluster_id for ap in aps]
    
    scatter = plt.scatter(ap_x, ap_y, c=ap_clusters, cmap='viridis', 
                         s=150, edgecolors='black', marker='^', zorder=2)
    
    plt.xlabel("X Position (m)")
    plt.ylabel("Y Position (m)")
    plt.title(f"IRON Arch: AP Clustering ({len(aps)} APs, {len(users)} Users)")
    plt.colorbar(scatter, label="Cluster ID")
    plt.grid(alpha=0.3)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved topology plot: {save_path}")

def plot_energy_comparison(iron_energy, traditional_energy, save_path="results/energy_comparison.png"):
    """Line plot: Energy consumption over simulation time"""
    time_steps = range(len(iron_energy))
    
    plt.figure(figsize=(10, 6))
    plt.plot(time_steps, iron_energy, label='IRON Arch (DVFS + Clustering)', 
             color='#2ecc71', linewidth=2.5)
    plt.plot(time_steps, traditional_energy, label='Traditional WiFi (Always-On)', 
             color='#e74c3c', linewidth=2.5, linestyle='--')
    
    plt.xlabel("Simulation Time Step")
    plt.ylabel("Cumulative Energy (Joules)")
    plt.title("Energy Efficiency: IRON Arch vs. Traditional Architecture")
    plt.legend()
    plt.grid(alpha=0.3)
    
    # Add annotation for savings
    if len(iron_energy) > 0 and traditional_energy[-1] > 0:
        savings = (1 - iron_energy[-1]/traditional_energy[-1]) * 100
        plt.annotate(f'{savings:.1f}% Energy Savings', 
                    xy=(0.95, 0.05), xycoords='axes fraction',
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
                    fontsize=10)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved energy comparison: {save_path}")

def plot_sinr_cdf(sinr_iron, sinr_traditional, save_path="results/sinr_cdf.png"):
    """CDF plot of SINR values (key QoS metric)"""
    sinr_iron_sorted = np.sort(sinr_iron)
    sinr_trad_sorted = np.sort(sinr_traditional)
    cdf_iron = np.arange(1, len(sinr_iron_sorted)+1) / len(sinr_iron_sorted)
    cdf_trad = np.arange(1, len(sinr_trad_sorted)+1) / len(sinr_trad_sorted)
    
    plt.figure(figsize=(10, 6))
    plt.plot(sinr_iron_sorted, cdf_iron, label='IRON Arch', color='#2ecc71', linewidth=2.5)
    plt.plot(sinr_trad_sorted, cdf_trad, label='Traditional WiFi', color='#e74c3c', linewidth=2.5, linestyle='--')
    
    plt.xlabel("SINR (dB)")
    plt.ylabel("Cumulative Probability")
    plt.title("SINR Distribution: Reliability Comparison")
    plt.legend()
    plt.grid(alpha=0.3)
    
    # Mark typical threshold (e.g., 10 dB for good throughput)
    plt.axvline(x=10, color='blue', linestyle=':', alpha=0.5, label='Quality Threshold (10 dB)')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved SINR CDF: {save_path}")