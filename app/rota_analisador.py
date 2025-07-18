# app/rota_analisador.py

from .config import GARAGEM_COORDS, DISTANCIA_TOLERANCIA_KM
from .utils import haversine
from datetime import datetime
from .parada_detector import detectar_paradas

def analisar_rota(rows):
    pontos_filtrados = []
    saiu_da_garagem = False
    voltou_para_garagem = False

    for ponto in rows:
        lat, lon = ponto['latitude'], ponto['longitude']
        dist_garagem = haversine(lat, lon, *GARAGEM_COORDS)

        if not saiu_da_garagem and dist_garagem > DISTANCIA_TOLERANCIA_KM:
            saiu_da_garagem = True
            pontos_filtrados.append(ponto)
        elif saiu_da_garagem and not voltou_para_garagem:
            pontos_filtrados.append(ponto)
            if dist_garagem <= DISTANCIA_TOLERANCIA_KM:
                voltou_para_garagem = True
                break

    if len(pontos_filtrados) < 2:
        return {'erro': 'Viagem incompleta ou fora da garagem'}

    paradas = detectar_paradas(pontos_filtrados)

    distancia_total = 0.0
    for i in range(1, len(pontos_filtrados)):
        p1 = pontos_filtrados[i - 1]
        p2 = pontos_filtrados[i]
        distancia_total += haversine(p1['latitude'], p1['longitude'], p2['latitude'], p2['longitude'])

    tempo_inicio = datetime.fromisoformat(pontos_filtrados[0]['timestamp'])
    tempo_fim = datetime.fromisoformat(pontos_filtrados[-1]['timestamp'])
    tempo_total = (tempo_fim - tempo_inicio).total_seconds() / 60

    return {
        'placa': pontos_filtrados[0]['placa'],
        'distancia_km': round(distancia_total, 2),
        'tempo_minutos': round(tempo_total, 1),
        'paradas_detectadas': len(paradas),
        'paradas': paradas,
        'pontos_rota': pontos_filtrados,
        'inicio': tempo_inicio.strftime('%Y-%m-%d %H:%M'),
        'fim': tempo_fim.strftime('%Y-%m-%d %H:%M')
    }
