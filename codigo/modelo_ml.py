"""modelo_ml.py

Contiene funciones para leer los datos de simulación, entrenar un modelo simple
que predice la electrolinera/zona visitada y generar recomendaciones de demanda.
"""

import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report


DIRECTORIO_ML = os.path.dirname(os.path.abspath(__file__))
RUTA_DATOS = os.path.abspath(os.path.join(DIRECTORIO_ML, os.pardir, "datos"))
RUTA_ESTADISTICAS_CSV = os.path.join(RUTA_DATOS, "estadisticas.csv")
RUTA_ESTADISTICAS_XLSX = os.path.join(RUTA_DATOS, "estadisticas.xlsx")


def _normalizar_columnas(df):
    df = df.copy()
    df.columns = [
        str(c).strip().lower().replace(" ", "_").replace("(", "").replace(")", "")
        for c in df.columns
    ]
    df = df.rename(
        columns={
            "electrolinera(visitada)": "electrolinera",
            "electrolinera_visitada": "electrolinera",
            "numero_de_recorrido": "numero_recorrido",
            "bateria_a_recargar": "bateria_al_recargar",
            "nivel_bateria": "bateria_al_recargar",
        }
    )
    return df


def cargar_datos(ruta=None):
    """Carga el archivo de estadísticas de la simulación.

    Si no se provee ruta, intenta primero 'estadisticas.csv' y luego 'estadisticas.xlsx'.
    """
    if ruta:
        ruta = os.path.abspath(ruta)
    else:
        if os.path.exists(RUTA_ESTADISTICAS_CSV):
            ruta = RUTA_ESTADISTICAS_CSV
        elif os.path.exists(RUTA_ESTADISTICAS_XLSX):
            ruta = RUTA_ESTADISTICAS_XLSX
        else:
            raise FileNotFoundError(
                "No se encontró estadisticas.csv ni estadisticas.xlsx en el directorio datos."
            )

    print(f"[modelo_ml] Leyendo datos desde: {ruta}")

    if ruta.lower().endswith(".csv"):
        df = pd.read_csv(ruta)
    elif ruta.lower().endswith(('.xls', '.xlsx')):
        try:
            df = pd.read_excel(ruta, engine='openpyxl')
        except ImportError as e:
            raise ImportError(
                "Para leer archivos Excel necesita instalar openpyxl: pip install openpyxl"
            ) from e
    else:
        raise ValueError("Formato de archivo no soportado. Use CSV o XLSX.")

    print(f"[modelo_ml] Filas cargadas: {len(df)}")
    return df


def preprocesar_datos(df, target_col=None):
    """Prepara los datos para el modelo.

    Elige automáticamente 'electrolinera' o 'zona' como objetivo si no se especifica.
    """
    df = _normalizar_columnas(df)

    if target_col is None:
        if "electrolinera" in df.columns:
            target_col = "electrolinera"
        elif "zona" in df.columns:
            target_col = "zona"
        else:
            raise ValueError(
                "El archivo debe contener la columna 'electrolinera' o 'zona'."
            )

    if target_col not in df.columns:
        raise ValueError(f"No se encontró la columna objetivo '{target_col}'.")

    df = df.copy()
    posibles_numericas = ["bateria_al_recargar", "numero_recorrido", "fila"]
    numericas = [c for c in posibles_numericas if c in df.columns]
    categoricas = [c for c in ["vehiculo"] if c in df.columns]

    columnas_necesarias = numericas + categoricas + [target_col]
    df = df.dropna(subset=columnas_necesarias)

    for nombre in numericas:
        df[nombre] = pd.to_numeric(df[nombre], errors='coerce')

    df = df.dropna(subset=numericas + [target_col])

    X = df[numericas + categoricas].copy()
    if categoricas:
        X = pd.get_dummies(X, columns=categoricas, prefix=categoricas)

    encoder = LabelEncoder()
    y = encoder.fit_transform(df[target_col].astype(str))

    return X, y, encoder


def entrenar_modelo(df, target_col=None, test_size=0.2, random_state=42):
    """Entrena un modelo RandomForest y devuelve métricas básicas."""
    X, y, encoder = preprocesar_datos(df, target_col=target_col)

    if X.shape[0] < 2:
        raise ValueError("No hay suficientes filas válidas para entrenar el modelo.")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    modelo = RandomForestClassifier(n_estimators=100, random_state=random_state)
    modelo.fit(X_train, y_train)

    y_pred = modelo.predict(X_test)
    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "report": classification_report(y_test, y_pred, target_names=encoder.classes_, zero_division=0),
    }

    return modelo, encoder, X.columns.tolist(), metrics


def predecir_ubicaciones(modelo, encoder, datos_nuevos):
    """Predice la electrolinera o zona más probable para nuevos ejemplos."""
    if isinstance(datos_nuevos, dict):
        datos_nuevos = [datos_nuevos]

    df = pd.DataFrame(datos_nuevos)
    if df.empty:
        raise ValueError("No se han proporcionado datos nuevos para predecir.")

    df = _normalizar_columnas(df)
    if "vehiculo" in df.columns:
        df = pd.get_dummies(df, columns=["vehiculo"], prefix=["vehiculo"])

    feature_names = getattr(modelo, "feature_names_in_", None)
    if feature_names is None:
        feature_names = list(df.columns)

    for columna in feature_names:
        if columna not in df.columns:
            df[columna] = 0

    df = df[feature_names]

    probabilidades = modelo.predict_proba(df)
    pronosticos = []
    for fila_idx, fila_prob in enumerate(probabilidades):
        orden = fila_prob.argsort()[::-1]
        top = [
            {
                "electrolinera": encoder.inverse_transform([clase])[0],
                "probabilidad": float(fila_prob[clase]),
            }
            for clase in orden
        ]
        pronosticos.append(
            {
                "input": datos_nuevos[fila_idx],
                "predicted": top[0],
                "top": top,
            }
        )

    promedio = probabilidades.mean(axis=0)
    order_promedio = promedio.argsort()[::-1]
    aggregate = [
        {
            "electrolinera": encoder.inverse_transform([clase])[0],
            "probabilidad_media": float(promedio[clase]),
        }
        for clase in order_promedio
    ]

    return {"rows": pronosticos, "aggregate": aggregate}


def evaluar_modelo(modelo, X_test, y_test, encoder):
    """Calcula métricas de evaluación para un conjunto de prueba."""
    y_pred = modelo.predict(X_test)
    return {
        "accuracy": accuracy_score(y_test, y_pred),
        "report": classification_report(y_test, y_pred, target_names=encoder.classes_, zero_division=0),
    }


if __name__ == "__main__":
    try:
        df = cargar_datos()
    except FileNotFoundError as err:
        print(err)
    else:
        if df.empty:
            print("El archivo de estadísticas está vacío.")
        else:
            modelo, encoder, features, metrics = entrenar_modelo(df)
            print("Modelo entrenado.")
            print(f"Accuracy: {metrics['accuracy']:.2f}")
            print(metrics['report'])

            ejemplos = [
                {"vehiculo": "Baja", "bateria_al_recargar": 25, "numero_recorrido": 5},
                {"vehiculo": "Media", "bateria_al_recargar": 10, "numero_recorrido": 8},
            ]
            resultados = predecir_ubicaciones(modelo, encoder, ejemplos)
            print("Predicciones de ejemplo:")
            for fila in resultados["rows"]:
                print(fila)
            print("Demanda agregada:")
            for item in resultados["aggregate"][:5]:
                print(item)
