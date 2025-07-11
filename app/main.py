# app/main.py

from flask import Blueprint, request, jsonify
from .db import insert_location, finalize_trip
from .utils import process_point

main_bp = Blueprint('main', __name__)

@main_bp.route('/rastrear', methods=['POST'])
def rastrear():
    data = request.get_json()
    required_keys = ['placa', 'timestamp', 'latitude', 'longitude', 'velocidade']
    if not all(k in data for k in required_keys):
        return jsonify({'error': 'JSON mal formatado'}), 400

    process_point(data)
    insert_location(data)
    return jsonify({'status': 'dados registrados com sucesso'})

@main_bp.route('/finalizar_entrega', methods=['POST'])
def finalizar_entrega():
    data = request.get_json()
    placa = data.get('placa')
    if not placa:
        return jsonify({'error': 'Placa do caminhão não informada'}), 400

    resumo = finalize_trip(placa)
    return jsonify(resumo)
