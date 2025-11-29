# 5. Avaliação, Interpretação dos Resultados e Conclusão

## 5.1. Avaliação dos Modelos de Machine Learning

Três modelos de regressão foram aplicados para prever a popularidade das músicas com base em suas características: Regressão Linear, Random Forest Regressor e XGBoost Regressor. A avaliação foi realizada utilizando as métricas **R² (Coeficiente de Determinação)** e **RMSE (Root Mean Squared Error)** no conjunto de dados de teste.

| Modelo | R² (Coeficiente de Determinação) | RMSE (Erro Quadrático Médio da Raiz) |
| :--- | :--- | :--- |
| Regressão Linear | 0.0234 | 0.2195 |
| **Random Forest Regressor** | **0.5236** | **0.1533** |
| XGBoost Regressor | 0.3215 | 0.1830 |

### Interpretação das Métricas

O modelo de **Regressão Linear** apresentou um desempenho muito baixo (R² ≈ 0.02), indicando que as características de áudio e gênero têm uma relação predominantemente não-linear com a popularidade, e que um modelo linear é inadequado para capturar essa complexidade.

O **Random Forest Regressor** demonstrou o melhor desempenho, com um **R² de 0.5236**. Isso significa que o modelo é capaz de explicar aproximadamente **52.36% da variância** na popularidade das músicas. Embora não seja um R² extremamente alto, é um resultado significativo para um problema complexo e ruidoso como a previsão de popularidade, que é influenciada por fatores externos (marketing, tendências culturais, etc.) não presentes no dataset. O RMSE de 0.1533, em uma escala normalizada de 0 a 1, indica um erro de previsão relativamente baixo.

O **XGBoost Regressor** obteve um desempenho intermediário (R² ≈ 0.32), superando a Regressão Linear, mas ficando aquém do Random Forest.

## 5.2. Análise de Importância de Features (Random Forest)

A análise de importância de features do modelo Random Forest, o de melhor desempenho, revela quais características mais contribuíram para a previsão da popularidade:

| Feature | Importância (Score) |
| :--- | :--- |
| `genre_encoded` | 0.1998 |
| `acousticness` | 0.0866 |
| `duration_s` | 0.0832 |
| `danceability` | 0.0801 |
| `valence` | 0.0777 |
| `loudness` | 0.0763 |
| `speechiness` | 0.0753 |
| `tempo` | 0.0750 |
| `energy` | 0.0721 |
| `liveness` | 0.0652 |

A feature mais importante é o **gênero (`genre_encoded`)**, o que é intuitivo, pois a popularidade está intrinsecamente ligada ao nicho musical. Entre as características de áudio, a **acústica (`acousticness`)**, a **duração (`duration_s`)**, a **danceabilidade (`danceability`)** e a **valência (`valence`)** são as mais relevantes.

**Conclusões da Análise de Features:**
*   **Gênero é o Fator Dominante:** A popularidade é fortemente influenciada pelo gênero musical, confirmando a necessidade de incluir essa variável no modelo.
*   **Características Sonoras Relevantes:** Músicas com menor `acousticness` (mais produzidas/eletrônicas), duração específica, maior `danceability` (ritmo e adequação para dança) e maior `valence` (positividade/alegria) tendem a ter maior impacto na popularidade, de acordo com o modelo.

## 5.3. Conclusão Geral e Aprendizados

O projeto demonstrou que é possível prever a popularidade de músicas do Spotify com uma precisão razoável (R² de 0.52) utilizando apenas as características de áudio e o gênero. O modelo **Random Forest Regressor** foi o mais eficaz, confirmando que a relação entre as features e a popularidade é complexa e não-linear.

**Principais Aprendizados:**
1.  **A Importância do ETL:** O processo de ETL, incluindo a normalização das features e a codificação do gênero, foi crucial para o sucesso da modelagem.
2.  **Não-Linearidade da Popularidade:** A baixa performance da Regressão Linear reforça que a popularidade é um fenômeno complexo que exige modelos mais robustos (como Random Forest ou XGBoost) para ser modelado.
3.  **Fatores de Popularidade:** O gênero e as características de áudio como `acousticness`, `danceability` e `valence` são os principais preditores.

## 5.4. Limitações e Possíveis Melhorias

**Limitações:**
*   **Fatores Externos:** O modelo não considera fatores externos cruciais para a popularidade, como o histórico do artista, o investimento em marketing, a data de lançamento e o contexto cultural.
*   **Codificação de Gênero:** A codificação do gênero (`genre_encoded`) com Label Encoding pode ter introduzido uma ordem artificial. Uma melhoria seria usar técnicas de *Target Encoding* ou *Embedding* para lidar com a alta cardinalidade do gênero de forma mais eficaz.

**Melhorias Futuras:**
1.  **Otimização de Hiperparâmetros:** Realizar uma busca em grade (Grid Search) ou otimização bayesiana para refinar os hiperparâmetros do Random Forest e do XGBoost.
2.  **Feature Engineering Avançada:** Explorar a criação de novas features, como a média de popularidade do artista ou a popularidade média do gênero.
3.  **Modelos de Deep Learning:** Testar redes neurais (como uma MLP) para capturar relações ainda mais complexas.
4.  **Análise de Classificação:** Transformar o problema em classificação (ex: "Top 10% mais populares") para ver se a acurácia melhora.

---
*Este documento atende aos entregáveis do Integrante 4 para as etapas 4 e 5 do projeto.*
