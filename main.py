from etl_spotify import realizar_etl_spotify
from eda import perform_eda
from modelagem import perform_modeling
import os

# Caminhos dos arquivos
caminho_dataset = 'arquivoOriginal/dataset.csv'
caminho_saida_eda = 'results'
caminho_saida_csv = 'spotify_tracks_transformed.csv'

# --- ETL ---
df_limpo, resumo = realizar_etl_spotify(caminho_dataset)

print("\n" + "="*50)
print("RESUMO DO PROCESSO ETL")
print("="*50)
for chave, valor in resumo.items():
    print(f"{chave}: {valor}")

# Salvar o DataFrame transformado
df_limpo.to_csv(os.path.join(os.getcwd(), caminho_saida_csv), index=False) # <-- Use esta linha
print(f"DataFrame transformado salvo em '{caminho_saida_csv}'")

# --- EDA ---
df_final = perform_eda(caminho_saida_csv, caminho_saida_eda)

# --- Modelagem e Machine Learning ---
model_results = perform_modeling(caminho_saida_csv, caminho_saida_eda)

print("\n" + "="*50)
print("RESULTADOS DA MODELAGEM")
print("="*50)
for nome, resultados in model_results.items():
    print(f"\nModelo: {nome}")
    print(f"  R²: {resultados['R2']:.4f}")
    print(f"  RMSE: {resultados['RMSE']:.4f}")
    if 'Feature Importances' in resultados:
        print("  Top 5 Importâncias de Features:")
        top_5 = list(resultados['Feature Importances'].items())[:5]
        for feature, importance in top_5:
            print(f"    - {feature}: {importance:.4f}")
