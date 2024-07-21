$(document).ready(function() {
    // Enviar mensaje al servidor
    $("form").submit(function(event) {
        event.preventDefault();
        var message = $("textarea[name='message']").val();
        var model = $("select[name='model']").val();

        if (message.trim() !== "") {
            $.ajax({
                type: "POST",
                url: "/chat",
                data: {
                    message: message,
                    model: model
                },
                success: function(response) {
                    // Agregar mensaje del usuario
                    $(".chat-messages").append(
                        '<div class="chat-message user">' +
                        message +
                        '</div>'
                    );

                    // Agregar mensaje del chatbot
                    $(".chat-messages").append(
                        '<div class="chat-message bot">' +
                        response.response +
                        '</div>'
                    );

                    // Limpiar el campo de texto
                    $("textarea[name='message']").val("");

                    // Desplazar al final de la lista de mensajes
                    $(".chat-messages").scrollTop($(".chat-messages")[0].scrollHeight);
                },
                error: function(error) {
                    console.error(error);
                    alert("Error al enviar el mensaje.");
                }
            });
        }
    });
});