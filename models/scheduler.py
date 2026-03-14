import numpy as np
from config import SLOTS_PER_CLUSTER

class TDMAScheduler:
    def __init__(self, slots_per_cluster=SLOTS_PER_CLUSTER):
        self.slots_per_cluster = slots_per_cluster
        self.slot_assignments = {}  # {cluster_id: {slot: [user_ids]}}
        
    def allocate_slots(self, users, aps):
        """
        Simple round-robin slot allocation within each cluster
        In real system: could use proportional fairness, QoS weights, etc.
        """
        # Group users by serving AP cluster
        cluster_users = {}
        for user in users:
            if user.serving_ap and user.serving_ap.cluster_id is not None:
                cid = user.serving_ap.cluster_id
                if cid not in cluster_users:
                    cluster_users[cid] = []
                cluster_users[cid].append(user)
        
        # Allocate slots per cluster
        for cluster_id, users_in_cluster in cluster_users.items():
            self.slot_assignments[cluster_id] = {}
            for slot in range(self.slots_per_cluster):
                # Round-robin: assign users to slots
                assigned_users = [u for i, u in enumerate(users_in_cluster) if i % self.slots_per_cluster == slot]
                self.slot_assignments[cluster_id][slot] = assigned_users
                
    def get_user_slot(self, user):
        """Return which TDMA slot a user is assigned to"""
        if not user.serving_ap or user.serving_ap.cluster_id is None:
            return None
        cid = user.serving_ap.cluster_id
        if cid not in self.slot_assignments:
            return None
        for slot, users in self.slot_assignments[cid].items():
            if user in users:
                return slot
        return None