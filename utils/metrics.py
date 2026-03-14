import numpy as np

def compute_network_metrics(iron_energy, trad_energy, sinr_iron, sinr_trad):
    """Compute key performance indicators"""
    results = {}
    
    # Energy metrics
    final_iron = iron_energy[-1] if iron_energy else 0
    final_trad = trad_energy[-1] if trad_energy else 0
    results['energy_savings_joules'] = final_trad - final_iron
    results['energy_savings_percent'] = (1 - final_iron/final_trad) * 100 if final_trad > 0 else 0
    
    # SINR metrics
    results['sinr_iron_mean_db'] = np.mean(sinr_iron) if sinr_iron else 0
    results['sinr_trad_mean_db'] = np.mean(sinr_trad) if sinr_trad else 0
    results['sinr_improvement_db'] = results['sinr_iron_mean_db'] - results['sinr_trad_mean_db']
    
    # Reliability: % of users above SINR threshold (e.g., 10 dB)
    threshold = 10.0
    results['iron_reliability_percent'] = np.mean([s >= threshold for s in sinr_iron]) * 100 if sinr_iron else 0
    results['trad_reliability_percent'] = np.mean([s >= threshold for s in sinr_trad]) * 100 if sinr_trad else 0
    
    return results