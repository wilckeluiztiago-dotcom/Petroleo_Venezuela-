import sys
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Setup paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dados.ingestao import OpecDataLoader
from analise.engenharia_reservatorios import DeclineCurveAnalyzer

def teste_dca_simulacao():
    print("Iniciando teste de fluxo de análise...")
    
    # 1. Carregar Dados
    loader = OpecDataLoader()
    df_prod = loader.carregar_producao_mensal()
    
    # Filtrar um campo específico para análise
    campo_alvo = 'Campo Tia Juana'
    df_campo = df_prod[df_prod['campo'] == campo_alvo].sort_values('data')
    
    print(f"Dados carregados para {campo_alvo}: {len(df_campo)} meses.")
    
    # 2. Executar Análise de Declínio
    analyzer = DeclineCurveAnalyzer()
    
    # Usar a produção como série temporal
    y_prod = df_campo['producao_bpd'].values
    datas = df_campo['data'].values
    
    print("Ajustando curva de declínio...")
    resultados = analyzer.fit_decline_curve(datas, y_prod)
    
    if resultados['success']:
        print("Ajuste bem sucedido:")
        print(f"  qi: {resultados['qi']:.2f}")
        print(f"  di (anual): {resultados['di_anual_nominal']:.2f} ({resultados['di_anual_nominal']*100:.1f}%)")
        print(f"  b: {resultados['b']:.2f}")
        print(f"  R2: {resultados['r2']:.4f}")
        
        # 3. Gerar Previsão para os próximos 5 anos (60 meses)
        len_hist = len(y_prod)
        previsao = analyzer.forecast_from_parameters(resultados, tempo_inicio_previsao=len_hist, duracao_meses=60)
        
        # Datas futuras
        ultima_data = pd.to_datetime(datas[-1])
        datas_futuras = pd.date_range(start=ultima_data + pd.Timedelta(days=30), periods=60, freq='ME')
        
        # Calcular curva ajustada sobre o histórico (para plotar o fit)
        ajuste_historico = analyzer.forecast_from_parameters(resultados, 0, len_hist)
        
        # 4. Plotar Resultados
        plt.figure(figsize=(10, 6))
        plt.scatter(datas, y_prod, alpha=0.5, color='gray', label='Histórico Real (Simulado)', s=10)
        plt.plot(datas, ajuste_historico, color='blue', linewidth=2, label='Ajuste DCA')
        plt.plot(datas_futuras, previsao, color='green', linestyle='--', linewidth=2, label='Previsão (5 anos)')
        
        plt.title(f"Análise de Declínio de Produção - {campo_alvo}")
        plt.xlabel("Data")
        plt.ylabel("Produção (bbl/dia)")
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        output_file = os.path.join(os.path.dirname(__file__), '../visualizacao/dca_teste.png')
        plt.savefig(output_file)
        print(f"Gráfico salvo em: {output_file}")
        
    else:
        print("Falha no ajuste da curva.")
        print(resultados)

if __name__ == "__main__":
    teste_dca_simulacao()
