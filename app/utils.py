# app/utils.py

import math
from datetime import datetime

ULTIMO_PONTO = {}
from .config import GARAGEM_COORDS, DISTANCIA_TOLERANCIA_KM

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
