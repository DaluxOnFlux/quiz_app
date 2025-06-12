import hashlib
import sqlite3
from flask import Flask
from flask_cors import CORS
from flask import Flask, request, jsonify, abort
from jwt_utils import build_token, decode_token, JwtError
from question import Question, insert, get_by_position, get_by_id, update as update_q, delete_all

app = Flask(__name__)
CORS(app)  

@app.route('/')
def hello_world():
    x = 'Ichrak Dalil Alassane'
    return f"Hello, {x}"

@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
	return {"size": 0, "scores": []}, 200

ADMIN_PASSWORD = "flask2023"  

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

def _check_admin_token() -> None:
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        abort(401)
    token = auth.split(" ", 1)[1]
    try:
        decode_token(token)
    except JwtError:
        abort(401)

@app.route("/questions", methods=["POST"])
def post_question():
    """POST /questions  — ajout d’une question."""
    _check_admin_token()
    body = request.get_json() or {}
    required = {"position", "title", "text", "image"}
    if not required.issubset(body):
        return {"error": f"Champs obligatoires : {', '.join(required)}"}, 400

    q = Question(
        id=None,
        position=int(body["position"]),
        title=body["title"],
        text=body["text"],
        image=body["image"],
    )
    try:
        qid = insert(q)
    except sqlite3.IntegrityError:
        return {"error": "Une question occupe déjà cette position."}, 409

    return {"id": qid}, 201


@app.route("/questions", methods=["GET"])
def get_question_by_position():
    pos = request.args.get("position", type=int)
    if pos is None:
        return {"error": "Paramètre ?position=<int> manquant."}, 400

    q = get_by_position(pos)
    if q is None:
        return {}, 404
    return jsonify(q.to_dict()), 200


@app.route("/questions/<int:qid>", methods=["PUT"])
def put_question(qid: int):
    _check_admin_token()
    if get_by_id(qid) is None:
        return {}, 404

    body = request.get_json() or {}
    required = {"position", "title", "text", "image"}
    if not required.issubset(body):
        return {"error": f"Champs obligatoires : {', '.join(required)}"}, 400

    q = Question(
        id=qid,
        position=int(body["position"]),
        title=body["title"],
        text=body["text"],
        image=body["image"],
    )
    try:
        if not update_q(qid, q):
            return {}, 404
    except sqlite3.IntegrityError:
        return {"error": "Une autre question occupe déjà cette position."}, 409

    return {}, 204


@app.route("/questions/all", methods=["DELETE"])
def delete_all_questions():
    _check_admin_token()
    delete_all()
    return {}, 204

@app.route("/questions/<int:qid>", methods=["DELETE"])
def delete_question_by_id(qid: int):
    _check_admin_token()
    from question import delete_by_id
    if delete_by_id(qid):
        return {}, 204
    else:
        return {}, 404

