from campus_data import buildings, intersections
from dijkstra import CampusGraph, Dijkstra

NAME = dict(buildings + intersections)
graph = CampusGraph()
router = Dijkstra(graph)


def show(origin, destination):
    distance, route = router.find_shortest_route(origin, destination)
    print(f"\n{NAME[origin]}  ->  {NAME[destination]}")
    if route is None:
        print("  no route found")
        return
    print(f"  total: {distance} m,  {len(route)} stops")
    for loc_id in route:
        print(f"   {loc_id:>2}  {NAME[loc_id]}")


if __name__ == "__main__":
    show(1, 11)     # Olin Science Center -> Dining Commons
    show(23, 17)    # McGregor CS Center  -> Garrett House
    show(8, 22)     # Shanahan Center     -> Linde Residence Hall
    show(5, 5)      # trivial: same node
    show(2, 19)     # Beckman Hall        -> Atwood Hall
