import sys

from campus_data import buildings, intersections, edges
from hash_map import HashTable
from heap import MinHeap


class CampusGraph:

    def __init__(self, accessible=False):
        self.accessible = accessible
        self.all_locations = [loc_id for loc_id, _ in buildings + intersections]
        self.walking_paths = self._build_walking_paths()

    def _build_walking_paths(self):
        paths = HashTable()
        for loc_id in self.all_locations:
            paths.insert(str(loc_id), [])
        for edge in edges:
            from_loc, to_loc, step_distance = edge[0], edge[1], edge[2]
            stairs = edge[3] if len(edge) > 3 else False
            if self.accessible and stairs:
                continue
            paths.search(str(from_loc)).append((to_loc, step_distance))
            paths.search(str(to_loc)).append((from_loc, step_distance))
        return paths

    def neighbors(self, loc_id):
        return self.walking_paths.search(str(loc_id))


class Dijkstra:

    def __init__(self, graph):
        self.graph = graph

    def find_shortest_route(self, origin, destination):

        distance = HashTable()
        previous_loc = HashTable()
        unvisited = MinHeap()

        for loc in self.graph.all_locations:
            distance.insert(str(loc), sys.maxsize)
            previous_loc.insert(str(loc), None)
        distance.insert(str(origin), 0)
        unvisited.push([0, origin])

        while unvisited:
            current_distance, current_loc = unvisited.pop()

            if current_distance > distance.search(str(current_loc)):
                continue

            if current_loc == destination:
                route = [current_loc]
                while previous_loc.search(str(current_loc)) is not None:
                    current_loc = previous_loc.search(str(current_loc))
                    route.append(current_loc)
                route.reverse()
                return current_distance, route

            for next_loc, step_distance in self.graph.neighbors(current_loc):
                new_distance = current_distance + step_distance
                if new_distance < distance.search(str(next_loc)):
                    distance.insert(str(next_loc), new_distance)
                    previous_loc.insert(str(next_loc), current_loc)
                    unvisited.push([new_distance, next_loc])

        return None, None