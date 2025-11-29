import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, r2_score
import os
import json

def perform_modeling(file_path, output_dir):
    """
    Executa as etapas de Modelagem e Machine Learning.
    """
    print("Iniciando Modelagem e Machine Learning...")
    
    # Garante diretório de saída
    os.makedirs(output_dir, exist_ok=True)

    # 1. Carregar dataset
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"Erro ao carregar o arquivo: {e}")
        return

    # 2. Definição de Features (X) e Target (y)
    # Variáveis a serem usadas como features (X)
    features = [
        'danceability', 'energy', 'key', 'loudness', 'speechiness', 
        'acousticness', 'instrumentalness', 'liveness', 'valence', 
        'tempo', 'time_signature', 'duration_s', 'explicit', 
        'mode_1', 'genre_encoded'
    ]
    
    # Variável Target (y)
    target = 'popularity'
    
    # Filtra apenas as colunas que existem no DataFrame
    features = [f for f in features if f in df.columns]
    
    X = df[features]
    y = df[target]

    # 3. Separação de Dados (Treino e Teste)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"Dados separados: Treino ({len(X_train)} amostras), Teste ({len(X_test)} amostras)")

    # 4. Modelos a serem testados
    models = {
        "Regressão Linear": LinearRegression(),
        "Random Forest Regressor": RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1),
        "XGBoost Regressor": XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42, n_jobs=-1)
    }

    results = {}
    
    # 5. Treinamento e Avaliação
    for name, model in models.items():
        print(f"\nTreinando {name}...")
        model.fit(X_train, y_train)
        
        # Previsão no conjunto de teste
        y_pred = model.predict(X_test)
        
        # Avaliação
        r2 = r2_score(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        
        results[name] = {
            "R2": r2,
            "RMSE": rmse
        }
        
        print(f"  R²: {r2:.4f}")
        print(f"  RMSE: {rmse:.4f}")
        
        # Se for Random Forest ou XGBoost, salva a importância das features
        if name in ["Random Forest Regressor", "XGBoost Regressor"]:
            feature_importances = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)
            results[name]["Feature Importances"] = feature_importances.to_dict()

    # 6. Salvar Resultados
    results_path = os.path.join(output_dir, 'model_results.json')
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=4)
        
    print(f"\nResultados salvos em '{results_path}'")
    
    return results

if __name__ == '__main__':
    # Configurações
    caminho_dados = 'spotify_tracks_transformed.csv'
    caminho_saida = 'results'
    
    # Executa a modelagem
    perform_modeling(caminho_dados, caminho_saida)
