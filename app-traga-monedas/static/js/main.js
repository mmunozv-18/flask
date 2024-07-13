const reels = document.getElementById('reels');
const symbols = ['static/img/img1.png', 'static/img/img2.png', 'static/img/img3.png',
                'static/img/img4.png', 'static/img/img5.png', 'static/img/img6.png',
                'static/img/img7.png', 'static/img/img8.png', 'static/img/img9.png']; // Agrega tus propios símbolos

document.getElementById('spin-button').addEventListener('click', function() {
    // Genera números aleatorios para cada carrete
    const reel1 = Math.floor(Math.random() * symbols.length);
    const reel2 = Math.floor(Math.random() * symbols.length);
    const reel3 = Math.floor(Math.random() * symbols.length);

    // Agrega los símbolos a los carretes
    reels.innerHTML = `
        <img src="${symbols[reel1]}" alt="">
        <img src="${symbols[reel2]}" alt="">
        <img src="${symbols[reel3]}" alt="">
    `;
});
