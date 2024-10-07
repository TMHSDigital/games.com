const startButton = document.getElementById('start-game');

startButton.addEventListener('click', () => {
    fetch('/start_game')
        .then(response => response.text())
        .then(data => {
            console.log(data);
            // Here you could update the UI to indicate the game has started
        })
        .catch(error => console.error('Error:', error));
});