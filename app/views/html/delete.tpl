<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Deletar Perfil - Sonar Studio</title>
    <link rel="icon" type="image/x-icon" href="/static/img/favicon.ico" />
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/static/css/delete.css">
    
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
        <div class="delete-container">
            <h2>Atenção: Deletar Perfil</h2>
            <p>Você está prestes a deletar a sua conta de usuário. Esta ação é irreversível.</p>
            
            <div class="profile-details">
                <p><strong>Usuário a ser deletado:</strong> {{ current_user.username }}</p>
                <p><strong>Tipo de Conta:</strong> {{ 'Administrador' if current_user.isAdmin() else 'Cliente' }}</p>
            </div>
            
            <p>Tem certeza que deseja continuar?</p>
            
            <div class="action-buttons">
                <form action="/delete" method="POST">
                    <button type="submit" class="delete-button-confirm">Sim, Deletar Minha Conta</button>
                </form>
                
                <a href="/home" class="cancel-button">Cancelar</a>
            </div>
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