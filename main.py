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

# JSON Config load(They mentioned that not to hardcod so we are loading the universe data from a JSON file)
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
    dead_zones: Optional[str] = Query(None, description="Comma-separated dead planet IDs")
):
    dead_nodes = set()
    if dead_zones:
        dead_nodes = set(dead_zones.split(","))
        
    nodes_map = {n['id']: n for n in universe_data['nodes']}
    
    if origin not in nodes_map or destination not in nodes_map:
        raise HTTPException(status_code=400, detail="Invalid origin or destination ID")
        
    # Find the shortest path with Djkstra
    result = find_shortest_path(origin, destination, universe_data, dead_nodes)
    
    if result is None:
        return {"status": "undeliverable", "message": "No route could bridge the gap :( "}
        
    formatted_hop_log = []
    current_message = payload
    
    for hop in result["hop_details"]:
        next_node = nodes_map[hop["to"]]
        next_codex = next_node["codex"]
        
        # turn next hop to Codex
        hop_encoded_payload = encode_payload_for_hop(current_message, next_codex)
        
        formatted_hop = {
            "from_node": hop["from"],
            "to_node": hop["to"],
            "tx_tower": hop["tx_tower"],
            "rx_tower": hop["rx_tower"],
            "void_distance_km": round(hop["void_distance_km"], 2),
            "crust_latency_ms": round(hop["crust_latency_ms"], 4),
            "void_latency_ms": round(hop["void_latency_ms"], 4),
            "total_hop_latency_ms": round(hop["crust_latency_ms"] + hop["void_latency_ms"], 4),
            "next_hop_codex": next_codex,
            "serialized_transmission_stream": hop_encoded_payload
        }
        formatted_hop_log.append(formatted_hop)

    # Final Packet schema
    return {
        "status": "success",
        "packet_schema": {
            "origin_id": origin,
            "destination_id": destination,
            "current_id": origin,
            "raw_payload": payload,
            "hop_log": formatted_hop_log
        },
        "total_route_latency_ms": round(result["total_latency_ms"], 4)
    }