import math

def haversine(coord1, coord2):
    R = 6371000
    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    return R * 2 * math.asin(math.sqrt(a))

buildings = [
    (1,  "F.W. Olin Science Center"),
    (2,  "Beckman Hall"),
    (3,  "W.M. Keck Laboratories"),
    (4,  "Norman F. Sprague Center"),
    (5,  "Parsons Engineering Building"),
    (6,  "Galileo Hall"),
    (7,  "Jacobs Science Center"),
    (8,  "R. Michael Shanahan Center for Teaching and Learning"),
    (9,  "Kingston Hall"),
    (10, "Joseph B. Platt Campus Center"),
    (11, "Hoch-Shanahan Dining Commons"),
    (12, "South Hall/Marks Residence Hall"),
    (13, "West Hall"),
    (14, "North Hall"),
    (15, "East Hall/Mildred E. Mudd"),
    (16, "Ronald and Maxine Linde Activities Center"),
    (17, "Garrett House"),
    (18, "Frederick and Susan Sontag Residence Hall"),
    (19, "J.L. Atwood Hall"),
    (20, "Wayne and Julie Drinkward Residence Hall"),
    (21, "Case Residence Hall"),
    (22, "Ronald and Maxine Linde Residence Hall"),
    (23, "Scott A. McGregor Computer Science Center"),
]

intersections = [
    (24, "West Courtyard Hub"),
    (25, "Parsons-Shanahan Hub"),
    (26, "Central Plaza Hub"),
    (27, "Kingston South Junction"),
    (28, "North-East Walkway Junction"),
    (29, "South-East Walkway Junction"),
    (30, "Residence West Hub"),
    (31, "Residence East Hub"),
    (32, "Southeast Branch"),
    (33, "South Road Junction"),
    (34, "Garrett Branch Node"),
]

node_coords = {
    # Academic Buildings
    1:  (34.1060236, -117.7127559), # * Olin Science Center (confirmed)
    2:  (34.1064,    -117.7126),    # Beckman Hall (estimated, adjacent to Olin)
    3:  (34.1058,    -117.7118),    # Keck Laboratories
    4:  (34.1054,    -117.7120),    # Sprague Center
    5:  (34.1068,    -117.7119),    # Parsons Engineering
    6:  (34.1062,    -117.7116),    # Galileo Hall
    7:  (34.1054,    -117.7110),    # Jacobs Science Center
    8:  (34.10643,   -117.71085),   # * Shanahan Center (confirmed)
    9:  (34.1062,    -117.7104),    # Kingston Hall
    10: (34.10649,   -117.70984),   # * Platt Campus Center (confirmed)
    11: (34.1054,    -117.7096),    # Dining Commons
    16: (34.1066,    -117.7074),    # Linde Activities Center
    23: (34.1056716, -117.7127274), # * McGregor CS Center (confirmed)

    # Residence Halls
    12: (34.1061,    -117.7089),    # South Hall
    13: (34.1054,    -117.7089),    # West Hall
    14: (34.1066,    -117.7084),    # North Hall
    15: (34.1056,    -117.7080),    # East Hall
    17: (34.1050935, -117.7073944), # * Garrett House (confirmed)
    18: (34.10638,   -117.70681),   # * Sontag Hall (confirmed)
    19: (34.1056,    -117.7064),    # Atwood Hall
    20: (34.1066,    -117.7062),    # Drinkward Hall
    21: (34.1056,    -117.7058),    # Case Hall
    22: (34.1066,    -117.7054),    # Linde Residence Hall

    # Intersections
    24: (34.1058,    -117.7124),    # West Courtyard Hub
    25: (34.1064,    -117.7116),    # Parsons-Shanahan Hub
    26: (34.1058,    -117.7105),    # Central Plaza Hub
    27: (34.1056,    -117.7100),    # Kingston South Junction
    28: (34.1066,    -117.7086),    # NE Walkway Junction
    29: (34.1055,    -117.7091),    # SE Walkway Junction
    30: (34.1061,    -117.7077),    # Residence West Hub
    31: (34.1062,    -117.7066),    # Residence East Hub
    32: (34.1058,    -117.7059),    # Southeast Branch
    33: (34.1047,    -117.7090),    # South Road Junction
    34: (34.1049,    -117.7080),    # Garrett Branch Node
}

