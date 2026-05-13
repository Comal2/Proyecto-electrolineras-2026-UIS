import os
import folium
import pandas as pd
from folium.plugins import HeatMap
#from simulacion import ruta_estadisticas

#enrutamos los csv y los definimos 
DIRECTORIO = os.path.dirname(os.path.abspath(__file__)) #guarda la ubicacion del mapa.py
#guardamos las ubicaciones de los archivos csv

df_e = pd.read_csv(os.path.join(DIRECTORIO, "../datos/electrolineras_con_nodos.csv"))
df_p = pd.read_csv(os.path.join(DIRECTORIO, "../datos/puntos_con_nodos.csv"))
#definimos las rutas de los csv

#creacion del mapa
mapa = folium.Map(location=[7.1254, -73.1198], zoom_start=13)

#creacion nodos 'ELECTROLINERAS'
for _, fila in df_e.iterrows():
    #Diferenciamos por tipo de carga
    if fila['tipo_carga'] == 'alta_potencia':   #Electrolineras de alata potencia
        folium.Marker(
            location=[fila['latitud'], fila['longitud']],
            tooltip=fila['nombre'],
            icon=folium.Icon(color='lightgreen', icon='bolt', prefix='fa')
        ).add_to(mapa)

    else:
        #electrolineras de potencia normal
        folium.Marker(
            location=[fila['latitud'], fila['longitud']],
            tooltip=fila['nombre'],
            icon=folium.Icon(color='green', icon='bolt', prefix='fa')
        ).add_to(mapa)

#creacion nodos 'PUNTOS REFERENCIA'
for _, fila in df_p.iterrows():
    folium.Marker(
        location=[fila['latitud'], fila['longitud']],
        tooltip=fila['nombre'],
        icon=folium.Icon(color='blue')
    ).add_to(mapa)

#centrar el mapa respecto a los nodos
mapa.fit_bounds([
    [df_e['latitud'].min(), df_e['longitud'].min()],
    [df_p['latitud'].max(), df_p['longitud'].max()]
])

#guardamos el mapa en los resultados
mapa.save(os.path.join(DIRECTORIO, "../resultados/mapa_base.html")) # codigo de prueba o referencia visual, no refleja el resultado final.

#prueba zonas + visitadas
if __name__ == "__main__":
    #visitas = 

    #datos_color = df_e[['latitud', 'longitud', 'visitas']].values.tolist
    pass