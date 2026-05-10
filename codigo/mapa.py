import webbrowser #visualizacion para el mapa en html
import os
import folium
import pandas as pd

#enrutamos los csv y los definimos 
directorio_mapa = os.path.dirname(os.path.abspath(__file__)) #guarda la ubicacion del mapa.py
carpeta_resultados = os.path.join(directorio_mapa, '..', 'resultados')  #subimos a la carpeta de resultados
ruta_csv_e = os.path.join(directorio_mapa, '..', 'datos', 'electrolineras_con_nodos.csv')
ruta_csv_p = os.path.join(directorio_mapa, '..', 'datos', 'puntos_con_nodos.csv' )
#guardamos las ubicaciones de los archivos csv

df_e = pd.read_csv(ruta_csv_e)
df_p = pd.read_csv(ruta_csv_p)
#definimos y leemos las ruta y nueestro csv

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

ruta_html = os.path.join(carpeta_resultados, 'mapa_base.html') #guardamos la ubicacion del mapa_base
mapa.save(ruta_html) # codigo de prueba o referencia visual, no refleja el resultado final.
#print(f"Mapa guardado con exito en: {ruta_html}")

def abrir_mapa_html():
    webbrowser.open('file://'+os.path.abspath(ruta_html))       #abrimos el html en la web
    print("El mapa se a abierto automaticamente en tu navegador web :) ")
