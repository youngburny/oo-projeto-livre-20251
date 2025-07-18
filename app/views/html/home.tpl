<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bem-vindo, {{current_user.username}}!</title>
    <link rel="icon" type="image/x-icon" href="/static/img/favicon.ico" />
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/static/css/pagina.css">
</head>
<body class="landing-page-body">
    % if transfered:
    <header class="main-header glass-header">
        <div class="logo">
            <a href="/home">Sonar Studio</a>
        </div>
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

    <main class="hero-section">
        <div class="hero-content">
            <h1 class="hero-title">Pronto para criar?</h1>
            <p class="hero-subtitle">
                Sua próxima obra-prima começa aqui. Agende sua sessão no estúdio com apenas um clique.
            </p>
            <div class="hero-actions">
                <a href="/agendar" class="cta-button primary">Agendar Sessão</a>
            </div>
        </div>
    </main>

    % else:
    <div class="login-prompt">
        <h1>Página Exclusiva para Clientes</h1>
        <h3>Realize o login para agendar sua sessão.</h3>
        <a href="/portal" class="cta-button">Ir para o Portal</a>
    </div>
    % end

    <footer class="main-footer">
        <p>&copy; 2025 Sonar Studio - All rights reserved.</p>
    </footer>

    <script src="/static/js/script.js"></script>

</body>
</html>