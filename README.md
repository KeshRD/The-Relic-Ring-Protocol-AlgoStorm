# Zeta-26: The Relic Ring Protocol

Organized by **IEEE Computer Society Student Branch Chapter - University of Kelaniya** for **LAUNCH26**.

## Executive Summary
This project implements a ruthlessly efficient network routing simulation to reconnect the fractured Zeta-26 star system using primitive, legacy infrastructure (underground fiber cables and laser transceivers). The system calculates exact latency based on physical parameters, dynamically translates payload dialects, and instantly routes around dead zones.

---

## Technical Implementation Details

### 1. Shortest-Path & Resilience (Dijkstra's Algorithm)
- **Algorithm:** The system implements Dijkstra's algorithm utilizing a priority queue (Min-Heap) to guarantee the lowest end-to-end latency path.
- **Dynamic Rerouting (Chaos Test):** The core routing loop accepts a list of "dead zones". Nodes or links marked as failed are completely isolated from the graph traversal during real-time queries without disrupting data flows.
- **Wireless Signal Threshold ($L_{max}$):** Any void hop exceeding `50,000,000 km` is instantly discarded as a valid edge, forcing multi-hop traversal via intermediate worlds.

### 2. Mathematical Modeling & Latency Breakdown
All formulas strictly adhere to the physical laws of the Zeta-26 system:
- **Void Distance ($L$):** Computed center-to-center minus atmospheric shells and planetary radii.
- **Void Travel Time ($T_v$):** Factored with atmospheric refraction indexes ($n$) and the speed of light ($C$).
- **Internal Crust Transit Time ($T_p$):** Calculates the specific shortest fiber-arc distance between the receiving tower and sending tower on any given relay node, adding precise processing penalties ($m \times \Delta t$).

### 3. Data Translation & Encoding (Codex Conversion)
- To prevent data loss across incompatible planetary dialects, raw payloads undergo dynamic ASCII-to-Base translation.
- Text characters are split into standard ASCII bytes, serialized into the corresponding target base layout (Base 5, 6, 14, 16, etc.), and cleanly presented as a flat transmission stream inside the logs.

---

## Technology Stack
- **Backend:** Python 3, FastAPI (Highly scalable, typed JSON parsing)
- **Frontend:** Plain HTML5, CSS3 (Cyberpunk/Terminal UI), JavaScript (Async Fetch API)

---

## Project Structure
```text
Launch26-Project/
│
├── main.py                # Primary FastAPI application & REST endpoints
├── network.py             # Latency calculations, Dijkstra logic & Codex helpers
├── universe-config.json   # Input configuration containing metadata and node schemas
├── index.html             # Visualization and interactive User Interface dashboard
└── README.md              # Technical documentation (This file)