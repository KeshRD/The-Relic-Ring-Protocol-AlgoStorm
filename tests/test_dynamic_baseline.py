import os
import sys
import time
import json
import urllib.request
import urllib.parse
import multiprocessing
import uvicorn
import math

# Reconfigure stdout for utf-8 on Windows console
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Ensure project root is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.encoding.codex import (
    decode_payload_from_hop,
    get_void_transmission_bitstream,
    tokens_to_bitstream,
    base_to_int
)
from src.core.latency import (
    calculate_void_distance,
    calculate_void_transit_latency,
    calculate_atmospheric_latency,
    calculate_fiber_segments,
    calculate_subsurface_fiber_latency,
    calculate_tower_processing_latency
)

def run_server():
    from main import app
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="error")

def wait_for_server(url, timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with urllib.request.urlopen(url) as response:
                if response.status == 200:
                    return True
        except Exception:
            time.sleep(0.2)
    return False

def run_test_matrix():
    config_file = os.environ.get("UNIVERSE_CONFIG", "universe-config.json")
    with open(config_file, "r") as f:
        universe_data = json.load(f)
    nodes_map = {n['id']: n for n in universe_data['nodes']}
    metadata = universe_data['universe_metadata']
    speed_of_light = metadata['speed_of_light_kms']
    tower_delay_ms = metadata['tower_processing_delay_ms']
    fiber_fraction = metadata['fiber_speed_fraction']
    scale_unit = metadata['coordinate_scale_unit_km']
    max_hop_distance = metadata['max_void_hop_distance_km']

    if "manual" in config_file.lower() or "OriginAlpha" in nodes_map:
        scenarios = [
            {
                "id": "MANUAL-1",
                "name": "Isolated Single Hop Test",
                "origin": "OriginAlpha",
                "destination": "DestBeta",
                "payload": "A"
            }
        ]
    else:
        scenarios = [
            {
                "id": "A",
                "name": "Standard Short Path",
                "origin": "Aegis",
                "destination": "Dawn",
                "payload": "Hello World!"
            },
            {
                "id": "B",
                "name": "Deep Multi-Hop Topology Validation",
                "origin": "Aegis",
                "destination": "Caelum",
                "payload": "Launch26 Alpha-Numeric Test #101"
            },
            {
                "id": "C",
                "name": "Edge-Case Codex Evaluation",
                "origin": "Dawn",
                "destination": "Caelum",
                "payload": "Base14-Test-XYZ-999"
            }
        ]

    print("======================================================================")
    print("📐 STARTING DYNAMIC LATENCY ACCURACY VERIFICATION MATRIX")
    print("======================================================================")

    for sc in scenarios:
        print(f"\n[TEST CASE #{sc['id']}]")
        print("----------------------------------------------------------------------")
        print(f"• Configuration Ingested: System Cluster '{metadata.get('system_name', 'Zeta-26')}'")
        print(f"• Routing Pair: {sc['origin']} -> {sc['destination']}")

        try:
            url = f"http://127.0.0.1:8000/route?origin={sc['origin']}&destination={sc['destination']}&payload={urllib.parse.quote(sc['payload'])}"
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode('utf-8'))

            if data.get("status") != "success":
                raise Exception(f"API returned status '{data.get('status')}': {data.get('message', 'No route could bridge the gap')}")

            packet = data["packet_schema"]
            hop_log = packet["hop_log"]

            # Assertion 1: Verify End-to-End Delivery and Endpoint Match
            assert packet["origin_id"] == sc["origin"], f"Origin mismatch! Expected {sc['origin']}, got {packet['origin_id']}"
            assert packet["destination_id"] == sc["destination"], f"Destination mismatch! Expected {sc['destination']}, got {packet['destination_id']}"
            assert hop_log[-1]["to_node"] == sc["destination"], f"Final hop destination mismatch!"

            # Assertion 2: Match payload character length & decode accuracy
            final_hop = hop_log[-1]
            decoded_payload = decode_payload_from_hop(final_hop["serialized_transmission_stream"], final_hop["next_hop_codex"])
            assert decoded_payload == sc["payload"], f"Payload mismatch! Original: '{sc['payload']}', Decoded: '{decoded_payload}'"
            assert len(decoded_payload) == len(sc["payload"]), f"Payload character length mismatch!"

            # Assertion 3: Respect max_void_hop_distance_km limit
            for hop in hop_log:
                assert hop["void_distance_km"] <= max_hop_distance, f"Hop distance {hop['void_distance_km']} km exceeds limit {max_hop_distance} km"

            path_nodes = [packet["origin_id"]] + [h["to_node"] for h in hop_log]
            path_str = " -> ".join(path_nodes)
            print(f"• Active Graph Path Traversed: {path_str}")

            print("\n➔ STEP-BY-STEP HOPS LATENCY PERFORMANCE DATA:")

            total_tv_sec = 0.0
            total_atmo_sec = 0.0
            total_fiber_sec = 0.0
            total_tower_sec = 0.0

            for idx, hop in enumerate(hop_log, 1):
                from_node = nodes_map[hop["from_node"]]
                to_node = nodes_map[hop["to_node"]]

                L = calculate_void_distance(from_node, to_node, scale_unit)
                tv_sec = calculate_void_transit_latency(L, speed_of_light)
                ta_sec = calculate_atmospheric_latency(from_node, to_node, speed_of_light)

                if idx == 1:
                    entry_t = hop["tx_tower"]
                else:
                    entry_t = hop_log[idx - 2]["rx_tower"]
                exit_t = hop["tx_tower"]

                tf_sec, s_segments = calculate_subsurface_fiber_latency(from_node, entry_t, exit_t, speed_of_light, fiber_fraction)
                tp_sec, m_towers = calculate_tower_processing_latency(s_segments, tower_delay_ms)

                net_hop_time = tv_sec + ta_sec + tf_sec + tp_sec

                print(f"  * Hop {idx}: {hop['from_node']} (Exit Tower: {hop['tx_tower']}) -> {hop['to_node']} (Entry Tower: {hop['rx_tower']})")
                print(f"    - Vacuum Distance (L): {L:.6f} km")
                print(f"    - Raw Void Delay (Tv): {tv_sec:.6f} seconds")
                print(f"    - Ionized Atmospheric Shell Drag (Ta): {ta_sec:.6f} seconds")
                print(f"    - Crustal Fiber Ring Transit (Tf): {s_segments} segments traveled at {fiber_fraction}c -> {tf_sec:.6f} seconds")
                t_delay_str = f"{int(tower_delay_ms)}ms" if tower_delay_ms.is_integer() else f"{tower_delay_ms}ms"
                print(f"    - Tower Processing Overhead (Tp): {m_towers} towers hit * {t_delay_str} -> {tp_sec:.6f} seconds")
                print(f"    - NET HOP TRANSIT TIME: {net_hop_time:.6f} seconds")

                total_tv_sec += tv_sec
                total_atmo_sec += ta_sec
                total_fiber_sec += tf_sec
                total_tower_sec += tp_sec

            # Add final landing tower processing delay at destination
            dest_tp_sec = tower_delay_ms / 1000.0
            total_tower_sec += dest_tp_sec

            total_accumulated_latency = total_tv_sec + total_atmo_sec + total_fiber_sec + total_tower_sec

            print("\n➔ GLOBAL PATH LATENCY METRIC SUMMARY LEDGER:")
            print(f"  - Aggregated Void Interplanetary Delay (Σ Tv): {total_tv_sec:.6f} seconds")
            print(f"  - Aggregated Ionized Atmosphere Refraction Delay (Σ Ta): {total_atmo_sec:.6f} seconds")
            print(f"  - Aggregated Subsurface Fiber Ring Local Delay (Σ Tf): {total_fiber_sec:.6f} seconds")
            print(f"  - Aggregated Tower Hardware Execution Processing Delay (Σ Tp): {total_tower_sec:.6f} seconds")
            print(f"  - TOTAL END-TO-END NETWORK ACCUMULATED LATENCY: {total_accumulated_latency:.6f} seconds")

            print("\nSTATUS COMPLIANCE AUDIT: SUCCESS")

        except Exception as e:
            print(f"\nSTATUS COMPLIANCE AUDIT: FAILURE - {str(e)}")

    print("\n======================================================================")

if __name__ == "__main__":
    server_process = multiprocessing.Process(target=run_server)
    server_process.start()
    try:
        if wait_for_server("http://127.0.0.1:8000/"):
            run_test_matrix()
        else:
            print("Failed to start server.")
    finally:
        server_process.terminate()
        server_process.join()
