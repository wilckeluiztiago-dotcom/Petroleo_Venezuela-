import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score

class DeclineCurveAnalyzer:
    """
    Realiza Análise de Curva de Declínio (DCA) usando equações de Arps.
    """
    
    @staticmethod
    def arps_equation(t, qi, di, b):
        """
        Equação geral de Arps.
        t: tempo (meses)
        qi: vazão inicial
        di: taxa de declínio inicial (mensal)
        b: fator de declínio (0=exp, 1=harm, 0<b<1=hiper)
        """
        # Evitar divisão por zero ou números complexos
        if di <= 0: return np.full_like(t, qi)
        
        # Exponencial (limite quando b -> 0)
        if abs(b) < 1e-4:
            return qi * np.exp(-di * t)
        else:
            return qi / ((1 + b * di * t)**(1/b))

    def fit_decline_curve(self, datas, producao):
        """
        Ajusta a curva de declínio aos dados de produção.
        Retorna parâmetros ótimos (qi, di, b) e métricas de ajuste.
        """
        # Normalizar tempo (t=0 no início do histórico fornecido)
        t = np.arange(len(producao))
        
        # Limites para parâmetros: qi > 0, di > 0, 0 <= b <= 1 (b pode ser > 1 em fraturados, mas vamos limitar)
        # Chute inicial (qi=max, di=0.01, b=0.5)
        p0 = [max(producao), 0.01, 0.5]
        bounds = ([0, 0, 0], [np.inf, 1.0, 2.0]) # di até 100%/mês, b até 2.0
        
        try:
            popt, pcov = curve_fit(self.arps_equation, t, producao, p0=p0, bounds=bounds)
            qi_fit, di_fit, b_fit = popt
            
            # Calcular R2
            y_pred = self.arps_equation(t, *popt)
            r2 = r2_score(producao, y_pred)
            
            return {
                'qi': qi_fit,
                'di_mensal': di_fit,
                'di_anual_nominal': di_fit * 12,
                'b': b_fit,
                'r2': r2,
                'success': True
            }
        except Exception as e:
            print(f"Erro no ajuste DCA: {e}")
            return {'success': False, 'error': str(e)}

    def prever_producao(self, params, meses_futuros=120):
        """
        Gera previsão baseada nos parâmetros ajustados.
        """
        if not params.get('success'):
            return None
            
        t_futuro = np.arange(meses_futuros)
        # Para previsão, o t=0 é o início do declínio ajustado. 
        # Se quisermos continuar do fim do histórico, precisaríamos ajustar t.
        # Mas Arps é t=0 no qi. 
        # Vamos assumir que a previsão é a continuação da curva "ideal"
        
        # O t para previsão deve começar onde o histórico parou? 
        # Sim, se qi for o qi ORIGINAL do poço.
        # Se fitamos qi no início do histórico, ok.
        
        # ATENÇÃO: Se o histórico for longo, t_futuro deve ser deslocado
        # Vamos retornar a curva completa (histórico fitado + futuro) ou apenas futuro?
        # Apenas futuro continuando a curva
        
        # Vamos assumir que o usuário quer a previsão a partir do tempo T_atual.
        # Precisamos saber qual o T correspondente ao fim do histórico.
        # Como fit_decline_curve não salva estado, o ideal é o usuário passar o T_start da previsão.
        pass # Simplificação: O método arps retorna a vazão dado um T relativo ao qi.
        
        qi = params['qi']
        di = params['di_mensal']
        b = params['b']
        
        q_pred = self.arps_equation(t_futuro, qi, di, b)
        return q_pred # Isso retornaria a curva desde o início t=0. 
    
    def forecast_from_parameters(self, params, tempo_inicio_previsao, duracao_meses):
        """
        Calcula a vazão para um período futuro, dado que t=0 foi o início do ajuste.
        """
        t_range = np.arange(tempo_inicio_previsao, tempo_inicio_previsao + duracao_meses)
        return self.arps_equation(t_range, params['qi'], params['di_mensal'], params['b'])
