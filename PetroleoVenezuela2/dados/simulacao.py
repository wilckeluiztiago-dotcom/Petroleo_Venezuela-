import numpy as np
import pandas as pd
from datetime import datetime, timedelta

class SimuladorProducao:
    """
    Gera dados sintéticos de produção de petróleo para campos venezuelanos,
    simulando curvas de declínio e sazonalidade.
    """
    
    def __init__(self, seed=42):
        np.random.seed(seed)
    
    def gerar_historico_campo(self, nome_campo, data_inicio='2000-01-01', data_fim='2023-12-31', 
                              qi=100000, di_anual=0.10, b=0.5, ruido=0.05):
        """
        Gera histórico mensal de produção usando modelo hiperbólico modificado com ruído.
        
        Params:
            qi: Vazão inicial (bbl/dia)
            di_anual: Taxa de declínio nominal anual
            b: Fator hiperbólico (0=exponencial, 1=harmônico)
            ruido: Desvio padrão do ruído aleatório (percentual)
        """
        datas = pd.date_range(start=data_inicio, end=data_fim, freq='ME')
        meses = np.arange(len(datas))
        
        # Converter declínio anual efetivo para nominal mensal
        # di_mensal ~ di_anual / 12 (aproximação simples para simulação)
        di = di_anual / 12.0
        
        # Modelo de Declínio Hiperbólico: q(t) = qi / (1 + b * di * t)^(1/b)
        if abs(b) < 1e-3: # Exponencial
            q = qi * np.exp(-di * meses)
        else:
            q = qi / ((1 + b * di * meses)**(1/b))
        
        # Adicionar sazonalidade e ruído operacional
        fator_ruido = np.random.normal(1, ruido, size=len(meses))
        
        # Eventos de "shutdown" ou problemas operacionais (picos negativos ocasionais)
        eventos = np.random.choice([1.0, 0.8, 0.5], size=len(meses), p=[0.95, 0.04, 0.01])
        
        producao = q * fator_ruido * eventos
        
        df = pd.DataFrame({
            'data': datas,
            'campo': nome_campo,
            'producao_bpd': producao.astype(int),
            'metodo_recuperacao': 'Primaria/Secundaria'
        })
        
        return df

    def simular_cenario_venezuela(self):
        """
        Gera um dataset combinado para os principais campos.
        """
        # Dados aproximados para simulação
        campos = [
            {'nome': 'Campo Tia Juana', 'qi': 150000, 'di': 0.08, 'b': 0.3}, # Campo maduro, declínio lento
            {'nome': 'Campo Carabobo (Faja)', 'qi': 80000, 'di': 0.02, 'b': 0.8}, # Pesado, declínio muito lento
            {'nome': 'Campo El Furrial', 'qi': 120000, 'di': 0.12, 'b': 0.4}  # Convencional leste
        ]
        
        dfs = []
        for c in campos:
            df = self.gerar_historico_campo(c['nome'], qi=c['qi'], di_anual=c['di'], b=c['b'])
            dfs.append(df)
            
        return pd.concat(dfs, ignore_index=True)
