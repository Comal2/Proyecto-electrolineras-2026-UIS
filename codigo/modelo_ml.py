"""modelo_ml.py

Modelo de Machine Learning para predecir electrolineras y detectar zonas de demanda.
"""

import os
import pickle
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report


DIRECTORIO_ML = os.path.dirname(os.path.abspath(__file__))
RUTA_DATOS = os.path.join(DIRECTORIO_ML, 'datos')
RUTA_CSV = os.path.join(RUTA_DATOS, 'estadisticas.csv')
RUTA_MODELO = os.path.join(RUTA_DATOS, 'modelo_entrenado.pkl')
RUTA_ENCODER = os.path.join(RUTA_DATOS, 'encoder.pkl')
RUTA_SCALER = os.path.join(RUTA_DATOS, 'scaler.pkl')


def cargar_datos(ruta=None):
    """Carga el CSV de estadísticas de simulación."""
    if ruta is None:
        ruta = RUTA_CSV

    try:
        df = pd.read_csv(ruta)
        print(f"[✓] Archivo cargado: {ruta}", flush=True)
        print(f"[✓] Registros encontrados: {len(df)}", flush=True)
        return df

    except FileNotFoundError:
        print(f"[✗] ERROR: archivo no encontrado en {ruta}", flush=True)
        print(f"    Primero debes generar datos simulando recorridos", flush=True)
        return None

    except pd.errors.EmptyDataError:
        print("[✗] ERROR: el archivo CSV está vacío", flush=True)
        return None

    except Exception as e:
        print(f"[✗] ERROR inesperado: {e}", flush=True)
        return None


def preprocesar_datos(df):
    """
    Limpia y transforma los datos.
    Retorna: X (features), y (target), encoder, scaler
    """
    try:
        df = df.copy()

        # 1. Elimina filas con valores críticos faltantes
        columnas_requeridas = ["vehiculo", "electrolinera", "bateria_al_recargar", "numero_recorrido"]
        df = df.dropna(subset=columnas_requeridas)

        if df.empty:
            raise ValueError("El DataFrame quedó vacío después de eliminar valores nulos")

        print(f"[✓] Filas válidas después de limpieza: {len(df)}", flush=True)

        # 2. Convierte columnas numéricas
        df["bateria_al_recargar"] = pd.to_numeric(df["bateria_al_recargar"], errors='coerce')
        df["numero_recorrido"] = pd.to_numeric(df["numero_recorrido"], errors='coerce')
        df = df.dropna(subset=["bateria_al_recargar", "numero_recorrido"])

        # 3. Normaliza strings
        df["vehiculo"] = df["vehiculo"].str.strip().str.replace(" ", "_")

        # 4. One-hot encoding para vehiculo
        df_encoded = pd.get_dummies(df, columns=["vehiculo"], prefix="vehiculo", dtype=int)

        # 5. Escalado de valores numéricos
        scaler = MinMaxScaler()
        columnas_numericas = ["bateria_al_recargar", "numero_recorrido"]
        df_encoded[columnas_numericas] = scaler.fit_transform(df_encoded[columnas_numericas])

        # 6. Codifica el target (electrolinera)
        encoder = LabelEncoder()
        y = encoder.fit_transform(df_encoded["electrolinera"].astype(str))

        # 7. Features (X) son todas las columnas excepto electrolinera
        X = df_encoded.drop(columns=["electrolinera"])

        print(f"[✓] Preprocesamiento completado", flush=True)
        print(f"    Features: {list(X.columns)}", flush=True)
        print(f"    Clases (electrolineras): {list(encoder.classes_)}", flush=True)

        return X, y, encoder, scaler

    except KeyError as e:
        print(f"[✗] ERROR: columna no encontrada: {e}", flush=True)
        return None, None, None, None

    except ValueError as e:
        print(f"[✗] ERROR de valor: {e}", flush=True)
        return None, None, None, None

    except Exception as e:
        print(f"[✗] ERROR inesperado en preprocesamiento: {e}", flush=True)
        return None, None, None, None


def entrenar_modelo(df, test_size=0.2, random_state=42):
    """
    Entrena el RandomForest y retorna el modelo, encoder, scaler y métricas.
    """
    try:
        # Preprocesa los datos
        X, y, encoder, scaler = preprocesar_datos(df)

        if X is None or y is None:
            raise ValueError("Preprocesamiento falló")

        if len(X) < 2:
            raise ValueError("No hay suficientes datos para entrenar")

        # Divide en entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )

        # Entrena el modelo
        print("[✓] Entrenando modelo Random Forest...", flush=True)
        modelo = RandomForestClassifier(n_estimators=100, random_state=random_state, n_jobs=-1)
        modelo.fit(X_train, y_train)

        # Evalúa el modelo
        y_pred = modelo.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        print(f"[✓] Modelo entrenado exitosamente", flush=True)
        print(f"    Precisión: {accuracy:.2%}", flush=True)

        # Reporte detallado
        report = classification_report(y_test, y_pred, target_names=encoder.classes_, zero_division=0)

        metrics = {
            "accuracy": accuracy,
            "report": report,
            "n_train": len(X_train),
            "n_test": len(X_test),
            "n_classes": len(encoder.classes_)
        }

        return modelo, encoder, scaler, metrics, X.columns.tolist()

    except Exception as e:
        print(f"[✗] ERROR al entrenar el modelo: {e}", flush=True)
        return None, None, None, None, None


