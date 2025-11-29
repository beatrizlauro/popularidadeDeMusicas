# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, LabelEncoder

# -----------------------------------------------------------------------------
# 2. Coleta e ETL (Extração, Transformação e Limpeza dos Dados)
# -----------------------------------------------------------------------------

def realizar_etl_spotify(caminho_arquivo):
    """
    Executa o processo de Extração, Transformação e Limpeza (ETL)
    no conjunto de dados de faixas do Spotify.

    Args:
        caminho_arquivo (str): O caminho para o arquivo CSV do dataset.

    Returns:
        tuple: Um DataFrame limpo e transformado, e um dicionário com o resumo do ETL.
    """
    resumo_etl = {}
    
    # 1. EXTRAÇÃO (E)
    try:
        # Assumindo que o arquivo CSV está no formato correto
        df = pd.read_csv(caminho_arquivo)
        resumo_etl['Registros Iniciais'] = len(df)
        resumo_etl['Colunas Iniciais'] = len(df.columns)
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado no caminho: {caminho_arquivo}")
        # Cria um DataFrame de exemplo com a estrutura esperada para demonstração
        print("Criando DataFrame de Exemplo para demonstração do ETL.")
        df = criar_dataframe_exemplo()
        resumo_etl['Registros Iniciais'] = len(df)
        resumo_etl['Colunas Iniciais'] = len(df.columns)
    
    # 2. LIMPEZA (L)
    
    # Renomear colunas para facilitar o uso e padronizar (opcional, mas boa prática)
    df.columns = df.columns.str.lower().str.replace('[^a-z0-9_]', '', regex=True)
    
    # Remover colunas irrelevantes para a maioria dos modelos de ML
    colunas_remover = ['track_id', 'album_name']
    df = df.drop(columns=[col for col in colunas_remover if col in df.columns], errors='ignore')
    
    # Tratamento de Valores Ausentes (NaN)
    # Para colunas numéricas, preencher com a média (imputação)
    colunas_numericas = df.select_dtypes(include=np.number).columns
    for col in colunas_numericas:
        if df[col].isnull().any():
            df[col].fillna(df[col].mean(), inplace=True)
            resumo_etl[f'NaNs tratados em {col}'] = 'Imputação por Média'
            
    # Para colunas categóricas (como 'artists' ou 'track_name'), preencher com 'desconhecido'
    colunas_categoricas = df.select_dtypes(include='object').columns
    for col in colunas_categoricas:
        if df[col].isnull().any():
            df[col].fillna('desconhecido', inplace=True)
            resumo_etl[f'NaNs tratados em {col}'] = 'Preenchido com "desconhecido"'
            
    # Tratamento de Duplicatas
    df.drop_duplicates(inplace=True)
    resumo_etl['Registros Após Duplicatas'] = len(df)
    
    # 3. TRANSFORMAÇÃO (T)
    
    # Feature Engineering: Converter duração de milissegundos para segundos
    if 'duration_ms' in df.columns:
        df['duration_s'] = df['duration_ms'] / 1000
        df = df.drop(columns=['duration_ms'])
        resumo_etl['Feature Engineering'] = 'duration_ms -> duration_s'
        
    # Codificação de Variáveis Categóricas
    
    # Codificação One-Hot Encoding (para variáveis nominais com poucos valores únicos)
    # Ex: 'explicit' (True/False) e 'mode' (0/1) já são binárias ou quase.
    # Vamos aplicar One-Hot em 'mode' para garantir que não seja tratada como ordinal.
    if 'mode' in df.columns:
        df['mode'] = df['mode'].astype(str) # Garante que é string para get_dummies
        df = pd.get_dummies(df, columns=['mode'], prefix='mode', drop_first=True)
        resumo_etl['Codificação Mode'] = 'One-Hot Encoding'
        
    # Codificação Label Encoding (para variáveis ordinais ou de alta cardinalidade que serão removidas)
    # Para 'track_genre', que tem alta cardinalidade (125 gêneros), vamos usar Label Encoding
    # apenas para demonstração, mas geralmente é melhor remover ou usar técnicas avançadas.
    if 'track_genre' in df.columns:
        le = LabelEncoder()
        df['genre_encoded'] = le.fit_transform(df['track_genre'])
        # df = df.drop(columns=['track_genre'])
        resumo_etl['Codificação track_genre'] = 'Label Encoding'
        
    # Normalização/Escalonamento de Features Numéricas
    # Aplicar MinMaxScaler (Normalização) nas features numéricas para que fiquem entre 0 e 1
    colunas_para_normalizar = ['popularity', 'danceability', 'energy', 'loudness', 
                               'speechiness', 'acousticness', 'instrumentalness', 
                               'liveness', 'valence', 'tempo', 'duration_s']
    
    # Filtra apenas as colunas que existem no DataFrame
    colunas_existentes = [col for col in colunas_para_normalizar if col in df.columns]
    
    if colunas_existentes:
        scaler = MinMaxScaler()
        df[colunas_existentes] = scaler.fit_transform(df[colunas_existentes])
        resumo_etl['Normalização'] = 'MinMaxScaler nas features de áudio'
        
    resumo_etl['Registros Finais'] = len(df)
    resumo_etl['Colunas Finais'] = len(df.columns)
    
    return df, resumo_etl

