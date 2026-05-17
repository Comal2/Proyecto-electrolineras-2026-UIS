# Cronograma y plan de trabajo

![Estado](https://img.shields.io/badge/estado-finalizado-green)
![Entrega Código](https://img.shields.io/badge/código-18%20mayo%202026-red)
![Entrega PPT](https://img.shields.io/badge/PPT-26%20mayo%202026-blue)
![Equipo](https://img.shields.io/badge/equipo-3%20personas-informational)

## Sistema de Electrolineras — Área Metropolitana de Bucaramanga
**Universidad Industrial de Santander | Semestre 2026-1**

| Entrega | Fecha límite |
|---|---|
| Código completo del proyecto | Lunes 18 de mayo de 2026 — 23:55 |
| Presentación PPT | Lunes 26 de mayo de 2026 — 20:00 |

---

## Estado actual — Pre-Semana 1 (antes del 3 de mayo de 2026)

### Persona 1 — Líder / Grafo
- Archivo `area_metropolitana.graphml` generado y funcional (nodos, calles, sentidos y pesos, ==grafo dirigido ponderado==).
- `grafo.py` carga el grafo, procesa electrolineras y puntos, y guarda los resultados.
- `datos/electrolineras_con_nodos.csv` generado (8 electrolineras con columna `nodo_mapa`).
- `datos/puntos_con_nodos.csv` generado (10 puntos con columna `nodo_mapa`).
- **Bug pendiente:** error `File is not a zip file` al leer `estadisticas.xlsx`. La función `procesar_estadisticas()` hay que comentarla hasta que P2 genere el archivo real.

### Persona 2 — Simulación
- Lectura del archivo `vehiculos.json` funcionando.
- Lógica de consumo de batería implementada (fórmula `(km / autonomia) * 100`).
- Trigger de alerta al 20% de batería funcionando.
- **Pendiente de corrección:** Pull Request subido directo a `main`, hay que moverlo a la rama `feature/simulacion`.
- El código debe convertirse en clase `Vehiculo` importable (ahora mismo es un script suelto).
- Función `recargar()` no implementada (reseteo de batería y contador de recargas).
- Simulación de recorridos aleatorios no implementada.
- Generación de estadísticas en `.csv`, `.json`, `.xlsx` no implementada.

### Persona 3 — ML + Visualización + Menú
- Archivo `main.py` con menú base creado.
- **Atrasado:** el menú no está conectado a los otros módulos (`grafo.py`, `simulacion.py`, `modelo_ml.py`).
- **Atrasado:** no ha probado que `scikit-learn` esté instalado y funcionando.
- **Atrasado:** no ha probado que `folium` esté instalado y funcionando.
- **Atrasado:** `modelo_ml.py` no tiene estructura ni código base.
- Mapa interactivo Folium no iniciado.
- Modelo ML no iniciado.

---

## Itinerario — Del 4 de mayo al 26 de mayo de 2026

---

## SEMANA 1 — Del 4 al 8 de mayo
### *Objetivo: dejar cada módulo funcional de forma independiente*

---

### Persona 1 — Tareas del 4 al 8 de mayo

#### Lunes 4 mayo
**Corregir el bug del Excel en `grafo.py`**

Buscar la línea que llama a `procesar_estadisticas()` y ponerle un `#` al inicio para desactivarla por ahora. El Excel todavía está vacío porque P2 no ha generado datos reales. Cuando los tenga, se vuelve a activar la línea.
```python
# datos_estadisticas = procesar_estadisticas(RUTA_ESTADISTICAS)  # Activar cuando P2 genere datos
```
Verificar que `grafo.py` corre de principio a fin sin errores.

#### Martes 5 — Miércoles 6 mayo
**Implementar `electrolinera_mas_cercana(grafo, nodo_origen)` en `grafo.py`**

La función recibe el nodo actual del vehículo y devuelve cuál de las 8 electrolineras queda más cerca por carretera (no en línea recta).

Pasos:
1. Cargar `electrolineras_con_nodos.csv` para tener la lista de nodos de las 8 electrolineras.
2. Para cada electrolinera, calcular la distancia desde `nodo_origen` con Dijkstra (`networkx.shortest_path_length`).
3. Retornar el nombre y nodo de la electrolinera con menor distancia.

#### Jueves 7 mayo
**Probar la función con nodos reales**

Tomar un nodo cualquiera del grafo (por ejemplo el de `UIS Campus Central` del archivo `puntos_con_nodos.csv`) y llamar la función. Verificar que devuelve una electrolinera real y una distancia con sentido (entre 500m y 15km aproximadamente).

#### Viernes 8 mayo
**Commit y push a rama `feature/grafo`**
```bash
git add codigo/grafo.py
git commit -m "feat: función electrolinera_mas_cercana con Dijkstra"
git push origin feature/grafo
```
Avisar a P2 que la función ya está lista para integrarla en la simulación.

---

### Persona 2 — Tareas del 4 al 8 de mayo

#### Lunes 4 mayo
**Mover el código a la rama correcta y convertirlo en clase**

Primero crear la rama:
```bash
git checkout -b feature/simulacion # Si ya existe, ignorar
```

Luego reestructurar el código actual como clase `Vehiculo`. La lógica de consumo ya está bien, solo hay que reorganizarla. La clase debe tener:
- `__init__()`: recibe el diccionario de un vehículo del JSON y guarda sus atributos.
- `consumir(km)`: descuenta batería y retorna `True` si llegó al 20%.
- `recargar()`: vuelve la batería a 100%, resetea el aviso y suma 1 al contador de recargas.

#### Martes 5 mayo
**Implementar la simulación de recorridos aleatorios**

La simulación funciona así:
1. Cargar el JSON de vehículos y crear un objeto `Vehiculo` para cada uno.
2. Tener la lista de nodos de los 10 puntos de referencia (del archivo `puntos_con_nodos.csv`).
3. Escoger un punto de origen y un punto de destino aleatorios (distintos).
4. Calcular la distancia entre ellos (P1 da esa función, o usar valor simulado por ahora).
5. Llamar `vehiculo.consumir(distancia)`.
6. Si retorna `True`, llamar `vehiculo.recargar()` y registrar qué electrolinera se usó.
7. Repetir `n` veces (mínimo 20 recorridos por vehículo por ahora).

#### Miércoles 6 mayo
**Guardar estadísticas en archivos**

Cada vez que un vehículo recargue, guardar una fila en una lista con:
- Nombre del vehículo o ID.
- ID de la electrolinera usada.
- Porcentaje de batería al momento de recargar.
- Número de recorrido (1, 2, 3...).

Al terminar todos los recorridos, guardar esa lista en tres formatos:
```python
import pandas as pd

df = pd.DataFrame(registros)
df.to_csv("datos/estadisticas.csv", index=False)
df.to_json("datos/estadisticas.json", orient="records", indent=2)
df.to_excel("datos/estadisticas.xlsx", index=False) # Código de referencia nada más
```

#### Jueves 7 — Viernes 8 mayo
**Verificar que los 3 archivos se generan bien**

Correr la simulación completa y abrir cada archivo para confirmar que tienen datos reales, no están vacíos y las columnas tienen sentido. Hacer commit:
```bash
git add codigo/simulacion.py datos/estadisticas.*
git commit -m "feat: clase Vehiculo, simulación completa, estadísticas generadas"
git push origin feature/simulacion
```

---

### Persona 3 — Tareas del 4 al 8 de mayo

> Esta semana P3 tiene el trabajo acumulado de semanas anteriores. Todo lo de abajo es obligatorio para no bloquear la integración final.

#### Lunes 4 mayo
**Verificar instalación de librerías**

Abrir la terminal y ejecutar:
```bash
pip install scikit-learn folium
```
Luego probar que funcionan con estas líneas:
```python
from sklearn.ensemble import RandomForestClassifier
print("scikit-learn OK")

import folium
mapa = folium.Map(location=[7.1254, -73.1198], zoom_start=13)
mapa.save("resultados/prueba.html")
print("folium OK")
```
Si ambas corren sin error, las librerías están listas.

#### Martes 5 mayo
**Conectar el menú a los módulos reales en `main.py`**

El menú debe importar los otros archivos y llamar sus funciones al seleccionar cada opción. Por ahora las opciones pueden mostrar "En construcción" si la función todavía no existe, pero el menú no debe romperse con ninguna opción:
```python
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from grafo import cargar_grafo, electrolinera_mas_cercana  # funciones de P1
# from simulacion import Vehiculo  # descomentar cuando P2 entregue

def main():
    while True:
        print("\n=== SISTEMA DE ELECTROLINERAS — UIS 2026 ===")
        print("1. Cargar mapa y grafo")
        print("2. Ver electrolineras y puntos de referencia")
        print("3. Simular recorridos de vehículos")
        print("4. Buscar ruta más corta a electrolinera")
        print("5. Ver estadísticas de uso")
        print("6. Modelo predictivo de nuevas electrolineras")
        print("7. Salir")

        opcion = input("\nElige una opción: ").strip()

        if opcion == "1":
            pass  # TODO: llamar cargar_grafo() — el pass es relleno, eliminar cuando esté
        elif opcion == "7":
            print("Saliendo...")
            break
        else:
            print("Opción en construcción.")

        # código de referencia visual nada más
```

#### Miércoles 6 mayo
**Crear estructura base de `modelo_ml.py`**

No hace falta que el modelo funcione todavía, pero el archivo debe tener la estructura clara con comentarios de qué va en cada sección:
```python
# modelo_ml.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

def cargar_datos(ruta_csv):
    """Carga las estadísticas generadas por la simulación."""
    # TODO: implementar cuando P2 entregue estadisticas.csv
    pass

def entrenar_modelo(df):
    """Entrena el modelo con los datos de uso de electrolineras."""
    # TODO: definir features (zona, hora, vehículo) y target (electrolinera)
    pass

def predecir_ubicaciones(modelo, datos_nuevos):
    """Predice qué zonas necesitan nuevas electrolineras."""
    # TODO: implementar predicción
    pass
```

#### Jueves 7 — Viernes 8 mayo
**Crear el mapa base en Folium**

Abrir el mapa de Bucaramanga en el navegador con las 8 electrolineras y 10 puntos marcados. Los datos salen de los CSV que ya generó P1:
```python
import folium
import pandas as pd

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

mapa.save("resultados/mapa_base.html") # código de prueba o referencia visual, no refleja el resultado final
```
Abrir `resultados/mapa_base.html` en el navegador y verificar que aparecen los 18 puntos.

---

## SEMANA 2 — Del 9 al 13 de mayo
### *Objetivo: integrar todo en un solo programa funcional*

---

### Reunión obligatoria — Lunes 9 mayo (30 minutos) *variar solo un poco esta fecha*
**Objetivo:** conectar los tres módulos. Cada persona muestra lo que tiene funcionando y se identifican los puntos de conexión:
- P1 le explica a P2 cómo usar `electrolinera_mas_cercana()`.
- P2 le muestra a P3 la estructura del `estadisticas.csv` para que P3 sepa qué columnas usar en el ML.
- P3 muestra el menú conectado para que todos vean el flujo.

---

### Persona 1 — Tareas del 9 al 13 de mayo

#### Lunes 9 — Martes 10 mayo
**Integrar `grafo.py` y `simulacion.py`**

La simulación de P2 está usando distancias inventadas. Hay que conectarla con el grafo real para que las distancias salgan de calles reales. P1 debe exponer una función `distancia_entre_nodos(grafo, nodo_a, nodo_b)` que P2 pueda llamar desde su simulación.

#### Miércoles 11 — Jueves 12 mayo
**Integrar todo en `main.py` junto con P3**

Cada opción del menú debe llamar a su función real:
- Opción 1 → `cargar_grafo()`
- Opción 3 → `simular_recorridos()`
- Opción 4 → `electrolinera_mas_cercana()`
- Opción 5 → leer y mostrar `estadisticas.csv`
- Opción 6 → `predecir_ubicaciones()`

#### Viernes 13 mayo
**Prueba de flujo completo**

Correr `main.py` de principio a fin sin que se rompa en ninguna opción. Anotar todos los errores que aparezcan.

---

### Persona 2 — Tareas del 9 al 13 de mayo

#### Lunes 9 — Martes 10 mayo
**Reemplazar distancias inventadas por las del grafo real**

Cuando P1 exponga `distancia_entre_nodos()`, reemplazar la lista `distancias = [50, 80, 60, 90...]` por una llamada real al grafo entre dos nodos aleatorios de los puntos de referencia.

#### Miércoles 11 mayo
**Probar la simulación con los 2 vehículos reales**

Correr la simulación con el BMW i4 y el Nissan LEAF por separado. Verificar que:
- El BMW recarga menos veces (mayor autonomía).
- El LEAF recarga más veces.
- Los archivos de estadísticas reflejan esa diferencia.

#### Jueves 12 — Viernes 13 mayo
**Agregar validación de entradas**

Si el usuario ingresa una letra donde va un número, o un número fuera del rango del menú, el programa no debe romperse. Agregar `try/except` en los `input()` de ser necesario.

---

### Persona 3 — Tareas del 9 al 13 de mayo

#### Lunes 9 — Martes 10 mayo
**Entrenar el modelo ML con datos reales**

Cuando P2 genere `estadisticas.csv`, cargar ese archivo y entrenar un `RandomForestClassifier` básico. El modelo recibe como entrada la zona y los km recorridos, y predice qué electrolinera sería la más usada. No tiene que ser perfecto, solo tiene que correr sin errores.

#### Miércoles 11 mayo
**Actualizar el mapa Folium con rutas**

Agregar al mapa las rutas que tomaron los vehículos durante la simulación. Folium permite dibujar líneas entre coordenadas con `folium.PolyLine()`.

#### Jueves 12 — Viernes 13 mayo
**Agregar predicciones del modelo al mapa**

Marcar con un color distinto (uno vistoso) los puntos que el modelo sugiere como posibles ubicaciones para nuevas electrolineras.

---

## FASE FINAL A — Del 14 al 18 de mayo
### *Objetivo: código pulido y subido a Moodle*

---

### Miércoles 14 mayo — Revisión final del código

Todos juntos (1 hora):
- Correr `main.py` de principio a fin sin que se rompa en ninguna opción.
- Verificar que los 3 archivos de estadísticas se generan bien (`.csv`, `.json`, `.xlsx`).
- Verificar que el mapa `.html` abre en el navegador y muestra los 18 puntos.
- Verificar que todas las opciones del menú responden, incluso con entradas incorrectas.

---

### Jueves 15 mayo — Correcciones finales de código

- Cada persona corrige los últimos errores que aparecieron el miércoles en su propio archivo.
- P1 hace merge de todas las ramas a `main` y verifica que el proyecto corre desde cero en un computador limpio.
- Comprimir todo el proyecto en un `.zip`.

---

### Viernes 16 mayo — Buffer

- Día de reserva para imprevistos de último momento.
- Si no hay errores, se usa para empezar a estructurar las diapositivas.

---

### Domingo 17 mayo — Buffer adicional y verificación

- Último día para revisar el `.zip` y confirmar que todo está en orden.
- Si quedó alguna duda con la integración, este es el día para resolverla.

---

### Lunes 18 mayo — ENTREGA 1: Código

- Subir el `.zip` del proyecto a Moodle antes de las 22:00 (no esperar a las 23:55).
- Cada integrante sube individualmente desde su cuenta de Moodle.
- Confirmar por Discord cuando cada uno haya subido, de ser posible.

---

## FASE FINAL B — Del 19 al 26 de mayo
### *Objetivo: presentación lista y subida a Moodle*

> El código ya está entregado. Esta fase es solo para preparar la presentación PPT y practicar la sustentación.

---

### Martes 19 — Miércoles 20 mayo — Preparar diapositivas individuales

Cada persona prepara su bloque de 3 a 4 diapositivas:

**P1:**
- Diapositiva 1: descripción del problema y del área metropolitana.
- Diapositiva 2: cómo se construyó el grafo (OSMnx, qué son nodos y aristas, cuántos hay).
- Diapositiva 3: demostración de `electrolinera_mas_cercana()` con captura de pantalla del resultado real.

**P2:**
- Diapositiva 1: cómo funciona la simulación (diagrama de flujo simple: vehículo → consume → 20% → recarga).
- Diapositiva 2: diferencia entre el BMW i4 y el Nissan LEAF (tabla comparativa de recargas).
- Diapositiva 3: captura del Excel o CSV con las estadísticas generadas.

**P3:**
- Diapositiva 1: cómo funciona el modelo ML explicado sin tecnicismos (qué datos recibe, qué predice).
- Diapositiva 2: captura del mapa interactivo con los 18 puntos y las rutas visibles.
- Diapositiva 3: captura de los puntos sugeridos por el modelo para nuevas electrolineras.

---

### Jueves 21 — Viernes 22 mayo — Unir la presentación

- P1 junta las diapositivas de los tres en un solo archivo `.pptx`.
- Revisar que el orden tenga sentido: introducción → grafo → simulación → ML → conclusiones.
- Agregar portada con nombres, grupo y fecha.
- Subir el `.pptx` al repositorio en `documentos/presentacion_final.pptx`.

---

### Sábado 23 — Domingo 24 mayo — Primer ensayo

- Ensayo completo cronometrado: cada persona explica su sección en máximo 5-10 minutos.
- P1 hace de moderador y toma nota de lo que hay que mejorar.
- Practicar respuestas a posibles preguntas del profesor:
  - ¿Por qué usaron Dijkstra?
  - ¿Qué tan preciso es el modelo ML y cómo lo midieron?
  - ¿Cómo manejan el caso donde no hay ruta entre dos nodos del grafo?
  - ¿Qué pasa si la batería llega a 0% antes de encontrar una electrolinera?

---

### Lunes 25 mayo — Segundo ensayo y ajustes

- Corregir lo que se identificó en el primer ensayo.
- Segundo ensayo completo, esta vez sin leer las diapositivas.
- Ajustar diapositivas si algo no queda claro visualmente.

---

### Martes 26 mayo — ENTREGA 2: Presentación

- Subir el `.pptx` final a Moodle antes de las 19:00 (no esperar a las 20:00).
- Cada integrante sube individualmente desde su cuenta de Moodle.
- Confirmar por Discord cuando cada uno haya subido, de ser posible.

---

## Reglas de trabajo para estas 2 semanas

1. **Nadie sube código directo a `main`.** Siempre en rama propia, siempre avisar antes de hacer merge.
2. **Si alguien se va a atrasar**, avisa con 48 horas de anticipación, no el mismo día del límite. Eso nos complica a todos.
3. **Nadie modifica el archivo de otro** sin avisar primero por Discord.
4. **Los archivos generados** (`.graphml`, `.xlsx`, `.csv` de estadísticas, imágenes `.png`, mapas `.html`) **no se suben a GitHub**. Solo el código fuente y los CSV de datos base. Básicamente, archivos generados: etiquetarlos para no olvidar.
5. **Ante cualquier duda técnica**, preguntarla en las reuniones, no esperar a que bloquee el trabajo.
