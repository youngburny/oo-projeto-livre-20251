<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Editar Perfil - Sonar Studio</title>
    <link rel="icon" type="image/x-icon" href="/static/img/favicon.ico" />
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/static/css/edit.css">
    
    
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
        <div class="form-container">
            <h2>Editar Perfil</h2>
            
            <div class="info-block">
                <p><strong>Usuário Atual:</strong> {{ current_user.username }}</p>
                <p><strong>Tipo de Conta:</strong> {{ 'Administrador' if current_user.isAdmin() else 'Cliente' }}</p>
            </div>
            
            <form action="/edit" method="POST">
                <div class="input-group">
                    <label for="username">Novo Usuário (opcional):</label>
                    <input type="text" id="username" name="username" value="{{current_user.username}}" required>
                </div>
                <div class="input-group">
                    <label for="password">Nova Senha:</label>
                    <input type="password" id="password" name="password" placeholder="Digite a nova senha" required>
                </div>
                
                <button type="submit" class="submit-button">Salvar Alterações</button>
            </form>
            
            <a href="/home" class="back-link">Cancelar e Voltar</a>
        </div>
    </main>

    <footer class="main-footer">
        <p>&copy; 2025 Sonar Studio - All rights reserved.</p>
    </footer>

    % else:
    <div class="login-prompt">
        <h1>Página Exclusiva para Usuários Logados</h1>
        <h3>Realize o login para acessar esta página.</h3>
        <a href="/portal" class="cta-button">Ir para o Portal</a>
    </div>
    % end
</body>
</html>