def predecir_ubicaciones(modelo, encoder, scaler, feature_names, datos_nuevos):
    """
    Predice la electrolinera más probable para nuevos casos.
    
    entrada: lista de diccionarios con vehiculo, bateria_al_recargar, numero_recorrido
    salida: diccionario con predicciones por fila y demanda agregada
    """
    try:
        if isinstance(datos_nuevos, dict):
            datos_nuevos = [datos_nuevos]

        df_nuevos = pd.DataFrame(datos_nuevos)

        # Procesa igual que en entrenamiento
        df_nuevos["vehiculo"] = df_nuevos["vehiculo"].str.strip().str.replace(" ", "_")
        df_nuevos = pd.get_dummies(df_nuevos, columns=["vehiculo"], prefix="vehiculo", dtype=int)

        # Asegura que tenga todas las columnas
        for col in feature_names:
            if col not in df_nuevos.columns:
                df_nuevos[col] = 0

        df_nuevos = df_nuevos[feature_names]

        # Escala los valores numéricos
        columnas_numericas = ["bateria_al_recargar", "numero_recorrido"]
        df_nuevos[columnas_numericas] = scaler.transform(df_nuevos[columnas_numericas])

        # Predicciones
        probabilidades = modelo.predict_proba(df_nuevos)

        predicciones = []
        for idx, probs in enumerate(probabilidades):
            indices_ordenados = probs.argsort()[::-1]
            top_predicciones = []

            for clase_idx in indices_ordenados:
                top_predicciones.append({
                    "electrolinera": encoder.classes_[clase_idx],
                    "probabilidad": float(probs[clase_idx])
                })

            predicciones.append({
                "input": datos_nuevos[idx],
                "prediccion_principal": top_predicciones[0],
                "top_5": top_predicciones[:5]
            })

        # Agregado: demanda total por electrolinera
        demanda_agregada = probabilidades.mean(axis=0)
        demanda_ordenada = []

        for idx in demanda_agregada.argsort()[::-1]:
            demanda_ordenada.append({
                "electrolinera": encoder.classes_[idx],
                "demanda": float(demanda_agregada[idx])
            })

        return {
            "predicciones": predicciones,
            "demanda_agregada": demanda_ordenada
        }

    except Exception as e:
        print(f"[✗] ERROR en predicción: {e}", flush=True)
        return None


def guardar_modelo(modelo, encoder, scaler):
    """Guarda el modelo, encoder y scaler para reutilizar después."""
    try:
        with open(RUTA_MODELO, 'wb') as f:
            pickle.dump(modelo, f)
        with open(RUTA_ENCODER, 'wb') as f:
            pickle.dump(encoder, f)
        with open(RUTA_SCALER, 'wb') as f:
            pickle.dump(scaler, f)
        print(f"[✓] Modelo guardado en {RUTA_DATOS}", flush=True)
    except Exception as e:
        print(f"[✗] ERROR al guardar: {e}", flush=True)


def cargar_modelo_guardado():
    """Carga un modelo entrenado previamente."""
    try:
        with open(RUTA_MODELO, 'rb') as f:
            modelo = pickle.load(f)
        with open(RUTA_ENCODER, 'rb') as f:
            encoder = pickle.load(f)
        with open(RUTA_SCALER, 'rb') as f:
            scaler = pickle.load(f)
        print(f"[✓] Modelo cargado desde {RUTA_DATOS}", flush=True)
        return modelo, encoder, scaler
    except FileNotFoundError:
        print(f"[✗] No hay modelo guardado", flush=True)
        return None, None, None


# PRUEBA CUANDO EJECUTAS ESTE ARCHIVO DIRECTAMENTE
if __name__ == "__main__":
    df = cargar_datos()
    if df is not None:
        modelo, encoder, scaler, metrics, features = entrenar_modelo(df)
        if modelo is not None:
            print("\n" + "="*50)
            print("REPORTE DE EVALUACIÓN")
            print("="*50)
            print(metrics["report"])
            
            # Ejemplo de predicción
            ejemplos = [
                {"vehiculo": "Baja", "bateria_al_recargar": 25, "numero_recorrido": 5},
                {"vehiculo": "Media", "bateria_al_recargar": 10, "numero_recorrido": 8},
            ]
            
            resultados = predecir_ubicaciones(modelo, encoder, scaler, features, ejemplos)
            if resultados:
                print("\n" + "="*50)
                print("PREDICCIONES DE EJEMPLO")
                print("="*50)
                for pred in resultados["predicciones"]:
                    print(f"Input: {pred['input']}")
                    print(f"  → {pred['prediccion_principal']['electrolinera']} ({pred['prediccion_principal']['probabilidad']:.2%})")
                
                print("\n" + "="*50)
                print("DEMANDA AGREGADA")
                print("="*50)
                for dem in resultados["demanda_agregada"][:5]:
                    print(f"  {dem['electrolinera']}: {dem['demanda']:.2%}")
