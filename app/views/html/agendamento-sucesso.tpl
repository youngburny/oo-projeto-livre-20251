<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Sonar Studio - Sucesso!</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" />
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/static/css/agendamento-sucesso.css" />
</head>
<body>
    <header class="main-header">
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
                            <a href="/minhas-sessoes" class="active">Minhas Sessões</a>
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

        <div class="success-card">
            <div class="success-icon">
                <i class="fas fa-check-circle"></i>
            </div>
            
            <h2>Sessão Agendada com Sucesso!</h2>
            
            <p>
                Recebemos o seu pedido de agendamento. Em breve, nossa equipe entrará em contato através do seu e-mail para confirmar todos os detalhes e próximos passos.
            </p>

            <div class="actions">
                <a href="/home" class="cta-button">Voltar à página inicial</a>
            </div>
        </div>

    </main>

    <footer class="main-footer">
        <p>&copy; 2025 Sonar Studio - Todos os direitos reservados.</p>
    </footer>

    <script src="/static/js/script.js"></script>

</body>
</html>