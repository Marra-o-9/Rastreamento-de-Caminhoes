# app/sheets_exporter.py

import gspread
from oauth2client.service_account import ServiceAccountCredentials

def exportar_para_google_sheets(resumo, pontos):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("google-credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("Relatorio de Entregas")

    try:
        resumo_ws = sheet.worksheet("Resumo da Entrega")
    except:
        resumo_ws = sheet.add_worksheet(title="Resumo da Entrega", rows="1000", cols="10")
        resumo_ws.append_row(["Placa", "ID da Entrega", "Início", "Fim", "Tempo Total (min)", "Distância Total (km)", "Total de Paradas"])

    entrega_id = len(resumo_ws.get_all_values())
    resumo_ws.append_row([
        resumo['placa'], entrega_id, resumo['inicio'], resumo['fim'], resumo['tempo_minutos'], resumo['distancia_km'], resumo['paradas_detectadas']
    ])

    try:
        log_ws = sheet.worksheet("Log da Rota")
    except:
        log_ws = sheet.add_worksheet(title="Log da Rota", rows="2000", cols="10")
        log_ws.append_row(["Entrega ID", "Timestamp", "Latitude", "Longitude", "Velocidade (km/h)"])

    for p in pontos:
        log_ws.append_row([
            entrega_id, p['timestamp'], p['latitude'], p['longitude'], p['velocidade']
        ])

    if resumo.get('paradas'):
        try:
            paradas_ws = sheet.worksheet("Paradas")
        except:
            paradas_ws = sheet.add_worksheet(title="Paradas", rows="1000", cols="10")
            paradas_ws.append_row(["Entrega ID", "Timestamp", "Latitude", "Longitude", "Velocidade (km/h)"])

        for p in resumo['paradas']:
            paradas_ws.append_row([
                entrega_id, p['timestamp'], p['latitude'], p['longitude'], p['velocidade']
            ])
