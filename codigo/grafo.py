import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import os

# ── Configuración ──────────────────────────────────
GRAPHML_PATH = os.path.join("datos", "area_metropolitana.graphml")
IMAGEN_PATH  = os.path.join("resultados", "mapa_con_nodos.png")

# Tus puntos de carga (Electrolineras)
ELECTROLINERAS = [
    ("E1 Homecenter", 7.1166407, -73.1201270),
    ("E2 Quinta Etapa", 7.1154206, -73.1076613),
    ("E3 Cacique", 7.0992906, -73.1071340),
    ("E4 Canaveral", 7.0708246, -73.1062650),
    ("E5 Terpel Piedecuesta", 6.9980135, -73.0521321),
    ("E6 Éxito La Rosita", 7.1133560, -73.1231384),
    ("E7 La Florida", 7.0696035, -73.1052876),
    ("E8 Oriente", 7.0853656, -73.1646908)
]

# Tus Puntos de Interés (Universidades y otros)
PUNTOS_CLAVE = [
    ("P1 UIS Central", 7.1388520, -73.1202742),
    ("P2 UIS Florida", 7.0616660, -73.0885503),
    ("P3 UIS Guatiguará", 6.9946863, -73.0666782),
    ("P4 UIS Bucarica", 7.1197422, -73.1230935),
    ("P5 Cenfer", 7.0825632, -73.1540915),
    ("P6 UNAB", 7.1170079, -73.1045411),
    ("P7 UTS", 7.1051693, -73.1238175),
    ("P8 UPB", 7.0385418, -73.0721803),
    ("P9 PTAR", 7.0656181, -73.1280572),
    ("P10 Hacienda Catay", 6.9760605, -73.0415568)
]

# ── Funciones ──────────────────────────────────────

def descargar_mapa_metropolitano():
    """Descarga el área metropolitana de forma robusta."""
    ox.settings.use_cache = True
    ox.settings.timeout = 1000  # Tiempo amplio para evitar desconexiones
    
    print("🚗 Descargando mapa METROPOLITANO...")
    
    # Método infalible: Pasar la lista directamente a OSMnx
    lugares = [
        "Bucaramanga, Santander, Colombia",
        "Floridablanca, Santander, Colombia", 
        "Girón, Santander, Colombia",
        "Piedecuesta, Santander, Colombia"
    ]
    
    try:
        # Al pasar una lista, OSMnx une los polígonos automáticamente
        G = ox.graph_from_place(lugares, network_type="drive", simplify=True)
        print(f"✅ ÉXITO: {G.number_of_nodes():,} nodos descargados.")
        return G
    except Exception as e:
        print(f"⚠️ Falló la descarga por lugares: {e}")
        print("🔄 Intentando método de Bounding Box como respaldo...")
        
        # Respaldo: BBox amplia (N, S, E, W) adaptada a versiones recientes de OSMnx
        try:
            # Nota: Si usas OSMnx v2.0+, la sintaxis correcta es bbox=(n, s, e, w)
            # Cubre desde el norte de BGA hasta el sur de Piedecuesta
            G = ox.graph_from_bbox(bbox=(7.150, 6.950, -73.000, -73.200), network_type="drive", simplify=True)
            print(f"✅ ÉXITO (BBox): {G.number_of_nodes():,} nodos descargados.")
            return G
        except Exception as ex:
            print(f"❌ Falló también el respaldo: {ex}")
            return None

def cargar_o_descargar():
    os.makedirs("datos", exist_ok=True)
    if os.path.exists(GRAPHML_PATH):
        print(f"📂 Cargando mapa local desde: {GRAPHML_PATH}")
        return ox.load_graphml(GRAPHML_PATH)
    
    G = descargar_mapa_metropolitano()
    if G is not None:
        ox.save_graphml(G, filepath=GRAPHML_PATH)
        print(f"💾 Mapa guardado en: {GRAPHML_PATH}")
    return G

def visualizar_con_nodos(G):
    """Genera la imagen del mapa con tus puntos superpuestos."""
    print("\n🖼️ Generando imagen con nodos...")
    os.makedirs("resultados", exist_ok=True)
    
    # Dibujar el grafo base
    fig, ax = ox.plot_graph(
        G, figsize=(16, 16), node_size=0, 
        edge_linewidth=0.5, edge_color="#999999",
        bgcolor="white", show=False, close=False
    )
    
    # Extraer coordenadas para graficar
    lats_e = [lat for _, lat, _ in ELECTROLINERAS]
    lons_e = [lon for _, _, lon in ELECTROLINERAS]
    
    lats_p = [lat for _, lat, _ in PUNTOS_CLAVE]
    lons_p = [lon for _, _, lon in PUNTOS_CLAVE]

    # Graficar Electrolineras (Rojo)
    ax.scatter(lons_e, lats_e, c='red', s=100, zorder=5, label='Electrolineras', edgecolors='black')
    
    # Graficar Puntos Clave (Azul)
    ax.scatter(lons_p, lats_p, c='blue', s=80, zorder=5, marker='s', label='Puntos Clave (UIS, etc)', edgecolors='black')

    ax.set_title("🗺️ Mapa Vial con Nodos de Carga - Área Metropolitana", fontsize=20, fontweight='bold', pad=20)
    ax.legend(fontsize=12, loc='upper left')
    
    plt.tight_layout()
    plt.savefig(IMAGEN_PATH, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"✅ Imagen generada exitosamente en: {IMAGEN_PATH}")

# ── EJECUCIÓN ──────────────────────────────────────
if __name__ == "__main__":
    print("=" * 50)
    print("🚗 INICIANDO PROCESAMIENTO DE MAPA")
    print("=" * 50)
    
    G = cargar_o_descargar()
    
    if G is not None:
        visualizar_con_nodos(G)
        print("\n🎉 ¡GRAFO LISTO! Ahora puedes extraer o manipular los nodos más cercanos a tus puntos.")
    else:
        print("❌ No se pudo obtener el grafo.")