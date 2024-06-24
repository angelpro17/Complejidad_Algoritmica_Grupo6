import json
import time
import tkinter as interface
from tkinter import ttk, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
from window import centrarVentana
from prim import Load_Grafo as Load_Grafo_prim, prim, rebuild_ruta
from kruskal import Load_Grafo as Load_Grafo_kruskal, kruskal, rebuild_mst

dataset_json = "dataset.json"
informacion_casas = {}
name_a_id = {}
id_a_name = {}

def cargar_nodos(dataset_json):
    global informacion_casas, name_a_id, id_a_name
    with open(dataset_json, "r") as archivo:
        lista_casas = json.load(archivo)
    nodes = [node["Address"]["name"] for node in lista_casas]
    informacion_casas = {node["Address"]["name"]: node for node in lista_casas}
    name_a_id = {node["Address"]["name"]: node["ID"] for node in lista_casas}
    id_a_name = {node["ID"]: node["Address"]["name"] for node in lista_casas}
    return nodes

def generar_grafo(ruta):
    arreglo = ruta.split('->')

    # Creamos un grafo dirigido
    G = nx.DiGraph()

    # Agregamos nodos al grafo
    for i, valor in enumerate(arreglo):
        G.add_node(i, label=str(valor))

    # Agregamos aristas entre nodos consecutivos
    for i in range(len(arreglo) - 1):
        G.add_edge(i, i + 1)

    # Dibujamos el grafo
    pos = nx.spring_layout(G)  # Layout para posicionar los nodos
    nx.draw(G, pos, with_labels=True, labels=nx.get_node_attributes(G, 'label'),
            node_color='#dff0d8', node_size=2000, font_size=10, font_color='black', edge_color='black', width=2.0)

    # Mostramos el grafo
    plt.title('Grafo con Arreglo')
    plt.show()

def obtener_aristas_de_ruta(ruta, grafo):
    aristas = []
    for i in range(len(ruta) - 1):
        u = ruta[i]
        v = ruta[i + 1]
        for vecino, weight in grafo[u]:
            if vecino == v:
                aristas.append((u, v, weight))
                break
    return aristas

def calcular_ruta_mas_corta(algoritmo, valor1, valor2, ventana_anterior):
    global ruta_global, algoritmo_global, aristas_global

    if not valor1 or not valor2:
        messagebox.showwarning("Advertencia", "Seleccione la conexión de origen y la conexión de llegada.")
        return

    id1 = name_a_id[valor1]
    id2 = name_a_id[valor2]

    if algoritmo.get() == "Prim":
        grafo = Load_Grafo_prim(dataset_json)
        inicio = time.perf_counter()
        father, costo, aristas = prim(grafo, id1)
        ruta, suma_weights = rebuild_ruta(father, id1, id2, grafo)
        # Medición de tiempo
        fin = time.perf_counter()
        tiempo_prim = (fin - inicio) * 1000
        aristas_global = obtener_aristas_de_ruta(ruta.split('->'), grafo)
        tiempo_ejecucion = f"Tiempo de ejecución de Prim: {tiempo_prim:.2f} ms"
    elif algoritmo.get() == "Kruskal":
        grafo, aristas = Load_Grafo_kruskal(dataset_json)
        inicio = time.perf_counter()
        mst = kruskal(grafo, aristas)
        ruta, suma_weights = rebuild_mst(mst)
        # Medición de tiempo
        fin = time.perf_counter()
        tiempo_kruskal = (fin - inicio) * 1000
        aristas_global = obtener_aristas_de_ruta(ruta.split('->'), grafo)
        tiempo_ejecucion = f"Tiempo de ejecución de Kruskal: {tiempo_kruskal:.2f} ms"

    ruta_global = ruta
    algoritmo_global = algoritmo

    ventana_anterior.withdraw()  # Ocultar la ventana principal de la calculadora

    mostrar_ventana_resultados(valor1, valor2, ruta, suma_weights, tiempo_ejecucion)

