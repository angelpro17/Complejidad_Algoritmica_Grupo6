import json
import random
import networkx as nx
import matplotlib.pyplot as plt

WIDTH = 1920
HEIGHT = 1080
NUM_BUILDINGS = 1500
MIN_RESIDENTS = 1
MAX_RESIDENTS = 7
MIN_GAS_PER_PERSON = 150
MAX_GAS_PER_PERSON = 500
MIN_EXT_CONNECTIONS = 1
MAX_EXT_CONNECTIONS = 10

def gen_random(min, max):
    return random.randint(min, max)


def gen_unique_name(node_id, streets):
    street = random.choice(streets)
    return f"{street} {node_id}"

def gen_node(node_id, streets):
    addr = {
        "name": gen_unique_name(node_id, streets),
        "x": gen_random(0, WIDTH),
        "y": gen_random(0, HEIGHT)
    }
    residents = gen_random(MIN_RESIDENTS, MAX_RESIDENTS)
    gas_per_person = gen_random(MIN_GAS_PER_PERSON, MAX_GAS_PER_PERSON)
    total_gas = residents * gas_per_person

    node = {
        "ID": node_id,
        "Address": addr,
        "Residents": residents,
        "External_connections": [],
        "Avg_gas_per_person": gas_per_person,
        "Total_gas_consumption": total_gas
    }
    return node

def gen_graph():
    streets = load_streets()
    nodes = [gen_node(i, streets) for i in range(1, NUM_BUILDINGS + 1)]

    G = nx.Graph()

    for node in nodes:
        G.add_node(node["ID"], pos=(node["Address"]["x"], node["Address"]["y"]))

    for node in nodes:
        ext_connections = set()
        while len(ext_connections) < gen_random(MIN_EXT_CONNECTIONS, MAX_EXT_CONNECTIONS):
            possible_conn = gen_random(1, NUM_BUILDINGS)
            if possible_conn != node["ID"]:
                ext_connections.add(possible_conn)
        node["External_connections"] = list(ext_connections)
        for conn in ext_connections:
            G.add_edge(node["ID"], conn)

    if not nx.is_connected(G):
        print("Graph is not connected. Connecting components...")
        for component in list(nx.connected_components(G))[1:]:
            rand_node = random.choice(list(component))
            rand_conn = random.choice(list(nx.connected_components(G)[0]))
            G.add_edge(rand_node, rand_conn)

    with open("dataset.json", "w") as file:
        json.dump(nodes, file, indent=4)

    return "dataset.json"
