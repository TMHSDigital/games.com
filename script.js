document.addEventListener('DOMContentLoaded', () => {
    const gameButtons = document.querySelectorAll('.game-button');
    const startGameButton = document.getElementById('start-game');
    const selectedGameTitle = document.getElementById('selected-game-title');
    const gameDescription = document.getElementById('game-description');
    
    let selectedGame = null;

    const gameInfo = {
        snake: {
            title: "Snake",
            description: "Control a snake to eat food and grow longer, but don't hit the walls or yourself!"
        },
        tetris: {
            title: "Tetris",
            description: "Arrange falling blocks to create complete lines and score points."
        },
        pong: {
            title: "Pong",
            description: "Classic two-player game. Hit the ball past your opponent's paddle to score."
        }
    };

    gameButtons.forEach(button => {
        button.addEventListener('click', () => {
            selectedGame = button.getAttribute('data-game');
            updateGameInfo(selectedGame);
            startGameButton.style.display = 'inline-block';
        });
    });

    startGameButton.addEventListener('click', () => {
        if (selectedGame) {
            fetch(`/start_game/${selectedGame}`)
                .then(response => response.text())
                .then(data => {
                    console.log(data);
                    // Here you could update the UI to indicate the game has started
                })
                .catch(error => console.error('Error:', error));
        }
    });

    function updateGameInfo(game) {
        selectedGameTitle.textContent = gameInfo[game].title;
        gameDescription.textContent = gameInfo[game].description;
    }
});