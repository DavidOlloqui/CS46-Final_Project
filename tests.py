
 
from hash_map import HashTable
from campus_data import buildings, intersections, edges
from dijkstra import CampusGraph, Dijkstra
 
NAME = dict(buildings + intersections)
TOTAL_NODES = len(buildings) + len(intersections)  # 34
 
passed = 0
failed = 0
 
def check(description, condition):
    global passed, failed
    if condition:
        print(f"  PASS  {description}")
        passed += 1
    else:
        print(f"  FAIL  {description}")
        failed += 1
 
 
# 1. HASH TABLE TESTS
 
print("\n--- HashTable ---")
 
ht = HashTable()
 
# Basic insert and search
ht.insert("Olin Science Center", 1)
ht.insert("Dining Commons", 11)
ht.insert("Garrett House", 17)
 
check("insert + search returns correct value",
      ht.search("Olin Science Center") == 1)
 
check("search second key",
      ht.search("Dining Commons") == 11)
 
check("__contains__ returns True for existing key",
      "Garrett House" in ht)
 
check("__contains__ returns False for missing key",
      "Nonexistent Building" not in ht)
 
check("__len__ reflects inserted items",
      len(ht) == 3)
 
# Update existing key
ht.insert("Olin Science Center", 99)
check("re-insert updates value without growing size",
      ht.search("Olin Science Center") == 99 and len(ht) == 3)
 
# Remove
ht.remove("Dining Commons")
check("remove deletes key",
      "Dining Commons" not in ht)
 
check("__len__ decrements after remove",
      len(ht) == 2)
 
# KeyError on missing search
try:
    ht.search("Does Not Exist")
    check("search missing key raises KeyError", False)
except KeyError:
    check("search missing key raises KeyError", True)
 
# KeyError on missing remove
try:
    ht.remove("Does Not Exist")
    check("remove missing key raises KeyError", False)
except KeyError:
    check("remove missing key raises KeyError", True)
 
# Collision handling — load table to force collisions
ht2 = HashTable(capacity=4)   # tiny table guarantees collisions
for node_id, name in buildings[:8]:
    ht2.insert(name, node_id)
collision_ok = all(ht2.search(name) == node_id for node_id, name in buildings[:8])
check("chaining handles collisions correctly (capacity=4)", collision_ok)
 
# All 34 campus nodes should load without error
ht3 = HashTable()
for node_id, name in buildings + intersections:
    ht3.insert(name, node_id)
check("all 34 campus nodes inserted",
      len(ht3) == TOTAL_NODES)
check("all 34 campus nodes searchable",
      all(ht3.search(name) == node_id for node_id, name in buildings + intersections))
 
 
# 2. CAMPUS GRAPH TESTS
 
print("\n--- CampusGraph ---")
 
graph = CampusGraph()
 
check("graph contains all 34 nodes",
      len(graph.all_locations) == TOTAL_NODES)
 
check("Olin (1) has at least one neighbor",
      len(graph.neighbors(1)) > 0)
 
check("Dining Commons (11) has at least one neighbor",
      len(graph.neighbors(11)) > 0)
 
# Undirected — if A connects to B, B connects to A
def has_neighbor(graph, a, b):
    return any(n == b for n, _ in graph.neighbors(a))
 
check("graph is undirected: Olin↔West Hub both directions",
      has_neighbor(graph, 1, 24) and has_neighbor(graph, 24, 1))
 
check("graph is undirected: Dining↔SE Junction both directions",
      has_neighbor(graph, 11, 29) and has_neighbor(graph, 29, 11))
 
check("edge weights are positive",
      all(w > 0 for _, w in graph.neighbors(1)))
 
# Accessible graph excludes stair edges
graph_accessible = CampusGraph(accessible=True)
stair_edges = [(n1, n2) for n1, n2, w, stairs in edges if stairs]
accessible_ok = True
for n1, n2 in stair_edges:
    if has_neighbor(graph_accessible, n1, n2):
        accessible_ok = False
        break
check("accessible graph excludes all stair edges", accessible_ok)
 
 
# 3. DIJKSTRA TESTS
 
print("\n--- Dijkstra ---")
 
router = Dijkstra(graph)
 
# Same node
dist, route = router.find_shortest_route(1, 1)
check("same start and end returns distance 0",
      dist == 0 and route == [1])
 
# Known short route: Kingston (9) → Dining (11) via Kingston South Junction (27)
dist, route = router.find_shortest_route(9, 11)
check("Kingston → Dining finds a route",
      route is not None)
check("Kingston → Dining distance is positive",
      dist is not None and dist > 0)
check("Kingston → Dining route starts and ends correctly",
      route[0] == 9 and route[-1] == 11)
 
# Longer route: Olin (1) → Garrett House (17)
dist, route = router.find_shortest_route(1, 17)
check("Olin → Garrett House finds a route",
      route is not None and dist is not None)
check("Olin → Garrett House route starts and ends correctly",
      route is not None and route[0] == 1 and route[-1] == 17)
 
# Triangle inequality: direct should never be longer than detour
dist_1_11, _ = router.find_shortest_route(1, 11)
dist_1_26, _ = router.find_shortest_route(1, 26)
dist_26_11, _ = router.find_shortest_route(26, 11)
check("triangle inequality holds (Olin→Dining ≤ Olin→Plaza + Plaza→Dining)",
      dist_1_11 <= dist_1_26 + dist_26_11)
 
# Symmetry: A→B == B→A
dist_fwd, _ = router.find_shortest_route(5, 22)
dist_rev, _ = router.find_shortest_route(22, 5)
check("route is symmetric: Parsons→Linde == Linde→Parsons",
      dist_fwd == dist_rev)
 
# All pairs reachable (campus is fully connected)
all_nodes = [node_id for node_id, _ in buildings + intersections]
unreachable = []
for dest in all_nodes:
    d, r = router.find_shortest_route(1, dest)
    if r is None and dest != 1:
        unreachable.append(dest)
check(f"all nodes reachable from Olin (node 1)",
      len(unreachable) == 0)
 
# Accessible mode
router_accessible = Dijkstra(CampusGraph(accessible=True))
dist_a, route_a = router_accessible.find_shortest_route(8, 11)
if route_a is not None:
    stair_set = {(min(n1,n2), max(n1,n2)) for n1, n2, w, stairs in edges if stairs}
    route_uses_stairs = any(
        (min(route_a[i], route_a[i+1]), max(route_a[i], route_a[i+1])) in stair_set
        for i in range(len(route_a) - 1)
    )
    check("accessible route uses no stair edges", not route_uses_stairs)
else:
    check("accessible route found from Olin to Dining", False)
 
 
# SUMMARY


print(f"\n{'='*40}")
print(f"  Results: {passed} passed, {failed} failed")
print(f"{'='*40}\n")