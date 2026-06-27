<div align="center">

<br />

```
███████╗███████╗████████╗ █████╗       ██████╗  ██████╗
╚══███╔╝██╔════╝╚══██╔══╝██╔══██╗      ╚════██╗ ██╔════╝
  ███╔╝ █████╗     ██║   ███████║       █████╔╝ ███████╗
 ███╔╝  ██╔══╝     ██║   ██╔══██║      ██╔═══╝  ██╔═══██╗
███████╗███████╗   ██║   ██║  ██║      ███████╗ ╚██████╔╝
╚══════╝╚══════╝   ╚═╝   ╚═╝  ╚═╝      ╚══════╝  ╚═════╝
```

# ⬡ THE RELIC RING PROTOCOL

**Reconnecting the Fractured Star System — One Hop at a Time**

<br />

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Algorithm](https://img.shields.io/badge/Algorithm-Dijkstra's-FF6B35?style=for-the-badge)](#)
[![Status](https://img.shields.io/badge/Status-Online-00FF88?style=for-the-badge)](#)

<br />

> *"When the relics fail, the ring must hold."*

<br />

**Organized by the IEEE Computer Society Student Branch — University of Kelaniya**
Submitted for **LAUNCH26**

<br />

---

</div>

## ◈ Team AlgoStrom

| Member | Role |
|---|---|
| **Ishakya Ranhiru** | Leader |
| **Hasini Lawanya** | 
| **Weenuka Rajapakshe** | 
| **Januli Wansandi** | 
| **Keshana Roshaka** | 

---

## ◈ What Is This?

Zeta-26's star system is fractured. Underground fiber cables corrode. Laser transceivers flicker. Relay towers on distant worlds go dark without warning.

**The Relic Ring Protocol** is a ruthlessly efficient network routing simulation that rebuilds those connections — calculating exact signal latency from physical parameters, dynamically rerouting around dead nodes in real time, and translating incompatible planetary data dialects at every hop.

**No approximations. No shortcuts. Just physics.**

---

## ◈ Core Capabilities

### 🔷 Shortest-Path Routing · Dijkstra's Algorithm

The routing engine implements Dijkstra's algorithm backed by a **priority queue (min-heap)**, guaranteeing the absolute lowest end-to-end latency path between any two nodes — inclusive of destination processing delays.

```
Origin ──[T_v]──► Relay Node ──[T_v]──► Relay Node ──► Destination
              ↕ [T_a]              ↕ [T_a]
           Atmosphere           Atmosphere
              ↕ [T_f]              ↕ [T_f]
           Fiber Arc            Fiber Arc
```

**Wireless Signal Threshold `L_max`:** Any void hop exceeding **50,000,000 km** is immediately discarded, forcing multi-hop traversal through intermediate worlds.

---

### 🔷 Dynamic Fault Isolation · Chaos Test Mode

Dead nodes and broken links are fed to the routing loop as **"dead zones"** and **"dead links"**. Failed elements are fully isolated from graph traversal during live queries — without disrupting active data flows.

```
 [Node A] ─────────────────── [Node B]
     │         VOID HOP           │
     │     ~~~~LINK DEAD~~~~       │
     │                             │
     └──── [Node C] ──────────────┘
              ↑ REROUTED
```

---

### 🔷 High-Resolution Latency Breakdown

Every path computation resolves into **four strict physical components:**

| Symbol | Component | Description |
|---|---|---|
| **T_v** | Vacuum Void Travel | Center-to-center distance, minus atmospheric shells, divided by `C` (speed of light) |
| **T_a** | Atmospheric Refraction | Laser penetration factored with planetary atmospheric indices `n` |
| **T_f** | Subsurface Fiber Transit | Shortest fiber-arc distance between the receiving and sending towers |
| **T_p** | Tower Processing Delay | Per-tower processing penalty `m × Δt` applied at every routing hop |

> All formulas adhere strictly to the physical laws governing the Zeta-26 system, with dynamic fallback defaults for incomplete node configurations.

---

### 🔷 Codex Translation · Planetary Dialect Encoding

Raw payloads are transformed at **every single hop** to prevent data loss across incompatible planetary dialects.

```
┌─────────────────────────────────────────────────────────┐
│  PLANET A (Base 5)  →  ASCII Bridge  →  PLANET B (Base 14)  │
│                                                         │
│  Incoming stream decoded locally from previous codex.   │
│  Re-encoded into destination planet's native base       │
│  before crossing the void.                              │
│                                                         │
│  Result serialized into JSON hop logs per transmission. │
└─────────────────────────────────────────────────────────┘
```

---

## ◈ Technology Stack

| Layer | Technology | Why |
|---|---|---|
| **Backend** | Python 3 + FastAPI | Highly scalable, typed JSON parsing, dynamic schema enforcement |
| **Frontend** | HTML5 + CSS3 + JS | Cyberpunk/Tactical Terminal UI, zero framework dependencies |
| **Routing** | Dijkstra's (min-heap) | Optimal path guarantee with O((V + E) log V) complexity |
| **Config** | JSON Schema | Human-readable universe definitions; hot-swappable node configs |

---

## ◈ Project Structure

```
Launch26-Project/
│
├── main.py                 ← FastAPI application & REST endpoints
├── network.py              ← Latency engine, Dijkstra logic & Codex translation
├── universe-config.json    ← Node metadata, system topology & physical parameters
├── index.html              ← Tactical dashboard UI
└── README.md               ← You are here
```

---

## ◈ Setup & Running

### Prerequisites

- Python **3.8+** installed on your system

### Step 1 — Install Dependencies

```bash
pip install fastapi uvicorn
```

### Step 2 — Start the Backend Server

```bash
uvicorn main:app --reload
```

> API is now live at **`http://127.0.0.1:8000`**

### Step 3 — Open the Dashboard

Navigate to the project folder and open **`index.html`** in any modern browser.

---

## ◈ Using the Dashboard

```
┌──────────────────────────────────────────────────────────────┐
│  RELIC RING PROTOCOL — TACTICAL CONSOLE                      │
├──────────────────────────────────────────────────────────────┤
│  Origin Node        [ PLANET AVAR-7         ▼ ]             │
│  Destination Node   [ RELAY STATION KETH-3  ▼ ]             │
│  Payload            [ TRANSMISSION DATA...    ]             │
├──────────────────────────────────────────────────────────────┤
│  ☠ Dead Zones       [ NODE_ID_1, NODE_ID_2    ]             │
│  ✂ Dead Links       [ LINK_ID_A, LINK_ID_B    ]             │
│                                                              │
│  [ INITIATE ROUTE ]                [ CHAOS TEST MODE ]      │
└──────────────────────────────────────────────────────────────┘
```

1. Set **Origin** and **Destination** nodes
2. Enter the **Payload** to transmit
3. Optionally inject **Dead Zones** or **Dead Links** to trigger dynamic rerouting
4. Hit **Initiate Route** — watch the Relic Ring hold

---

<div align="center">

<br />

```
  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
  ▓   ZETA-26 NETWORK · SIGNAL RESTORED   ▓
  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
```

**IEEE Computer Society Student Branch · University of Kelaniya**
*LAUNCH26 Submission · Team AlgoStrom*

<br />

</div>