import sys
import os
#from modelo_ml import predecir_zonas_ml()
from grafo import IMAGEN_PATH  #importamos el grafo con los "nodos"
#from estadisticas.csv import leer_estadisticas()    #funcion de estadisticas
#import simular_recorridos(grafo_area)       #import opcion de la simulacion

sys.path.insert(0, os.path.dirname(__file__))
#cargar correctamente los otros modulos


    
"""=== MENU PRINCIPAl ==="""

while True:
    print("\n=== MENÚ PRINCIPAL ===")
    print("1. Ver mapa y grafo")  
    print("2. Ver estadisticas de uso")
    print("3. Modelo predictivo de nuevas electrolineras")
    print("4. Salir")
    opcion = int(input("\nElige una opción: "))
        
    match(opcion):
        case 1:
            grafo_area = None               #Variable global
            """=== SUBMENU DENTRO DE LA OP 1 ==="""

            def submenu_mapa_grafos_simulacion():                  # <- definimos la fun que llamamos
                global grafo_area           #como activar su uso

                while True:
                    print("\n=== Mapa, grafo y simulaciones ===")
                    print("1. Cargar mapa/grafo")
                    print("2. Simular recorridos")
                    print("3. Volver al menu principal")
                    sub_opcion = int(input("Elige una opcion: "))
                        
                    match(sub_opcion):
                        case 1:
                            print("\nCargando mapa/grafo...")
                            grafo_area = IMAGEN_PATH
                            print(grafo_area)
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
                #print(predecir_ubicaciones.main())
                pass
        case 4:
            print("\nSaliendo... ")
            break 
        case _:
            print("Opcion no valida")