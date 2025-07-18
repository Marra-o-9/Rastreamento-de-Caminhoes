# app/db.py

import sqlite3
from .rota_analisador import analisar_rota
from .sheets_exporter import exportar_para_google_sheets

def get_db_connection():
    conn = sqlite3.connect('rastreamento.db')
    conn.row_factory = sqlite3.Row
    return conn

def insert_location(data):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS localizacoes (
            id INTEGER PRIMARY KEY,
            placa TEXT,
            timestamp TEXT,
            latitude REAL,
            longitude REAL,
            velocidade REAL
        )
    ''')

    cur.execute('''
        INSERT INTO localizacoes (placa, timestamp, latitude, longitude, velocidade)
        VALUES (?, ?, ?, ?, ?)
    ''', (data['placa'], data['timestamp'], data['latitude'], data['longitude'], data['velocidade']))

    conn.commit()
    conn.close()

def finalize_trip(placa):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM localizacoes WHERE placa = ? ORDER BY timestamp', (placa,))
    rows = cur.fetchall()
    conn.close()

    if not rows:
        return {'erro': 'Nenhum dado encontrado para essa placa'}

    resumo = analisar_rota(rows)
    if 'erro' in resumo:
        return resumo

    exportar_para_google_sheets(resumo, resumo['pontos_rota'])
    return {
        'placa': resumo['placa'],
        'distancia_km': resumo['distancia_km'],
        'tempo_minutos': resumo['tempo_minutos'],
        'paradas_detectadas': resumo['paradas_detectadas']
    }
