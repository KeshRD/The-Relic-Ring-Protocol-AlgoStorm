import math
import heapq

def calculate_void_distance(node1, node2, scale_unit):
    dx = node2['x'] - node1['x']
    dy = node2['y'] - node1['y']
    grid_dist = math.sqrt(dx**2 + dy**2)
    
    r1_h1 = node1['radius_km'] + node1['atmosphere_thickness_km']
    r2_h2 = node2['radius_km'] + node2['atmosphere_thickness_km']
    
    L = (grid_dist * scale_unit) - r1_h1 - r2_h2
    return L

def calculate_void_latency(node1, node2, L, speed_of_light):
    h1_n1 = node1['atmosphere_thickness_km'] * node1['refraction_index']
    h2_n2 = node2['atmosphere_thickness_km'] * node2['refraction_index']
    T_v = (h1_n1 + h2_n2 + L) / speed_of_light
    return T_v

def get_tower_coordinates(node, tower_index, scale_unit):
    N = node['active_towers']
    R = node['radius_km']
    
    # Clockwise angle
    angle_rad = math.radians(90 - (tower_index * (360.0 / N)))
    
    center_x = node['x'] * scale_unit
    center_y = node['y'] * scale_unit
    
    tower_x = center_x + R * math.cos(angle_rad)
    tower_y = center_y + R * math.sin(angle_rad)
    
    return tower_x, tower_y

def find_closest_towers(node1, node2, scale_unit):
    best_t1 = 0
    best_t2 = 0
    min_dist = float('inf')
    
    for t1 in range(node1['active_towers']):
        x1, y1 = get_tower_coordinates(node1, t1, scale_unit)
        for t2 in range(node2['active_towers']):
            x2, y2 = get_tower_coordinates(node2, t2, scale_unit)
            
            dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            if dist < min_dist:
                min_dist = dist
                best_t1 = t1
                best_t2 = t2
                
    return best_t1, best_t2

def calculate_crust_latency(node, entry_tower, exit_tower, speed_of_light, fiber_fraction, tower_delay_ms):
    r = node['radius_km']
    N = node['active_towers']
    
    if entry_tower == exit_tower:
        s = 0
        m = 1
    else:
        diff = abs(exit_tower - entry_tower)
        s = min(diff, N - diff)
        m = s + 1
        
    fiber_time_sec = (2 * math.pi * r * s) / (N * fiber_fraction * speed_of_light)
    fiber_time_ms = fiber_time_sec * 1000
    
    total_tower_delay = m * tower_delay_ms
    
    T_p = fiber_time_ms + total_tower_delay
    return T_p

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
    
    # added None.it remeber prev_rx_tower for next hop crust latency calculation
    queue = [(0.0, start_id, [start_id], [], None)] 
    distances = {n['id']: float('inf') for n in universe_data['nodes']}
    distances[start_id] = 0.0
    
    while queue:
        current_latency, curr_id, path, logs, prev_rx_tower = heapq.heappop(queue)
        
        if curr_id == end_id:
            return {
                "path": path,
                "total_latency_ms": current_latency,
                "hop_details": logs
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
                
            T_v = calculate_void_latency(curr_node, neighbor_node, L, speed_of_light) * 1000
            
            tx_tower, rx_tower = find_closest_towers(curr_node, neighbor_node, scale_unit)
            
            # this is the change.if previouse toewer  there it become entry tower for next hop crust latency calculation
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
                
                # when go to next round pass  rx_tower to prev_rx_tower 
                heapq.heappush(queue, (new_latency, neigh_id, path + [neigh_id], logs + [hop_log_entry], rx_tower))
                
    return None

def int_to_base(n, base):
    if n == 0:
        return "0"
    
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    if base > len(digits):
        raise ValueError("Base is too large for the defined digits.")
        
    result = ""
    while n > 0:
        result = digits[n % base] + result
        n //= base
    return result

def encode_payload_for_hop(payload: str, next_codex: int) -> list:
    encoded_list = []
    for char in payload:
        ascii_val = ord(char)
        base_val = int_to_base(ascii_val, next_codex)
        encoded_list.append(base_val)
    return encoded_list
#he he :)