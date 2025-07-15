<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Painel Admin - Sonar Studio</title>
    <link rel="icon" type="image/x-icon" href="/static/img/favicon.ico" />
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
    
    <link rel="stylesheet" href="/static/css/pagina.css">
    <link rel="stylesheet" href="/static/css/admin.css">

</head>
<body class="landing-page-body">
    % if current_user and current_user.isAdmin():
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

    <main class="admin-dashboard">
        <h2>Painel de Administração</h2>

        % if feedback_message:
            <p class="feedback-message {{ 'success' if 'sucesso' in feedback_message else 'error' }}">
                {{ feedback_message }}
            </p>
        % end

        <div class="dashboard-section">
            <h3 class="section-title">Todas as Sessões Agendadas</h3>
            % if sessoes:
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>ID Sessão</th>
                            <th>Cliente</th>
                            <th>Serviço</th>
                            <th>Data</th>
                            <th>Horário</th>
                            <th>Detalhes</th>
                            <th>Ações</th> </tr>
                    </thead>
                    <tbody>
                        % for sessao in sessoes:
                        <tr>
                            <td>{{ str(sessao.idSessao)[:8] }}...</td>
                            <td>{{ sessao.cliente }}</td>
                            <td>{{ sessao.tipoServico }}</td>
                            <td>{{ sessao.dataServico }}</td>
                            <td>{{ sessao.horarioServico }}</td>
                            <td>{{ sessao.detalhes }}</td>
                            <td>
                                <a href="/editar-sessao/{{sessao.idSessao}}" class="button-link edit-admin-button">Editar</a>
                                <a href="/confirmar-remocao-sessao/{{sessao.idSessao}}" class="button-link delete-admin-button">Remover</a>
                            </td>
                        </tr>
                        % end
                    </tbody>
                </table>
            % else:
                <p class="no-data">Nenhuma sessão agendada no momento.</p>
            % end
        </div>

        <div class="dashboard-section">
            <h3 class="section-title">Contas de Usuário</h3>
            % if usuarios:
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Usuário</th>
                            <th>Tipo de Conta</th>
                        </tr>
                    </thead>
                    <tbody>
                        % for usuario in usuarios:
                        <tr>
                            <td>{{ usuario.username }}</td>
                            <td>{{ 'Administrador' if usuario.isAdmin() else 'Cliente' }}</td>
                        </tr>
                        % end
                    </tbody>
                </table>
            % else:
                <p class="no-data">Nenhuma conta de usuário registrada.</p>
            % end
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