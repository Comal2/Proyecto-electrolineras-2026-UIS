"""main/menu"""
import pandas as pd
import os
from modelo_ml import cargar_datos, entrenar_modelo, predecir_zonas
from grafo import cargar_grafo, RUTA_GRAPHML  
#from simulacion import simular_recorridos

DIRECTORIO_MAIN = os.path.dirname(os.path.abspath(__file__))


    
"""=== MENU PRINCIPAl ==="""
grafo_area = None               #Variable global
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
                global grafo_area           #como activar el uso de la variable global

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
                ruta_estadisticas = os.path.join(DIRECTORIO_MAIN, 'datos', 'estadisticas.csv' )

                try:
                    df = pd.read_csv(ruta_estadisticas)
                    print(df.to_string()) 
                except FileNotFoundError:
                    print("ERROR : no se encontro el archivo, primero simule")
                pass
            
        case 3:
            print("\n=== Modelo para nuevas Electrolineras ===")
            if grafo_area is None:
                print("ERROR. (primero seleccione la opcion 1)")   
            else:
                
                #try:
                    #llamo fun cargar_datos -> 
                    #llamo fun entrenar_modelo 
                #except FileNotFoundError:
                    #print("ERROR : no se encontro el archivo, primero simule")

                pass
        case 4:
            print("\nSaliendo... ")
            break 
        case _:
            print("Opcion no valida")
