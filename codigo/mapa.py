import os
import folium
import json
import pandas as pd
from folium.plugins import HeatMap
#from simulacion import ruta_estadisticas

#enrutamos los csv y los definimos 
DIRECTORIO = os.path.dirname(os.path.abspath(__file__)) #guarda la ubicacion del mapa.py
#guardamos las ubicaciones de los archivos csv

df_e = pd.read_csv(os.path.join(DIRECTORIO, "../datos/electrolineras_con_nodos.csv"))
df_p = pd.read_csv(os.path.join(DIRECTORIO, "../datos/puntos_con_nodos.csv"))
#definimos las rutas de los csv

def generar_mapa_con_demanda():
    """Genera el mapa base con electrolineras, puntos y zonas de demanda."""
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

    # Leer predicciones del modelo si existen
    ruta_predicciones = os.path.join(DIRECTORIO, "../datos/predicciones_demanda.json")
    try:
        with open(ruta_predicciones, 'r') as f:
            zonas_demanda = json.load(f)
            
            # Marcar zonas de demanda en el mapa
            for zona in zonas_demanda:
                elec = df_e[df_e['nombre'] == zona['electrolinera']]
                if not elec.empty:
                    for _, fila in elec.iterrows():
                        # Círculo de demanda
                        demanda_pct = zona['demanda']
                        if demanda_pct > 0.5:
                            color = 'red'
                            radius = 800
                        elif demanda_pct > 0.3:
                            color = 'orange'
                            radius = 600
                        else:
                            color = 'yellow'
                            radius = 400
                        
                        folium.Circle(
                            location=[fila['latitud'], fila['longitud']],
                            radius=radius,
                            color=color,
                            fill=True,
                            fillColor=color,
                            fillOpacity=0.4,
                            popup=f"{zona['electrolinera']}: {demanda_pct:.1%} demanda"
                        ).add_to(mapa)
    except FileNotFoundError:
        print("No hay predicciones de demanda para mostrar en el mapa.")
    except Exception as e:
        print(f"Error al cargar predicciones: {e}")

    #centrar el mapa respecto a los nodos
    mapa.fit_bounds([
        [df_e['latitud'].min(), df_e['longitud'].min()],
        [df_p['latitud'].max(), df_p['longitud'].max()]
    ])

    #guardamos el mapa en los resultados
    ruta_mapa = os.path.join(DIRECTORIO, "../resultados/mapa_con_demanda.html")
    mapa.save(ruta_mapa)
    print(f"Mapa generado y guardado en: {ruta_mapa}")
    return ruta_mapa

#prueba zonas + visitadas
if __name__ == "__main__":
    generar_mapa_con_demanda()
