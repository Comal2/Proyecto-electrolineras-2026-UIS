import os
import folium
import pandas as pd
import resultados

#enrutamos los csv y los definimos 
DIRECTORIO = os.path.dirname(os.path.abspath(__file__)) #guarda la ubicacion del mapa.py
#guardamos las ubicaciones de los archivos csv

df_e = pd.read_csv(os.path.join(DIRECTORIO, "../datos/electrolineras_con_nodos.csv"))
df_p = pd.read_csv(os.path.join(DIRECTORIO, "../datos/puntos_con_nodos.csv"))
#definimos las rutas de los csv

#creacion del mapa
mapa = folium.Map(location=[7.1254, -73.1198], zoom_start=13)

for _, fila in df_e.iterrows():
    folium.Marker(
        location=[fila['latitud'], fila['longitud']],
        tooltip=fila['nombre'],
        icon=folium.Icon(color='green', icon='bolt', prefix='fa')
    ).add_to(mapa)

for _, fila in df_p.iterrows():
    folium.Marker(
        location=[fila['latitud'], fila['longitud']],
        tooltip=fila['nombre'],
        icon=folium.Icon(color='blue')
    ).add_to(mapa)

mapa.save(os.path.join(DIRECTORIO, "../resultados/mapa_base.html")) # codigo de prueba o referencia visual, no refleja el resultado final.
print(f"Mapa guardado con exito en {resultados}")

