import json
from collections import defaultdict

# Función para cargar el grafo desde el archivo JSON
def Load_Grafo(archivo):
    with open(archivo) as f:
        data = json.load(f)
    grafo = defaultdict(list)
    for node in data:
        for conexion in node["external_connections"]:
            grafo[node["ID"]].append((conexion, node["total_consumption"]))
            grafo[conexion].append((node["ID"], node["total_consumption"]))
    return grafo

# Función para implementar el algoritmo de Prim
def prim(grafo, inicio):
    visitados = set()
    aristas = []
    father = {}
    costo = {}
    for node in grafo:
        costo[node] = float('inf')
    costo[inicio] = 0
    
    while len(visitados) != len(grafo):
        node_min = None
        for node in grafo:
            if node not in visitados and (node_min is None or costo[node] < costo[node_min]):
                node_min = node
        if node_min is None:
            break
        visitados.add(node_min)
        for vecino, weight in grafo[node_min]:
            if vecino not in visitados and weight < costo[vecino]:
                father[vecino] = node_min
                costo[vecino] = weight
                aristas.append((node_min, vecino, weight))
    return father, costo, aristas

# Función para reconstruir la ruta más corta y calcular la suma de weights
def rebuild_ruta(father, inicio, fin, grafo):
    ruta = []
    node = fin
    suma_weights = 0
    while node != inicio:
        ruta.append(node)
        node_father = father[node]
        for vecino, weight in grafo[node_father]:
            if vecino == node:
                suma_weights += weight
                break
        node = node_father
    ruta.append(inicio)
    ruta.reverse()
    return "->".join(str(node) for node in ruta), suma_weights