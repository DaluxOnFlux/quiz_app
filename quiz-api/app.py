from flask import Flask
from flask_cors import CORS  # Import du package

app = Flask(__name__)
CORS(app)  # Activation de CORS sur l'application Flask

@app.route('/')
def hello_world():
    x = 'world'
    return f"Hello, {x}"

if __name__ == "__main__":
    app.run()
