# modelo_ml.py
import pandas as pd         #lib para el analisis y manejos de los datos
from sklearn.ensemble import RandomForestClassifier     #nuestro algoritmo de machine learning

def cargar_datos(ruta_csv):
    #Implementamos las estadisticas (csv)
    """Carga las estadísticas generadas por la simulación."""
    pass

def entrenar_modelo(df):
    #definimos el maodelo para poder entrenarlo (con los features y targest)
    """Entrena el modelo con los datos de uso de electrolineras."""
    #features (zona, hora, vehículo); target (electrolinera)
    pass

def predecir_ubicaciones(modelo, datos_nuevos):
    #cosechamos el modelaje y predecimos datos nuevos (zonas)
    """Predice qué zonas necesitan nuevas electrolineras."""
    #implementar predicción
    pass