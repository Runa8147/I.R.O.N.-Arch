# Network Topology
NUM_APS = 30
NUM_USERS = 150
AREA_SIZE = 1000  # meters (e.g., stadium footprint)
AP_TRANSMIT_POWER = 20  # dBm
USER_SENSITIVITY = -82  # dBm

# Channel Model
PATH_LOSS_EXPONENT = 2.7  # Indoor stadium environment
NOISE_FLOOR = -95  # dBm
BANDWIDTH_MHZ = 20

# DVFS Parameters (Voltage in V, Frequency in GHz)
DVFS_MODES = [
    {"name": "low", "voltage": 0.9, "frequency": 1.2, "min_load": 0.0},
    {"name": "mid", "voltage": 1.0, "frequency": 1.8, "min_load": 0.3},
    {"name": "high", "voltage": 1.2, "frequency": 2.4, "min_load": 0.7}
]

# IRON Arch Parameters
NUM_CLUSTERS = 5  # K for K-Means
SLOTS_PER_CLUSTER = 10  # TDMA slots
FREQUENCY_CHANNELS = [2.412, 2.437, 2.462]  # 3 orthogonal 2.4GHz channels

# Simulation
TIME_STEPS = 200
RANDOM_SEED = 42