<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Minhas Sessões</title>
    <link rel="icon" type="image/x-icon" href="/static/img/favicon.ico" />
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" type="text/css" href="/static/css/pagina.css"/>
    <style>
        .sessoes-grid-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 25px;
        }
        .sessao-card {
            background-color: #2a2a2a;
            border: 1px solid #8000ff;
            border-left: 5px solid #a259ff;
            border-radius: 15px;
            padding: 20px;
            display: flex;
            flex-direction: column;
            transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
        }
        .sessao-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 20px rgba(128, 0, 255, 0.4);
        }
        .sessao-card h4 {
            color: #a259ff; margin-top: 0; font-size: 1.3em;
            border-bottom: 1px solid #444; padding-bottom: 10px; margin-bottom: 15px;
        }
        .sessao-card p {
            margin: 4px 0; line-height: 1.5; color: #d1d1d1; flex-grow: 1;
        }
        .sessao-card strong { color: #ffffff; }
        .sem-sessoes { text-align: center; padding: 40px; font-size: 1.2em; }
    </style>
</head>
<body>
    % if transfered:
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

    <main class="container" style="max-width: 1200px; margin: 20px auto; padding: 20px;">
        <h2 style="font-size: 2rem; color: #eee; margin-bottom: 30px;">
            <i class="fas fa-history"></i> Sessões Agendadas
        </h2>

        % if sessoes:
            <div class="sessoes-grid-container">
                % for sessao in sessoes:
                    <div class="sessao-card">
                        <h4>Serviço de: {{ sessao.tipoServico if sessao.tipoServico else 'Não especificado' }}</h4>
                        <p><strong>Data:</strong> {{ sessao.dataServico if sessao.dataServico else 'N/A' }}</p>
                        <p><strong>Horário:</strong> {{ sessao.horarioServico if sessao.horarioServico else 'N/A' }}</p>
                        <p><strong>Detalhes:</strong> {{ sessao.detalhes if sessao.detalhes else 'Sem detalhes' }}</p>
                        <div class="sessao-actions">
                            <a href="/editar-sessao/{{sessao.idSessao}}" class="button-link edit-button">Editar</a>
                            <a href="/confirmar-remocao-sessao/{{sessao.idSessao}}" class="button-link delete-button">Remover</a>
                        </div>
                    </div>
                % end
            </div>
        % else:
            <div class="sem-sessoes">
                <p>Você ainda não agendou nenhuma sessão.</p>
                <a href="/agendar" class="button-link" style="text-decoration:none; display:inline-block; margin-top:20px;">Agendar sua primeira sessão</a>
            </div>
        % end
    </main>

    <footer class="main-footer">
        <p>&copy; 2025 Sonar Studio - All rights reserved.</p>
    </footer>

    % else:
    <div class="login-prompt">
        <h1>Página Exclusiva para Clientes</h1>
        <h3>Realize o login para agendar sua sessão.</h3>
        <a href="/portal" class="cta-button">Ir para o Portal</a>
    </div>
    % end

    <script src="/static/js/script.js"></script>
</body>
</html>