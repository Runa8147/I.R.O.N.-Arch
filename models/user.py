class User:
    def __init__(self, x, y, user_id=None):
        self.user_id = user_id
        self.x = x
        self.y = y
        self.serving_ap = None  # Assigned during association logic
        self.traffic_demand = 0.0  # 0.0 to 1.0 (optional, used for advanced load modeling)
        self.assigned_slot = None # Assigned by TDMA scheduler
        self.sinr_history = []    # Track QoS over time

    def associate(self, ap):
        """Link this user to an Access Point"""
        self.serving_ap = ap

    def update_demand(self, demand):
        """Update traffic demand (0.0 to 1.0)"""
        self.traffic_demand = max(0.0, min(1.0, demand))

    def __repr__(self):
        ap_id = self.serving_ap.ap_id if self.serving_ap else "None"
        return f"User-{self.user_id}(x={self.x:.1f}, y={self.y:.1f}, AP={ap_id})"