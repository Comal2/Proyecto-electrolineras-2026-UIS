import sys
import os
import folium
import pandas as pd


sys.path.insert(0, os.path.dirname(__file__))


df_e = pd.read_csv("datos/electrolineras_con_nodos.csv")
df_p = pd.read_csv("datos/puntos_con_nodos.csv")

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

mapa.save("resultados/mapa_base.html") # codigo de prueba o referencia visual, no refleja el resultado final.