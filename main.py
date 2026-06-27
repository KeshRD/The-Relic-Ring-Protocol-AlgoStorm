import json
from fastapi import FastAPI, HTTPException, Query
from typing import Optional
from network import find_shortest_path, encode_payload_for_hop
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import os

# JSON Config load
config_file = os.environ.get('UNIVERSE_CONFIG', 'universe-config.json')
with open(config_file, 'r') as f:
    universe_data = json.load(f)

@app.get("/")
def read_root():
    return {"message": "Launch26 System Online"}

@app.get("/route")
def get_route(
    origin: str, 
    destination: str, 
    payload: str = "Hello world", 
    dead_zones: Optional[str] = Query(None, description="Comma-separated dead planet IDs")
):
    dead_nodes = set()
    if dead_zones:
        dead_nodes = set(dead_zones.split(","))
        
    nodes_map = {n['id']: n for n in universe_data['nodes']}
    
    if origin not in nodes_map or destination not in nodes_map:
        raise HTTPException(status_code=400, detail="Invalid origin or destination ID")
        
    result = find_shortest_path(origin, destination, universe_data, dead_nodes)
    
    if result is None:
        return {"status": "undeliverable", "message": "No route could bridge the gap :( "}
        
    formatted_hop_log = []
    current_message = payload
    
    for hop in result["hop_details"]:
        next_node = nodes_map[hop["to"]]
        next_codex = next_node["codex"]
        
        hop_encoded_payload = encode_payload_for_hop(current_message, next_codex)
        
        formatted_hop = {
            "from_node": hop["from"],
            "to_node": hop["to"],
            "tx_tower": hop["tx_tower"],
            "rx_tower": hop["rx_tower"],
            "exit_tower": hop["tx_tower"],
            "entry_tower": hop["rx_tower"],
            "void_distance_km": round(hop["void_distance_km"], 2),
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
            "current_id": origin,
            "raw_payload": payload,
            "hop_log": formatted_hop_log,
            "node_tower_schema": result.get("node_tower_schema", [])
        },
        "total_route_latency_ms": round(result["total_latency_ms"], 4)
    }