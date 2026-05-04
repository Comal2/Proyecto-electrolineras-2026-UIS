#modelo de machine learning 
import pandas as pd         #lib para las dataframes
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier      #nuestro alg. de 
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import joblib

def cargar_datos(ruta_csv):
    pass

def entrenar_modelo(df):
    # Features básicas
    features = ['zona',     #en que zona esta el vehiculo
                'porcentaje_bateria',  #porcentaje de bateria cuando llego      #(entradas hasta el momento)
                'hora']     #a que horas ocurrio una recarga
    
    # Target: electrolinera más usada en esa zona 
    df['electrolinera_target'] = df['id_electrolinera']  #predice cual se utilizo elc se uso
    
    X = pd.get_dummies(df[features])   # convierte zona y hora en numéricas
    y = df['electrolinera_target']      #target de elc usada
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                            #dividimos los datos entre entrenamiento y prueba

    modelo = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)          #<- creacion y entrenamiento del mod.
    modelo.fit(X_train, y_train)
    
    print(classification_report(y_test, modelo.predict(X_test)))  #evaluamos su aprendizaje
    return modelo

import numpy as np
#predecira nuevas elc en zonas que lo necesiten
def predecir_ubicaciones(modelo, datos_nuevos = None):
    """implemetamos el modelo entrenado para suferir los nuevos puntos
    """
    print("\n=== Generando predicciones de nuevas ubicaciones...")

    if datos_nuevos is None:        #creamos posible zonas candidatas 
        datos_nuevos = pd.DataFrame({
            'zona': [0],   # zonas candidatas
            'porcentaje_bateria': [],
            'hora': []            
        })

    #== Predecimos ==
    #convertimos los features otra vez
    X_nuevo = pd.get_dumies(datos_nuevos[['zona', 'porcentaje_bateria', 'hora']])

    columnas_entrenamiento = modelo.feature_names_in if hasattr(modelo, 'feature_names_in_')else None

    if columnas_entrenamiento is not None:
        X_nuevo = X-X_nuevo.reindex(columns=columnas_entrenamiento, fill_value=0)
    
    #Hacemos las predicciones
    predicciones = modelo.predict(X_nuevo)
    probabilidades = modelo.predict(X_nuevo)

    #Agregamos resultados al dataframe(datos_nuevos)
    datos_nuevos = datos_nuevos.copy()
    datos_nuevos["Electrolinera_predicha"] = predicciones
    datos_nuevos["confianza"] = np.max(probabilidades, axis=1)*100      # % de confianza

    #Analizamos la demanda
    demanda = datos_nuevos["electrolinera_predicha"].value_counts()  #contamos cuantas veces se predice cada electrolinera (alta demanda)

    print("\n=== Predicciones de nuevas Electrolineras ===")
    print(datos_nuevos[['zona', 'hora', 'porcentaje_bateria', 
                       'electrolinera_predicha', 'confianza']].round(2))

    print("\nDemanda predicha por electrolinera existente: ")
    print(demanda)

    print("\n Zonas recomendadas para nuevas electrolineras:")
    
    zonas_recomendadas = datos_nuevos.sort_values("confianza", ascending=False)
    print(zonas_recomendadas[['zona', 'electrolinera_predicha', "confianza"]])

    #guardamos los resultados
    datos_nuevos.to_csv("resultados/predicciones_nuevas_zonas.csv", index=False)

    return datos_nuevos, demanda

if __name__ == "__main__":
    df = cargar_datos("datos/estadisticas.csv")
    modelo = entrenar_modelo(df)
    predicciones, demanda = predecir_ubicaciones(modelo)