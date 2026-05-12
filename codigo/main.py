#main/menu
import sys
import os
#from modelo_ml import predecir_ubicaciones
from grafo import cargar_grafo, RUTA_GRAPHML  #importamos el grafo con los "nodos"
from mapa import DIRECTORIO, mapa
#import simular_recorridos(grafo_area)       #import opcion de la simulacion

sys.path.insert(0, os.path.dirname(__file__))
#cargar correctamente los otros modulos


    
"""=== MENU PRINCIPAl ==="""
grafo_area = None               #Variable global
while True:
    print("\n=== MENÚ PRINCIPAL ===")
    print("1. Ver mapa y grafo")  
    print("2. Ver estadisticas de uso")
    print("3. Modelo predictivo de nuevas electrolineras")
    print("4. Salir")
    opcion = int(input("\nElige una opción: "))
        
    match(opcion):
        case 1:
            """=== SUBMENU DENTRO DE LA OP 1 ==="""

            def submenu_mapa_grafos_simulacion():                  # <- definimos la fun que llamamos
                global grafo_area           #como activar el uso de la variable global

                while True:
                    print("\n=== SUBMENÚ ===")
                    print("1. Cargar mapa/grafo")
                    print("2. Simular recorridos")
                    print("3. Volver al menu principal")
                    sub_opcion = int(input("Elige una opcion: "))
                        
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
                                #print(simular_recorridos(grafo_area))                  #simulacion
                            

                        case 3:
                            print("\nVolviendo al menu")
                            break
                        case _:
                            print("Opcion invalida")

            submenu_mapa_grafos_simulacion()                     # <- Llamamos la fun que definimos
                   
        
        case 2:
            print("\nMostrando estadisticas...")
            if grafo_area is None:
                print("ERROR. (primero selecciones la opcion 1)")
            else:
                #print(leer_estadisticas())
                pass
        case 3:
            print("\n=== Modelo para nuevas Electrolineras ===")
            if grafo_area is None:
                print("ERROR. (primero selecciones la opcion 1)")   
            else:             
                #print(predecir_ubicaciones(modelo, datos_nuevos))      #prediccion
                pass
        case 4:
            print("\nSaliendo... ")
            break 
        case _:
            print("Opcion no valida")