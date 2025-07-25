const socket = io('http://localhost:8080', {
    autoConnect: false // Desabilita a auto-conexão imediata
});

// Elementos da interface
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');
const fileInput = document.getElementById('fileInput');
const sendFileButton = document.getElementById('sendFileButton'); // Botão "Enviar Arquivo"
const messageDisplay = document.getElementById('messageDisplay');
const usersDisplay = document.getElementById('usersDisplay');
const onlineUsersTitle = document.getElementById('onlineUsersTitle');

// --- Inicia a conexão manualmente quando o DOM estiver pronto ---
document.addEventListener('DOMContentLoaded', () => {
    socket.connect(); // Conecta o Socket.IO quando a página carrega
    
    // Configura os event listeners após o DOM estar pronto
    if (sendButton) {
        sendButton.addEventListener('click', sendMessage);
    }
    if (fileInput) {
        fileInput.addEventListener('change', handleFileInputChange); // Escuta quando um arquivo é selecionado
    }
    if (sendFileButton) {
        sendFileButton.addEventListener('click', sendFile); // Escuta o clique no botão "Enviar Arquivo"
    }
    if (messageInput) {
        // Permite enviar mensagem ao pressionar Enter
        messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault(); // Impede o comportamento padrão do Enter (ex: nova linha em textarea, submeter form)
                sendMessage();
            }
        });
    }
    
    // Rola para o final do chat ao carregar a página
    scrollToBottom(messageDisplay);
});


// --- Eventos Socket.IO ---

socket.on('connect', () => {
    console.log('Conexão estabelecida com o servidor Socket.IO');
    socket.emit('request_users_list'); // Solicita a lista de usuários ao conectar
});

// Evento de conexão confirmado pelo servidor
socket.on('connected', (data) => {
    console.log('Servidor confirmou conexão:', data.data);
});

// Recebimento de mensagens de texto E arquivos
socket.on('message', (data) => {
    displayMessage(data); // A função displayMessage agora lida com diferentes tipos
    scrollToBottom(messageDisplay); // Rola para o final a cada nova mensagem
});

// Recebimento de uma nova lista de usuários conectados
socket.on('update_users_event', (data) => {
    updateUserList(data.users);
});


// --- Funções para Envio e Exibição ---

function sendMessage() {
    const message = messageInput.value.trim();
    if (message) {
        socket.emit('message', message);
        messageInput.value = '';
    }
}

function handleFileInputChange() {
    if (fileInput.files.length > 0) {
        sendFileButton.style.display = 'inline-block';
        sendButton.style.display = 'none'; // Esconde o botão de enviar texto
        messageInput.disabled = true; // Desabilita o input de texto
    } else {
        sendFileButton.style.display = 'none';
        sendButton.style.display = 'inline-block'; // Mostra o botão de enviar texto novamente
        messageInput.disabled = false;
    }
}

async function sendFile() {
    console.log("DEBUG: Função sendFile() chamada."); // NOVO DEBUG PRINT

    if (fileInput.files.length === 0) {
        alert('Por favor, selecione um arquivo para enviar.');
        console.log("DEBUG: Nenhum arquivo selecionado.");
        return;
    }

    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('file', file);

    console.log("DEBUG: Tentando enviar arquivo:", file.name, "com tamanho", file.size, "bytes."); // NOVO DEBUG PRINT

    try {
        const response = await fetch('/upload-file', {
            method: 'POST',
            body: formData,
        });

        if (response.ok) {
            const result = await response.json();
            console.log('DEBUG: Arquivo enviado com sucesso:', result);
        } else {
            const errorText = await response.text();
            console.error('ERRO: Falha no upload do arquivo:', response.status, response.statusText, errorText); // Mais detalhes no erro
            alert('Falha ao enviar arquivo: ' + errorText);
        }
    } catch (error) {
        console.error('ERRO: Erro de rede ao enviar arquivo:', error); // Erro de rede/conexão
        alert('Erro de rede ao enviar arquivo.');
    } finally {
        console.log("DEBUG: Finalizando processo de envio de arquivo."); // NOVO DEBUG PRINT
        fileInput.value = ''; // Limpa o campo de seleção de arquivo
        sendFileButton.style.display = 'none';
        sendButton.style.display = 'inline-block';
        messageInput.disabled = false;
    }
}

// Função displayMessage agora recebe um objeto 'data'
function displayMessage(data) {
    if (messageDisplay) {
        const listItem = document.createElement('li');
        // Adiciona classe para estilização de "minhas mensagens"
        if (data.username === getLoggedInUsername()) { 
             listItem.classList.add('my-message');
        }

        if (data.type === 'file') {
            // Se for um arquivo, cria um link para download
            listItem.classList.add('file-message');
            listItem.innerHTML = `<strong>${data.username}</strong>: Arquivo enviado: <a href="${data.url}" target="_blank" download="${data.filename}">${data.filename}</a>`;
        } else { // Para mensagens de texto
            // Garante que o texto tenha o estilo de bolha
            listItem.innerHTML = `<strong>${data.username}</strong>: ${data.content}`;
        }
        
        messageDisplay.appendChild(listItem);
    } else {
        console.error('Elemento messageDisplay não encontrado');
    }
}

function updateUserList(users) {
    if (usersDisplay) {
        usersDisplay.innerHTML = '';
        const onlineCount = users.length;
        if (onlineUsersTitle) {
            onlineUsersTitle.textContent = `Online`;
        }

        users.forEach(user => {
            const listItem = document.createElement('li');
            listItem.textContent = user.username;
            usersDisplay.appendChild(listItem);
        });
    } else {
        console.error('Elemento usersDisplay não encontrado');
    }
}

function scrollToBottom(element) {
    if (element) {
        element.scrollTop = element.scrollHeight;
    }
}

function getLoggedInUsername() {
    // Tenta obter o nome de usuário do cabeçalho da página
    const userSpan = document.querySelector('.user-menu span'); 
    if (userSpan) {
        const text = userSpan.textContent;
        const match = text.match(/Olá, (.+)/);
        if (match && match[1]) {
            return match[1].trim();
        }
    }
    return 'Desconhecido';
}