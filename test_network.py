import pytest
import json
from network import find_shortest_path

# universe-config.json load 
with open('universe-config.json', 'r') as f:
    universe_data = json.load(f)


@pytest.mark.parametrize("origin, destination, expected_latency", [
    ("Aegis", "Boreas", 60074.0028), 
    ("Dawn", "Fenix", 70715.6795),
    ("Aegis", "Caelum", 229495.1678),
    ("Boreas", "Elysium", 97165.2338),
])
def test_route_latency(origin, destination, expected_latency):
    # test the API logic
    result = find_shortest_path(origin, destination, universe_data)
    
    
    assert result is not None
    
   
    assert result["total_latency_ms"] == pytest.approx(expected_latency, abs=0.1)

def test_chaos_test():
    result = find_shortest_path("Aegis", "Caelum", universe_data, dead_nodes={"Dawn"})
    assert result is not None
    assert "Dawn" not in result["path"]