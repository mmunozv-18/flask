// App 2: Manejo de formulario y envío de datos JSON
document.getElementById('app2-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Evita la recarga de la página
    const formData = new FormData(this);
    fetch('/app2', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('div3-content').innerHTML = `
            <p>Nombre: ${data.name}</p>
            <p>Fecha de nacimiento: ${data.birthdate}</p>
        `;
    })
    .catch(error => console.error('Error:', error));
});

// App 3: Ejemplo de código para mostrar un calendario
document.addEventListener('DOMContentLoaded', function() {
    // Aquí puedes usar una biblioteca de calendario de JavaScript (como FullCalendar o Moment.js)
    // para crear un calendario en el div4
});