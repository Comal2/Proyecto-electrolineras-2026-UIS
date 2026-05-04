# grafo.py
#simulacion.py
#modelo_ml.py
#estadisticas

#//// Importamos otros programas a utilizar

import grafo
import simulacion         # <- import programs 
import modelo_ml
#import estadisticas

"""El submenu dentro de la op. 1"""

def submenu_mapa_grafos_simulacion():                  # <- definimos la fun que llamamos
    while True:
        print("\n=== Mapa, grafo y simulaciones ===")
        print("1. Cargar mapa y grafo")
        print("2. Simular recorridos")
        print("3. Buscar mejor ruta a electrolinera")
        print("4. Volver al menu principal")
        sub_opcion = int(input("Elige una opcion: "))
        
        match(sub_opcion):
            case 1:
                print("\nMostrando mapa y grafo")
                grafo.main()                           # <- llamamos el programa que importamos
            case 2:
                print("\nSimulando recorrido...")
                simulacion.main() 
            case 3:
                print("\nMostrando mejor ruta...")
                modelo_ml.main()
            case 4:
                print("\nVolviendo al menu")
                break
            case _:
                print("Opcion invalida")


"""Tendremos nuestro menu principal"""

while True:
    print("\n=== MENÚ PRINCIPAL ===")
    print("1. Ver mapa y grafo")  
    print("2. Ver estadisticas de uso")
    print("3. Modelo predictivo de nuevas electrolineras")
    print("4. Salir")
    opcion = int(input("\nElige una opción: "))
    
    match(opcion):
        case 1:
            submenu_mapa_grafos_simulacion()                     # <- Llamamos la fun que definimos
        case 2:
            print("\nMostrando estadisticas...")
            #estadisticas.main()
        case 3:
            print("\n=== Modelo para nuevas Electrolineras ===")
            modelo_ml.main()
        case 4:
            print("\nSaliendo... ")
            break 
        case _:
            print("Opcion no valida")

