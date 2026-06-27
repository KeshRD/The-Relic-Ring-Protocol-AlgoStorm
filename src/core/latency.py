import math

def calculate_void_distance(node1, node2, scale_unit):
    """
    Calculates the true vacuum path length (L) in kilometers.
    L = Grid Distance * scale_unit - radius1 - radius2
    """
    dx = node2['x'] - node1['x']
    dy = node2['y'] - node1['y']
    grid_dist = math.sqrt(dx**2 + dy**2)
    L = (grid_dist * scale_unit) - node1['radius_km'] - node2['radius_km']
    return L

def calculate_void_transit_latency(L, speed_of_light):
    """
    1. Void Transit Latency (Tv) in seconds.
    Tv = L / C
    """
    return L / speed_of_light

def calculate_atmospheric_latency(node1, node2, speed_of_light):
    """
    2. Atmospheric Refraction Latency (Ta) in seconds.
    Ta = (h1 * n1 + h2 * n2) / C
    """
    h1_n1 = node1['atmosphere_thickness_km'] * node1['refraction_index']
    h2_n2 = node2['atmosphere_thickness_km'] * node2['refraction_index']
    return (h1_n1 + h2_n2) / speed_of_light

def calculate_fiber_segments(entry_tower, exit_tower, active_towers):
    def parse_tower_idx(t):
        if t is None:
            return None
        if isinstance(t, str) and t.startswith("T_"):
            return int(t.split("_")[1])
        return int(t)
    
    t_in = parse_tower_idx(entry_tower)
    t_out = parse_tower_idx(exit_tower)
    
    if t_in is None or t_out is None or t_in == t_out:
        return 0
    diff = abs(t_out - t_in)
    return min(diff, active_towers - diff)

def calculate_subsurface_fiber_latency(node, entry_tower, exit_tower, speed_of_light, fiber_fraction):
    """
    3. Subsurface Fiber Ring Latency (Tf) in seconds.
    Distance = s * (2 * pi * r / N)
    Velocity = fiber_fraction * C
    Tf = Distance / Velocity
    """
    r = node['radius_km']
    N = node['active_towers']
    s = calculate_fiber_segments(entry_tower, exit_tower, N)
    if s == 0:
        return 0.0, 0
    fiber_sec = (2 * math.pi * r * s) / (N * fiber_fraction * speed_of_light)
    return fiber_sec, s

def calculate_tower_processing_latency(s, tower_delay_ms):
    """
    4. Tower Hardware Processing Delay (Tp) in seconds.
    m = 1 if s == 0 else s + 1
    Tp = (m * tower_delay_ms) / 1000.0
    """
    m = 1 if s == 0 else s + 1
    tp_sec = (m * tower_delay_ms) / 1000.0
    return tp_sec, m

def calculate_void_latency(node1, node2, L, speed_of_light):
    """
    Helper returning combined void + atmospheric latency in seconds.
    """
    tv = calculate_void_transit_latency(L, speed_of_light)
    ta = calculate_atmospheric_latency(node1, node2, speed_of_light)
    return tv + ta

def calculate_crust_latency(node, entry_tower, exit_tower, speed_of_light, fiber_fraction, tower_delay_ms):
    """
    Helper returning crust latency (Tf + Tp) in milliseconds.
    """
    tf_sec, s = calculate_subsurface_fiber_latency(node, entry_tower, exit_tower, speed_of_light, fiber_fraction)
    tp_sec, m = calculate_tower_processing_latency(s, tower_delay_ms)
    return (tf_sec + tp_sec) * 1000.0

def get_tower_coordinates(node, tower_index, scale_unit):
    N = node['active_towers']
    R = node['radius_km']
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
