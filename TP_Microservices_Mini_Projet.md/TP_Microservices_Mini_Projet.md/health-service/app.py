from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required
import requests
import os
from datetime import timedelta

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'secret-key-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

jwt = JWTManager(app)

# Simulation de stockage pour les données de santé
health_db = {}

PERSON_SERVICE_URL = os.environ.get('PERSON_SERVICE_URL', 'http://person-service:5001')

def person_exists(person_id):
    """Vérifier que la personne existe via le service Personne"""
    try:
        resp = requests.get(f"{PERSON_SERVICE_URL}/persons/{person_id}", timeout=5)
        return resp.status_code == 200
    except:
        return False

@app.route('/health/<int:person_id>', methods=['GET'])
@jwt_required()
def get_health(person_id):
    """Lire les données de santé"""
    # Vérifier l'existence de la personne
    if not person_exists(person_id):
        return jsonify({"error": "Person does not exist"}), 404

    health_data = health_db.get(person_id, {})
    return jsonify(health_data), 200

@app.route('/health/<int:person_id>', methods=['POST'])
@jwt_required()
def add_health(person_id):
    """Ajouter des données de santé"""
    # Vérifier l'existence de la personne
    if not person_exists(person_id):
        return jsonify({"error": "Person does not exist"}), 404

    data = request.json
    if person_id not in health_db:
        health_db[person_id] = {}
    
    # Ajouter les données (ne pas supprimer les existantes)
    health_db[person_id].update(data)
    return jsonify({"status": "Success", "data": health_db[person_id]}), 200

@app.route('/health/<int:person_id>', methods=['PUT'])
@jwt_required()
def update_health(person_id):
    """Modifier des données de santé"""
    # Vérifier l'existence de la personne
    if not person_exists(person_id):
        return jsonify({"error": "Person does not exist"}), 404

    data = request.json
    if person_id not in health_db:
        health_db[person_id] = {}
    
    # Remplacer complètement les données
    health_db[person_id] = data
    return jsonify({"status": "Success", "data": health_db[person_id]}), 200

@app.route('/health/<int:person_id>', methods=['DELETE'])
@jwt_required()
def delete_health(person_id):
    """Supprimer les données de santé"""
    # Vérifier l'existence de la personne
    if not person_exists(person_id):
        return jsonify({"error": "Person does not exist"}), 404

    health_db.pop(person_id, None)
    return jsonify({"message": "Health data deleted"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)