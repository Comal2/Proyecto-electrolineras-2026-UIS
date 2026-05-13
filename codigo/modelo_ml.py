"""modelo_ml.py"""
import os                   #lib para el manejo de archivos
import pandas as pd         #lib para el analisis y manejos de los datos
from sklearn.ensemble import RandomForestClassifier     #nuestro algoritmo de machine learning
from sklearn.preprocessing import LabelEncoder, MinMaxScaler          #convertir el texto a numeros para nuestro modelo

DIRECTORIO_ML =  os.path.dirname(os.path.abspath(__file__))
ruta_csv = os.path.join(DIRECTORIO_ML, 'datos', 'estadisticas.csv')
    #ruta de los datos a utilizar (ESTADISTICAS
df = None
    #inicializamos el df para que el return lo llene luego 


def cargar_datos(ruta_csv):
    """Carga las estadísticas generadas por la simulación."""

    
    #verificar que el csv si exista
    try :
        df = pd.read_csv(ruta_csv) #leemos el archivo
        print(f"Leyendo archivo: {ruta_csv}",flush=True)
        print("Archivo cargado exitosamente.",flush=True)

    except  FileNotFoundError:
        print(f"ERROR: archivo no encontrado en {ruta_csv}, primero simule",flush=True)
    #captura el error si el archivo no existe

    except pd.errors.EmptyDataError:
        print("ERROR: el archivo csv esta vacio",flush=True)
    #captura el error si el archivo esta vacio

    except Exception as e:
        print(f"ERROR INESPERADO : {e}",flush=True)
    #captura cualquier otro error inesperado

        return df

def preprocesar_datos(df):
    """Limpieza y Transformacion de los datos"""
    
    try: 
        df = df.copy()
        #copia el dataframe para no afectarlo y nos de errores

        df = df.dropna(subset=["vehiculo", "electrolinera","bateria_al_recargar","numero_recorrido" ])
        # 1. limpia el dataset de posibles filas vacias
        if df.empty:
            raise ValueError("El dataframe quedo vacio despues de eliminar valores nulos :( ")

        df["bateria_al_recargar"] = df["bateria_al_recargar"].astype(float)
        df["numero_recorrido"] = df["numero_recorrido"].astype(float)
        # 2. convertimos esas columnas en decimales, para evitar errores de valores

        df["vehiculo"] = df["vehiculo"].str.replace(" ","_")
        # 3. formateamos los strings para evitar problemas por espacios

        df = pd.get_dummies(df, columns = ["vehiculo"], prefix = "vehiculo", dtype = int)
        # 4. asigna un numero a cada variable de vehiculo para que pase de string a int
    
        escalador = MinMaxScaler()
        columas_a_escalar = ["bateria_al_recargar", "numero_recorrido"]
        df[columas_a_escalar] = escalador.fit_transform(df[columas_a_escalar])
        #ajusta los valores de los recorridos y bateria para que no tome los que tengan

        print("Preprocesamiento listo ✓ ")
        return df
    
    except KeyError as e:
        print(f"ERROR: no se encontro la columna requerida en el dataset: {e}")
    
    except ValueError as e:
        print(f"ERROR de formato (datos numericos no encontrados): {e}")
    
    except Exception as e:
        print(f"ERROR INESPERADO: {e}")

def entrenar_modelo(df):
    df = df.copy



#probar cada funcion 
if __name__ == "__main__":
    cargar_datos(ruta_csv)
    preprocesar_datos(df)
    #entrenar_modelo(df)