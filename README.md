# Zeta-26: The Relic Ring Protocol

**Organized by the IEEE Computer Society Student Branch Chapter — University of Kelaniya**
**Submitted for LAUNCH26**

---

## Table of Contents

- [Executive Summary](#executive-summary)
- [Technical Implementation Details](#technical-implementation-details)
  - [1. Shortest-Path & Resilience (Dijkstra's Algorithm)](#1-shortest-path--resilience-dijkstras-algorithm)
  - [2. Mathematical Modeling & Latency Breakdown](#2-mathematical-modeling--latency-breakdown)
  - [3. Data Translation & Encoding (Codex Conversion)](#3-data-translation--encoding-codex-conversion)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Setup & Running Instructions](#setup--running-instructions)
  - [Prerequisites](#prerequisites)
  - [1. Install Dependencies](#1-install-dependencies)
  - [2. Start the Backend Server](#2-start-the-backend-server)
  - [3. Open the Dashboard](#3-open-the-dashboard)

---

## Executive Summary

This project implements a ruthlessly efficient network routing simulation designed to reconnect the fractured Zeta-26 star system using primitive, legacy infrastructure — underground fiber cables and laser transceivers. The system calculates exact latency based on physical parameters, dynamically translates payload dialects, and instantly routes around dead zones in real time.

---

## Technical Implementation Details

### 1. Shortest-Path & Resilience (Dijkstra's Algorithm)

- **Algorithm:** Implements Dijkstra's algorithm with a priority queue (min-heap) to guarantee the lowest end-to-end latency path between any two nodes.
- **Dynamic Rerouting (Chaos Test):** The core routing loop accepts a list of "dead zones." Nodes or links marked as failed are completely isolated from graph traversal during real-time queries, without disrupting active data flows.
- **Wireless Signal Threshold ($L_{max}$):** Any void hop exceeding `50,000,000 km` is instantly discarded as a valid edge, forcing the algorithm to find a multi-hop traversal via intermediate worlds.

### 2. Mathematical Modeling & Latency Breakdown

All formulas strictly adhere to the physical laws of the Zeta-26 system:

| Component | Description |
|---|---|
| **Void Distance ($L$)** | Computed center-to-center, minus atmospheric shells and planetary radii. |
| **Void Travel Time ($T_v$)** | Factored with atmospheric refraction indexes ($n$) and the speed of light ($C$). |
| **Internal Crust Transit Time ($T_p$)** | Calculates the shortest fiber-arc distance between the receiving tower and sending tower on any given relay node, adding precise processing penalties ($m \times \Delta t$). |

### 3. Data Translation & Encoding (Codex Conversion)

To prevent data loss across incompatible planetary dialects, raw payloads undergo dynamic ASCII-to-Base translation:

- Text characters are split into standard ASCII bytes.
- Bytes are serialized into the corresponding target base layout (Base 5, 6, 14, 16, etc.).
- The result is presented as a flat transmission stream inside the logs.

---

## Technology Stack

| Layer | Technologies |
|---|---|
| **Backend** | Python 3, FastAPI (highly scalable, typed JSON parsing) |
| **Frontend** | Plain HTML5, CSS3 (Cyberpunk/Terminal UI), JavaScript (Async Fetch API) |

---

## Project Structure

```text
Launch26-Project/
│
├── main.py                # Primary FastAPI application & REST endpoints
├── network.py             # Latency calculations, Dijkstra logic & Codex helpers
├── universe-config.json   # Input configuration containing metadata and node schemas
├── index.html             # Visualization and interactive User Interface dashboard
└── README.md              # Technical documentation (this file)
```

---

## Setup & Running Instructions

### Prerequisites

Make sure you have **Python 3.8+** installed on your system.

### 1. Install Dependencies

Open your terminal in the project directory and execute:

```bash
pip install fastapi uvicorn
```

### 2. Start the Backend Server

Run the Uvicorn live-reload server:

```bash
uvicorn main:app --reload
```

The API will spin up and become accessible at `http://127.0.0.1:8000`.

### 3. Open the Dashboard

- Navigate to your workspace folder and double-click `index.html` to open it in any modern web browser.
- Input your **Origin**, **Destination**, and **Payload**, and test failures in real time.