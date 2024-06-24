import json
from collections import defaultdict

def Load_Grafo(archivo):
    with open(archivo) as f:
        data = json.load(f)
    grafo = defaultdict(list)
    aristas = []
    for node in data:
        for conexion in node["external_connections"]:
            grafo[node["ID"]].append((conexion, node["total_consumption"]))
            grafo[conexion].append((node["ID"], node["total_consumption"]))
            aristas.append((node["total_consumption"], node["ID"], conexion))
    return grafo, aristas

def Find(father, node):
    if father[node] == node:
        return node
    return Find(father, father[node])

def bind(father, rango, node1, node2):
    raiz1 = Find(father, node1)
    raiz2 = Find(father, node2)
    
    if rango[raiz1] < rango[raiz2]:
        father[raiz1] = raiz2
    elif rango[raiz1] > rango[raiz2]:
        father[raiz2] = raiz1
    else:
        father[raiz2] = raiz1
        rango[raiz1] += 1

def kruskal(grafo, aristas):
    aristas.sort()  
    father = {}
    rango = {}
    
    for node in grafo:
        father[node] = node
        rango[node] = 0
    
    mst = []
    for weight, node1, node2 in aristas:
        if Find(father, node1) != Find(father, node2):
            bind(father, rango, node1, node2)
            mst.append((node1, node2, weight))
    
    return mst

def rebuild_mst(mst):
    mst.sort()
    suma_weights = sum(weight for _, _, weight in mst)
    ruta = " -> ".join(f"{node1}-{node2}({weight})" for node1, node2, weight in mst)
    return ruta, suma_weights
