import numpy as np
from config import DVFS_MODES

class AccessPoint:
    def __init__(self, ap_id, x, y, channel=None):
        self.ap_id = ap_id
        self.x = x
        self.y = y
        self.channel = channel  # Assigned FDMA channel
        self.cluster_id = None  # Assigned by K-Means
        
        # DVFS state
        self.current_dvfs_mode = DVFS_MODES[-1]  # Start at high performance
        self.voltage = self.current_dvfs_mode["voltage"]
        self.frequency = self.current_dvfs_mode["frequency"]
        
        # Traffic & Energy
        self.traffic_load = 0.0  # 0.0 to 1.0
        self.energy_history = []
        self.total_energy = 0.0
        
        # Physics constants
        self.base_power = 5.0  # Watts at max DVFS mode
        
    def update_load(self, new_load):
        """Update traffic load and trigger DVFS adjustment"""
        self.traffic_load = np.clip(new_load, 0.0, 1.0)
        self._apply_dvfs()
        
    def _apply_dvfs(self):
        """DVFS Logic: Select mode based on traffic load"""
        for mode in reversed(DVFS_MODES):  # Check high→low
            if self.traffic_load >= mode["min_load"]:
                self.current_dvfs_mode = mode
                break
        self.voltage = self.current_dvfs_mode["voltage"]
        self.frequency = self.current_dvfs_mode["frequency"]
    
    def compute_instantaneous_power(self):
        """
        Power model: P = P_base * (V/V_max)^2 * (f/f_max) * load
        Based on CMOS dynamic power: P ∝ CV²f
        """
        v_ratio = self.voltage / DVFS_MODES[-1]["voltage"]
        f_ratio = self.frequency / DVFS_MODES[-1]["frequency"]
        return self.base_power * (v_ratio ** 2) * f_ratio * max(self.traffic_load, 0.1)
    
    def step_energy(self, delta_t=1.0):
        """Accumulate energy for this time step"""
        power = self.compute_instantaneous_power()
        energy = power * delta_t  # Joules
        self.total_energy += energy
        self.energy_history.append(self.total_energy)
        return energy
    
    def __repr__(self):
        return f"AP-{self.ap_id}(cluster={self.cluster_id}, ch={self.channel}, load={self.traffic_load:.2f})"