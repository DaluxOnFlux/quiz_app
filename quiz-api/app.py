import hashlib
from flask import Flask
from flask_cors import CORS  # Import du package
from flask import Flask, request
from jwt_utils import build_token, decode_token, JwtError

app = Flask(__name__)
CORS(app)  # Activation de CORS sur l'application Flask

@app.route('/')
def hello_world():
    x = 'Ichrak Dalil Alassane'
    return f"Hello, {x}"

@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
	return {"size": 0, "scores": []}, 200

ADMIN_PASSWORD = "flask2023"  # à adapter selon le mot de passe à tester dans Postman

@app.route('/login', methods=['POST'])
def login():
    body = request.get_json()
    if not body or 'password' not in body:
        return {"error": "Mot de pass requis"}, 400

    if body['password'] != ADMIN_PASSWORD:
        return {"error": "Mot de pass incorrect"}, 401

    token = build_token()
    return {"token": token}, 200

if __name__ == "__main__":
    app.run()
