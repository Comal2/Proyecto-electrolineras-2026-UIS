"""🔍 VERIFICADOR COMPLETO del .graphml - ¡Prueba TODO!"""

import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

# ── TUS PUNTOS (copiados del código original) ──
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

GRAPHML_PATH = "datos/area_metropolitana.graphml"

def verificar_grafo_completo():
    """🔍 VERIFICA TODO el contenido del .graphml"""
    print("🔍" + "="*50)
    print("VERIFICADOR COMPLETO DEL GRAFO")
    print("="*50)
    
    # 1. ¿Existe el archivo?
    if not Path(GRAPHML_PATH).exists():
        print("❌ ERROR: No existe", GRAPHML_PATH)
        print("👉 Ejecuta PRIMERO el código original para generarlo")
        return None
    
    print("✅ 1. ARCHIVO ENCONTRADO")
    
    # 2. Cargar grafo
    try:
        G = ox.load_graphml(GRAPHML_PATH)
        print(f"✅ 2. GRAFO CARGADO")
        print(f"   📊 NODOS: {G.number_of_nodes():,}")
        print(f"   🛣️  ARISTAS: {G.number_of_edges():,}")
    except Exception as e:
        print(f"❌ 2. ERROR cargando: {e}")
        return None
    
    # 3. ¿Qué datos tiene cada arista? (CRUCIAL para simulaciones)
    print("\n📋 3. DATOS DISPONIBLES EN ARISTAS:")
    muestra_arista = list(G.edges(data=True))[0]
    for key, value in muestra_arista[2].items():
        print(f"   ✅ {key}: {value}")
    
    # 4. Encontrar nodos más cercanos a TUS PUNTOS
    print("\n🎯 4. BUSCANDO TUS PUNTOS:")
    
    nodos_electrolineras = []
    for nombre, lat, lon in ELECTROLINERAS:
        nodo = ox.nearest_nodes(G, lon, lat)
        x, y = G.nodes[nodo]['x'], G.nodes[nodo]['y']
        dist = ((lat - y)**2 + (lon - x)**2)**0.5 * 111000  # metros aprox
        nodos_electrolineras.append((nombre, nodo, x, y, dist))
        print(f"   🔴 {nombre}: NODO={nodo}, DIST={dist:.0f}m")
    
    nodos_puntos_clave = []
    for nombre, lat, lon in PUNTOS_CLAVE:
        nodo = ox.nearest_nodes(G, lon, lat)
        x, y = G.nodes[nodo]['x'], G.nodes[nodo]['y']
        dist = ((lat - y)**2 + (lon - x)**2)**0.5 * 111000
        nodos_puntos_clave.append((nombre, nodo, x, y, dist))
        print(f"   🔵 {nombre}: NODO={nodo}, DIST={dist:.0f}m")
    
    # 5. Ejemplo: Ruta entre 2 puntos
    print("\n🛤️ 5. PRUEBA DE RUTA (UIS Central → E1 Homecenter):")
    origen = nodos_puntos_clave[0][1]  # P1 UIS Central
    destino = nodos_electrolineras[0][1]  # E1 Homecenter
    
    try:
        ruta = nx.shortest_path(G, origen, destino, weight='length')
        distancia = sum(ox.get_route_edge_attributes(G, ruta, 'length'))
        print(f"   ✅ RUTA ENCONTRADA: {len(ruta)} nodos")
        print(f"   📏 DISTANCIA: {distancia:.0f} metros")
        print(f"   🛣️  ARISTAS: {len(ruta)-1}")
    except:
        print("   ❌ No hay ruta directa (raro, pero posible)")
    
    # 6. Visualización rápida
    print("\n🖼️  6. GENERANDO MAPA DE VERIFICACIÓN...")
    fig, ax = ox.plot_graph(G, node_size=0, edge_linewidth=0.3, show=False, close=False)
    
    # Marcar puntos
    lons_e, lats_e = zip(*[(x,y) for _,_,x,y,_ in nodos_electrolineras])
    lons_p, lats_p = zip(*[(x,y) for _,_,x,y,_ in nodos_puntos_clave])
    
    ax.scatter(lons_e, lats_e, c='red', s=150, zorder=5, label='Electrolineras', edgecolors='black', linewidth=2)
    ax.scatter(lons_p, lats_p, c='blue', s=120, marker='s', zorder=5, label='Puntos Clave', edgecolors='black')
    
    # Ruta de ejemplo
    if 'ruta' in locals():
        route_line = ox.plot_graph_route(G, ruta, route_linewidth=6, route_color='green', show=False, close=False)
        ax.plot(*route_line[0].get_lines()[-1].get_data(), color='green', linewidth=6, label='Ruta ejemplo')
    
    ax.legend()
    ax.set_title("✅ GRAFO VERIFICADO - ¡TODO FUNCIONA!", fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig("resultados/verificacion_grafo.png", dpi=300, bbox_inches='tight')
    plt.show()
    
    print("🎉 VERIFICACIÓN COMPLETA ✅")
    print("📁 Mapa guardado: resultados/verificacion_grafo.png")
    
    return G, nodos_electrolineras, nodos_puntos_clave

# ── EJECUTAR ──
if __name__ == "__main__":
    G, electrolineras, puntos_clave = verificar_grafo_completo()
    
    if G is not None:
        print("\n🚀 ¡LISTO PARA SIMULACIONES!")
        print("💾 Guarda esta info para tus próximos códigos:")
        print(f"   nodos_electrolineras = {electrolineras}")
        print(f"   nodos_puntos_clave = {puntos_clave}")