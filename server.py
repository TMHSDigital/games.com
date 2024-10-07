from flask import Flask, send_from_directory
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_file(path):
    return send_from_directory('.', path)

@app.route('/start_game')
def start_game():
    subprocess.Popen(['python', 'python/snake_game.py'])
    return "Game started!", 200

if __name__ == "__main__":
    app.run(debug=True)