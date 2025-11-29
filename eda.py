import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Configuração de visualização
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['figure.dpi'] = 100

def perform_eda(file_path, output_dir):
    """
    Realiza EDA baseado no dataset transformado pelo ETL.
    Não faz limpeza, apenas análise, estatísticas e gráficos.
    """
    print("Iniciando a Análise Exploratória de Dados (EDA)...")

    # Garante diretório de saída
    os.makedirs(output_dir, exist_ok=True)

    # 1. Carregar dataset já tratado pelo ETL
    try:
        df = pd.read_csv(file_path)
        print(f"Dados carregados com sucesso. Linhas: {len(df)}, Colunas: {len(df.columns)}")
    except Exception as e:
        print(f"Erro ao carregar o arquivo: {e}")
        return

    # ===============================
    # 2. Estatísticas Descritivas
    # ===============================
    print("\nGerando estatísticas descritivas...")
    desc_stats = df.describe().T

    # Salvar estatísticas
    desc_stats_md = desc_stats.to_markdown()
    with open(os.path.join(output_dir, 'desc_stats.md'), 'w', encoding='utf-8') as f:
        f.write("## Estatísticas Descritivas\n\n")
        f.write(desc_stats_md)

    print("Estatísticas descritivas salvas.")

    # ===============================
    # 3. Correlação
    # ===============================
    numeric_cols = df.select_dtypes(include=np.number).columns
    corr_matrix = df[numeric_cols].corr()

    popularity_corr = corr_matrix['popularity'].sort_values(ascending=False)

    # Salvar correlação com popularidade
    popularity_corr_md = popularity_corr.to_frame().to_markdown()
    with open(os.path.join(output_dir, 'popularity_corr.md'), 'w', encoding='utf-8') as f:
        f.write("## Correlação com Popularidade\n\n")
        f.write(popularity_corr_md)

    print("Correlação com popularidade salva.")

    # ===============================
    # 4. Heatmap
    # ===============================
    plt.figure(figsize=(14, 12))
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap='coolwarm')
    plt.title("Matriz de Correlação")
    plt.savefig(os.path.join(output_dir, "corr_matrix.png"))
    plt.close()

    # ===============================
    # 5. Gráficos de distribuição
    # ===============================
    plt.figure()
    sns.histplot(df['popularity'], bins=30, kde=True)
    plt.title("Distribuição da Popularidade")
    plt.savefig(os.path.join(output_dir, "popularity_histogram.png"))
    plt.close()

    # ===============================
    # 6. Dispersões
    # ===============================
    if 'instrumentalness' in df.columns:
        plt.figure()
        sns.scatterplot(x='instrumentalness', y='popularity', data=df, alpha=0.3)
        plt.title("Instrumentalness vs Popularidade")
        plt.savefig(os.path.join(output_dir, "scatter_instrumentalness_popularity.png"))
        plt.close()

    if 'loudness' in df.columns:
        plt.figure()
        sns.scatterplot(x='loudness', y='popularity', data=df, alpha=0.3)
        plt.title("Loudness vs Popularidade")
        plt.savefig(os.path.join(output_dir, "scatter_loudness_popularity.png"))
        plt.close()

    # ===============================
    # 7. Boxplot time_signature
    # ===============================
    if 'time_signature' in df.columns:
        plt.figure()
        sns.boxplot(x='time_signature', y='popularity', data=df)
        plt.title("Popularidade por Time Signature")
        plt.savefig(os.path.join(output_dir, "boxplot_time_signature_popularity.png"))
        plt.close()

    # ===============================
    # 8. Top 10 artistas por média
    # ===============================
    # Se o ETL deixou múltiplos artistas na coluna "artists", pega só o primeiro
    df['main_artist'] = df['artists'].astype(str).str.split(',').str[0].str.strip()

    top_artists = df.groupby('main_artist')['popularity'].mean().nlargest(10)
    df_top_artists = df[df['main_artist'].isin(top_artists.index)]

    plt.figure()
    sns.barplot(x='main_artist', y='popularity', data=df_top_artists,
                estimator=np.mean, ci=None)
    plt.xticks(rotation=45, ha='right')
    plt.title("Top 10 Artistas por Popularidade Média")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "barplot_top_artists_popularity.png"))
    plt.close()

    # ===============================
    # 9. Top 10 gêneros por média
    # ===============================
    # Usar a coluna 'track_genre' se existir, senão usar 'genre_encoded' como fallback
    if 'track_genre' in df.columns:
        genre_col = 'track_genre'
    elif 'genre_encoded' in df.columns:
        genre_col = 'genre_encoded'
    else:
        genre_col = None
        print("Não há coluna de gênero disponível para o top 10 de gêneros.")

    if genre_col:
        top_genres = df.groupby(genre_col)['popularity'].mean().nlargest(10)
        df_top_genres = df[df[genre_col].isin(top_genres.index)]

        plt.figure()
        sns.barplot(x=genre_col, y='popularity', data=df_top_genres,
                    estimator=np.mean, ci=None, palette="magma")
        plt.xticks(rotation=45, ha='right')
        plt.title("Top 10 Gêneros por Popularidade Média")
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "barplot_top_genres_popularity.png"))
        plt.close()

    print("\nEDA concluído com sucesso! Arquivos salvos em:", output_dir)
    return df
