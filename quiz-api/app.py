import os
import sqlite3
from flask import Flask, request, jsonify, abort
from flask_cors import CORS

from jwt_utils import build_token, decode_token, JwtError
from question import Question, insert, get_by_position, get_by_id, update as update_q, delete_all
from answer import insert as insert_answer, Answer, get_all_by_question
from participation import insert_participation, delete_all_participations, get_all_scores

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return "Hello, Quiz App"

@app.route("/rebuild-db", methods=["POST"])
def rebuild_db():
    db_path = "quiz.db"

    if os.path.exists(db_path):
        os.remove(db_path)

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE Question (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            position INTEGER NOT NULL UNIQUE,
            title TEXT NOT NULL,
            text TEXT NOT NULL,
            image TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE Answer (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            is_correct BOOLEAN NOT NULL,
            id_question INTEGER NOT NULL,
            FOREIGN KEY (id_question) REFERENCES Question(id)
        )
    """)

    cur.execute("""
        CREATE TABLE Participation (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player TEXT NOT NULL,
            score INTEGER NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE ParticipationAnswer (
            id_participation INTEGER NOT NULL,
            id_question INTEGER NOT NULL,
            id_answer INTEGER NOT NULL,
            FOREIGN KEY (id_participation) REFERENCES Participation(id),
            FOREIGN KEY (id_question) REFERENCES Question(id),
            FOREIGN KEY (id_answer) REFERENCES Answer(id)
        )
    """)

    conn.commit()
    conn.close()

    return "Ok", 200


@app.route("/quiz-info", methods=["GET"])
def get_quiz_info():
    from question import _get_conn
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM Question")
    size = cur.fetchone()[0]
    conn.close()

    from participation import get_all_scores
    scores = get_all_scores()

    return jsonify({"size": size, "scores": scores}), 200



ADMIN_PASSWORD = "iloveflask"

@app.route('/login', methods=['POST'])
def login():
    body = request.get_json()
    if not body or 'password' not in body:
        return {"error": "Mot de passe requis"}, 400
    if body['password'] != ADMIN_PASSWORD:
        return {"error": "Mot de passe incorrect"}, 401

    token = build_token()
    return {"token": token}, 200


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
    _check_admin_token()
    body = request.get_json() or {}
    required = {"position", "title", "text", "image", "possibleAnswers"}
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

        for ans in body["possibleAnswers"]:
            a = Answer(
                id=None,
                text=ans["text"],
                is_correct=bool(ans["isCorrect"]),
                id_question=qid
            )
            insert_answer(a)

    except sqlite3.IntegrityError:
        return {"error": "Une question occupe déjà cette position."}, 409

    return {"id": qid}, 200


@app.route("/questions", methods=["GET"])
def get_question_by_position():
    pos = request.args.get("position", type=int)
    if pos is None:
        return {"error": "Paramètre ?position=<int> manquant."}, 400

    q = get_by_position(pos)
    if q is None:
        return {}, 404

    answers = get_all_by_question(q.id)
    q_dict = q.to_dict()
    q_dict["possibleAnswers"] = [a.to_dict() for a in answers]

    return jsonify(q_dict), 200


@app.route("/questions/<int:qid>", methods=["PUT"])
def put_question(qid: int):
    _check_admin_token()
    if get_by_id(qid) is None:
        return {}, 404

    body = request.get_json() or {}
    required = {"position", "title", "text", "image", "possibleAnswers"}
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

        conn = sqlite3.connect("quiz.db")
        cur = conn.cursor()
        cur.execute("DELETE FROM Answer WHERE id_question = ?", (qid,))
        conn.commit()

        for ans in body["possibleAnswers"]:
            a = Answer(
                id=None,
                text=ans["text"],
                is_correct=bool(ans["isCorrect"]),
                id_question=qid
            )
            insert_answer(a)

        return {}, 204
    except sqlite3.IntegrityError:
        return {"error": "Erreur mise à jour"}, 400


@app.route("/questions/all", methods=["DELETE"])
def delete_all_questions():
    _check_admin_token()
    delete_all()
    return {"message": "Les questions ont été supprimées avec succès."}, 204


@app.route("/questions/<int:qid>", methods=["DELETE"])
def delete_question_by_id(qid: int):
    _check_admin_token()
    from question import delete_by_id
    if delete_by_id(qid):
        return {"message": "La question a été supprimée avec succès."}, 204
    else:
        return {}, 404


@app.route("/answers", methods=["POST"])
def post_answer():
    _check_admin_token()
    body = request.get_json() or {}
    required = {"text", "is_correct", "id_question"}
    if not required.issubset(body):
        return {"error": "Champs requis : text, is_correct, id_question"}, 400

    answer = Answer(
        id=None,
        text=body["text"],
        is_correct=bool(body["is_correct"]),
        id_question=int(body["id_question"])
    )
    try:
        aid = insert_answer(answer)
    except sqlite3.IntegrityError:
        return {"error": "Erreur insertion answer"}, 400

    return {"id": aid}, 200


@app.route("/questions/<int:qid>/answers", methods=["GET"])
def get_answers_for_question(qid: int):
    answers = get_all_by_question(qid)
    return jsonify([a.to_dict() for a in answers]), 200


@app.route("/participations", methods=["POST"])
def post_participation():
    body = request.get_json() or {}
    if not isinstance(body.get("playerName"), str) or not isinstance(body.get("answers"), list):
        return jsonify({"error": "Champs requis : playerName, answers"}), 400

    from question import _get_conn
    conn = _get_conn()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM Question")
    nb_questions = cur.fetchone()[0]

    if len(body["answers"]) != nb_questions:
        conn.close()
        return jsonify({"error": f"Le joueur doit répondre à {nb_questions} questions."}), 400

    final_answers = []
    score = 0

    for i, answer_position in enumerate(body["answers"]):
        question_position = i + 1
        cur.execute("SELECT id FROM Question WHERE position = ?", (question_position,))
        question_row = cur.fetchone()
        if question_row is None:
            conn.close()
            return jsonify({"error": f"Question à la position {question_position} introuvable."}), 400

        question_id = question_row[0]
        cur.execute("SELECT id, is_correct FROM Answer WHERE id_question = ? ORDER BY id", (question_id,))
        answers = cur.fetchall()

        if not answers or len(answers) < answer_position or answer_position < 1:
            conn.close()
            return jsonify({"error": f"Réponse {answer_position} invalide pour la question {question_position}."}), 400

        selected_answer_id, is_correct = answers[answer_position - 1]

        if is_correct:
            score += 1

        final_answers.append({
            "id_question": question_id,
            "id_answer": selected_answer_id
        })

    try:
        from participation import insert_participation as insert_participation_with_score
        pid, _ = insert_participation_with_score(body["playerName"], final_answers, score)

        conn.close()
        return jsonify({
            "playerName": body["playerName"],
            "score": score
        }), 200

    except Exception as e:
        conn.close()
        return jsonify({"error": str(e)}), 400




@app.route("/participations/all", methods=["DELETE"])
def delete_participations():
    _check_admin_token()
    delete_all_participations()
    return {"message": "Toutes les participations ont été supprimées."}, 204


@app.route("/questions/<int:qid>", methods=["GET"])
def get_question_by_id(qid: int):
    q = get_by_id(qid)
    if q is None:
        return {}, 404

    answers = get_all_by_question(qid)
    return jsonify({
        **q.to_dict(),
        "possibleAnswers": [a.to_dict() for a in answers]
    }), 200


if __name__ == "__main__":
    app.run()
