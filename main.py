import json
from fastapi import FastAPI, HTTPException, Query
from typing import Optional
from network import find_shortest_path, encode_payload_for_hop, decode_payload_from_hop
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

with open('universe-config.json', 'r') as f:
    universe_data = json.load(f)

@app.get("/")
def read_root():
    return {"message": "Launch26 System Online"}

@app.get("/route")
def get_route(
    origin: str, 
    destination: str, 
    payload: str = "Hello world", 
    dead_zones: Optional[str] = Query(None, description="Comma-separated dead planet IDs"),
    dead_links: Optional[str] = Query(None, description="Comma-separated dead links (e.g., Aegis-Boreas)")
):
    dead_nodes = set(dead_zones.split(",")) if dead_zones else set()
    dead_links_set = set(dead_links.split(",")) if dead_links else set()
        
    nodes_map = {n['id']: n for n in universe_data['nodes']}
    
    if origin not in nodes_map or destination not in nodes_map:
        raise HTTPException(status_code=400, detail="Invalid origin or destination ID")
        
    result = find_shortest_path(origin, destination, universe_data, dead_nodes, dead_links_set)
    
    if result is None:
        return {"status": "undeliverable", "message": "No route could bridge the gap."}
        
    formatted_hop_log = []
    current_ascii_payload = payload
    
    for hop in result["hop_details"]:
        next_node = nodes_map[hop["to"]]
        next_codex = next_node["codex"]
        
        # 1. Encoding for send in the void
        hop_encoded_payload = encode_payload_for_hop(current_ascii_payload, next_codex)
        
        # 2. Local Decoding for send inside the planet
        decoded_back_to_ascii = decode_payload_from_hop(hop_encoded_payload, next_codex)
        current_ascii_payload = decoded_back_to_ascii
        
        formatted_hop = {
            "from_node": hop["from"],
            "to_node": hop["to"],
            "tx_tower": hop["tx_tower"],
            "rx_tower": hop["rx_tower"],
            "void_distance_km": round(hop["void_distance_km"], 2),
            "latency_breakdown": {
                "fiber_ms": round(hop["fiber_latency_ms"], 4),
                "tower_ms": round(hop["tower_latency_ms"], 4),
                "atmosphere_ms": round(hop["atmosphere_latency_ms"], 4),
                "vacuum_ms": round(hop["vacuum_latency_ms"], 4)
            },
            "crust_latency_ms": round(hop["crust_latency_ms"], 4),
            "void_latency_ms": round(hop["void_latency_ms"], 4),
            "total_hop_latency_ms": round(hop["crust_latency_ms"] + hop["void_latency_ms"], 4),
            "next_hop_codex": next_codex,
            "serialized_transmission_stream": hop_encoded_payload
        }
        formatted_hop_log.append(formatted_hop)

    return {
        "status": "success",
        "packet_schema": {
            "origin_id": origin,
            "destination_id": destination,
            "current_id": destination,
            "payload": payload,
            "hop_log": formatted_hop_log
        },
        "total_route_latency_ms": round(result["total_latency_ms"], 4)
    }