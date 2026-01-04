import plotly.graph_objects as go
import numpy as np
import pandas as pd
import geopandas as gpd
import sys
import os

# Importar módulos locais
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from geografia.camadas_geo import criar_bacia_maracaibo_detalhada

def gerar_visualizacao_3d_maracaibo():
    """
    Gera uma visualização 3D topográfica/batimétrica simulada da Bacia de Maracaibo.
    Salva como arquivo HTML.
    """
    print("Gerando visualização 3D da Bacia de Maracaibo...")
    
    # 1. Obter dados vetoriais da bacia
    gdf_bacia, gdf_campos = criar_bacia_maracaibo_detalhada()
    
    # 2. Criar Grade (Grid) para Superfície 3D
    # Intervalo de coordenadas da bacia (simplificado)
    x_range = np.linspace(-73.0, -70.0, 100) # Longitude
    y_range = np.linspace(9.0, 12.0, 100)    # Latitude
    X, Y = np.meshgrid(x_range, y_range)

    # 3. Modelar Profundidade (Simulação)
    # A bacia é mais profunda no centro e rasa nas bordas
    # Z representa a profundidade do embasamento (negativo)
    cx, cy = -71.5, 10.5 # Centro aproximado
    dist_sq = (X - cx)**2 + (Y - cy)**2
    # Modelo Gaussiano invertido para simular a bacia
    Z = -5000 * np.exp(-dist_sq / 0.5)  # Profundidade em metros (máx 5km)
    
    # Adicionar relevo randômico para realismo
    Z += np.random.normal(0, 100, Z.shape)

    # 4. Plotar Superfície da Bacia
    bs_surface = go.Surface(
        z=Z, x=X, y=Y,
        colorscale='Viridis',
        name='Embasamento Sedimentar',
        opacity=0.9
    )

    # 5. Adicionar Campos de Petróleo como "Patches" flutuantes na superfície ou acima dela
    # Vamos representá-los como pontos 3D projetados na superfície
    campos_x = []
    campos_y = []
    campos_z = []
    campos_text = []
    
    for idx, row in gdf_campos.iterrows():
        # Centroid do polígono do campo
        centroid = row.geometry.centroid
        cx_pt = centroid.x
        cy_pt = centroid.y
        
        # Encontrar profundidade aproximada nesse ponto (interpolação simples)
        # Para visualização, vamos colocá-los "no topo" ou em uma camada de reservatório
        # Z_reservatorio ~ Z * 0.8
        dist_pt = (cx_pt - cx)**2 + (cy_pt - cy)**2
        z_pt = -5000 * np.exp(-dist_pt / 0.5) * 0.8
        
        campos_x.append(cx_pt)
        campos_y.append(cy_pt)
        campos_z.append(z_pt)
        campos_text.append(f"{row['nome']}<br>Reservas: {row['reservas_estimadas_gb']} Gb")

    campos_scatter = go.Scatter3d(
        x=campos_x, y=campos_y, z=campos_z,
        mode='markers+text',
        marker=dict(
            size=10,
            color='red',
            symbol='diamond'
        ),
        text=[t.split('<')[0] for t in campos_text], # Apenas nome no texto direto
        textposition="top center",
        hovertext=campos_text,
        name='Campos de Petróleo'
    )

    # 6. Configurar Layout
    layout = go.Layout(
        title='Modelo 3D da Bacia de Maracaibo (Simulação Estrutural)',
        width=1200,
        height=800,
        scene=dict(
            xaxis_title='Longitude',
            yaxis_title='Latitude',
            zaxis_title='Profundidade (m)',
            aspectratio=dict(x=1, y=1, z=0.4), # Exagero vertical
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.2)
            )
        ),
        template='plotly_dark'
    )

    fig = go.Figure(data=[bs_surface, campos_scatter], layout=layout)
    
    output_path = os.path.join(os.path.dirname(__file__), 'bacia_maracaibo_3d.html')
    fig.write_html(output_path)
    print(f"Visualização 3D salva em: {output_path}")

if __name__ == "__main__":
    gerar_visualizacao_3d_maracaibo()
