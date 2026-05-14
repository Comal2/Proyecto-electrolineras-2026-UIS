import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
DATA_FILE = os.path.join(BASE_DIR, "datos", "estadisticas.csv")

def cargar_datos(ruta=None):
    if ruta is None:
        ruta = DATA_FILE
    df = pd.read_csv(ruta)
    return df

def preparar_datos(df):
    df = df.copy()
    df.columns = [
        c.strip().lower().replace(" ", "_").replace("(", "").replace(")", "")
        for c in df.columns
    ]

    df = df.dropna(subset=["vehiculo", "electrolinera", "bateria_al_recargar", "numero_recorrido"])
    df["bateria_al_recargar"] = pd.to_numeric(df["bateria_al_recargar"], errors="coerce")
    df["numero_recorrido"] = pd.to_numeric(df["numero_recorrido"], errors="coerce")
    df = df.dropna(subset=["bateria_al_recargar", "numero_recorrido"])
    df["vehiculo"] = df["vehiculo"].str.strip().str.replace(" ", "_")

    X = pd.get_dummies(df[["vehiculo", "bateria_al_recargar", "numero_recorrido"]], columns=["vehiculo"])
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_scaled = pd.DataFrame(X_scaled, columns=X.columns)

    encoder = LabelEncoder()
    y = encoder.fit_transform(df["electrolinera"].astype(str))

    return X_scaled, y, encoder, scaler

def entrenar_modelo(df):
    X, y, encoder, scaler = preparar_datos(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    modelo = RandomForestClassifier(n_estimators=100, random_state=42)
    modelo.fit(X_train, y_train)

    y_pred = modelo.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, target_names=encoder.classes_, output_dict=True)

    return modelo, encoder, scaler, {"accuracy": accuracy, "report": report}, X.columns.tolist()

def predecir_ubicaciones(modelo, encoder, scaler, feature_names, datos_nuevos):
    df_nuevos = pd.DataFrame(datos_nuevos)
    df_nuevos["vehiculo"] = df_nuevos["vehiculo"].str.strip().str.replace(" ", "_")
    df_nuevos = pd.get_dummies(df_nuevos, columns=["vehiculo"], prefix="vehiculo", dtype=int)

    for col in feature_names:
        if col not in df_nuevos.columns:
            df_nuevos[col] = 0
    df_nuevos = df_nuevos[feature_names]

    # Escalar los datos nuevos
    df_nuevos_scaled = scaler.transform(df_nuevos)
    df_nuevos_scaled = pd.DataFrame(df_nuevos_scaled, columns=feature_names)

    probs = modelo.predict_proba(df_nuevos_scaled)
    resultados = []
    for i, fila in enumerate(probs):
        orden = fila.argsort()[::-1]
        top = [{"electrolinera": encoder.classes_[idx], "probabilidad": float(fila[idx])} for idx in orden]
        resultados.append({
            "input": datos_nuevos[i],
            "prediccion_principal": top[0],
            "top_5": top[:5]
        })

    demanda = probs.mean(axis=0)
    demanda_ordenada = sorted(
        [{"electrolinera": encoder.classes_[i], "demanda": float(demanda[i])} for i in range(len(demanda))],
        key=lambda x: x["demanda"],
        reverse=True
    )

    return {"predicciones": resultados, "demanda_agregada": demanda_ordenada}

if __name__ == "__main__":
    print("Probando el modelo de ML...")
    try:
        df = cargar_datos()
        print(f"Datos cargados: {len(df)} filas")

        modelo, encoder, scaler, metrics, features = entrenar_modelo(df)
        print(f"Modelo entrenado. Precisión: {metrics['accuracy']:.2f}")

        ejemplos = [
            {"vehiculo": "Nissan LEAF Standard Range 52 kWh", "bateria_al_recargar": 25, "numero_recorrido": 5},
            {"vehiculo": "BMW i4 eDrive40", "bateria_al_recargar": 10, "numero_recorrido": 8},
        ]
        resultados = predecir_ubicaciones(modelo, encoder, scaler, features, ejemplos)

        print("\nPredicciones de ejemplo:")
        for idx, fila in enumerate(resultados["predicciones"], start=1):
            print(f"Caso {idx}: {fila['input']}")
            print(f"  Predicción principal: {fila['prediccion_principal']['electrolinera']} ({fila['prediccion_principal']['probabilidad']:.2f})")

        print("\nDemanda agregada por electrolinera:")
        for candidato in resultados['demanda_agregada'][:5]:
            print(f"  - {candidato['electrolinera']}: {candidato['demanda']:.2f}")

        # Guardar predicciones
        ruta_predicciones = os.path.join(BASE_DIR, "datos", "predicciones_demanda.json")
        with open(ruta_predicciones, 'w') as f:
            json.dump(resultados["demanda_agregada"], f, indent=2)
        print(f"\nPredicciones guardadas en: {ruta_predicciones}")

    except Exception as e:
        print(f"Error: {e}")
