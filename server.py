from flask import Flask
import os

app = Flask(__name__)

@app.route('/start_game')
def start_game():
    os.system('python python/snake_game.py')
    return "Game started!", 200

if __name__ == "__main__":
    app.run(debug=True)
