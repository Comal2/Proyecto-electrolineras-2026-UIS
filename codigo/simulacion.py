import json  # Leer el archivo json
import os    # Con esto manejamos las carpetas y rutas sin importar donde se ejecute
import pandas as pd # Leer los archivos csv
import networkx as nx # Para manejar el grafo del mapa y calcular rutas/distancias
import random # Para seleccionar puntos de referencia aleatorios
import osmnx as ox # Para trabajar con datos de OpenStreetMap y grafo
from grafo import electrolinera_mas_cercana # Importamos la funcion del grafo para encontrar la electrolinera mas cercana
from grafo import cargar_grafo # Importamos la funcion para cargar el grafo
from grafo import RUTA_ELECTROLINERAS_NODOS, RUTA_PUNTOS_NODOS


# ==============================================================
#                CREACIÓN DE LA CLASE
# ==============================================================


# 4. Clase del vehículo eléctrico 

class Vehiculo:

    def __init__(self, datos_vehiculo):
        self.modelo               = datos_vehiculo["modelo"]
        self.autonomia            = datos_vehiculo["autonomia_km"]
        self.bateria_kwh          = datos_vehiculo["bateria_kwh"]
        self.eficiencia           = datos_vehiculo["Eficiencia/consumo_Wh_por_km"]
        self.bateria_actual       = 100.0
        self.contador_recargas    = 0

    def consumir(self, km):
        consumo = (km / self.autonomia) * 100
        self.bateria_actual = round(self.bateria_actual - consumo, 1)

        if self.bateria_actual < 0:
            self.bateria_actual = 0.0

        print(f"{self.modelo} recorrió {km:.2f} km — Batería: {self.bateria_actual}%")

        return self.bateria_actual <= 20.0

    def recargar(self):
        self.bateria_actual = 100.0
        self.contador_recargas += 1
        print(f"🔋 {self.modelo} recargado al 100%")

        print()

def pedir_numero_recorridos():
    """Solicita al usuario un número entero positivo de recorridos."""

    while True:

        try:
            n = int(input("Ingrese la cantidad de recorridos: "))
            if n > 0:
                return n
            else:
                print("Por favor, ingrese un número entero positivo.")

        except ValueError:
            print("Error: ingresa solo números enteros.")

def simular_recorridos(G=None): 
 
    # ==============================================================
    #                CARGA DE DATOS
    # ==============================================================


    # 1. Cargar datos desde el archivo JSON

    ruta_json = os.path.join(os.path.dirname(__file__), "../datos/vehiculos.json") #Contruye una ruta absoluta hacie el json
    with open(ruta_json, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

    vehiculos = datos["vehiculos"]  #Tenemos una lista de diccionarios con los datos de cada vehículo eléctrico

    # 2. Cargar los datos de los puntos de referencia y las electrolinera

    #Convertimos los DataFrames a listas de diccionarios para facilitar su uso en la simulación

    puntos = pd.read_csv(RUTA_PUNTOS_NODOS).to_dict(orient="records") #Tenemos una lista de diccionarios con los datos de cada punto de referencia, incluyendo su nodo en el grafo del mapa
    electrolineras = pd.read_csv(RUTA_ELECTROLINERAS_NODOS).to_dict(orient="records") #Tenemos una lista de diccionarios con los datos de cada electrolinera, incluyendo su nodo en el grafo

    # 3. Cargar grafo

    ruta_mapa = os.path.join(os.path.dirname(__file__), "../datos/area_metropolitana.graphml")
    G = cargar_grafo(ruta_mapa)
    print()


    lista_vehiculos = [] #Creamos una lista vacía para almacenar los objetos de la clase "Vehiculo" que representarán cada vehículo eléctrico en la simulación

    for v in vehiculos:

        auto = Vehiculo(v) #Creamos un objeto de la clase "Vehiculo" para cada vehículo en la lista de datos y lo agregamos a la lista_vehiculos
        lista_vehiculos.append(auto) #Agregamos el objeto a la lista de vehículos

    #Recargas
    historial_recargas = []
    n = pedir_numero_recorridos()


    # ==============================================================
    #                LÓGICA DE LA SIMULACIÓN
    # ==============================================================

            
    # Elegir un punto aleatorio de partida y un punto aleatorio de destino para cada recorrido

    for recorrido in range(n):  #Iteramos sobre el número de recorridos que el usuario ha solicitado para la simulación

        origen  = random.choice(puntos) #Seleccionamos un punto de referencia aleatorio de la lista de puntos para ser el origen del recorrido
        destino = random.choice(puntos) #Seleccionamos otro punto de referencia aleatorio de la lista de puntos para ser el destino del recorrido

        while destino == origen:                #Si el destino es igual al origen, repetimos el proceso hasta que sean diferentes para evitar que el vehículo recorra una distancia de 0 km
            destino = random.choice(puntos)     #Seleccionamos otro punto de destino aleatorio de la lista de puntos

        distancia_m = nx.shortest_path_length(G, source=int(origen["nodo_mapa"]), target=int(destino["nodo_mapa"]), weight='length') / 1000

        for auto in lista_vehiculos:    #Iteramos sobre cada vehículo en la lista de vehículos y llamamos al método "consumir" para simular el consumo de batería durante el recorrido. Si el método devuelve True, significa que la batería está por debajo del 20% y el vehículo necesita recargar, por lo que llamamos al método "recargar".
            necesita_recarga = auto.consumir(distancia_m)   #Llamamos al método "consumir" del vehículo para simular el consumo de batería durante el recorrido. El método devuelve True si la batería está por debajo del 20% después de consumir, lo que indica que el vehículo necesita recargar. Guardamos este resultado en la variable "necesita_recarga" para usarlo en la siguiente parte de la lógica de la simulación.
    
            if necesita_recarga:

                electrolinera = electrolinera_mas_cercana(G, int(destino["nodo_mapa"]))  #Si el vehículo necesita recargar, utilizamos la función "electrolinera_mas_cercana" para encontrar la electrolinera más cercana al destino del recorrido, utilizando el grafo del mapa y el nodo del destino como referencia
                historial_recargas.append({
                        "vehiculo": auto.modelo,
                        "electrolinera": electrolinera["nombre"],
                        "bateria_al_recargar": auto.bateria_actual,
                        "numero_recorrido": recorrido + 1
                    })
                auto.recargar() #Si el vehículo necesita recargar, llamamos al método "recargar" para simular la recarga de la batería al 100%


    # ==============================================================
    #                EXPORTACIÓN DE LAS ESTADISTICAS
    # ==============================================================


    df = pd.DataFrame(historial_recargas)
    ruta_estadisticas = os.path.join(os.path.dirname(__file__), "../datos")
    df.to_csv(os.path.join(ruta_estadisticas, "estadisticas.csv"), index=False)
    df.to_json(os.path.join(ruta_estadisticas, "estadisticas.json"), orient="records", indent=2)
    df.to_excel(os.path.join(ruta_estadisticas, "estadisticas.xlsx"), index=False)
   
if __name__ == "__main__":
    simular_recorridos()