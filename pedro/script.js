// script.js

// Função para carregar o jogo Python no canvas
function loadGame() {
    // Incluir código para carregar o jogo Python aqui
    // Por exemplo:
    const canvas = document.getElementById('game-canvas');
    const ctx = canvas.getContext('2d');
    
    // Exemplo de desenho no canvas
    ctx.fillStyle = 'red';
    ctx.fillRect(50, 50, 100, 100);
}

// Executar a função para carregar o jogo quando a página for carregada
window.onload = function() {
    loadGame();
};
