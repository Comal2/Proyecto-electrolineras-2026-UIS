import osmnx as ox
import pandas as pd
import os

# ==============================================================
# CONFIGURACIÓN DE RUTAS (Se calculan automáticamente)
# ==============================================================

# Obtiene la carpeta donde está guardado ESTE archivo (grafo.py)
DIRECTORIO_SCRIPT = os.path.dirname(os.path.abspath(__file__))

# Sube un nivel para llegar a la raíz del proyecto
DIRECTORIO_PROYECTO = os.path.dirname(DIRECTORIO_SCRIPT)

# Construye las rutas absolutas a cada archivo
RUTA_GRAPHML        = os.path.join(DIRECTORIO_PROYECTO, "datos", "area_metropolitana.graphml")
RUTA_ELECTROLINERAS = os.path.join(DIRECTORIO_PROYECTO, "datos", "electrolineras.csv")
RUTA_ESTADISTICAS   = os.path.join(DIRECTORIO_PROYECTO, "datos", "estadisticas.xlsx")
RUTA_PUNTOS         = os.path.join(DIRECTORIO_PROYECTO, "datos", "puntos_referencia.csv")

# ==============================================================


def cargar_grafo(ruta_archivo):
    """Carga el grafo desde el archivo .graphml y muestra sus estadísticas."""
    try:
        print(f"📂 Buscando grafo en:\n   {ruta_archivo}\n")
        print("⏳ Cargando el mapa, esto puede tomar unos segundos...")
        
        G = ox.load_graphml(ruta_archivo)
        
        nodos  = len(G.nodes)
        calles = len(G.edges)
        
        print(f"✅ Mapa cargado con éxito.")
        print(f"   📍 Nodos (Intersecciones): {nodos}")
        print(f"   🛣️  Calles (Tramos)       : {calles}")
        return G
    
    except FileNotFoundError:
        print(f"❌ Archivo no encontrado: {ruta_archivo}")
        print("   Verifica que el archivo .graphml esté en la carpeta 'datos'.")
        return None
    except Exception as e:
        print(f"❌ Error al cargar el grafo: {e}")
        return None


def encontrar_nodo_cercano(grafo, latitud, longitud):
    """Encuentra el nodo más cercano en el grafo a partir de coordenadas GPS."""
    # OJO: osmnx usa X=longitud, Y=latitud (orden invertido al convencional)
    nodo = ox.distance.nearest_nodes(grafo, X=longitud, Y=latitud)
    return nodo


def procesar_electrolineras(G, ruta_csv):
    """Lee el CSV de electrolineras y asigna el nodo del grafo a cada una."""
    print(f"\n{'='*50}")
    print("⚡ Procesando Electrolineras...")
    print(f"   Archivo: {ruta_csv}")
    print(f"{'='*50}")
    
    try:
        df = pd.read_csv(ruta_csv)
        print(f"   Registros encontrados: {len(df)}")
        
        # Busca el nodo más cercano para cada fila
        df['nodo_mapa'] = df.apply(
            lambda fila: encontrar_nodo_cercano(G, fila['latitud'], fila['longitud']),
            axis=1
        )
        
        print("\n📋 Resultado:")
        print(df[['nombre', 'latitud', 'longitud', 'nodo_mapa']].to_string(index=False))
        return df
    
    except FileNotFoundError:
        print(f"❌ Archivo no encontrado: {ruta_csv}")
        return None
    except KeyError as e:
        print(f"❌ Columna faltante en el CSV: {e}")
        print("   El CSV debe tener columnas: 'nombre', 'latitud', 'longitud'")
        return None


def procesar_puntos(G, ruta_csv):
    """Lee el CSV de puntos de referencia y asigna nodo del grafo a cada uno."""
    print(f"\n{'='*50}")
    print("📍 Procesando Puntos de Referencia...")
    print(f"   Archivo: {ruta_csv}")
    print(f"{'='*50}")

    try:
        df = pd.read_csv(ruta_csv)
        print(f"   Registros encontrados: {len(df)}")

        df['nodo_mapa'] = df.apply(
            lambda fila: encontrar_nodo_cercano(G, fila['latitud'], fila['longitud']),
            axis=1
        )

        print("\n📋 Resultado:")
        print(df[['nombre', 'latitud', 'longitud', 'nodo_mapa']].to_string(index=False))
        return df

    except FileNotFoundError:
        print(f"❌ Archivo no encontrado: {ruta_csv}")
        return None
    except KeyError as e:
        print(f"❌ Columna faltante en el CSV: {e}")
        return None


def procesar_estadisticas(ruta_xlsx):
    """Lee el archivo Excel de estadísticas y muestra un resumen."""
    print(f"\n{'='*50}")
    print("📊 Procesando Estadísticas...")
    print(f"   Archivo: {ruta_xlsx}")
    print(f"{'='*50}")
    
    try:
        # Carga todas las hojas del Excel
        hojas = pd.read_excel(ruta_xlsx, sheet_name=None, engine='openpyxl')
        
        print(f"   Hojas encontradas: {list(hojas.keys())}")
        
        for nombre_hoja, df_hoja in hojas.items():
            print(f"\n--- Hoja: '{nombre_hoja}' ({len(df_hoja)} filas x {len(df_hoja.columns)} columnas) ---")
            print(df_hoja.head(5).to_string(index=False))  # Muestra primeras 5 filas
        
        return hojas
    
    except FileNotFoundError:
        print(f"❌ Archivo no encontrado: {ruta_xlsx}")
        return None
    except Exception as e:
        print(f"❌ Error al leer el Excel: {e}")
        print("   Asegúrate de tener instalado: pip install openpyxl")
        return None


# ==============================================================
# PROGRAMA PRINCIPAL
# ==============================================================

if __name__ == "__main__":
    
    print("=" * 55)
    print("  SISTEMA DE ELECTROLINERAS - UIS 2026")
    print("=" * 55)
    
    # 1. Cargar el grafo vial
    grafo_area = cargar_grafo(RUTA_GRAPHML)
    
    if grafo_area is not None:
        
        # 2. Procesar electrolineras y mapearlas al grafo
        df_electro = procesar_electrolineras(grafo_area, RUTA_ELECTROLINERAS)
        
        # 3. Procesar puntos de referencia y mapearlos al grafo
        df_puntos = procesar_puntos(grafo_area, RUTA_PUNTOS)
        
        # 4. Procesar el archivo Excel de estadísticas
        datos_estadisticas = procesar_estadisticas(RUTA_ESTADISTICAS)
        
        # 5. Guardar resultados
        if df_electro is not None:
            ruta_salida_electro = os.path.join(DIRECTORIO_PROYECTO, "datos", "electrolineras_con_nodos.csv")
            df_electro.to_csv(ruta_salida_electro, index=False)
            print(f"\n💾 Resultado guardado en:\n   {ruta_salida_electro}")
            
        if df_puntos is not None:
            ruta_salida_puntos = os.path.join(DIRECTORIO_PROYECTO, "datos", "puntos_con_nodos.csv")
            df_puntos.to_csv(ruta_salida_puntos, index=False)
            print(f"\n💾 Resultado guardado en:\n   {ruta_salida_puntos}")
    
    else:
        print("\n⚠️  No se puede continuar sin el grafo vial.")