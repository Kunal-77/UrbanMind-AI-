import networkx as nx
import random

# ✅ moved seed inside function for consistency
def create_graph():
    random.seed(42)

    G = nx.Graph()

    nodes = ["A", "B", "C", "D", "E", "F", "G"]

    edges = [
        ("A", "B"),
        ("B", "C"),
        ("A", "D"),
        ("D", "E"),
        ("E", "C"),
        ("E", "F"),
        ("F", "G"),
        ("C", "G"),
        ("B", "F"),
    ]

    for u, v in edges:
        base_time = random.randint(5, 15)
        traffic_factor = random.uniform(1.0, 2.5)

        G.add_edge(
            u, v,
            base_time=base_time,
            traffic=traffic_factor,
            weight=base_time * traffic_factor
        )

    return G


def apply_traffic(G):
    for u, v in G.edges():
        G[u][v]['weight'] = G[u][v]['base_time'] * G[u][v]['traffic']
    return G


def emergency_priority(G):
    for u, v in G.edges():
        G[u][v]['weight'] = G[u][v]['base_time'] * 0.7
    return G


# 🔥 SAFE ROUTE FUNCTION
def get_route(start, end, emergency=False):
    G = create_graph()

    if isinstance(start, str):
        start = start.upper()
    if isinstance(end, str):
        end = end.upper()

    if start not in G.nodes or end not in G.nodes:
        return [start, end], 0

    if emergency:
        G = emergency_priority(G)
    else:
        G = apply_traffic(G)

    path = nx.shortest_path(G, start, end, weight='weight')
    cost = nx.shortest_path_length(G, start, end, weight='weight')

    return path, round(cost, 2)


# 🔥 DIRECT ROUTE (USED NOW IN APP)
def get_direct_route(start, end):
    G = create_graph()

    if isinstance(start, str):
        start = start.upper()
    if isinstance(end, str):
        end = end.upper()

    if start not in G or end not in G:
        return [start, end], "Invalid"

    if G.has_edge(start, end):
        cost = G[start][end]['base_time']
        return [start, end], round(cost, 2)

    return [start, end], "Not Direct"