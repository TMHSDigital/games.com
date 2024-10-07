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

@app.route('/start_game/<game>')
def start_game(game):
    if game == 'snake':
        subprocess.Popen(['python', 'python/snake_game.py'])
        return "Snake game started!", 200
    elif game == 'tetris':
        # Placeholder for Tetris game
        return "Tetris game not implemented yet", 501
    elif game == 'pong':
        # Placeholder for Pong game
        return "Pong game not implemented yet", 501
    else:
        return "Unknown game", 400

if __name__ == "__main__":
    app.run(debug=True)