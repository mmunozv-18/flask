// static/js/script.js
document.addEventListener('DOMContentLoaded', () => {
    const providerSelect = document.getElementById('provider');
    const modelSelect = document.getElementById('model');
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const loader = document.querySelector('.loader');
    const copyBtn = document.createElement('button');
    const clearHistoryBtn = document.createElement('button');

    clearHistoryBtn.textContent = 'Borrar Historial';
    clearHistoryBtn.id = 'clear-history-btn';
    clearHistoryBtn.classList.add('btn', 'btn-primary', 'mt-2');

    document.querySelector('.chat-container').insertBefore(clearHistoryBtn, chatMessages);

    let availableModels = {};
    let chatHistory = [];
    let currentModel = null;
    let currentProvider = null;

    // Cargar modelos disponibles
    fetch('/get_models')
        .then(response => response.json())
        .then(models => {
            console.log("Modelos recibidos:", models);
            availableModels = models;
            updateProviderOptions();
        })
        .catch(error => {
            console.error('Error al cargar los modelos:', error);
            addMessage('error', 'Error al cargar los modelos. Por favor, recarga la página.');
        });

    function updateProviderOptions() {
        providerSelect.innerHTML = '<option value="">Seleccione un proveedor</option>';
        Object.keys(availableModels).forEach(provider => {
            const option = document.createElement('option');
            option.value = provider;
            option.textContent = provider.charAt(0).toUpperCase() + provider.slice(1);
            providerSelect.appendChild(option);
        });
    }

    providerSelect.addEventListener('change', () => {
        const selectedProvider = providerSelect.value;
        modelSelect.innerHTML = '<option value="">Seleccione un modelo</option>';
        if (selectedProvider && availableModels[selectedProvider]) {
            availableModels[selectedProvider].forEach(model => {
                const option = document.createElement('option');
                option.value = model;
                option.textContent = model;
                modelSelect.appendChild(option);
            });
        }
    });

    // Manejar el envío de mensajes
    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    clearHistoryBtn.addEventListener('click', clearHistory);

    function sendMessage() {
        const message = userInput.value.trim();
        const provider = providerSelect.value;
        const model = modelSelect.value;

        if (!message || !provider || !model) {
            alert('Por favor, complete todos los campos');
            return;
        }

        if (currentModel !== model || currentProvider !== provider) {
            chatHistory = [];
            addMessage('system', `Cambiando a ${provider} - ${model}`);
            currentModel = model;
            currentProvider = provider;
        }

        addMessage('user', message);
        userInput.value = '';

        loader.style.display = 'flex'; // Mostrar loader
        sendBtn.disabled = true;

        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message, provider, model }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                addMessage('error', data.error);
            } else {
                addMessage('bot', data.response);
                chatHistory = data.history;
            }
            loader.style.display = 'none'; // Ocultar loader
            sendBtn.disabled = false;
        })
        .catch(error => {
            addMessage('error', 'Error de conexión: ' + error.message);
            loader.style.display = 'none'; // Ocultar loader
            sendBtn.disabled = false;
        });
    }

    function addMessage(sender, content) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', `${sender}-message`);

        if (sender === 'bot') {
            // Renderizar el contenido Markdown para mensajes del bot
            messageElement.innerHTML = marked.parse(content);
        } else {
            messageElement.textContent = content;
        }

        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function clearHistory() {
        fetch('/clear_history', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                console.log(data.message);
                chatHistory = [];
                chatMessages.innerHTML = '';
                addMessage('system', 'Historial borrado');
            })
            .catch(error => {
                console.error('Error al borrar el historial:', error);
                addMessage('error', 'Error al borrar el historial');
            });
    }

    function copyToClipboard(text) {
        navigator.clipboard.writeText(text)
            .then(() => {
                // El texto se copió correctamente
            })
            .catch(err => {
                console.error('Error al copiar al portapapeles:', err);
            });
    }

    function addCopyButton(messageElement, content) {
        copyBtn.textContent = 'Copiar';
        copyBtn.classList.add('copy-button');
        copyBtn.addEventListener('click', () => {
            copyToClipboard(content);
            copyBtn.textContent = 'Copiado!';
            setTimeout(() => {
                copyBtn.textContent = 'Copiar';
            }, 1000);
        });
        messageElement.appendChild(copyBtn);
    }

    // Añadir botón de copiar a los mensajes del bot
    chatMessages.addEventListener('DOMNodeInserted', (e) => {
        if (e.target.classList.contains('bot-message')) {
            addCopyButton(e.target, e.target.textContent);
        }
    });
});