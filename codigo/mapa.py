import sys
import os
import folium
import pandas as pd

#enrutamos los csv y los definimos 
directorio_mapa = os.path.dirname(os.path.abspath(__file__))
carpeta_resultados = os.path.join(directorio_mapa, '..', 'resultados')
ruta_csv_e = os.path.join(directorio_mapa, '..', 'datos', 'electrolineras_con_nodos.csv')
ruta_csv_p = os.path.join(directorio_mapa, '..', 'datos', 'puntos_con_nodos.csv' )


df_e = pd.read_csv(ruta_csv_e)
df_p = pd.read_csv(ruta_csv_p)

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

ruta_html = os.path.join(carpeta_resultados, 'mapa_base.html')
mapa.save(ruta_html) # codigo de prueba o referencia visual, no refleja el resultado final.
print(f"Mapa guardado con exito en: {ruta_html}")