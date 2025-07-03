<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Editar Sessão - Sonar Studio</title>
    <link rel="icon" type="image/x-icon" href="/static/img/favicon.ico" />
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/static/css/pagina.css">
    <style>
        /* Estilos específicos para o formulário de edição, se desejar */
        .form-container {
            max-width: 600px;
            margin: 40px auto;
            padding: 30px;
            background-color: #2a2a2a;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
            border: 1px solid #8000ff;
        }
        .form-container h2 {
            color: #a259ff;
            text-align: center;
            margin-bottom: 30px;
            font-size: 2em;
        }
        .form-group {
            margin-bottom: 20px;
        }
        .form-group label {
            display: block;
            margin-bottom: 8px;
            color: #d1d1d1;
            font-weight: 600;
        }
        .form-group input[type="text"],
        .form-group input[type="date"],
        .form-group input[type="time"],
        .form-group textarea,
        .form-group select {
            width: 100%;
            padding: 12px;
            background-color: #333;
            border: 1px solid #555;
            border-radius: 8px;
            color: #eee;
            font-size: 1em;
            box-sizing: border-box; /* Garante que padding não aumente a largura total */
        }
        .form-group textarea {
            resize: vertical;
            min-height: 100px;
        }
        .form-group input[type="submit"] {
            background-color: #a259ff;
            color: white;
            padding: 12px 25px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1.1em;
            font-weight: 700;
            transition: background-color 0.3s ease, transform 0.2s ease;
            width: auto;
            display: block;
            margin: 0 auto;
        }
        .form-group input[type="submit"]:hover {
            background-color: #8000ff;
            transform: translateY(-2px);
        }
        .back-link {
            display: block;
            text-align: center;
            margin-top: 20px;
            color: #a259ff;
            text-decoration: none;
            font-weight: 600;
            transition: color 0.3s ease;
        }
        .back-link:hover {
            color: #8000ff;
            text-decoration: underline;
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
        <div class="form-container">
            <h2>Editar Sessão</h2>
            <form action="/editar-sessao/{{sessao.idSessao}}" method="POST">
                <div class="form-group">
                    <label for="service_type">Tipo de Serviço:</label>
                    <select id="service_type" name="service_type" required>
                        <option value="Mixagem" {{'selected' if sessao.tipoServico == 'Mixagem' else ''}}>Mixagem</option>
                        <option value="Masterização" {{'selected' if sessao.tipoServico == 'Masterização' else ''}}>Masterização</option>
                        <option value="Produção Musical" {{'selected' if sessao.tipoServico == 'Produção Musical' else ''}}>Produção Musical</option>
                        <option value="Gravação" {{'selected' if sessao.tipoServico == 'Gravação' else ''}}>Gravação</option>
                        <option value="Consultoria" {{'selected' if sessao.tipoServico == 'Consultoria' else ''}}>Consultoria</option>
                        <option value="Outro" {{'selected' if sessao.tipoServico == 'Outro' else ''}}>Outro</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="session_date">Data da Sessão:</label>
                    <input type="date" id="session_date" name="session_date" value="{{sessao.dataServico}}" required>
                </div>
                <div class="form-group">
                    <label for="session_time">Horário da Sessão:</label>
                    <input type="time" id="session_time" name="session_time" value="{{sessao.horarioServico}}" required>
                </div>
                <div class="form-group">
                    <label for="project_details">Detalhes do Projeto:</label>
                    <textarea id="project_details" name="project_details" rows="5">{{sessao.detalhes}}</textarea>
                </div>
                <div class="form-group">
                    <input type="submit" value="Salvar Alterações">
                </div>
            </form>
            <a href="/minhas-sessoes" class="back-link">Cancelar e Voltar</a>
        </div>
    </main>

    <footer class="main-footer">
        <p>&copy; 2025 Sonar Studio - All rights reserved.</p>
    </footer>

    % else:
    <div class="login-prompt">
        <h1>Página Exclusiva para Clientes</h1>
        <h3>Realize o login para editar sua sessão.</h3>
        <a href="/portal" class="cta-button">Ir para o Portal</a>
    </div>
    % end

    <script src="/static/js/script.js"></script>
</body>
</html>