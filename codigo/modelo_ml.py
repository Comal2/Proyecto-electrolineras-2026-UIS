"""modelo_ml.py"""
import os                   #lib para el manejo de archivos
import pandas as pd         #lib para el analisis y manejos de los datos
from sklearn.ensemble import RandomForestClassifier     #nuestro algoritmo de machine learning
from sklearn.preprocessing import LabelEncoder          #convertir el texto a numeros para nuestro modelo


DIRECTORIO_ML =  os.path.dirname(os.path.abspath(__file__))

def cargar_datos(ruta_csv):
    """Carga las estadísticas generadas por la simulación."""
    print(f"[cargar_datos] Leyendo archivo: {ruta_csv}")
    ruta_csv = os.path.join(DIRECTORIO_ML, 'datos', 'estadisticas.csv')
    if not os.path.exists(ruta_csv):
        raise FileNotFoundError(f"no se encontro el archivo {ruta_csv}")
    df = pd.read_csv(ruta_csv)
    print(f"[cargar_datos] filas cargadas: {len(df)}")
    return df

def prepocesar_datos(df):
    """convertimos los datos a valores que el modelo entienda"""
    print("Iniciando preprocesamiento...")
    df = df.copy()  
    #copia el dataframe del csv
    df= df.dropna(subset=["vehiculo", "bateria_al_recargar", "km_recorridos", "zona"])
    #elimina las filas con valores nulos
    df["bateria_al_recargar"] = df["bateria_al_recargar"].astype(float)
    df["km_recorridos"] = df["km_recorridos"].astype(float)
    #convierte estas frames y los convierte el decimales(float)
    df = pd.get_dummies(df, columns = ["vehiculo"], prefix = "vehiculo")
    
    return df

def entrenar_modelo(df):
    """Entrena el modelo con los datos de uso de electrolineras."""
    df = df.copy()
    encoder = LabelEncoder()
    df["zona_encoded"] = encoder.fit_transform(df["zona"])
    df_pre = prepocesar_datos(df)

    caracteristicas = [c for c in df_pre.columns if c.startswith("vehiculo_") or c in ["bateria_al_recargar", "km_recorridos"]]
    X = df_pre[caracteristicas]
    Y = df_pre["zona_encoded"]

    modelo = RandomForestClassifier(n_estimators=100, random_state=42)
    modelo.fit(X, Y)
    
    return modelo, encoder


def predecir_zonas(modelo, datos_nuevos):
    """Predice qué zonas necesitan nuevas electrolineras."""
    """df = pd.DataFrame(datos_nuevos)
    df["bateria_al_recargar"] = df["bateria_al_recargar"].astype(float)
    df["km_recorridos"] = df["km_recorridos"].astype(float)
    df = pd.get_dummies(df, columns = ["vehiculo"], prefix = "vehiculo")

    feature_names = getattr(modelo, "feature_names_in_", df.columns)
    for columna in [c for c in feature_names if c not in df.columns]:
        df[columna] = 0
    df = df[feature_names]

    probabilidades = modelo.predict_proba(df)
    medias = probabilidades.means(axis=0)
    orden = medias.argsort()[::-1]
    zonas = encoder.inverse_transform(orden)

    return [(zona, medias[idx])for idx, zona in zip(orden, zonas)]

ruta_csv = os.path.join(DIRECTORIO_ML, 'datos', 'estadisticas.csv')
df = cargar_datos(ruta_csv)
modelo, encoder = entrenar_modelo(df)

ejemplos = [
    {"vehiculo": "Baja", "bateria_al_recargar": 25, "km_recorridos": 75},
    {"vehiculo": "Media", "bateria_al_recargar": 10, "km_recorridos": 95},
]
predicciones = predecir_zonas(modelo, encoder, ejemplos)
print("Zonas sugeridas:", predicciones)"""