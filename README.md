# CS46-Final_Project
# HMC Campus Navigation System

A campus navigation tool for Harvey Mudd College that finds the shortest walking route between any two buildings. 

## Overview

The system models the HMC campus as a weighted undirected graph where buildings and pedestrian junctions are nodes and walkable paths are edges. Edge weights represent approximate walking distances in meters computed from GPS coordinates using the Haversine formula.

The core data structures (hash tables and graphs) are implemented from scratch. Shortest paths are computed using Dijkstra's algorithm with a custom min-heap priority queue. An accessibility mode allows users to find routes that avoid staircases.

## Project Structure

```
CS46-Final_Project/
├── campus_data.py   # Node definitions, GPS coordinates, edge list
├── hash_map.py      # Hash table with chaining (from scratch)
├── heap.py          # Min-heap priority queue (from scratch)
├── dijkstra.py      # Graph class and Dijkstra's algorithm
├── main.py          # Interactive CLI interface
├── diagnosis.py     # Correctness and edge case tests
└── README.md
```

## Requirements

- Python 3.x
- No external libraries required

## How to Run

### Navigation interface
```bash
python3 main.py
```

You will be shown a numbered list of all 23 campus buildings. Enter a start and destination number, choose whether you want accessible mode (avoids stairs), and the system prints the shortest route with step-by-step stops and an estimated walk time.

### Tests
```bash
python3 diagnosis.py
```

Runs 30 tests covering hash table correctness, graph construction, Dijkstra routing, accessibility filtering, and edge cases.

### Campus data inspection
```bash
python3 campus_data.py
```

Prints the full edge list with distances and stair flags.

## Data

The campus map includes 23 named building nodes, 11 pedestrian intersection nodes, and 38 edges with walking distances and stair flags. GPS coordinates for key buildings were confirmed via Google Maps. Remaining coordinates were estimated from the official HMC campus map. Edge weights are computed automatically using the Haversine formula.

## Algorithms and Data Structures

**Hash Table** (`hash_map.py`) — chaining with a polynomial rolling hash function. Used as the adjacency list backing store in the graph and for distance tracking in Dijkstra.

**Graph** (`dijkstra.py`) — undirected weighted adjacency list. Supports standard and accessibility-filtered construction.

**Min-Heap** (`heap.py`) — binary min-heap with sift-up and sift-down. Used as the priority queue in Dijkstra.

**Dijkstra's Algorithm** (`dijkstra.py`) — finds the shortest weighted path between two nodes. Uses lazy deletion to handle stale heap entries efficiently.

## Contributions

David Olloqui: Campus Data, Main, Diagnosis, GitHub Management, Slides
Rion Otsuka: Hash Map, Diagnosis, Slides
Rohan Mathew: Djikstra, Visualizations, Slides
