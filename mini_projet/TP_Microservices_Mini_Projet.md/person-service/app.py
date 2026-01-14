from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import os
from datetime import timedelta

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'secret-key-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

db = SQLAlchemy(app)
jwt = JWTManager(app)

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

with app.app_context():
    db.create_all()

# Endpoint d'authentification
@app.route('/auth/login', methods=['POST'])
def login():
    """Générer un token JWT"""
    data = request.json
    if not data or not data.get('username'):
        return jsonify({"error": "Username required"}), 400
    
    access_token = create_access_token(identity=data['username'])
    return jsonify({"access_token": access_token}), 200

@app.route('/persons', methods=['POST'])
@jwt_required()
def create_person():
    """Créer une personne"""
    data = request.json
    if not data or not data.get('name'):
        return jsonify({"error": "Name required"}), 400
    
    new_person = Person(name=data['name'])
    db.session.add(new_person)
    db.session.commit()
    return jsonify({"id": new_person.id, "name": new_person.name}), 201

@app.route('/persons/<int:person_id>', methods=['GET'])
def get_person(person_id):
    """Récupérer une personne (pas d'auth pour permettre au service santé d'appeler)"""
    person = Person.query.get(person_id)
    if not person:
        return jsonify({"error": "Not found"}), 404
    return jsonify({"id": person.id, "name": person.name}), 200

@app.route('/persons/<int:person_id>', methods=['DELETE'])
@jwt_required()
def delete_person(person_id):
    """Supprimer une personne"""
    person = Person.query.get(person_id)
    if not person:
        return jsonify({"error": "Not found"}), 404
    db.session.delete(person)
    db.session.commit()
    return jsonify({"message": "Deleted"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)