import pandas as pd
import numpy as np

class GerenciadorDadosPetroleo:
    """
    Classe responsável por gerenciar e simular a coleta de dados de fontes
    como OPEP, EIA e BP para a indústria petrolífera venezuelana.
    """
    def __init__(self):
        # Simulação de cache de dados
        self.dados_producao = None
        self.dados_reservas = None

    def buscar_dados_eia(self):
        """
        Simula a busca de dados históricos de produção da EIA
        (Energy Information Administration).
        Retorna um DataFrame com produção diária (milhões de barris).
        """
        print("Conectando à API da EIA (Simulado)...")
        # Dados simulados com base em tendências históricas reais aproximadas
        datas = pd.date_range(start='2010-01-01', end='2024-01-01', freq='M')
        
        # Tendência de declínio simulada
        producao_base = 2.5  # 2.5 MMbbl/d em 2010
        declinio = np.linspace(0, 1.8, len(datas)) # Queda para ~0.7 MMbbl/d
        noise = np.random.normal(0, 0.05, len(datas)) # Variações mensais
        
        valores_producao = np.maximum(producao_base - declinio + noise, 0.5)
        
        self.dados_producao = pd.DataFrame({
            'Data': datas,
            'Producao_MMbbl': valores_producao,
            'Fonte': 'EIA Simulado'
        })
        return self.dados_producao

    def buscar_dados_opep(self):
        """
        Simula dados de reservas provadas da OPEP (Annual Statistical Bulletin).
        """
        print("Consultando dados anuais da OPEP (Simulado)...")
        # Venezuela tem as maiores reservas provadas do mundo (~303 Bilhões de barris)
        anos = [2018, 2019, 2020, 2021, 2022]
        reservas = [302.8, 303.8, 303.5, 303.4, 303.3] # Bilhões de barris
        
        self.dados_reservas = pd.DataFrame({
            'Ano': anos,
            'Reservas_Gbbl': reservas,
            'Fonte': 'OPEC ASB Simulado'
        })
        return self.dados_reservas

    def integracao_satelite_mock(self):
        """
        Simula a integração com dados de satélite (ex: VIIRS para flaring).
        Retorna coordenadas de pontos de calor (flaring) detectados.
        """
        print("Integrando com Google Earth Engine (Mock)...")
        # Coordenadas aproximadas na região de Monagas/Anzoátegui (Faixa do Orinoco)
        pontos_flaring = [
            {'lat': 9.15, 'lon': -63.50, 'intensidade': 'Alta'},
            {'lat': 9.20, 'lon': -63.80, 'intensidade': 'Media'},
            {'lat': 9.80, 'lon': -63.20, 'intensidade': 'Alta'},
            # Lago de Maracaibo
            {'lat': 10.40, 'lon': -71.50, 'intensidade': 'Baixa'}
        ]
        return pd.DataFrame(pontos_flaring)
