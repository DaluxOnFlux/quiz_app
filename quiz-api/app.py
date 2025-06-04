from flask import Flask
from flask_cors import CORS  # Import du package

app = Flask(__name__)
CORS(app)  # Activation de CORS sur l'application Flask

@app.route('/')
def hello_world():
    x = 'Ichrak Dalil Alassane'
    return f"Hello, {x}"

@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
	return {"size": 0, "scores": []}, 200

if __name__ == "__main__":
    app.run()
