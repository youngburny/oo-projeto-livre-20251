<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Confirmar Remoção de Usuário - Sonar Studio</title>
    <link rel="icon" type="image/x-icon" href="/static/img/favicon.ico" />
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/static/css/pagina.css">
    
    <link rel="stylesheet" href="/static/css/admin.css">

    <style>
        /* Estilos específicos para a página de confirmação de usuário */
        .confirmation-card {
            max-width: 600px;
            margin: 60px auto;
            padding: 40px;
            background-color: #1e1e1e;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
            border: 2px solid #dc3545; /* Borda vermelha para indicar atenção */
            text-align: center;
        }
        .confirmation-card h2 {
            color: #dc3545; /* Título vermelho */
            margin-bottom: 25px;
            font-size: 2.2em;
            font-weight: 700;
        }
        .confirmation-card p {
            color: #d1d1d1;
            margin-bottom: 30px;
            font-size: 1.1em;
            line-height: 1.6;
        }
        .user-details-block {
            background-color: #2a2a2a;
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 30px;
            text-align: left;
            color: #eee;
            border-left: 5px solid #dc3545;
        }
        .user-details-block p {
            margin: 5px 0;
        }
        .user-details-block strong {
            color: #fff;
        }
        .confirmation-actions {
            display: flex;
            justify-content: center;
            gap: 20px;
        }
        .confirm-delete-button {
            background-color: #dc3545;
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-size: 1.1em;
            font-weight: 700;
            transition: background-color 0.3s ease, transform 0.2s ease;
        }
        .confirm-delete-button:hover {
            background-color: #c82333;
            transform: translateY(-2px);
        }
        .cancel-button {
            background-color: #6c757d;
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-size: 1.1em;
            font-weight: 700;
            text-decoration: none;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: background-color 0.3s ease, transform 0.2s ease;
        }
        .cancel-button:hover {
            background-color: #5a6268;
            transform: translateY(-2px);
        }
    </style>
</head>
<body>
    % if current_user and current_user.isAdmin():
    <header class="main-header glass-header">
        <div class="logo"><a href="/home">Sonar Studio</a></div>
        <nav class="main-nav">
            <ul>
                <li><a href="/portal">Portal</a></li>
                <li><a href="/chat">Mensagens</a></li>
                <li><a href="/admin">Admin</a></li>
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
        <div class="confirmation-card">
            <h2>Confirmar Remoção de Usuário</h2>
            <p>Você está prestes a deletar a conta do usuário <strong>{{ usuario_a_remover.username }}</strong> e **TODAS AS SESSÕES ASSOCIADAS** a ele. Esta ação é irreversível.</p>
            
            <div class="user-details-block">
                <p><strong>Usuário:</strong> {{ usuario_a_remover.username }}</p>
                <p><strong>Tipo de Conta:</strong> {{ 'Administrador' if usuario_a_remover.isAdmin() else 'Cliente' }}</p>
            </div>

            <p>Tem certeza que deseja continuar?</p>
            
            <div class="confirmation-actions">
                <form action="/admin/remover-usuario/{{usuario_a_remover.username}}" method="POST">
                    <button type="submit" class="confirm-delete-button">Sim, Remover Usuário e Sessões</button>
                </form>
                
                <a href="/admin" class="cancel-button">Não, Cancelar</a>
            </div>
        </div>
    </main>

    <footer class="main-footer">
        <p>&copy; 2025 Sonar Studio - All rights reserved.</p>
    </footer>

    % else:
    <div class="login-prompt">
        <h1>Acesso Restrito</h1>
        <h3>Você precisa ser um administrador para acessar esta página.</h3>
        <a href="/portal" class="cta-button">Ir para o Portal</a>
    </div>
    % end
</body>
</html>