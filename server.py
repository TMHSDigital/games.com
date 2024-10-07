from flask import Flask, send_from_directory, jsonify
import subprocess
import os

app = Flask(__name__)

# Ensure the current working directory is set correctly
os.chdir(os.path.dirname(os.path.abspath(__file__)))

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_file(path):
    return send_from_directory('.', path)

@app.route('/start_game/<game>')
def start_game(game):
    if game == 'snake':
        try:
            subprocess.Popen(['python', 'python/snake_game.py'])
            return jsonify({"message": "Snake game started!", "status": "success"}), 200
        except Exception as e:
            return jsonify({"message": f"Error starting Snake game: {str(e)}", "status": "error"}), 500
    elif game == 'tetris':
        try:
            subprocess.Popen(['python', 'python/tetris_game.py'])
            return jsonify({"message": "Tetris game started!", "status": "success"}), 200
        except Exception as e:
            return jsonify({"message": f"Error starting Tetris game: {str(e)}", "status": "error"}), 500
    elif game == 'pong':
        # Placeholder for Pong game
        return jsonify({"message": "Pong game not implemented yet", "status": "not_implemented"}), 501
    else:
        return jsonify({"message": "Unknown game", "status": "error"}), 400

@app.route('/games')
def get_games():
    games = [
        {"id": "snake", "name": "Snake", "description": "Classic snake game. Eat food, grow longer, don't hit the walls!"},
        {"id": "tetris", "name": "Tetris", "description": "Arrange falling blocks to create complete lines and score points."},
        {"id": "pong", "name": "Pong", "description": "Classic two-player game. Hit the ball past your opponent's paddle to score."}
    ]
    return jsonify(games)

if __name__ == "__main__":
    app.run(debug=True)