# app/sheets_exporter.py

import gspread
from oauth2client.service_account import ServiceAccountCredentials

def exportar_para_google_sheets(resumo, pontos):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("google-credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("Relatorio de Entregas")

    # -------------------------
    # Aba 1: Resumo das Entregas
    # -------------------------
    try:
        resumo_ws = sheet.worksheet("Resumo")
    except:
        resumo_ws = sheet.add_worksheet(title="Resumo", rows="1000", cols="10")
        resumo_ws.append_row(["Caminhão", "Entrega ID", "Início", "Fim", "Duração (min)", "Distância (km)", "Paradas"])

    entrega_id = len(resumo_ws.get_all_values())  # Assume que cabeçalho está na linha 1

    resumo_ws.append_row([
        resumo['placa'],
        entrega_id,
        resumo['inicio'],
        resumo['fim'],
        resumo['tempo_minutos'],
        resumo['distancia_km'],
        resumo['paradas_detectadas']
    ])

    # -------------------------
    # Aba 2: Log da Rota
    # -------------------------
    try:
        log_ws = sheet.worksheet("Log da Rota")
    except:
        log_ws = sheet.add_worksheet(title="Log da Rota", rows="2000", cols="10")
        log_ws.append_row(["Entrega ID", "timestamp", "latitude", "longitude", "velocidade"])

    for p in pontos:
        log_ws.append_row([
            entrega_id,
            p['timestamp'],
            p['latitude'],
            p['longitude'],
            p['velocidade']
        ])

    # -------------------------
    # Aba 3: Paradas
    # -------------------------
    if resumo.get('paradas'):
        try:
            paradas_ws = sheet.worksheet("Paradas")
        except:
            paradas_ws = sheet.add_worksheet(title="Paradas", rows="1000", cols="10")
            paradas_ws.append_row(["Entrega ID", "timestamp", "latitude", "longitude", "velocidade"])

        for p in resumo['paradas']:
            paradas_ws.append_row([
                entrega_id,
                p['timestamp'],
                p['latitude'],
                p['longitude'],
                p['velocidade']
            ])
