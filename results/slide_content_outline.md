# Outline do Conteúdo para Slides Finais da Apresentação

Este outline é baseado nas etapas 4 e 5 do projeto (Modelagem, Avaliação e Conclusão).

## Slide 1: Título e Introdução
- **Título:** Previsão da Popularidade de Músicas do Spotify
- **Subtítulo:** Modelagem Preditiva e Análise de Resultados
- **Disciplina:** Análise de Dados
- **Integrantes:** (Incluir o nome do Integrante 4 e os demais listados no README)

## Slide 2: Objetivo e Escopo do Trabalho
- **Objetivo Central:** Prever a popularidade de músicas (variável-alvo) com base em suas características de áudio e gênero.
- **Tipo de Problema:** Regressão.
- **Base de Dados:** Spotify Tracks Dataset (114.000 faixas).
- **Foco da Apresentação:** Resultados da Modelagem e Conclusões.

## Slide 3: Resumo do Pré-Processamento (ETL)
- **Limpeza:** Tratamento de valores ausentes e remoção de duplicatas.
- **Transformação:** Normalização das features numéricas (MinMaxScaler).
- **Codificação:** Gênero (`track_genre`) codificado (Label Encoding) para uso nos modelos.
- **Features Utilizadas:** danceability, energy, loudness, acousticness, instrumentalness, valence, tempo, duration_s, key, time_signature, explicit, mode_1, genre_encoded.

## Slide 4: Modelos de Machine Learning Aplicados
- **Modelos Testados:**
    1. Regressão Linear (Baseline)
    2. Random Forest Regressor
    3. XGBoost Regressor
- **Métricas de Avaliação:**
    - R² (Coeficiente de Determinação)
    - RMSE (Root Mean Squared Error)

## Slide 5: Resultados Comparativos da Modelagem
- **Tabela de Métricas:**
    | Modelo | R² | RMSE |
    | :--- | :--- | :--- |
    | Regressão Linear | 0.0234 | 0.2195 |
    | **Random Forest Regressor** | **0.5236** | **0.1533** |
    | XGBoost Regressor | 0.3215 | 0.1830 |
- **Destaque:** O Random Forest Regressor obteve o melhor desempenho.

## Slide 6: Interpretação do Melhor Resultado (Random Forest)
- **R² = 0.5236:** O modelo Random Forest consegue explicar aproximadamente 52% da variância na popularidade das músicas.
- **Contexto:** Popularidade é um fenômeno complexo, influenciado por fatores externos (marketing, tendências) não presentes no dataset. Um R² de 0.52 é um resultado significativo.

## Slide 7: Importância de Features (Top 5)
- **Gráfico/Lista:** Apresentar as 5 features mais importantes do Random Forest.
    1. `genre_encoded` (≈ 20.0%)
    2. `acousticness` (≈ 8.7%)
    3. `duration_s` (≈ 8.3%)
    4. `danceability` (≈ 8.0%)
    5. `valence` (≈ 7.8%)
- **Conclusão:** O gênero é o fator dominante, seguido por características de áudio que definem a "sensação" da música.

## Slide 8: Discussão das Features Chave
- **Gênero:** A popularidade está fortemente ligada ao nicho musical, confirmando a importância dessa variável.
- **Acousticness:** Músicas menos acústicas (mais produzidas/eletrônicas) tendem a ter maior impacto na popularidade.
- **Danceability & Valence:** Músicas mais dançantes e com maior positividade/alegria são preditores importantes.

## Slide 9: Limitações do Estudo
- **Fatores Não-Modelados:** O modelo não considera o histórico do artista, o investimento em marketing ou o contexto cultural.
- **Codificação de Gênero:** O uso de Label Encoding para o gênero pode ter introduzido um viés ordinal.

## Slide 10: Sugestões de Melhoria
- **Otimização:** Realizar Grid Search ou Otimização Bayesiana para refinar hiperparâmetros.
- **Feature Engineering:** Criar features de agregação (ex: popularidade média do artista).
- **Modelos Alternativos:** Testar técnicas de *Target Encoding* para o gênero ou modelos de Deep Learning.

## Slide 11: Conclusão Final
- O projeto alcançou o objetivo de modelar a popularidade, com o Random Forest sendo o modelo mais robusto.
- A popularidade é um fenômeno não-linear, onde o gênero e a acústica são os principais fatores preditivos.
- O modelo serve como uma base sólida para entender a influência das características intrínsecas da música.

## Slide 12: Agradecimentos e Perguntas
- **Título:** Obrigado!
- **Conteúdo:** Espaço para perguntas e contatos.
- **Imagem:** (Sugestão de um gráfico relevante da EDA, como a matriz de correlação ou a distribuição da popularidade).
