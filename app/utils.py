# app/utils.py

import math
from datetime import datetime

GARAGEM_COORDS = (-23.55052, -46.63331)  # Exemplo: São Paulo (substitua pela real)
DISTANCIA_TOLERANCIA_KM = 0.2  # Aceita 200 metros como "dentro da garagem"
ULTIMO_PONTO = {}

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def process_point(data):
    placa = data['placa']
    ponto_atual = {
        'latitude': data['latitude'],
        'longitude': data['longitude'],
        'timestamp': datetime.fromisoformat(data['timestamp']),
        'velocidade': data['velocidade']
    }

    if placa not in ULTIMO_PONTO:
        ULTIMO_PONTO[placa] = ponto_atual
        return

    # Aqui você pode aplicar lógica de detecção de paradas em tempo real se quiser

def calcular_resumo_rota(rows):
    total_distancia = 0.0
    paradas = []
    pontos_filtrados = []

    # Define os limites da viagem (sai da garagem e retorna à garagem)
    saiu_da_garagem = False
    voltou_para_garagem = False

    for i in range(len(rows)):
        ponto = rows[i]
        lat = ponto['latitude']
        lon = ponto['longitude']
        dist_garagem = haversine(lat, lon, *GARAGEM_COORDS)

        if not saiu_da_garagem:
            if dist_garagem > DISTANCIA_TOLERANCIA_KM:
                saiu_da_garagem = True
                pontos_filtrados.append(ponto)
        elif not voltou_para_garagem:
            pontos_filtrados.append(ponto)
            if dist_garagem <= DISTANCIA_TOLERANCIA_KM:
                voltou_para_garagem = True
                break  # finaliza a viagem

    if len(pontos_filtrados) < 2:
        return {'erro': 'Viagem incompleta ou fora da garagem'}

    # Calcula distância e detecta paradas nos pontos filtrados
    for i in range(1, len(pontos_filtrados)):
        p1 = pontos_filtrados[i - 1]
        p2 = pontos_filtrados[i]
        dist = haversine(p1['latitude'], p1['longitude'], p2['latitude'], p2['longitude'])
        total_distancia += dist

        # Verifica se há parada (3 pontos consecutivos com velocidade < 5 km/h)
        if i >= 2 and all(float(pontos_filtrados[j]['velocidade']) < 5 for j in range(i - 2, i + 1)):
            paradas.append(pontos_filtrados[i])

    tempo_inicio = datetime.fromisoformat(pontos_filtrados[0]['timestamp'])
    tempo_fim = datetime.fromisoformat(pontos_filtrados[-1]['timestamp'])
    tempo_total = (tempo_fim - tempo_inicio).total_seconds() / 60

    return {
        'placa': pontos_filtrados[0]['placa'],
        'distancia_km': round(total_distancia, 2),
        'tempo_minutos': round(tempo_total, 1),
        'paradas_detectadas': len(paradas),
        'paradas': paradas,
        'pontos_rota': pontos_filtrados,
        'inicio': tempo_inicio.strftime('%Y-%m-%d %H:%M'),
        'fim': tempo_fim.strftime('%Y-%m-%d %H:%M')
    }