def edge_weight(n1, n2):
    return round(haversine(node_coords[n1], node_coords[n2]))

_raw_edges = [
    # West Cluster
    (1,  24, True),   # Olin ↔ West Courtyard Hub
    (2,  24, True),   # Beckman ↔ West Courtyard Hub
    (23, 24, True),   # McGregor ↔ West Courtyard Hub
    (4,  24, False),   # Sprague ↔ West Courtyard Hub
    (3,  24, True),   # Keck ↔ West Courtyard Hub
    (6,  25, False),   # Galileo ↔ Parsons-Shanahan Hub
    (5,  25, False),   # Parsons ↔ Parsons-Shanahan Hub
    (8,  25, False),   # Shanahan ↔ Parsons-Shanahan Hub
    (24, 25, False),   # West Courtyard Hub ↔ Parsons-Shanahan Hub
    (3,  7,  True),   # Keck ↔ Jacobs

    # Central
    (25, 26, False),   # Parsons-Shanahan Hub ↔ Central Plaza Hub
    (7,  26, False),   # Jacobs ↔ Central Plaza Hub
    (8,  9,  False),   # Shanahan ↔ Kingston
    (9,  26, False),   # Kingston ↔ Central Plaza Hub
    (9,  27, True),   # Kingston ↔ Kingston South Junction
    (26, 10, False),   # Central Plaza Hub ↔ Platt Campus Center
    (26, 11, False),   # Central Plaza Hub ↔ Dining Commons
    (27, 11, True),   # Kingston South Junction ↔ Dining Commons

    # East Transition
    (10, 28, False),   # Platt ↔ NE Walkway Junction
    (11, 29, True),   # Dining ↔ SE Walkway Junction
    (28, 29, False),   # NE Walkway Junction ↔ SE Walkway Junction

    # East Residential
    (28, 14, False),   # NE Walkway Junction ↔ North Hall
    (28, 16, False),   # NE Walkway Junction ↔ Linde Activities Center
    (28, 30, False),   # NE Walkway Junction ↔ Residence West Hub
    (29, 12, False),   # SE Walkway Junction ↔ South Hall
    (29, 13, False),   # SE Walkway Junction ↔ West Hall
    (29, 30, False),   # SE Walkway Junction ↔ Residence West Hub
    (30, 15, False),   # Residence West Hub ↔ East Hall
    (30, 31, False),   # Residence West Hub ↔ Residence East Hub
    (31, 18, False),   # Residence East Hub ↔ Sontag
    (31, 20, False),   # Residence East Hub ↔ Drinkward
    (31, 32, False),   # Residence East Hub ↔ Southeast Branch
    (32, 19, False),   # Southeast Branch ↔ Atwood
    (32, 21, True),   # Southeast Branch ↔ Case
    (32, 22, False),   # Southeast Branch ↔ Linde Residence Hall

    # Garett House
    (11, 33, False),   # Dining ↔ South Road Junction
    (33, 34, False),   # South Road Junction ↔ Garrett Branch Node
    (34, 17, True),   # Garrett Branch Node ↔ Garrett House
]

edges = [
    (n1, n2, edge_weight(n1, n2), stairs)
    for n1, n2, stairs in _raw_edges
]

if __name__ == "__main__":
    all_nodes = dict(buildings + intersections)
    print(f"{'From':<45} {'To':<45} {'Dist(m)':>8}  Stairs")
    print("-" * 105)
    for n1, n2, w, stairs in edges:
        print(f"{all_nodes[n1]:<45} {all_nodes[n2]:<45} {w:>8}m  {'YES' if stairs else 'no'}")
    print(f"\nTotal edges: {len(edges)}")
