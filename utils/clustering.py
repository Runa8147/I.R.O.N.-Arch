import numpy as np
from sklearn.cluster import KMeans
from config import NUM_CLUSTERS, FREQUENCY_CHANNELS

def cluster_access_points(aps):
    """
    Group APs into clusters using K-Means on (x,y) coordinates
    Returns: list of cluster assignments
    """
    coordinates = np.array([[ap.x, ap.y] for ap in aps])
    kmeans = KMeans(n_clusters=NUM_CLUSTERS, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(coordinates)
    
    # Assign cluster_id to each AP
    for ap, cluster_id in zip(aps, cluster_labels):
        ap.cluster_id = cluster_id
    
    return cluster_labels

def assign_frequencies_to_clusters(aps):
    """
    Assign orthogonal FDMA channels to clusters
    Simple round-robin: cluster i gets channel i % num_channels
    """
    unique_clusters = sorted(set(ap.cluster_id for ap in aps if ap.cluster_id is not None))
    
    for cluster_id in unique_clusters:
        channel = FREQUENCY_CHANNELS[cluster_id % len(FREQUENCY_CHANNELS)]
        for ap in aps:
            if ap.cluster_id == cluster_id:
                ap.channel = channel
    
    return {cid: FREQUENCY_CHANNELS[cid % len(FREQUENCY_CHANNELS)] for cid in unique_clusters}

def get_interfering_aps(target_ap, all_aps):
    """Return APs that could interfere (same channel, different cluster)"""
    return [ap for ap in all_aps 
            if ap.channel == target_ap.channel 
            and ap.cluster_id != target_ap.cluster_id]