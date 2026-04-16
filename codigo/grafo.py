"""
grafo.py - Cargar mapa de Bucaramanga
Descarga el mapa desde OpenStreetMap, lo convierte 
en grafo y lo guarda localmente.
"""

import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import os
import time


# ── Configuración ──────────────────────────────────
GRAPHML_PATH = os.path.join("datos", "area_metropolitana.graphml")
IMAGEN_PATH  = os.path.join("resultados", "mapa_area_metropolitana.png")

# Bounding box del área metropolitana
# Cubre: Bucaramanga, Floridablanca, Girón, Piedecuesta
BBOX = {
    "north": 7.2045,
    "south": 6.9682,
    "west":  -73.2170,
    "east":  -73.0357
}

# ── Funciones ──────────────────────────────────────

def descargar_mapa():
    """Descarga el mapa del área metropolitana desde OpenStreetMap."""

    print("Descargando area metropolitana de Bucaramanga...")
    print("Cubre: Bucaramanga, Floridablanca, Giron, Piedecuesta")
    print("(Requiere internet, puede tardar 2-5 minutos)\n")

    # Intento 1: por bounding box (más preciso para áreas grandes)
    try:
        print("Metodo 1: por bounding box...")
        inicio = time.time()
        G = ox.graph_from_bbox(
            bbox=(BBOX["north"], BBOX["south"], 
                  BBOX["east"],  BBOX["west"]),
            network_type="drive"
        )
        print(f"Listo en {time.time() - inicio:.1f}s")
        return G
    except Exception as e:
        print(f"Fallo: {e}")

    # Intento 2: por nombre de cada municipio
    try:
        print("Metodo 2: por nombre del area...")
        inicio = time.time()
        G = ox.graph_from_place(
            ["Bucaramanga, Santander, Colombia",
             "Floridablanca, Santander, Colombia",
             "Giron, Santander, Colombia",
             "Piedecuesta, Santander, Colombia"],
            network_type="drive"
        )
        print(f"Listo en {time.time() - inicio:.1f}s")
        return G
    except Exception as e:
        print(f"Fallo: {e}")

    print("No se pudo descargar el mapa.")
    return None

def cargar_mapa():
    """
    Carga el mapa: si ya existe el archivo local lo usa,
    si no lo descarga y lo guarda.
    """

    if os.path.exists(GRAPHML_PATH):
        print(f"Cargando mapa desde archivo local: {GRAPHML_PATH}")
        G = ox.load_graphml(GRAPHML_PATH)
        print(f"Cargado: {G.number_of_nodes():,} nodos, {G.number_of_edges():,} aristas")
        return G
    else:
        G = descargar_mapa()
        if G is not None:
            os.makedirs("datos", exist_ok=True)
            ox.save_graphml(G, filepath=GRAPHML_PATH)
            print(f"Mapa guardado en: {GRAPHML_PATH}")
            print("La proxima vez carga sin internet.")
        return G


def mostrar_info(G):
    """Muestra estadísticas básicas del grafo."""

    print("\n── Informacion del grafo ──────────────────")
    print(f"Nodos (intersecciones): {G.number_of_nodes():,}")
    print(f"Aristas (calles):       {G.number_of_edges():,}")

    if nx.is_strongly_connected(G):
        print("Conectividad: Fuertemente conexo")
    else:
        comps = list(nx.strongly_connected_components(G))
        mayor = max(comps, key=len)
        print(f"Componentes: {len(comps)} | Mayor: {len(mayor):,} nodos")

    nodos = list(G.nodes(data=True))
    lats = [d['y'] for _, d in nodos]
    lons = [d['x'] for _, d in nodos]
    print(f"Latitud:  {min(lats):.4f} a {max(lats):.4f}")
    print(f"Longitud: {min(lons):.4f} a {max(lons):.4f}")
    print("───────────────────────────────────────────")


def guardar_imagen(G):
    """Genera y guarda una imagen PNG del mapa."""

    print("\nGenerando imagen del mapa...")
    os.makedirs("resultados", exist_ok=True)

    fig, ax = ox.plot_graph(
        G,
        figsize=(12, 12),
        node_size=0,
        edge_linewidth=0.5,
        edge_color="#2196F3",
        bgcolor="white",
        show=False,
        close=False
    )

    ax.set_title(
        "Mapa Vial de Bucaramanga - OpenStreetMap",
        fontsize=16, fontweight='bold'
    )

    plt.tight_layout()
    plt.savefig(IMAGEN_PATH, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Imagen guardada: {IMAGEN_PATH}")


# ── Ejecución ──────────────────────────────────────

if __name__ == "__main__":

    print("=" * 45)
    print("  GRAFO.PY - Mapa de Bucaramanga")
    print("=" * 45 + "\n")

    G = cargar_mapa()

    if G is None:
        print("Error: no se pudo cargar el mapa.")
    else:
        mostrar_info(G)
        guardar_imagen(G)
        print("\nGrafo listo para usar en el proyecto.")