def mostrar_ventana_resultados(valor1, valor2, ruta, suma_weights, tiempo_ejecucion):
    ventanaMatriz = interface.Toplevel(aplicacion)
    ventanaMatriz.configure(bg='#dff0d8')
    ventanaMatriz.title(f"Calculadora de la ruta más corta entre dos casas - {algoritmo_global.get()}")

    centrarVentana(ventanaMatriz)

    # Mostrar información de las casas seleccionadas
    info_origen = informacion_casas[valor1]
    info_destino = informacion_casas[valor2]

    interface.Label(ventanaMatriz, text=f"Casa {valor1}:", bg='#dff0d8').pack(pady=5)
    interface.Label(ventanaMatriz, text=f"  Personas: {info_origen['population']}", bg='#dff0d8').pack(pady=5)
    interface.Label(ventanaMatriz, text=f"  Gas por persona: {info_origen['Consumer_average_for_people']} m³", bg='#dff0d8').pack(pady=5)
    interface.Label(ventanaMatriz, text=f"  Total de Gas: {info_origen['total_consumption']} m³", bg='#dff0d8').pack(pady=5)

    interface.Label(ventanaMatriz, text=f"Casa {valor2}:", bg='#dff0d8').pack(pady=5)
    interface.Label(ventanaMatriz, text=f"  Personas: {info_destino['population']}", bg='#dff0d8').pack(pady=5)
    interface.Label(ventanaMatriz, text=f"  Gas por persona: {info_destino['Consumer_average_for_people']} m³", bg='#dff0d8').pack(pady=5)
    interface.Label(ventanaMatriz, text=f"  Total de Gas: {info_destino['total_consumption']} m³", bg='#dff0d8').pack(pady=5)

    # Mostrar la ruta y el peso total
    interface.Label(ventanaMatriz, text=f"La ruta final entre la casa {valor1} y la casa {valor2} es:\n {ruta}", bg='#dff0d8').pack(pady=10)
    interface.Label(ventanaMatriz, text=f"La distancia más óptima para enviar Gas sin perdida de presión es: {suma_weights} metros", bg='#dff0d8').pack(pady=10)

    # Mostrar el tiempo de ejecución
    interface.Label(ventanaMatriz, text=tiempo_ejecucion, bg='#dff0d8').pack(pady=10)

    frame_grafico = interface.Frame(ventanaMatriz, bg='#dff0d8')
    frame_grafico.pack(fill=interface.BOTH, expand=True)

    interface.Button(ventanaMatriz, text="Generar Gráfico", command=lambda: generar_grafo(ruta), bg='blue', fg='white').pack(pady=10)
    interface.Button(ventanaMatriz, text="Cerrar", command=lambda: cerrar_ventana_resultados(ventanaMatriz), bg='red', fg='white').pack(pady=10)

def mostrar_interfaz_principal():
    pantalla_bienvenida.pack_forget()
    ventana_informacion.destroy()  # Cerrar la ventana de información

    ventana_principal = interface.Toplevel(aplicacion)
    ventana_principal.configure(bg='#dff0d8')
    ventana_principal.title("https://Calcular_Distancia.com")

    centrarVentana(ventana_principal)

    interface.Label(ventana_principal, text="Calcular la ruta más corta entre dos casas", bg='#dff0d8', font=("Arial", 16)).pack(pady=20)

    algoritmo = interface.StringVar()
    valor1 = interface.StringVar()
    valor2 = interface.StringVar()

    interface.Label(ventana_principal, text="Seleccione el algoritmo:", bg='#dff0d8').pack()
    ttk.Combobox(ventana_principal, textvariable=algoritmo, values=["Prim", "Kruskal"]).pack(pady=5)

    interface.Label(ventana_principal, text="Seleccione la conexión de origen:", bg='#dff0d8').pack()
    ttk.Combobox(ventana_principal, textvariable=valor1, values=cargar_nodos(dataset_json)).pack(pady=5)

    interface.Label(ventana_principal, text="Seleccione la conexión de llegada:", bg='#dff0d8').pack()
    ttk.Combobox(ventana_principal, textvariable=valor2, values=cargar_nodos(dataset_json)).pack(pady=5)

    interface.Button(ventana_principal, text="Calcular ruta más corta", command=lambda: calcular_ruta_mas_corta(algoritmo, valor1.get(), valor2.get(), ventana_principal), bg='blue', fg='white').pack(pady=20)

