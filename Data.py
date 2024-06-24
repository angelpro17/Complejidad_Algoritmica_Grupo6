import json
import networkx as nx
from grafos import pintar_grafo
from grafos import generar_node

NUM_CASAS = 1500

def generar_dataset():
    grafo = nx.Graph()
    for i in range(1, NUM_CASAS + 1):
        node = generar_node(i)
        grafo.add_node(node["ID"], **node)
    
    return nx.node_link_data(grafo)['nodes']

dataset = generar_dataset()

# Eliminar el campo "id" de cada node en el dataset
for node in dataset:
    del node["id"]

# Guardar el dataset generado en un archivo JSON
with open("dataset.json", "w") as archivo_salida:
    json.dump(dataset, archivo_salida, indent=4)

print("Generado exitosamente.")

# Descomentar para pintar el grafo utilizando el dataset generado
# dataset_json = "dataset.json"
# pintar_grafo(dataset_json)
