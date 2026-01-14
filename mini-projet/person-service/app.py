from flask import Flask, request, jsonify
import sqlite3
import jwt
from functools import wraps

app = Flask(__name__)
SECRET_KEY = "secret123"

def get_db():
    return sqlite3.connect("database.db")

#def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"message": "Token manquant"}), 401
        try:
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except:
            return jsonify({"message": "Token invalide"}), 401
        return f(*args, **kwargs)
    return decorated

@app.route("/persons", methods=["POST"])
#@token_required
def create_person():
    name = request.json.get("name")
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO person (name) VALUES (?)", (name,))
    conn.commit()
    person_id = cur.lastrowid
    conn.close()
    return jsonify({"id": person_id, "name": name}), 201

@app.route("/persons/<int:id>", methods=["GET"])
#@token_required
def get_person(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM person WHERE id=?", (id,))
    person = cur.fetchone()
    conn.close()
    if not person:
        return jsonify({"message": "Personne non trouvée"}), 404
    return jsonify({"id": person[0], "name": person[1]})

@app.route("/persons/<int:id>", methods=["DELETE"])
#@token_required
def delete_person(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM person WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return "", 204

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
