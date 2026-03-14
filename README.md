# IRON Arch

**Energy-Efficient Resource Allocation for Dense Wireless Networks**

A simulation framework for optimizing **Wi-Fi access point coordination** in dense environments using clustering, intelligent channel allocation, and dynamic power scaling.

---

# Overview

Dense Wi-Fi deployments (stadiums, campuses, malls) often suffer from:

* Co-channel interference between nearby Access Points (APs)
* Inefficient power usage
* Reduced signal quality for users

**IRON Arch** simulates a network architecture that improves efficiency by combining:

* **Geographic clustering of APs**
* **Frequency channel coordination**
* **Dynamic power scaling based on load**

The goal is to **reduce interference and energy consumption while maintaining reliable signal quality.**

---

# System Architecture

```
                +----------------------+
                |   Access Point Data  |
                |  (Location, Load)    |
                +----------+-----------+
                           |
                           v
                 +-------------------+
                 |   AP Clustering   |
                 |     (K-Means)     |
                 +---------+---------+
                           |
                           v
                +----------------------+
                |  Channel Assignment  |
                |  (Frequency Reuse)   |
                +----------+-----------+
                           |
                           v
                +----------------------+
                |   DVFS Controller    |
                | (Adaptive Power Use) |
                +----------+-----------+
                           |
                           v
                +----------------------+
                |   Network Analysis   |
                |  SINR & Energy Use   |
                +----------+-----------+
                           |
                           v
                    +-----------+
                    |  Results  |
                    | Visuals + |
                    |  Metrics  |
                    +-----------+
```

---

# Methodology

## 1. Access Point Clustering

APs are grouped geographically using **K-Means clustering**.

**Input**

* AP coordinates

**Output**

* Cluster assignment for each AP

This helps coordinate channel usage and reduce interference.

---

## 2. Channel Assignment

Each cluster is assigned a frequency channel.

Example Wi-Fi channels used:

| Channel | Frequency |
| ------- | --------- |
| 1       | 2.412 GHz |
| 6       | 2.437 GHz |
| 11      | 2.462 GHz |

Nearby clusters use **different channels**, while distant clusters can **reuse channels**.

---

## 3. Dynamic Voltage and Frequency Scaling (DVFS)

AP power consumption adapts based on load.

Power model:

```
P ∝ V² × f × load
```

| Network Load | Voltage | Frequency | Relative Power |
| ------------ | ------- | --------- | -------------- |
| Low          | 0.9V    | 1.2 GHz   | Low            |
| Medium       | 1.0V    | 1.8 GHz   | Moderate       |
| High         | 1.2V    | 2.4 GHz   | High           |

This reduces energy usage when traffic is low.

---

## 4. Signal Quality Calculation

Signal quality is measured using **SINR (Signal-to-Interference-plus-Noise Ratio)**.

Model parameters:

* Path loss exponent: **2.7**
* Noise floor: **−95 dBm**
* AP transmit power: **20 dBm**

Interference is calculated from **APs operating on the same channel**.

---

# Project Structure

```
IRON_ARC/
│
├── models/
│   ├── access_point.py
│   ├── channel.py
│   ├── scheduler.py
│   └── user.py
│
├── utils/
│   ├── clustering.py
│   ├── metrics.py
│   └── visualizer.py
│
├── results/
│   ├── topology_plot.png
│   ├── energy_comparison.png
│   ├── sinr_cdf.png
│   └── metrics.json
│
├── config.py
├── iron_arch.py
└── requirements.txt
```

# Installation

```bash
git clone https://github.com/Runa8147/I.R.O.N.-Arch.git
cd IRON_ARC

pip install -r requirements.txt
```

---

# Run Simulation

```bash
python iron_arch.py
```

Results will be saved in the **results/** directory.

---


# Results

Running the simulation generates visualizations and metrics.

### Network Topology

```
results/topology_plot.png
```

Shows AP distribution and clustering.

---

### Energy Consumption Comparison

```
results/energy_comparison.png
```

Compares baseline power usage vs optimized allocation.

---

### SINR Distribution

```
results/sinr_cdf.png
```

Shows signal reliability across users.

---

