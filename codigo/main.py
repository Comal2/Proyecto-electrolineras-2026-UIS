"""main/menu"""
import pandas as pd
import os
from modelo_ml import cargar_datos, entrenar_modelo, predecir_ubicaciones
from grafo import cargar_grafo, RUTA_GRAPHML  
#from simulacion import simular_recorridos

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
                ruta_estadisticas = os.path.abspath(os.path.join(DIRECTORIO_MAIN, os.pardir, 'datos', 'estadisticas.csv'))

                try:
                    df = pd.read_csv(ruta_estadisticas)
                    print(df.to_string())
                except FileNotFoundError:
                    print("ERROR: no se encontró el archivo estadisticas.csv. Simula primero para generar datos.")
                pass
            
        case 3:
            print("\n=== Modelo para nuevas Electrolineras ===")
            try:
                df = cargar_datos()
            except FileNotFoundError:
                print("ERROR: no se encontró el archivo de estadísticas. Simula primero para generar los datos.")
            except Exception as err:
                print(f"ERROR al cargar datos: {err}")
            else:
                if df.empty:
                    print("El archivo de estadísticas existe pero no contiene registros.")
                else:
                    try:
                        modelo, encoder, features, metrics = entrenar_modelo(df)
                    except Exception as err:
                        print(f"ERROR al entrenar el modelo: {err}")
                    else:
                        print(f"Modelo entrenado con {len(df)} filas.")
                        print(f"Precisión de prueba: {metrics['accuracy']:.2f}")
                        print(metrics['report'])

                        ejemplos = [
                            {"vehiculo": "Baja", "bateria_al_recargar": 25, "numero_recorrido": 5},
                            {"vehiculo": "Media", "bateria_al_recargar": 12, "numero_recorrido": 8},
                        ]
                        resultados = predecir_ubicaciones(modelo, encoder, ejemplos)

                        print("\nPredicciones de ejemplo:")
                        for idx, fila in enumerate(resultados["rows"], start=1):
                            print(f"Caso {idx}: {fila['input']}")
                            print(f"  Predicción principal: {fila['predicted']['electrolinera']} ({fila['predicted']['probabilidad']:.2f})")
                            print("  Top 3 candidatos:")
                            for candidato in fila['top'][:3]:
                                print(f"    - {candidato['electrolinera']}: {candidato['probabilidad']:.2f}")

                        print("\nDemanda agregada por electrolinera:")
                        for candidato in resultados['aggregate'][:5]:
                            print(f"  - {candidato['electrolinera']}: {candidato['probabilidad_media']:.2f}")
        
        case 4:
            print("\nSaliendo... ")
            break 
        case _:
            print("Opcion no valida")
