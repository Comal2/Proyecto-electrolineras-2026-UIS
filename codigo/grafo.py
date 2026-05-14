# ==============================================================
#  SISTEMA DE ELECTROLINERAS - UIS 2026
# ==============================================================
# Este archivo es el puente entre los datos del proyecto y el mapa vial real.
# Carga el mapa de Bucaramanga como un grafo, lee las electrolineras y los
# puntos de referencia, les asigna el nodo del mapa que les corresponde y
# permite calcular cuál electrolinera queda más cerca por carretera.
# ==============================================================

# osmnx -> trabaja con mapas reales de OpenStreetMap (cargar el mapa y
# encontrar el nodo más cercano a unas coordenadas).
import osmnx as ox

# networkx -> librería de grafos. La usamos para calcular la ruta más corta
# entre dos nodos sumando la longitud real de las calles.
import networkx as nx

# pandas -> maneja tablas (CSV y Excel se leen como DataFrames).
import pandas as pd

# os -> trabaja con rutas del sistema. Permite que el código funcione en
# cualquier computador sin tener que escribir rutas fijas tipo "C:/Users/...".
import os


# ==============================================================
# CONFIGURACIÓN DE RUTAS (se calculan automáticamente)
# ==============================================================
# La idea es que el programa encuentre solo los archivos del proyecto, sin
# importar dónde lo haya descargado cada compañero del equipo.

# Carpeta donde está guardado este archivo (grafo.py).
DIRECTORIO_SCRIPT = os.path.dirname(os.path.abspath(__file__))

# Sube un nivel para llegar a la raíz del proyecto.
DIRECTORIO_PROYECTO = os.path.dirname(DIRECTORIO_SCRIPT)

# Rutas absolutas a cada archivo de datos.
RUTA_GRAPHML        = os.path.join(DIRECTORIO_PROYECTO, "datos", "area_metropolitana.graphml")
RUTA_ELECTROLINERAS = os.path.join(DIRECTORIO_PROYECTO, "datos", "electrolineras.csv")
RUTA_ESTADISTICAS   = os.path.join(DIRECTORIO_PROYECTO, "datos", "estadisticas.xlsx")
RUTA_PUNTOS         = os.path.join(DIRECTORIO_PROYECTO, "datos", "puntos_referencia.csv")

# ==============================================================


def cargar_grafo(ruta_archivo):
    """Carga el grafo desde el archivo .graphml y muestra sus estadísticas."""
    # try / except: intenta ejecutar el bloque y si algo falla, no rompe el
    # programa, sino que entra al except y muestra un mensaje claro.
    try:
        print(f"Buscando grafo en la :\n   {ruta_archivo}\n")
        print("Cargando el mapa, esto puede demorar...")

        # osmnx lee el archivo .graphml y lo convierte en un grafo de Python.
        G = ox.load_graphml(ruta_archivo)

        # Los nodos son las intersecciones; las aristas son las calles.
        nodos  = len(G.nodes)
        calles = len(G.edges)

        print("Mapa cargado correctamente.")
        print(f"   Nodos (intersecciones): {nodos}")
        print(f"   Calles (tramos)       : {calles}")

        # return -> devuelve el grafo a quien llamó la función para poder usarlo.
        return G

    except FileNotFoundError:
        # Caso típico: el archivo .graphml no está en la carpeta esperada.
        print(f"Archivo no encontrado: {ruta_archivo}")
        print("   Verificar que el archivo .graphml esté en la carpeta 'datos'.")
        return None
    except Exception as e:
        # Cualquier otro error (archivo corrupto, librería faltante, etc.).
        print(f"Error al cargar el grafo: {e}")
        return None


def encontrar_nodo_cercano(grafo, latitud, longitud):
    """Encuentra el nodo más cercano en el grafo a partir de coordenadas GPS."""
    # Detalle que encontramos: osmnx invierte el orden habitual de leer esto.
    # En GPS se dice (latitud, longitud), pero osmnx pide X=longitud, Y=latitud.
    nodo = ox.distance.nearest_nodes(grafo, X=longitud, Y=latitud)
    return nodo


