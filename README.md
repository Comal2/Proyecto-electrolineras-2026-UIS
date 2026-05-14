# Proyecto-electrolineras-2026-UIS
Sistema de infraestructura de puntos de carga - UIS 2026

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![OSMnx](https://img.shields.io/badge/OSMnx-Mapas_y_Grafos-success?style=for-the-badge)
![NetworkX](https://img.shields.io/badge/NetworkX-Grafos-1f425f?style=for-the-badge)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-150458?style=for-the-badge&logo=pandas)
![Folium](https://img.shields.io/badge/Folium-Mapas_Interactivos-77B829?style=for-the-badge)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine_Learning-orange?style=for-the-badge&logo=scikitlearn)
![OpenPyXL](https://img.shields.io/badge/OpenPyXL-Excel_Processing-217346?style=for-the-badge)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualización-blueviolet?style=for-the-badge)
![Entrega](https://img.shields.io/badge/Entrega-17%2F05%2F2026-red?style=for-the-badge)

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
