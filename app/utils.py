# app/utils.py

import math
from datetime import datetime

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
    total_paradas = 0
    tempo_inicio = datetime.fromisoformat(rows[0]['timestamp'])
    tempo_fim = datetime.fromisoformat(rows[-1]['timestamp'])

    for i in range(1, len(rows)):
        p1 = rows[i - 1]
        p2 = rows[i]
        dist = haversine(p1['latitude'], p1['longitude'], p2['latitude'], p2['longitude'])
        total_distancia += dist

        # Detecta parada se velocidade for 0 por 3 registros consecutivos (~3 minutos)
        if all(float(rows[j]['velocidade']) < 5 for j in range(i - 2, i + 1)) and i >= 2:
            total_paradas += 1

    tempo_total = (tempo_fim - tempo_inicio).total_seconds() / 60
    return {
        'placa': rows[0]['placa'],
        'distancia_km': round(total_distancia, 2),
        'tempo_minutos': round(tempo_total, 1),
        'paradas_detectadas': total_paradas
    }