def cerrar_ventana_resultados(ventana):
    ventana.destroy()
    mostrar_interfaz_principal()

def cerrar_pantalla_bienvenida():
    pantalla_bienvenida.pack_forget()

    global ventana_informacion
    ventana_informacion = interface.Toplevel(aplicacion)
    ventana_informacion.configure(bg='#dff0d8')  # Fondo verde claro
    ventana_informacion.title("Información sobre EcoGas")

    centrarVentana(ventana_informacion)

    interface.Label(ventana_informacion, text="Bienvenido a EcoGas", bg='#dff0d8', fg='#3c763d', font=("Arial", 30, "bold")).pack(pady=20)
    interface.Label(ventana_informacion, text="Nuestra startup se dedica a optimizar la distribución de gas \n" +
                                               "en comunidades utilizando algoritmos avanzados. \n" +
                                               "Con nuestra tecnología, buscamos minimizar la pérdida de presión \n" +
                                               "y maximizar la eficiencia en la red de suministro de gas.\n\n", bg='#dff0d8', fg='black', font=("Arial", 15, "bold")).pack(pady=20)
    interface.Label(ventana_informacion, text="Descripción del Problema:", bg='#dff0d8', fg='#3c763d', font=("Arial", 30, "bold")).pack(pady=20)
    interface.Label(ventana_informacion, text="La gestión de los recursos de gas natural en Perú enfrenta desafíos significativos en un contexto de creciente demanda energética, \n"
                                               "infraestructura envejecida y la necesidad de optimizar el uso de este recurso en diversos sectores económicos. En conclusion, \n"
                                               "estos son los principales problemas que afectan la gestión del gas natural en el país\n\n", bg='#dff0d8', fg='black', font=("Arial", 15, "bold")).pack(pady=20)
    interface.Button(ventana_informacion, text="Continuar", command=mostrar_interfaz_principal, bg='blue', fg='white', font=("Arial", 14)).pack(pady=40)

# Configurar la aplicación principal
aplicacion = interface.Tk()
aplicacion.configure(bg='#dff0d8')
aplicacion.title("Bienvenido a EcoGas")

# Pantalla de bienvenida
pantalla_bienvenida = interface.Frame(aplicacion, bg='#dff0d8')
pantalla_bienvenida.pack(fill=interface.BOTH, expand=True)

# Cargar y mostrar la imagen
imagen_logo = Image.open("logo_upc.png")
logo = ImageTk.PhotoImage(imagen_logo)
interface.Label(pantalla_bienvenida, image=logo, bg='#dff0d8').pack(pady=20)

interface.Label(pantalla_bienvenida, text="Bienvenidos a la presentación de nuestro Trabajo Final \n\nStartUp: EcoGas", bg='#dff0d8', font=("Arial", 24)).pack(pady=20)
interface.Label(pantalla_bienvenida, text="Complejidad Algorítmica", bg='#dff0d8', font=("Arial", 16)).pack(pady=20)
interface.Label(pantalla_bienvenida, text="2024-01", bg='#dff0d8', font=("Arial", 16)).pack(pady=20)

participantes = [
    "Mallma Espíritu, Franky",
    "Anampa Lavado, Luis Angel",
    "Talizo Balbín, Joan Jefferson"
]

# Crear un LabelFrame para la lista de participantes
frame_participantes = interface.LabelFrame(aplicacion, text="Lista de Participantes", bg='#dff0d8', fg='black', font=("Arial", 14, "bold"), padx=20, pady=10)
frame_participantes.pack(pady=20)

# Ordenar y mostrar los nombres de los participantes
participantes.sort()
for participante in participantes:
    interface.Label(frame_participantes, text=participante, bg='#dff0d8', fg='black', font=("Arial", 12)).pack(anchor="w", pady=5)

interface.Button(pantalla_bienvenida, text="Continuar", command=cerrar_pantalla_bienvenida, bg='blue', fg='white', font=("Arial", 14)).pack(pady=40)

centrarVentana(aplicacion)

# Ejecutar la aplicación
aplicacion.mainloop()
