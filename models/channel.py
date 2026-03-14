import numpy as np
from config import PATH_LOSS_EXPONENT, NOISE_FLOOR, AP_TRANSMIT_POWER

class ChannelModel:
    @staticmethod
    def path_loss(distance_m, exponent=PATH_LOSS_EXPONENT):
        """
        Simplified path loss: PL(d) = PL0 + 10*α*log10(d/d0)
        Returns received power in dBm given transmit power
        """
        if distance_m < 1.0:
            distance_m = 1.0  # Avoid log(0)
        pl_db = 10 * exponent * np.log10(distance_m)
        return AP_TRANSMIT_POWER - pl_db  # Received power in dBm
    
    @staticmethod
    def calculate_sinr(ap, user, interfering_aps):
        """
        Calculate SINR for user connected to ap
        SINR = Signal / (Interference + Noise)
        """
        # Signal from serving AP
        dist_signal = np.sqrt((ap.x - user.x)**2 + (ap.y - user.y)**2)
        signal_power_dbm = ChannelModel.path_loss(dist_signal)
        signal_power_lin = 10**(signal_power_dbm/10)  # Convert to mW
        
        # Interference from other APs on same channel
        interference_power_lin = 0
        for other_ap in interfering_aps:
            if other_ap.ap_id == ap.ap_id:
                continue
            if other_ap.channel != ap.channel:  # FDMA isolation
                continue
            dist_int = np.sqrt((other_ap.x - user.x)**2 + (other_ap.y - user.y)**2)
            int_power_dbm = ChannelModel.path_loss(dist_int)
            interference_power_lin += 10**(int_power_dbm/10)
        
        # Noise floor
        noise_power_lin = 10**(NOISE_FLOOR/10)
        
        # SINR in linear scale
        sinr_lin = signal_power_lin / (interference_power_lin + noise_power_lin)
        return 10 * np.log10(sinr_lin)  # Return in dB
    
    @staticmethod
    def shannon_capacity(sinr_db, bandwidth_mhz):
        """Theoretical max throughput via Shannon-Hartley"""
        sinr_lin = 10**(sinr_db/10)
        return bandwidth_mhz * np.log2(1 + sinr_lin)  # Mbps