from flask import Flask, request, jsonify
import json
import requests
import jwt
from functools import wraps

app = Flask(__name__)
DATA_FILE = "data.json"
PERSON_SERVICE_URL = "http://person-service:5001/persons/"
SECRET_KEY = "secret123"

#def token_required(f):
#    @wraps(f)
 #   def decorated(*args, **kwargs):
  #      token = request.headers.get("Authorization")
   #     if not token:
     #       return jsonify({"message": "Token manquant"}), 401
     #   try:
      #      jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
     #   except:
      #      return jsonify({"message": "Token invalide"}), 401
      #  return f(*args, **kwargs)
   # return decorated

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def person_exists(person_id, token):
    r = requests.get(
        PERSON_SERVICE_URL + str(person_id),
        headers={"Authorization": token}
    )
    return r.status_code == 200

@app.route("/health/<int:person_id>", methods=["GET"])
#@token_required
def get_health(person_id):
    token = request.headers.get("Authorization")
    if not person_exists(person_id, token):
        return jsonify({"message": "Personne inexistante"}), 404

    data = load_data()
    return jsonify(data.get(str(person_id), {}))

@app.route("/health/<int:person_id>", methods=["POST", "PUT"])
#@token_required
def add_or_update_health(person_id):
    token = request.headers.get("Authorization")
    if not person_exists(person_id, token):
        return jsonify({"message": "Personne inexistante"}), 404

    data = load_data()
    data[str(person_id)] = request.json
    save_data(data)
    return jsonify(data[str(person_id)])

@app.route("/health/<int:person_id>", methods=["DELETE"])
#@token_required
def delete_health(person_id):
    token = request.headers.get("Authorization")
    if not person_exists(person_id, token):
        return jsonify({"message": "Personne inexistante"}), 404

    data = load_data()
    data.pop(str(person_id), None)
    save_data(data)
    return "", 204

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
