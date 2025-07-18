# app/parada_detector.py

from datetime import datetime, timedelta
from .config import TEMPO_MINIMO_PARADO_MIN, VELOCIDADE_LIMITE_PARADA

def detectar_paradas(pontos):
    paradas = []
    inicio_parada = None

    for i, p in enumerate(pontos):
        velocidade = float(p['velocidade'])
        timestamp = datetime.fromisoformat(p['timestamp'])

        if velocidade < VELOCIDADE_LIMITE_PARADA:
            if not inicio_parada:
                inicio_parada = {'inicio': timestamp, 'ponto': p}
            elif (timestamp - inicio_parada['inicio']) >= timedelta(minutes=TEMPO_MINIMO_PARADO_MIN):
                paradas.append(inicio_parada['ponto'])
                inicio_parada = None
        else:
            inicio_parada = None

    return paradas
