// script.js

// Função para carregar o jogo Python no canvas
function loadGame() {
    const canvas = document.getElementById('game-canvas');
    const ctx = canvas.getContext('2d');

    // Exemplo de desenho no canvas
    ctx.fillStyle = 'red';
    ctx.fillRect(50, 50, 100, 100);

    // Referenciar as cartas no caminho relativo
    const imagePath = "assets/cards/";
    const cardClubs1 = new Image();
    cardClubs1.src = imagePath + "cardClubs1.png";
    const cardDiamonds1 = new Image();
    cardDiamonds1.src = imagePath + "cardDiamonds1.png";
    const cardSpades1 = new Image();
    cardSpades1.src = imagePath + "cardSpades1.png";
    const cardHearts1 = new Image();
    cardHearts1.src = imagePath + "cardHearts1.png";

    // Exemplo de uso das cartas
    ctx.drawImage(cardClubs1, 50, 50, 100, 100);
    ctx.drawImage(cardDiamonds1, 150, 50, 100, 100);
    ctx.drawImage(cardSpades1, 250, 50, 100, 100);
    ctx.drawImage(cardHearts1, 350, 50, 100, 100);
}

// Executar a função para carregar o jogo quando a página for carregada
window.onload = function() {
    loadGame();
};