def procesar_electrolineras(G, ruta_csv):
    """Lee el CSV de electrolineras y asigna el nodo del grafo a cada una."""
    # Estos prints solo son separadores para que la consola se vea ordenada.
    print(f"\n{'='*50}")
    print("Procesando las electrolineras...")
    print(f"   Archivo encontrado en: {ruta_csv}")
    print(f"{'='*50}")

    try:
        # Leemos el CSV como tabla (DataFrame) de pandas.
        # Aquí estás creando un DataFrame, que conceptualmente es parecido a: Un arreglo bidimensional (tabla: filas × columnas), tema viso en clase
        df = pd.read_csv(ruta_csv)
        print(f"   Registros encontrados: {len(df)}")

        # Creamos una nueva columna llamada 'nodo_mapa'.
        # df.apply recorre la tabla fila por fila (axis=1 = por filas).
        # Para cada fila tomamos su latitud y longitud y buscamos el nodo
        # del grafo más cercano. El lambda es una mini-función sin nombre.
        df['nodo_mapa'] = df.apply(
            lambda fila: encontrar_nodo_cercano(G, fila['latitud'], fila['longitud']),
            axis=1
        )

        # Mostramos solo las columnas relevantes, sin el índice de pandas.
        print("\nResultado:")
        print(df[['nombre', 'latitud', 'longitud', 'nodo_mapa']].to_string(index=False))
        return df

    except FileNotFoundError:
        print(f"Archivo no encontrado: {ruta_csv}")
        return None
    except KeyError as e:
        # KeyError aparece cuando falta una columna esperada en el CSV.
        print(f"Columna faltante en el CSV: {e}")
        print("   El CSV debe tener columnas: 'nombre', 'latitud', 'longitud'")
        return None


def procesar_puntos(G, ruta_csv):
    """Lee el CSV de puntos de referencia y asigna nodo del grafo a cada uno."""
    # Esta función hace exactamente lo mismo que procesar_electrolineras,
    # pero aplicado al CSV de puntos de referencia (lugares de origen).
    print(f"\n{'='*50}")
    print("Procesando los puntos de referencia...")
    print(f"   Archivo encontrado en: {ruta_csv}")
    print(f"{'='*50}")

    try:
        df = pd.read_csv(ruta_csv)
        print(f"   Registros encontrados: {len(df)}")

        # Igual que en electrolineras: por cada fila se busca el nodo cercano.
        df['nodo_mapa'] = df.apply(
            lambda fila: encontrar_nodo_cercano(G, fila['latitud'], fila['longitud']),
            axis=1
        )

        print("\nResultado:")
        #Esto se parece a seleccionar columnas de una matriz
        print(df[['nombre', 'latitud', 'longitud', 'nodo_mapa']].to_string(index=False)) 
        return df

    except FileNotFoundError:
        print(f"Archivo no encontrado: {ruta_csv}")
        return None
    except KeyError as e:
        print(f"Columna faltante en el CSV: {e}")
        return None


def procesar_estadisticas(ruta_xlsx):
    """Lee el archivo Excel de estadísticas y muestra un resumen."""
    # Esta función está pensada para cuando P2 entregue los datos estadísticos.
    print(f"\n{'='*50}")
    print("Procesando Estadísticas...")
    print(f"   Archivo: {ruta_xlsx}")
    print(f"{'='*50}")

    try:
        # sheet_name=None -> lee todas las hojas del Excel a la vez.
        # El resultado 'hojas' es un diccionario { "Hoja1": df, "Hoja2": df, ... }
        hojas = pd.read_excel(ruta_xlsx, sheet_name=None, engine='openpyxl')

        print(f"   Hojas encontradas: {list(hojas.keys())}")

        # Recorremos cada hoja y mostramos un resumen rápido.
        for nombre_hoja, df_hoja in hojas.items():
            print(f"\n--- Hoja: '{nombre_hoja}' ({len(df_hoja)} filas x {len(df_hoja.columns)} columnas) ---")
            # head(5) muestra solo las primeras 5 filas, para no saturar la consola.
            print(df_hoja.head(5).to_string(index=False))

        return hojas

    except FileNotFoundError:
        print(f"Archivo no encontrado: {ruta_xlsx}")
        return None
    except Exception as e:
        print(f"Error al leer el Excel: {e}")
        print("   Asegúrate de tener instalado: pip install openpyxl")
        return None


