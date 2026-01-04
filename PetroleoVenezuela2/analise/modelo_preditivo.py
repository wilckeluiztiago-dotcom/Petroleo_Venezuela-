import numpy as np
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score

class AnaliseDeclinio:
    """
    Implementa Análise de Curva de Declínio (DCA - Decline Curve Analysis)
    focada no método de Arps (Exponencial, Hiperbólico, Harmônico).
    """
    
    def __init__(self):
        self.params = None
        self.modelo_tipo = None
    
    @staticmethod
    def _arps_model(t, qi, di, b):
        """
        Equação geral de Arps.
        qi: taxa inicial
        di: taxa de declínio inicial
        b: fator b (0=exponencial, 1=harmônico, 0<b<1=hiperbólico)
        """
        # Evitar divisão por zero ou potências inválidas
        # Para b=0, a equação é qi * exp(-di * t)
        # Como curve_fit ajusta parâmetros contínuos, tratamos casos limites
        
        if abs(b) < 1e-4: # Aproximação para Exponencial
            return qi * np.exp(-di * t)
        elif abs(b - 1) < 1e-4: # Aproximação para Harmônico
            return qi / (1 + di * t)
        else: # Hiperbólico
            # Proteção para base negativa
            base = 1 + b * di * t
            # Se base <= 0, o modelo físico não faz sentido, retornamos 0 ou nan
            return np.where(base > 0, qi / (base ** (1/b)), 0)

    def ajustar_modelo(self, tempos, producoes):
        """
        Ajusta o modelo de Arps aos dados históricos.
        tempos: array de dias/meses (numérico)
        producoes: array de taxas de produção
        """
        # Limites para os parâmetros: qi > 0, di > 0, 0 <= b <= 1
        bounds = ((0, 0, 0), (np.inf, np.inf, 1.0))
        
        # Chute inicial
        p0 = [np.max(producoes), 0.1, 0.5]
        
        try:
            self.params, _ = curve_fit(
                self._arps_model, 
                tempos, 
                producoes, 
                p0=p0, 
                bounds=bounds,
                maxfev=5000
            )
            
            # Determinar tipo com base no b encontrado
            b = self.params[2]
            if b < 0.1:
                self.modelo_tipo = "Exponencial"
            elif b > 0.9:
                self.modelo_tipo = "Harmônico"
            else:
                self.modelo_tipo = "Hiperbólico"
                
            return True
        except Exception as e:
            print(f"Erro ao ajustar modelo DCA: {e}")
            return False

    def prever_producao(self, tempos_futuros):
        """
        Gera previsões baseadas no modelo ajustado.
        """
        if self.params is None:
            raise ValueError("Modelo não ajustado. Execute ajustar_modelo primeiro.")
            
        return self._arps_model(tempos_futuros, *self.params)

    def calcular_metricas(self, tempos, producoes_reais):
        """
        Calcula R² para validação.
        """
        predicoes = self.prever_producao(tempos)
        return r2_score(producoes_reais, predicoes)

    def obter_parametros(self):
        if self.params is None:
            return {}
        return {
            'qi': self.params[0],
            'di': self.params[1],
            'b': self.params[2],
            'tipo': self.modelo_tipo
        }
