import geopandas as gpd
from shapely.geometry import Polygon, Point, LineString
import pandas as pd

def criar_bacia_maracaibo_detalhada():
    """
    Cria a Bacia de Maracaibo com detalhes dos Campos Costeiros de Bolívar (BCF).
    """
    # 1. Bacia Geral (Polígono maior)
    coords_bacia = [
        (-73.0, 12.0), (-70.5, 12.0), 
        (-70.0, 9.0), (-73.5, 9.0), (-73.0, 12.0)
    ]
    gdf_bacia = gpd.GeoDataFrame(
        {'nome': ['Bacia do Lago de Maracaibo'], 'tipo': ['Bacia Sedimentar']},
        geometry=[Polygon(coords_bacia)],
        crs="EPSG:4326"
    )

    # 2. Campos Específicos (Tia Juana, Lagunillas, Bachaquero) - Aproximados no Lago
    # Coordenadas aproximadas na costa leste do lago
    campos_data = {
        'nome': ['Campo Tia Juana', 'Campo Lagunillas', 'Campo Bachaquero'],
        'tipo': ['Oil Field', 'Oil Field', 'Oil Field'],
        'reservas_estimadas_gb': [15, 20, 12] 
    }
    
    # Polígonos aproximados para os campos (retângulos simplificados na costa)
    polys = []
    # Tia Juana (~10.3N)
    polys.append(Polygon([(-71.4, 10.4), (-71.2, 10.4), (-71.2, 10.2), (-71.4, 10.2)]))
    # Lagunillas (~10.1N)
    polys.append(Polygon([(-71.35, 10.15), (-71.15, 10.15), (-71.15, 9.95), (-71.35, 9.95)]))
    # Bachaquero (~9.9N)
    polys.append(Polygon([(-71.3, 9.9), (-71.1, 9.9), (-71.1, 9.7), (-71.3, 9.7)]))

    gdf_campos = gpd.GeoDataFrame(
        campos_data,
        geometry=polys,
        crs="EPSG:4326"
    )

    return gdf_bacia, gdf_campos

def criar_faja_orinoco_blocos():
    """
    Cria a Faixa Petrolífera do Orinoco dividida em seus 4 blocos principais:
    Boyacá, Junín, Ayacucho, Carabobo.
    """
    # Latitude aproximada da faixa: 8.0N a 9.0N
    # Longitude: -67.5 (Oeste) até -62.0 (Leste)
    
    # Coordenadas de divisão (Oeste -> Leste)
    limites = [-68.0, -66.0, -65.0, -64.0, -62.0]
    nomes = ['Boyacá', 'Junín', 'Ayacucho', 'Carabobo']
    
    polys = []
    for i in range(4):
        lon_min = limites[i]
        lon_max = limites[i+1]
        # Criar polígono retangular para cada bloco
        # A faixa é ligeiramente inclinada, mas usaremos retângulos para visualização clara
        poly = Polygon([
            (lon_min, 9.0), (lon_max, 9.0),
            (lon_max, 8.0), (lon_min, 8.0), (lon_min, 9.0)
        ])
        polys.append(poly)
        
    gdf_faja = gpd.GeoDataFrame(
        {'nome': nomes, 'tipo': ['Bloque de Producción'] * 4},
        geometry=polys,
        crs="EPSG:4326"
    )
    return gdf_faja

def criar_infraestrutura_avancada():
    """
    Refinarias e Terminais de Exportação precisos.
    """
    infra_data = {
        'nome': [
            'Complexo Amuay', 'Complexo Cardón', 'Refinaria El Palito', 
            'Refinaria Puerto La Cruz', 'Terminal José Antonio Anzoátegui',
            'Complexo Bajo Grande'
        ],
        'tipo': ['Refinaria', 'Refinaria', 'Refinaria', 'Refinaria', 'Terminal Exportação', 'Terminal Gás'],
        'capacidade': ['645 kbpd', '310 kbpd', '140 kbpd', '200 kbpd', 'Export Hub', 'Gas Hub'],
        'lat': [11.75, 11.63, 10.48, 10.22, 10.10, 10.50],
        'lon': [-70.22, -70.22, -68.12, -64.63, -64.87, -71.65] # Bajo Grande aprox
    }
    
    gdf_infra = gpd.GeoDataFrame(
        infra_data,
        geometry=gpd.points_from_xy(infra_data['lon'], infra_data['lat']),
        crs="EPSG:4326"
    )
    
    # Dutos (Linhas esquemáticas conectando campos a terminais)
    # 1. Orinoco (Carabobo) -> Terminal Jose
    # 2. Maracaibo -> Amuay/Cardon
    
    lines = [
        LineString([(-64.0, 8.5), (-64.87, 10.10)]), # Oleoduto Extra-Pesado
        LineString([(-71.25, 10.13), (-70.22, 11.63)]) # Duto Ulé-Amuay
    ]
    gdf_dutos = gpd.GeoDataFrame(
        {'nome': ['Duto Orinoco-Jose', 'Duto Ulé-Amuay'], 'tipo': ['Oleoduto', 'Oleoduto']},
        geometry=lines,
        crs="EPSG:4326"
    )
    
    return gdf_infra, gdf_dutos
