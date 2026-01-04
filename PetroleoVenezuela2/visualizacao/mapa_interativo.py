import folium
import geopandas as gpd
import sys
import os

# Adicionar diretório raiz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from geografia.camadas_geo import criar_bacia_maracaibo_detalhada, criar_faja_orinoco_blocos, criar_infraestrutura_avancada
from dados.gerenciador_dados import GerenciadorDadosPetroleo

def gerar_mapa_avancado():
    """
    Gera um mapa profissional e detalhado da indústria petrolífera venezuelana.
    """
    print("Gerando mapa interativo avançado...")
    
    # 1. Configuração do Mapa Base
    # Usar tiles 'CartoDB dark_matter' para contraste com cores vibrantes (look moderno)
    mapa = folium.Map(
        location=[8.5, -66.0], 
        zoom_start=6, 
        tiles='CartoDB dark_matter',
        control_scale=True
    )
    
    title_html = '''
             <h3 align="center" style="font-size:16px"><b>Venezuela Oil & Gas Intelligence Map</b></h3>
             '''
    mapa.get_root().html.add_child(folium.Element(title_html))

    # 2. Carregar Dados Detalhados
    gdf_bacia_maracaibo, gdf_campos_maracaibo = criar_bacia_maracaibo_detalhada()
    gdf_orinoco = criar_faja_orinoco_blocos()
    gdf_infra, gdf_dutos = criar_infraestrutura_avancada()
    
    # 3. Estilização e Adição de Camadas
    
    # --- Bacia de Maracaibo (Geral) ---
    folium.GeoJson(
        gdf_bacia_maracaibo,
        name='Bacias Sedimentares',
        style_function=lambda x: {
            'fillColor': '#215d6e', 
            'color': '#215d6e', 
            'weight': 1, 
            'fillOpacity': 0.2
        },
        tooltip=folium.GeoJsonTooltip(fields=['nome', 'tipo'])
    ).add_to(mapa)
    
    # --- Campos de Maracaibo (Detalhe) ---
    folium.GeoJson(
        gdf_campos_maracaibo,
        name='Campos Costeiros Bolívar',
        style_function=lambda x: {
            'fillColor': '#e6550d', # Laranja escuro
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.7
        },
        tooltip=folium.GeoJsonTooltip(fields=['nome', 'tipo', 'reservas_estimadas_gb'], aliases=['Campo', 'Tipo', 'Reservas (Gb)'])
    ).add_to(mapa)

    # --- Faixa do Orinoco (Blocos) ---
    # Cores distintas para cada bloco
    cores_blocos = {
        'Boyacá': '#8c564b', 
        'Junín': '#e377c2', 
        'Ayacucho': '#bcbd22', 
        'Carabobo': '#17becf'
    }
    
    folium.GeoJson(
        gdf_orinoco,
        name='Faixa do Orinoco (Blocos)',
        style_function=lambda feature: {
            'fillColor': cores_blocos.get(feature['properties']['nome'], 'gray'),
            'color': 'white', 
            'weight': 1, 
            'fillOpacity': 0.6
        },
        tooltip=folium.GeoJsonTooltip(fields=['nome', 'tipo'])
    ).add_to(mapa)
    
    # --- Infraestrutura (Refinarias e Terminais) ---
    infra_group = folium.FeatureGroup(name="Infraestrutura (Downstream)")
    
    for _, row in gdf_infra.iterrows():
        # Ícones personalizados baseados no tipo
        icon_color = 'red' if 'Refinaria' in row['tipo'] else 'blue'
        icon_type = 'fire' if 'Refinaria' in row['tipo'] else 'anchor'
        
        folium.Marker(
            location=[row.geometry.y, row.geometry.x],
            popup=folium.Popup(f"<b>{row['nome']}</b><br>Tipo: {row['tipo']}<br>Capacidade: {row['capacidade']}", max_width=300),
            icon=folium.Icon(color=icon_color, icon=icon_type, prefix='fa')
        ).add_to(infra_group)
    infra_group.add_to(mapa)

    # --- Dutos (Midstream) ---
    folium.GeoJson(
        gdf_dutos,
        name='Oleodutos Principais',
        style_function=lambda x: {'color': '#7f7f7f', 'weight': 4, 'opacity': 0.8},
        tooltip=folium.GeoJsonTooltip(fields=['nome', 'tipo'])
    ).add_to(mapa)

    # --- Satélite (Mock Flaring) ---
    gerenciador = GerenciadorDadosPetroleo()
    df_satelite = gerenciador.integracao_satelite_mock()
    
    heatmap_group = folium.FeatureGroup(name="Monitoramento Satélite (Análise de Flaring)")
    from folium.plugins import HeatMap
    
    # Converter para lista de [lat, lon, peso]
    heat_data = [[row['lat'], row['lon'], 1.0 if row['intensidade']=='Alta' else 0.5] for _, row in df_satelite.iterrows()]
    
    HeatMap(heat_data, radius=15, blur=10, max_zoom=10).add_to(heatmap_group)
    
    # Círculos individuais também para clique
    for _, row in df_satelite.iterrows():
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=5,
            color='yellow',
            fill=True,
            fill_opacity=0.5,
            popup=f"Fonte de Calor Detectada ({row['intensidade']})"
        ).add_to(heatmap_group)
        
    heatmap_group.add_to(mapa)

    # Controles
    folium.LayerControl(collapsed=False).add_to(mapa)
    
    # Legenda Customizada (HTML simples flutuante)
    legend_html = '''
     <div style="position: fixed; 
     bottom: 50px; left: 50px; width: 150px; height: 160px; 
     border:2px solid grey; z-index:9999; font-size:12px;
     background-color:rgba(255, 255, 255, 0.8);
     padding: 10px; border-radius: 5px;">
     <b>Legenda</b><br>
     <i style="background:#e6550d; width:10px; height:10px; display:inline-block;"></i> Campos Oil<br>
     <i style="background:#8c564b; width:10px; height:10px; display:inline-block;"></i> Bloco Boyacá<br>
     <i style="background:#e377c2; width:10px; height:10px; display:inline-block;"></i> Bloco Junín<br>
     <i style="background:#bcbd22; width:10px; height:10px; display:inline-block;"></i> Bloco Ayacucho<br>
     <i style="background:#17becf; width:10px; height:10px; display:inline-block;"></i> Bloco Carabobo<br>
     <i class="fa fa-fire" style="color:red"></i> Refinarias<br>
     <i class="fa fa-anchor" style="color:blue"></i> Terminais<br>
     </div>
     '''
    mapa.get_root().html.add_child(folium.Element(legend_html))

    # Salvar
    output_path = os.path.join(os.path.dirname(__file__), 'mapa_venezuela_avancado.html')
    mapa.save(output_path)
    print(f"Mapa Avançado salvo em: {output_path}")

if __name__ == "__main__":
    gerar_mapa_avancado()
