from campus_data import buildings, intersections
from dijkstra import CampusGraph, Dijkstra

NAME = dict(buildings + intersections)
graph = CampusGraph()
router = Dijkstra(graph)


def compare(origin, destination):
    fast_d, fast_r = router.find_shortest_route(origin, destination)
    safe_d, safe_r = router.find_shortest_route(origin, destination, accessible=True)
    print(f"\n{NAME[origin]} -> {NAME[destination]}")
    print(f"  [accessible=False] {fast_d} m, {len(fast_r)} hops")
    if safe_r is None:
        print(f"  [accessible=True ] unreachable without stairs")
    else:
        diff = safe_d - fast_d
        suffix = " (no stairs on fastest route)" if diff == 0 else f" (+{diff} m detour)"
        print(f"  [accessible=True ] {safe_d} m, {len(safe_r)} hops{suffix}")


if __name__ == "__main__":
    OLIN     = 1     # F.W. Olin Science Center
    PLATT    = 10    # Joseph B. Platt Campus Center
    SONTAG   = 18    # Frederick and Susan Sontag Residence Hall
    compare(OLIN,   PLATT)
    compare(PLATT,  SONTAG)
    compare(SONTAG, OLIN)