def criar_dataframe_exemplo():
    """Cria um DataFrame de exemplo com a estrutura esperada do Spotify Tracks Dataset."""
    data = {
        'track_id': ['t1', 't2', 't3', 't4', 't5'],
        'artists': ['Artist A', 'Artist B', 'Artist C', 'Artist D', 'Artist E'],
        'album_name': ['Album X', 'Album Y', 'Album Z', 'Album W', 'Album V'],
        'track_name': ['Song 1', 'Song 2', 'Song 3', 'Song 4', 'Song 5'],
        'popularity': [80, 65, 90, 40, 75],
        'duration_ms': [200000, 180000, 250000, 150000, 210000],
        'explicit': [True, False, True, False, False],
        'danceability': [0.7, 0.5, 0.9, 0.3, 0.6],
        'energy': [0.8, 0.4, 0.95, 0.2, 0.7],
        'loudness': [-5.0, -10.0, -3.0, -15.0, -6.0],
        'mode': [1, 0, 1, 0, 1],
        'speechiness': [0.05, 0.4, 0.1, 0.8, 0.08],
        'acousticness': [0.1, 0.8, 0.05, 0.9, 0.2],
        'instrumentalness': [0.0, 0.7, 0.0, 0.0, 0.0],
        'liveness': [0.1, 0.9, 0.2, 0.15, 0.3],
        'valence': [0.9, 0.3, 0.8, 0.1, 0.7],
        'tempo': [120.0, 90.0, 140.0, 70.0, 110.0],
        'time_signature': [4, 4, 3, 4, 4],
        'track_genre': ['pop', 'classical', 'pop', 'hip-hop', 'rock']
    }
    # Adiciona um valor NaN para demonstrar o tratamento
    data['popularity'][1] = np.nan
    data['artists'][3] = np.nan
    
    return pd.DataFrame(data)

# --- Execução do ETL ---
caminho_do_dataset = 'arquivoOriginal/dataset.csv' 
df_limpo, resumo = realizar_etl_spotify(caminho_do_dataset)

print("\n" + "="*50)
print("RESUMO DO PROCESSO ETL")
print("="*50)
for chave, valor in resumo.items():
    print(f"{chave}: {valor}")

print("\n" + "="*50)
print("AMOSTRA DO DATAFRAME APÓS ETL")
print("="*50)
print(df_limpo.head())

print("\n" + "="*50)
print("TIPOS DE DADOS FINAIS")
print("="*50)
print(df_limpo.dtypes)

# Salvar o DataFrame transformado para uso nas próximas etapas (EDA/Modelagem)
df_limpo.to_csv('spotify_tracks_transformed.csv', index=False)
print("\nDataFrame transformado salvo em 'spotify_tracks_transformed.csv'")
