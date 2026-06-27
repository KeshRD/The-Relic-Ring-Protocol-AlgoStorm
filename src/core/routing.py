import heapq
from src.core.latency import (
    calculate_void_distance,
    calculate_void_latency,
    find_closest_towers,
    calculate_crust_latency
)

def find_shortest_path(start_id, end_id, universe_data, dead_nodes=None):
    if dead_nodes is None:
        dead_nodes = set()
        
    nodes_map = {n['id']: n for n in universe_data['nodes']}
    metadata = universe_data['universe_metadata']
    
    scale_unit = metadata['coordinate_scale_unit_km']
    speed_of_light = metadata['speed_of_light_kms']
    max_hop_distance = metadata['max_void_hop_distance_km']
    fiber_fraction = metadata['fiber_speed_fraction']
    tower_delay_ms = metadata['tower_processing_delay_ms']
    
    if start_id not in nodes_map or end_id not in nodes_map:
        return None
    if start_id in dead_nodes or end_id in dead_nodes:
        return None
        
    # priority queue: (accumulated_latency, curr_id, path_list, hop_logs_list, prev_rx_tower)
    queue = [(0.0, start_id, [start_id], [], None)]
    distances = {n['id']: float('inf') for n in universe_data['nodes']}
    distances[start_id] = 0.0
    
    while queue:
        current_latency, curr_id, path, logs, prev_rx_tower = heapq.heappop(queue)
        
        if curr_id == end_id:
            # Construct asymmetric node tower map for audit
            node_tower_schema = []
            for i, node_name in enumerate(path):
                node_entry = {"node_id": node_name}
                if i == 0:
                    # Origin node: only exit_tower
                    node_entry["exit_tower"] = logs[0]["tx_tower"]
                elif i == len(path) - 1:
                    # Destination node: only entry_tower
                    node_entry["entry_tower"] = logs[i - 1]["rx_tower"]
                else:
                    # Intermediate relay node: entry_tower and exit_tower
                    node_entry["entry_tower"] = logs[i - 1]["rx_tower"]
                    node_entry["exit_tower"] = logs[i]["tx_tower"]
                node_tower_schema.append(node_entry)

            return {
                "path": path,
                "total_latency_ms": current_latency + tower_delay_ms,
                "hop_details": logs,
                "node_tower_schema": node_tower_schema
            }
            
        if current_latency > distances[curr_id]:
            continue
            
        curr_node = nodes_map[curr_id]
        
        for neighbor_node in universe_data['nodes']:
            neigh_id = neighbor_node['id']
            
            if neigh_id == curr_id or neigh_id in dead_nodes:
                continue
                
            L = calculate_void_distance(curr_node, neighbor_node, scale_unit)
            
            if L > max_hop_distance:
                continue
                
            T_v = calculate_void_latency(curr_node, neighbor_node, L, speed_of_light) * 1000.0
            
            tx_tower, rx_tower = find_closest_towers(curr_node, neighbor_node, scale_unit)
            
            entry_tower = prev_rx_tower if prev_rx_tower is not None else tx_tower
                
            T_p = calculate_crust_latency(curr_node, entry_tower, tx_tower, speed_of_light, fiber_fraction, tower_delay_ms)
            
            new_latency = current_latency + T_p + T_v
            
            if new_latency < distances[neigh_id]:
                distances[neigh_id] = new_latency
                
                hop_log_entry = {
                    "from": curr_id,
                    "to": neigh_id,
                    "tx_tower": f"T_{tx_tower}",
                    "rx_tower": f"T_{rx_tower}",
                    "void_distance_km": L,
                    "crust_latency_ms": T_p,
                    "void_latency_ms": T_v
                }
                
                heapq.heappush(queue, (new_latency, neigh_id, path + [neigh_id], logs + [hop_log_entry], rx_tower))
                
    return None
