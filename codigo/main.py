"""main/menu"""
import pandas as pd
import os
import json
from modelo_ml import cargar_datos, entrenar_modelo, predecir_ubicaciones
from grafo import (
    cargar_grafo, procesar_electrolineras, procesar_puntos,
    RUTA_GRAPHML, RUTA_ELECTROLINERAS, RUTA_PUNTOS,
    RUTA_ELECTROLINERAS_NODOS, RUTA_PUNTOS_NODOS,
)
from mapa import generar_mapa_con_demanda
from simulacion import simular_recorridos

DIRECTORIO_MAIN = os.path.dirname(os.path.abspath(__file__))


    
"""=== MENU PRINCIPAl ==="""
grafo_area = None           #variable global del grafo
while True:
    print("\n=== MENÚ PRINCIPAL ===")
    print("1. Ver mapa y grafo")  
    print("2. Ver estadisticas de uso")
    print("3. Modelo predictivo de nuevas electrolineras")
    print("4. Salir")
    try:
        opcion = int(input("\nElige una opción: "))
    except ValueError:
        print("Opcion invalida, ingrese un numero..")
        continue    

    match(opcion):
        case 1:
            """=== SUBMENU DENTRO DE LA OP 1 ==="""

            def submenu_mapa_grafos_simulacion(): #def funcion del submenu                 
                global grafo_area      #activacion de la variable global
                #esta variable hace que se mantenga incluso fuera del while
                #osea, cuando esta se carga con cargar_grafo(RUTA:GRAPHML) queda asi para todo el script
                while True:
                    print("\n=== SUBMENÚ ===")
                    print("1. Cargar mapa/grafo")
                    print("2. Simular recorridos")
                    print("3. Volver al menu principal")
                    try:
                        sub_opcion = int(input("Elige una opcion: "))
                    except ValueError:
                        print("Opcion invalida, ingrese un numero..")
                        continue    

                    match(sub_opcion):
                        case 1:
                            print("\nCargando mapa/grafo...")
                            grafo_area = cargar_grafo(RUTA_GRAPHML)
                            if grafo_area is not None:                 #validacion del mapa
                                print("mapa listo para usar :) ")
                                
                                if not os.path.exists(RUTA_ELECTROLINERAS_NODOS):
                                    procesar_electrolineras(grafo_area, RUTA_ELECTROLINERAS).to_csv(RUTA_ELECTROLINERAS_NODOS, index=False)

                                if not os.path.exists(RUTA_PUNTOS_NODOS):
                                    procesar_puntos(grafo_area, RUTA_PUNTOS).to_csv(RUTA_PUNTOS_NODOS, index=False)

                        case 2:
                            if grafo_area is None:                      
                                print("ERROR. (primero selecciones la opcion 1)")
                            else:
                                print("\nSimulando recorrido...")
                                simular_recorridos(grafo_area)
                                
                            
                        case 3:
                            print("\nVolviendo al menu")
                            break
                        case _:
                            print("Opcion invalida")

            submenu_mapa_grafos_simulacion()            # <- Llamamos la fun que definimos
                   
        
        case 2:
            print("\nMostrando estadisticas...")
            if grafo_area is None:
                print("ERROR. (primero selecciones la opcion 1)")
            else:
                ruta_estadisticas = os.path.join(DIRECTORIO_MAIN, '..', 'datos', 'estadisticas.csv')
                try:
                    df = pd.read_csv(ruta_estadisticas)
                    print(df.to_string()) 
                except FileNotFoundError:
                    print("ERROR : no se encontro el archivo, primero simule")
                pass
            
        case 3:
            print("\n=== Modelo para nuevas Electrolineras ===")
            try:
                df = cargar_datos()
            except FileNotFoundError:
                print("ERROR: no se encontró el archivo de estadísticas. Primero simula recorridos.")
            except Exception as err:
                print(f"ERROR al cargar datos: {err}")
            else:
                if df is None or df.empty:
                    print("El archivo de estadísticas existe pero no contiene registros.")
                else:
                    try:
                        modelo, encoder, scaler, metrics, features = entrenar_modelo(df)
                    except Exception as err:
                        print(f"ERROR al entrenar el modelo: {err}")
                    else:
                        print(f"Modelo entrenado con {len(df)} filas.")
                        print(f"Precisión de prueba: {metrics['accuracy']:.2f}")
                        print(metrics['report'])

                        ejemplos = [
                            {"vehiculo": "Baja", "bateria_al_recargar": 25, "numero_recorrido": 5},
                            {"vehiculo": "Media", "bateria_al_recargar": 10, "numero_recorrido": 8},
                        ]
                        resultados = predecir_ubicaciones(modelo, encoder, scaler, features, ejemplos)

                        if resultados:
                            print("\nPredicciones de ejemplo:")
                            for idx, fila in enumerate(resultados["predicciones"], start=1):
                                print(f"Caso {idx}: {fila['input']}")
                                print(f"  Predicción principal: {fila['prediccion_principal']['electrolinera']} ({fila['prediccion_principal']['probabilidad']:.2f})")
                                print("  Top 3 candidatos:")
                                for candidato in fila['top_5'][:3]:
                                    print(f"    - {candidato['electrolinera']}: {candidato['probabilidad']:.2f}")

                            print("\nDemanda agregada por electrolinera:")
                            for candidato in resultados['demanda_agregada'][:5]:
                                print(f"  - {candidato['electrolinera']}: {candidato['demanda']:.2f}")

                            # Guardar predicciones para el mapa
                            ruta_predicciones = os.path.join(DIRECTORIO_MAIN, os.pardir, 'datos', 'predicciones_demanda.json')
                            with open(ruta_predicciones, 'w') as f:
                                json.dump(resultados["demanda_agregada"], f, indent=2)
                            print(f"\nPredicciones guardadas en: {ruta_predicciones}")

                            # Generar mapa con demanda
                            print("\nGenerando mapa con zonas de demanda...")
                            ruta_mapa = generar_mapa_con_demanda()
                            print(f"Mapa actualizado: {ruta_mapa}")
                            print("Abre el archivo HTML en tu navegador para ver las zonas de demanda marcadas con círculos.")
        
        case 4:
            print("\nSaliendo... ")
            break 
        case _:
            print("Opcion no valida")
