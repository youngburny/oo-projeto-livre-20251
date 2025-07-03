<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Confirmar Remoção - Sonar Studio</title>
    <link rel="icon" type="image/x-icon" href="/static/img/favicon.ico" />
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/static/css/pagina.css">
    <style>
        .confirmation-card {
            max-width: 500px;
            margin: 60px auto;
            padding: 30px;
            background-color: #2a2a2a;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
            border: 1px solid #dc3545; /* Borda vermelha para indicar atenção */
            text-align: center;
        }
        .confirmation-card h2 {
            color: #dc3545; /* Título vermelho */
            margin-bottom: 20px;
            font-size: 2em;
        }
        .confirmation-card p {
            color: #d1d1d1;
            margin-bottom: 25px;
            font-size: 1.1em;
            line-height: 1.6;
        }
        .confirmation-details {
            background-color: #333;
            border: 1px solid #555;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 30px;
            text-align: left;
        }
        .confirmation-details p {
            margin: 5px 0;
            color: #eee;
            font-size: 1em;
        }
        .confirmation-details strong {
            color: #fff;
        }
        .confirmation-actions {
            display: flex;
            justify-content: center;
            gap: 20px;
        }
        .confirmation-actions button,
        .confirmation-actions a {
            padding: 12px 25px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1.1em;
            font-weight: 700;
            transition: background-color 0.3s ease, transform 0.2s ease;
            text-decoration: none;
            display: inline-block; /* Para que os links se comportem como botões */
            color: white;
            text-align: center;
        }
        .confirm-button {
            background-color: #dc3545; /* Vermelho para confirmar remoção */
        }
        .confirm-button:hover {
            background-color: #c82333;
            transform: translateY(-2px);
        }
        .cancel-button {
            background-color: #6c757d; /* Cinza para cancelar */
        }
        .cancel-button:hover {
            background-color: #5a6268;
            transform: translateY(-2px);
        }
    </style>
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
        <div class="confirmation-card">
            <h2>Confirmar Remoção de Sessão</h2>
            <p>Você tem certeza que deseja remover a seguinte sessão?</p>
            
            <div class="confirmation-details">
                <p><strong>ID da Sessão:</strong> {{ sessao.idSessao }}</p>
                <p><strong>Tipo de Serviço:</strong> {{ sessao.tipoServico if sessao.tipoServico else 'Não especificado' }}</p>
                <p><strong>Data:</strong> {{ sessao.dataServico if sessao.dataServico else 'N/A' }}</p>
                <p><strong>Horário:</strong> {{ sessao.horarioServico if sessao.horarioServico else 'N/A' }}</p>
                <p><strong>Detalhes:</strong> {{ sessao.detalhes if sessao.detalhes else 'Sem detalhes' }}</p>
            </div>

            <div class="confirmation-actions">
                <form action="/remover-sessao/{{sessao.idSessao}}" method="POST">
                    <button type="submit" class="confirm-button">Sim, Remover</button>
                </form>
                <a href="/minhas-sessoes" class="cancel-button">Não, Cancelar</a>
            </div>
        </div>
    </main>

    <footer class="main-footer">
        <p>&copy; 2025 Sonar Studio - All rights reserved.</p>
    </footer>

    % else:
    <div class="login-prompt">
        <h1>Página Exclusiva para Clientes</h1>
        <h3>Realize o login para remover sua sessão.</h3>
        <a href="/portal" class="cta-button">Ir para o Portal</a>
    </div>
    % end

    <script src="/static/js/script.js"></script>
</body>
</html>