def electrolinera_mas_cercana(grafo, nodo_origen):
    """Devuelve la electrolinera más cercana por carretera al nodo dado.

    Usa Dijkstra (shortest_path_length con peso 'length') sobre el grafo vial,
    leyendo la lista de electrolineras desde 'electrolineras_con_nodos.csv'.
    Retorna un dict con 'nombre', 'nodo' y 'distancia_m', o None si no hay ruta.
    """
    # PRECAUCION: aquí NO se usa el CSV original, sino el ya procesado, porque
    # necesitamos que cada electrolinera tenga la columna 'nodo_mapa'.
    # Ese archivo lo genera procesar_electrolineras().
    ruta_csv = os.path.join(DIRECTORIO_PROYECTO, "datos", "electrolineras_con_nodos.csv")

    print(f"\n{'='*50}")
    print("Buscando electrolinera más cercana por carretera...")
    print(f"   Nodo de origen: {nodo_origen}")
    print(f"{'='*50}")

    try:
        df = pd.read_csv(ruta_csv)
    except FileNotFoundError:
        print(f"Archivo no encontrado: {ruta_csv}")
        print("   Ejecuta primero procesar_electrolineras() para generarlo.")
        return None

    # 'mejor' guarda la mejor electrolinera encontrada hasta el momento.
    # Empieza vacía porque todavía no hemos revisado ninguna.
    mejor = None

    # iterrows() recorre la tabla fila por fila.
    # El '_' significa "este valor existe pero no me interesa" (es el índice).
    for _, fila in df.iterrows():
        # int() porque los nodos del grafo se manejan como números enteros.
        nodo_destino = int(fila['nodo_mapa'])

        try:
            # Distancia REAL por carretera (no en línea recta).
            # weight='length' -> usa los metros de cada calle como peso.
            # NetworkX aplica internamente Dijkstra cuando los pesos son positivos.
            distancia = nx.shortest_path_length(
                grafo, source=nodo_origen, target=nodo_destino, weight='length'
            )
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            # NetworkXNoPath -> no hay ruta entre los dos nodos.
            # NodeNotFound  -> alguno de los nodos no existe en el grafo.
            # En cualquiera de los dos casos, ignoramos esta electrolinera y
            # seguimos con la siguiente, sin caer el programa.
            continue

        # Si todavía no hay candidata, o la distancia actual es menor que la
        # mejor guardada, esta pasa a ser la mejor.
        if mejor is None or distancia < mejor['distancia_m']:
            mejor = {
                'nombre': fila['nombre'],
                'nodo': nodo_destino,
                'distancia_m': distancia,
            }

    # Si después de revisar todas seguimos sin candidata, no hay ruta válida.
    if mejor is None:
        print("No se encontró ruta a ninguna electrolinera.")
        return None

    print(f"Más cercana: {mejor['nombre']}")
    print(f"   Nodo       : {mejor['nodo']}")
    print(f"   Distancia  : {mejor['distancia_m']:.1f} m")
    return mejor

def distancia_entre_nodos(grafo, nodo_a, nodo_b):
    """Devuelve la distancia en metros por carretera entre dos nodos del grafo.
    
    Usa Dijkstra (weight='length') igual que electrolinera_mas_cercana().
    Retorna float con los metros, o None si no hay ruta entre los nodos.
    """
    try:
        # shortest_path_length calcula la suma de los 'length' de cada calle
        # en el camino más corto de nodo_a a nodo_b (Dijkstra internamente).
        return nx.shortest_path_length(grafo, nodo_a, nodo_b, weight='length')
    
    except nx.NetworkXNoPath:
        # No existe ningún camino entre los dos nodos (zonas desconectadas).
        return None
    
    except nx.NodeNotFound:
        # Alguno de los dos nodos no existe en el grafo.
        return None

# ==============================================================
# PROGRAMA PRINCIPAL
# ==============================================================
# El bloque "if __name__ == '__main__':" hace que esta parte solo se ejecute
# cuando se corre grafo.py directamente. Si otro archivo lo importa, no se
# dispara este bloque, y se pueden reutilizar las funciones libremente.

