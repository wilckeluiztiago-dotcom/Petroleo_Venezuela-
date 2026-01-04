# Pipeline Analítico da Indústria Petrolífera na Venezuela

**Autor:** Luiz Tiago Wilcke


## Visão Geral
Este projeto implementa um pipeline analítico em Python para modelar a indústria petrolífera venezuelana. O sistema integra dados de produção, mapeamento geográfico profundo de bacias e infraestrutura, e modelagem preditiva para análise de declínio de campos maduros.

## Estrutura do Projeto
- `dados/`: Módulos para ingestão e simulação de dados (OPEP, EIA, BP, Satélite).
- `geografia/`: Tratamento de dados espaciais (Bacias, Refinarias, Dutos).
- `analise/`: Modelos preditivos de engenharia de reservatórios.
- `visualizacao/`: Geração de mapas interativos e dashboards.

## Metodologia e Fontes de Dados

### 1. Fontes de Dados Integrais
O pipeline foi desenhado para ingerir dados de fontes autoritativas:
*   **Produção e Reservas:** OPEP (Annual Statistical Bulletin), EIA, e BP Statistical Review of World Energy.
*   **Geografia:** OpenStreetMap (OSM) e Natural Earth para limites administrativos e físicos.
*   **Sensoriamento Remoto:** Integração conceitual com Google Earth Engine para monitoramento de *flaring* e detecção de offshore slicks.

### 2. Camadas Geográficas (Mapas Profundos)
Utilizamos `Geopandas` e `Shapely` para manipular geometrias complexas:
*   **Polígonos de Bacias:** Delimitação precisa da Bacia de Maracaibo e da Faixa Petrolífera do Orinoco.
*   **Infraestrutura:** Localização georreferenciada de refinarias chave (Complexo Amuay-Cardón, Puerto La Cruz) e rede de dutos.

### 3. Modelagem Analítica
Aplicação de bibliotecas científicas (`Scikit-learn`, `NumPy`) para:
*   Análise de *Decline Curve Analysis* (DCA) em campos maduros.
*   Previsão de produção baseada em histórico.

### 4. Visualização Interativa
Uso de `Folium` para criar mapas táticos que permitem a inspeção detalhada de ativos e visualização espacial da produção.

## Como Executar
1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Execute o pipeline principal (exemplo):
   ```bash
   python visualizacao/mapa_interativo.py
   ```
