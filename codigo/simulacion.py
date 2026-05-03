import json  # Leer el archivo json
import os    # Con esto manejamos las carpetas y rutas sin importar donde se ejecute

# 1. Cargar datos desde el archivo JSON

ruta_json = os.path.join(os.path.dirname(__file__), "../datos/vehiculos.json")

with open(ruta_json, "r") as archivo:
    datos = json.load(archivo)

vehiculos = datos["vehiculos"]

# 2. Clase del vehículo eléctrico 

class vehiculo:

    def __init__(self, modelo, autonomia, bateria_kwh, eficiencia):
        self.modelo         = modelo
        self.autonomia      = autonomia
        self.bateria_kwh    = bateria_kwh
        self.eficiencia     = eficiencia
        self.bateria_actual = 100.0
        self.aviso          = False
        self.contador_recargas = 0
        self.acumulador_distancia = 0.0

    def consumo_bateria(self, km):
        consumo             = (km / self.autonomia) * 100
        self.bateria_actual = round(self.bateria_actual - consumo, 1)

        if self.bateria_actual < 0:     # Validamos que la bateria no sea negativa
            self.bateria_actual = 0.0

        print(f"{self.modelo} recorrió {km} km")
        print(f"Batería restante: {self.bateria_actual}%")

        if self.bateria_actual <= 20.0 and not self.aviso:
            print("⚠️  BATERÍA BAJA — Buscar electrolinera cercana")
            self.aviso = True

        print()

# 3. Mostrar los vehículos disponibles



print("=== Vehículos disponibles ===")
for i in range(len(vehiculos)):
    print(f"[{i+1}] {vehiculos[i]['modelo']} | Gama: {vehiculos[i]['gama']} | Autonomía: {vehiculos[i]['autonomia_km']} km")

print()

# 4. Seleccionar un vehículo

opcion = int(input("Elige una opcion: "))

print()

match opcion:
    case 1:
        indice = 0
    case 2:
        indice = 1
    case _:
        print("Opcion no valida")

modelo      = vehiculos[indice]["modelo"]
autonomia   = vehiculos[indice]["autonomia_km"]
bateria_kwh = vehiculos[indice]["bateria_kwh"]
eficiencia  = vehiculos[indice]["Eficiencia/consumo_Wh_por_km"]

# 5. Crear el objeto con los datos del vehículo seleccionado 

auto = vehiculo(modelo, autonomia, bateria_kwh, eficiencia)

# 6. Distancias de prueba (inventadas)

distancias = [50, 80, 60, 90, 40, 90, 50, 80, 60, 90, 40, 90]  # Lista de las distancias

# 7. Simulación

print(f"=== Simulación: {modelo} ===")
print(f"Autonomía: {autonomia} km | Batería: {bateria_kwh} kWh | Eficiencia: {eficiencia} Wh/km")
print()

for km in distancias:
    auto.consumo_bateria(km)
    auto.acumulador_distancia = auto.acumulador_distancia + km

    if auto.bateria_actual <= 20.0:
        auto.bateria_actual = 100.0
        auto.aviso          = False   # Reseteamos el aviso para el siguiente ciclo
        auto.contador_recargas = auto.contador_recargas +1
        

        print("🔋 Se recargó la batería al 100%")
        print()

print(f"El vehículo ha recargado {auto.contador_recargas} veces")
print(f"Distancia total recorrida: {auto.acumulador_distancia} km")