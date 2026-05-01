import json  #Leer el archivo json
import os    #Con esto manejamos las carpetas y rutas sin importar donde se ejecute
 
# 1. Cargar datos desde el archivo JSON
 
ruta_json = os.path.join(os.path.dirname(__file__), "../datos/vehiculos.json")

with open(ruta_json, "r") as archivo:
    datos = json.load(archivo)
 
vehiculos = datos["vehiculos"]
 
# 2. Mostrar los vehículos disponibles
 
print("=== Vehículos disponibles ===")
for i in range(len(vehiculos)):
    print(f"[{i+1}] {vehiculos[i]['modelo']} | Gama: {vehiculos[i]['gama']} | Autonomía: {vehiculos[i]['autonomia_km']} km")
 
print()
 
 # 3. Seleccionar un vehículo (1 = BMW , 2 = Nissan Leaf)

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

# 4. Estado inicial del vehículo

bateria_actual = 100.0   # porcentaje bateria
aviso = False

# 5. Distancias de prueba (inventadas)

distancias = [50, 80, 60, 90, 40, 90]  #Lista de las distancias

# 6. Simulación

print(f"=== Simulación: {modelo} ===")
print(f"Autonomía: {autonomia} km | Batería: {bateria_kwh} kWh | Eficiencia: {eficiencia} Wh/km")
print()

for km in distancias:
    consumo        = (km / autonomia) * 100
    bateria_actual = bateria_actual - consumo
    bateria_actual = round(bateria_actual, 1) #Redondeamos

    if bateria_actual < 0:      #Validamos que si la bateria es menor a cero la iguale a 0.0 para que no nos muestre numeros negativos
        bateria_actual = 0.0
    
    print(f"{modelo} recorrió {km} km")
    print(f"Batería restante: {bateria_actual}%")

    if bateria_actual <= 20.0 and not aviso:
        print("⚠️  BATERÍA BAJA — Buscar electrolinera cercana")
        aviso = True

    print()