if __name__ == "__main__":

    print("=" * 55)
    print("  SISTEMA DE ELECTROLINERAS - UIS 2026")
    print("=" * 55)

    # 1. Cargar el grafo vial.
    grafo_area = cargar_grafo(RUTA_GRAPHML)

    # Si el grafo no cargó, no tiene sentido continuar.
    if grafo_area is not None:

        # 2. Procesar electrolineras y mapearlas al grafo.
        df_electro = procesar_electrolineras(grafo_area, RUTA_ELECTROLINERAS)

        # 3. Procesar puntos de referencia y mapearlos al grafo.
        df_puntos = procesar_puntos(grafo_area, RUTA_PUNTOS)

        # 4. Procesar el archivo Excel de estadísticas.
        # Está comentado. P2 termina de generar el archivo.
        # datos_estadisticas = procesar_estadisticas(RUTA_ESTADISTICAS)

        # 5. Guardar resultados en CSV (con la columna nodo_mapa ya añadida).
        # index=False evita guardar la columna extra del índice de pandas.
        if df_electro is not None:
            ruta_salida_electro = os.path.join(DIRECTORIO_PROYECTO, "datos", "electrolineras_con_nodos.csv")
            df_electro.to_csv(ruta_salida_electro, index=False)
            print(f"\nEl resultado de guardado en:\n   {ruta_salida_electro}")

        if df_puntos is not None:
            ruta_salida_puntos = os.path.join(DIRECTORIO_PROYECTO, "datos", "puntos_con_nodos.csv")
            df_puntos.to_csv(ruta_salida_puntos, index=False)
            print(f"\nEl resultado de guardado en:\n   {ruta_salida_puntos}")

        # ==========================================================
        # 6. DEMO / PRUEBA RÁPIDA DE electrolinera_mas_cercana()
        # ==========================================================
        # Esta sección es solo una prueba: toma un punto de referencia
        # ("UIS Campus Central" si existe, si no el primero del CSV) y
        # llama a la función para ver qué electrolinera queda más cerca
        # por carretera. NO es necesaria para que el resto del programa
        # funcione: si un compañero quiere desactivarla, debe comentar
        # desde el "if df_puntos is not None..." hasta el último print
        # de "Verificación OK..." (o sea, todo el bloque de abajo).
        #
        # ¿Qué hace electrolinera_mas_cercana(grafo, nodo_origen)?
        #   - Recibe el grafo vial ya cargado y un nodo de partida.
        #   - Recorre todas las electrolineras del CSV procesado y, con
        #     Dijkstra (nx.shortest_path_length, peso='length'), calcula
        #     la distancia REAL por calles desde nodo_origen a cada una.
        #   - Devuelve un dict {nombre, nodo, distancia_m} con la más
        #     cercana, o None si no hay ruta.
        #
        # ¿Cómo modificarla para que el USUARIO ingrese el nodo?
        #   Reemplazar la búsqueda automática por algo como:
        #       nodo_usuario = int(input("Ingrese el nodo de origen: "))
        #       electrolinera_mas_cercana(grafo_area, nodo_usuario)
        #   O, más amigable, pedir el NOMBRE del punto y buscar su nodo:
        #       nombre = input("Punto de origen: ")
        #       fila = df_puntos[df_puntos['nombre'] == nombre].iloc[0]
        #       electrolinera_mas_cercana(grafo_area, int(fila['nodo_mapa']))
        # ==========================================================
        if df_puntos is not None and len(df_puntos) > 0:
            # Filtramos el DataFrame buscando filas cuyo 'nombre' contenga
            # "UIS Campus Central" (case=False -> no distingue mayúsculas;
            # na=False -> ignora celdas vacías sin lanzar error).
            coincidencia = df_puntos[df_puntos['nombre'].str.contains(
                "UIS Campus Central", case=False, na=False
            )]
            # Si encontró el punto lo usa; si no, cae al primero disponible.
            # Esto evita que la demo se rompa si cambian los nombres del CSV.
            punto_demo = coincidencia.iloc[0] if len(coincidencia) > 0 else df_puntos.iloc[0]

            # Mostramos desde dónde estamos buscando, para que en consola
            # quede claro qué punto y qué nodo se le pasó a la función.
            print(f"\nDemo desde '{punto_demo['nombre']}' (nodo {punto_demo['nodo_mapa']}):")

            # Llamada principal: aquí es donde realmente se ejecuta Dijkstra.
            # int(...) porque los nodos del grafo son enteros y pandas a veces
            # los entrega como float64. Guardamos el resultado para verificar.
            resultado = electrolinera_mas_cercana(grafo_area, int(punto_demo['nodo_mapa']))

            # Verificación rápida (sanity check):
            #   - 'nombre' no vacío -> la electrolinera devuelta es real.
            #   - distancia > 0     -> Dijkstra calculó algo con sentido
            #     (si fuera 0, el origen y el destino serían el mismo nodo,
            #      lo cual sería sospechoso en una demo desde la UIS).
            if resultado is not None:
                assert resultado['nombre'], "La electrolinera devuelta no tiene nombre."
                assert resultado['distancia_m'] > 0, "Distancia no válida."
                print("Verificación OK: electrolinera real y distancia con sentido.")

    else:
        print("\nNo se puede continuar sin el grafo vial.")
