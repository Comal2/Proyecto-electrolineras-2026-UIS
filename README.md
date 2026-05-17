# Proyecto-electrolineras-2026-UIS
Sistema de infraestructura de puntos de carga - UIS 2026

## Librerías utilizadas

![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-150458?style=flat&logo=pandas)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-orange?style=flat&logo=scikitlearn)
![NetworkX](https://img.shields.io/badge/NetworkX-Grafos-1f425f?style=flat)
![OSMnx](https://img.shields.io/badge/OSMnx-Mapas-success?style=flat)
![Folium](https://img.shields.io/badge/Folium-Mapas_HTML-77B829?style=flat)
![OpenPyXL](https://img.shields.io/badge/OpenPyXL-Excel-217346?style=flat)
![Versión](https://img.shields.io/badge/Versión-Final-blue?style=for-the-badge)
![Estado](https://img.shields.io/badge/Estado-Completado-brightgreen?style=for-the-badge)

| Librería | Uso |
|---|---|
| pandas | Manejo de datos y exportación |
| scikit-learn | Modelo de Machine Learning |
| networkx | Grafos y rutas |
| osmnx | Carga de mapas reales |
| folium | Visualización interactiva |
| openpyxl | Exportación a Excel |

### Librerías estándar

Incluidas con Python:

- os  
- json  
- random

## ¿Qué problema resuelve este proyecto?

¿Dónde deberían ubicarse nuevas electrolineras para minimizar recorridos y cubrir mejor la demanda en Bucaramanga?

**Sistema de Simulación de Vehículos Eléctricos**. Este proyecto en Python modela el flujo y consumo de energía de vehículos eléctricos (alta y baja gama) a través de las calles reales del área metropolitana de Bucaramanga. 

Nuestro objetivo final es utilizar los datos generados por la simulación para **entrenar un modelo de Inteligencia Artificial** que prediga las ubicaciones más estratégicas para futuras estaciones de carga.

---
## Instalación y ejecución

Antes de ejecutar el proyecto, instala las dependencias:

```bash
pip install pandas scikit-learn networkx osmnx folium openpyxl
```

```bash
python main.py #esto depende de donde y como se ejecute
```

---

### Archivos requeridos (esto también es clave)


## Archivos necesarios

La carpeta `datos/` debe contener:

```
datos/
├── area\_metropolitana.graphml
├── electrolineras.csv
├── puntos\_referencia.csv
├── vehiculos.json
```

Si alguno falta, el sistema falla.

## Outputs
### Archivos generados

El sistema produce automáticamente:

```markdown
- `estadisticas.csv`
- `estadisticas.json`
- `estadisticas.xlsx`
- `predicciones_demanda.json`
- `mapa_con_demanda.html`

```

***

## Arquitectura (simple)

### Estructura del proyecto

```markdown
main.py
│
├── simulacion.py
├── grafo.py
├── modelo\_ml.py
├── mapa.py

```

---

## Flujo de ejecución del sistema

El sistema sigue este orden lógico:

### 1. Cargar grafo (OBLIGATORIO)
Opción 1 → Subopción 1

- Carga `area_metropolitana.graphml`
- Genera archivos con nodos si no existen:
  - `electrolineras_con_nodos.csv`
  - `puntos_con_nodos.csv`

Sin este paso, el sistema no funciona.

---

### 2. Simulación de recorridos
Opción 1 → Subopción 2

- Genera recorridos aleatorios
- Exporta:
  - `estadisticas.csv`
  - `estadisticas.json`
  - `estadisticas.xlsx`

---

### 3. Modelo de Machine Learning
Opción 3

- Lee `estadisticas.csv`
- Entrena modelo predictivo
- Genera:
  - `predicciones_demanda.json`
  - `mapa_con_demanda.html`

---

### 4. Consulta de estadísticas
Opción 2

- Usa `estadisticas.csv` ya generado

---

## Características Principales

- **Mapeo real:** Uso de grafos viales del área metropolitana mediante `OSMnx` y `NetworkX`.
- **Consumo dinámico:** Simulación del uso de batería según distancia y tipo de vehículo.
- **Enrutamiento:** Cálculo de rutas más cortas hacia la electrolinera más cercana cuando la batería alcanza niveles críticos.
- **Generación de datos:** Exportación automática de resultados en `.csv`, `.json` y `.xlsx`.
- **Modelo predictivo:** Análisis de demanda para estimar ubicaciones estratégicas de nuevas estaciones.
- **Visualización:** Generación de mapas interactivos en `Folium` para análisis de rutas y demanda.

---

> **Seguimiento del proyecto**  
> El plan de trabajo, distribución de roles y cronograma ejecutado durante el desarrollo del proyecto puede consultarse en el siguiente documento:  
> 👉 **[Ver cronograma de trabajo](CRONOGRAMAS_&&_INSTRUCCIONES/CRONOGRAMA.md)**

---
