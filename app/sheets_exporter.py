# app/sheets_exporter.py

import gspread
from oauth2client.service_account import ServiceAccountCredentials

def exportar_para_google_sheets(resumo, pontos):
    # ATENÇÃO: você precisa de um arquivo .json de credenciais da API do Google
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("google-credentials.json", scope)
    client = gspread.authorize(creds)

    sheet = client.open("Relatorio de Entregas").sheet1
    sheet.append_row(["Placa", "Distância (km)", "Tempo (min)", "Paradas"])
    sheet.append_row([resumo['placa'], resumo['distancia_km'], resumo['tempo_minutos'], resumo['paradas_detectadas']])

    sheet.append_row(["---", "Log da Rota", "---", "---"])
    sheet.append_row(["timestamp", "latitude", "longitude", "velocidade"])
    for p in pontos:
        sheet.append_row([p['timestamp'], p['latitude'], p['longitude'], p['velocidade']])
