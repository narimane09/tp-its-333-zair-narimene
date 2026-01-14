from flask import Flask, jsonify
import jwt
import datetime

app = Flask(__name__)
SECRET_KEY = "secret123"

@app.route("/login", methods=["POST"])
def login():
    token = jwt.encode(
        {
            "user": "admin",
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        },
        SECRET_KEY,
        algorithm="HS256"
    )
    return jsonify({"token": token})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
