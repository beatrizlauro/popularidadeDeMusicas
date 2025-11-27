from etl_spotify import realizar_etl_spotify
from eda import perform_eda

# Caminhos dos arquivos
caminho_dataset = 'arquivoOriginal/dataset.csv'
caminho_saida_eda = 'results'

# --- ETL ---
df_limpo, resumo = realizar_etl_spotify(caminho_dataset)

print("\n" + "="*50)
print("RESUMO DO PROCESSO ETL")
print("="*50)
for chave, valor in resumo.items():
    print(f"{chave}: {valor}")

# Salvar o DataFrame transformado
df_limpo.to_csv('spotify_tracks_transformed.csv', index=False)
print("DataFrame transformado salvo em 'spotify_tracks_transformed.csv'")

# --- EDA ---
df_final = perform_eda('spotify_tracks_transformed.csv', caminho_saida_eda)
