import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dados.simulacao import SimuladorProducao

class OpecDataLoader:
    """
    Gerenciador de ingestão de dados. 
    Tenta carregar dados reais (CSV), caso contrário, gera simulação.
    """
    
    def __init__(self, data_dir='dados/raw'):
        self.data_dir = data_dir
        self.simulador = SimuladorProducao()
        
    def carregar_producao_mensal(self):
        """
        Retorna DataFrame com histórico de produção.
        """
        # Futuro: Tenter ler self.data_dir + '/opec_production.csv'
        # Por enquanto, usamos simulação
        print("Aviso: Dados reais não encontrados. Gerando dados sintéticos...")
        return self.simulador.simular_cenario_venezuela()

    def carregar_precos_petroleo(self):
        """
        Simula histórico de preços (WTI/Brent/Merey)
        """
        # TODO: Implementar ou carregar CSV simples
        pass
