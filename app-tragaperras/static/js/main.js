document.addEventListener('DOMContentLoaded', function() {
    const spinButton = document.getElementById('spin-button');
  
    spinButton.addEventListener('click', function() {
      // Actualiza la página al hacer clic en el botón (para reflejar los cambios en el servidor)
      window.location.href = '/';
    });
  });
  