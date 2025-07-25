<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" type="image/x-icon" href="/static/img/favicon.ico" />
    <title>Chat - Sonar Studio</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/static/css/pagina.css">
    <link rel="stylesheet" href="/static/css/chat.css"> 
</head>
<body>
    % if current_user:
    <header class="main-header glass-header">
        <div class="logo"><a href="/home">Sonar Studio</a></div>
        <nav class="main-nav">
            <ul>
                <li><a href="/portal">Portal</a></li>
                <li><a href="/chat">Mensagens</a></li>
                % if current_user.isAdmin():
                    <li><a href="/admin">Admin</a></li>
                % end
                <li>
                    <div class="user-menu">
                        <span>Olá, {{current_user.username}}</span>
                        <div class="dropdown-menu">
                            <a href="/edit">Editar Perfil</a>
                            <a href="/minhas-sessoes">Minhas Sessões</a>
                            <a href="/delete">Deletar Perfil</a>
                            <form action="/logout" method="post">
                                <button type="submit" class="logout-btn">Logout</button>
                            </form>
                        </div>
                    </div>
                </li>
            </ul>
        </nav>
    </header>

    <main class="container">
        <div class="chat-container">
            <div class="users-panel">
                <h3 id="onlineUsersTitle">Online (0)</h3>
                <ul id="usersDisplay" class="users-list">
                    </ul>
            </div>
            <div class="chat-main">
                <ul id="messageDisplay" class="messages-display">
                    % for msg in messages:
                        <li class="{{ 'my-message' if msg.username == current_user.username else '' }}">
                            <strong>{{msg.username}}</strong>: {{msg.content}}
                        </li>
                    % end
                </ul>
                <div class="message-input-area">
                    <input type="text" id="messageInput" placeholder="Digite sua mensagem...">
                    <button id="sendButton" class="send-button">Enviar</button>
                    
                    <label for="fileInput" class="file-upload-button">📎</label>
                    <input type="file" id="fileInput" style="display: none;">
                    <button id="sendFileButton" class="send-button" style="display: none;">Enviar Arquivo</button>
                </div>
            </div>
        </div>
    </main>

    <footer class="main-footer">
        <p>&copy; 2025 Sonar Studio - All rights reserved.</p>
    </footer>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.7.5/socket.io.js"></script>
    <script src="/static/js/chat.js"></script>

    % else:
    <div class="login-prompt">
        <h1>Página Exclusiva para Usuários Logados</h1>
        <h3>Realize o login para acessar o chat.</h3>
        <a href="/portal" class="cta-button">Ir para o Portal</a>
    </div>
    % end
</body>
</html>