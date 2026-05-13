# Proyecto-electrolineras-2026-UIS
Sistema de infraestructura de puntos de carga - UIS 2026

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![OSMnx](https://img.shields.io/badge/OSMnx-Grafos_Viales-success?style=for-the-badge)
![Machine Learning](https://img.shields.io/badge/Machine_Learning-Scikit_Learn-orange?style=for-the-badge)
![Status](https://img.shields.io/badge/Estado-En_Desarrollo-yellow?style=for-the-badge)

**Sistema de Simulación de Vehículos Eléctricos**. Este proyecto en Python modela el flujo y consumo de energía de vehículos eléctricos (alta y baja gama) a través de las calles reales del área metropolitana de Bucaramanga. 

Nuestro objetivo final es utilizar los datos generados por la simulación para **entrenar un modelo de Inteligencia Artificial** que prediga las ubicaciones más estratégicas para futuras estaciones de carga.

---

> [!IMPORTANT]  
> 📅 **¡ATENCIÓN EQUIPO Y REVISORES!** 📅  
> Toda la planificación, roles, fechas clave y las reuniones semanales están detalladas en nuestro documento de seguimiento.  
> 👉 **[CLIC AQUÍ PARA VER EL CRONOGRAMA DE ENTREGAS](CRONOGRAMAS_&&_INSTRUCCIONES/CRONOGRAMA.md)** 👈

---

## Características Principales

* 🗺️ **Mapeo Real:** Extracción y uso de grafos viales reales utilizando la API de OpenStreetMap (`OSMnx` y `NetworkX`).
* 🔋 **Consumo Dinámico:** Simulación de desgaste de batería según distancias reales y características técnicas de los vehículos.
* 📍 **Enrutamiento Inteligente:** Algoritmo de búsqueda de rutas más cortas para redirigir automáticamente los vehículos a la electrolinera más cercana cuando la batería cae al 20%.
* 📊 **Generación de Datos:** Registro automático de estadísticas de uso en formatos `.csv`, `.json` y `.xlsx`.
* 🤖 **Machine Learning:** Análisis predictivo de demanda espacial para sugerir la instalación de nuevas estaciones de carga.
* 🌍 **Visualización Interactiva:** Mapas renderizados en `Folium`/`Plotly` para observar las rutas y predicciones. *por confirmar
