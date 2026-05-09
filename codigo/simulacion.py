import json  # Leer el archivo json
import os    # Con esto manejamos las carpetas y rutas sin importar donde se ejecute
import pandas as pd # Leer los archivos csv
import networkx as nx # Para manejar el grafo del mapa y calcular rutas/distancias
import random # Para seleccionar puntos de referencia aleatorios

# 1. Cargar datos desde el archivo JSON

ruta_json = os.path.join(os.path.dirname(__file__), "../datos/vehiculos.json")
with open(ruta_json, "r") as archivo:
    datos = json.load(archivo)

vehiculos = datos["vehiculos"]

# 2. Cargar los datos de los puntos de referencia y las electrolinera

ruta_puntos = os.path.join(os.path.dirname(__file__), "../datos/puntos_con_nodos.csv")
ruta_electrolineras = os.path.join(os.path.dirname(__file__), "../datos/electrolineras_con_nodos.csv")

    #Pandas convierte el csv en un DataFrame(df)

df_puntos = pd.read_csv(ruta_puntos)        
df_electrolineras = pd.read_csv(ruta_electrolineras)

    #Convertimos los DataFrames a listas de diccionarios para facilitar su uso en la simulación

puntos      = df_puntos.to_dict(orient="records")
electrolineras = df_electrolineras.to_dict(orient="records")

# 3. Cargar el grafo del mapa

ruta_mapa = os.path.join(os.path.dirname(__file__), "../datos/area_metropolitana.graphml")
G = nx.read_graphml(ruta_mapa)

# Convertimos los pesos de las aristas a flotantes
for u, v, d in G.edges(data=True):
    d['length'] = float(d.get('length', 1)) # 'length' usa el nombre del peso en graphml

#Recargas
historial_recargas = []


# 4. Clase del vehículo eléctrico 

class Vehiculo:

    def __init__(self, modelo, autonomia, bateria_kwh, eficiencia):
        self.modelo               = modelo
        self.autonomia            = autonomia
        self.bateria_kwh          = bateria_kwh
        self.eficiencia           = eficiencia
        self.bateria_actual       = 100.0
        self.contador_recargas    = 0
        self.acumulador_distancia = 0.0

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

#5. La función para encontrar la electrolinera más cercana al punto de referencia seleccionado, usando las distancias entre nodos
def electrolinera_mas_cercana(G, nodo_actual, electrolineras):
    def distancia(e):
        try:
            return nx.shortest_path_length(G, source=nodo_actual, target=e["nodo_mapa"], weight='length')
        except:
            return float('inf')
    return min(electrolineras, key=distancia)

#6. Lógica de la simulación

if __name__ == "__main__":
    print("============== Simulación ==============")
    n = int(input("Ingrese la cantidad de recorridos que desea simular: "))

    for veh_data in vehiculos:
        auto = Vehiculo(veh_data["modelo"], veh_data["autonomia_km"], veh_data["bateria_kwh"], veh_data["Eficiencia/consumo_Wh_por_km"])
        
        for i in range(n):
            origen, destino = random.sample(puntos, 2)
            # Le dicimos a networkx la distancia entre el nodo de origen y destino, usando el peso 'length' que representa la distancia en km
            distancia_km = nx.shortest_path_length(G, source=str(origen["nodo_mapa"]), target=str(destino["nodo_mapa"]), weight='length') / 1000
            
            necesita_recarga = auto.consumir(distancia_km)
            
            if necesita_recarga:
                elec = electrolinera_mas_cercana(G, destino["nodo_mapa"], electrolineras)
                historial_recargas.append({
                    "vehiculo": auto.modelo,
                    "electrolinera": elec["nombre"],
                    "bateria_al_recargar": auto.bateria_actual,
                    "numero_recorrido": i + 1
                })
                auto.recargar()

    df = pd.DataFrame(historial_recargas)
    ruta_estadisticas = os.path.join(os.path.dirname(__file__), "../datos")
    df.to_csv(os.path.join(ruta_estadisticas, "estadisticas.csv"), index=False)
    df.to_json(os.path.join(ruta_estadisticas, "estadisticas.json"), orient="records", indent=2)
    df.to_excel(os.path.join(ruta_estadisticas, "estadisticas.xlsx"), index=False)
