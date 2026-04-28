from campus_data import buildings, intersections
from dijkstra import CampusGraph, Dijkstra

# --- Setup ---
NAME        = dict(buildings + intersections)
BUILDINGS   = buildings  # only show named buildings to user, not intersections

graph_normal     = CampusGraph(accessible=False)
graph_accessible = CampusGraph(accessible=True)
router_normal     = Dijkstra(graph_normal)
router_accessible = Dijkstra(graph_accessible)


# --- Helpers ---

def print_banner():
    print("=" * 55)
    print("   HMC Campus Navigation System")
    print("=" * 55)

def print_building_list():
    print("\nAvailable locations:")
    print("-" * 55)
    for node_id, name in BUILDINGS:
        print(f"  {node_id:>2}.  {name}")
    print("-" * 55)

def pick_building(prompt):
    valid_ids = {node_id for node_id, _ in BUILDINGS}
    while True:
        try:
            choice = int(input(prompt))
            if choice in valid_ids:
                return choice
            print(f"  Please enter a number between 1 and 23.")
        except ValueError:
            print("  Please enter a valid number.")

def print_route(label, distance, route):
    if route is None:
        print(f"\n  [{label}] No route found — destination unreachable.")
        return
    print(f"\n  [{label}]  {distance}m total  |  {len(route)} stops")
    print()
    for i, node_id in enumerate(route):
        if i == 0:
            tag = "START"
        elif i == len(route) - 1:
            tag = "END  "
        else:
            tag = "     "
        print(f"    {tag}  {NAME[node_id]}")

def estimate_minutes(meters):
    # average walking speed ~80m/min
    return round(meters / 80)


# --- Main loop ---

def main():
    print_banner()

    while True:
        print_building_list()

        origin      = pick_building("\nEnter start building number: ")
        destination = pick_building("Enter destination number:     ")

        if origin == destination:
            print("\n  You're already there!")
        else:
            acc_input = input("Accessible mode? (avoid stairs) [y/n]: ").strip().lower()
            accessible = acc_input == "y"

            if accessible:
                router = router_accessible
                mode   = "accessible"
            else:
                router = router_normal
                mode   = "standard"

            distance, route = router.find_shortest_route(origin, destination)

            print(f"\n{'=' * 55}")
            print(f"  {NAME[origin]}")
            print(f"  → {NAME[destination]}")
            print(f"  Mode: {mode}")
            print(f"{'=' * 55}")
            print_route(mode, distance, route)

            if distance is not None:
                mins = estimate_minutes(distance)
                print(f"\n  Estimated walk time: ~{mins} min")

            # also show accessible comparison if standard was chosen
            if not accessible and route is not None:
                acc_dist, acc_route = router_accessible.find_shortest_route(origin, destination)
                if acc_route is None:
                    print(f"\n  Note: no stair-free route exists between these buildings.")
                elif acc_dist == distance:
                    print(f"\n  Note: this route is already stair-free.")
                else:
                    print(f"\n  Accessible alternative: {acc_dist}m (+{acc_dist - distance}m detour)")

        print()
        again = input("Navigate again? [y/n]: ").strip().lower()
        if again != "y":
            print("\nGoodbye!\n")
            break


if __name__ == "__main__":
    main()