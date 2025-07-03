<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agendamento de Sessão</title>
    <link rel="icon" type="image/x-icon" href="/static/img/favicon.ico" />
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" type="text/css" href="/static/css/pagina.css"/>
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

    <main class="container">
        <section class="booking-section">
            <div class="booking-header">
                <h1>Agende sua Sessão</h1>
                <p>Preencha os detalhes abaixo para reservar seu horário no estúdio.</p>
            </div>
            
            <!--- <form id="booking-form" class="booking-form" action="/agendamento-sucesso" method="post"> -->
            <form id="booking-form" class="booking-form" action="/agendar" method="post">    
                <div class="form-group">
                    <label for="service-type">Tipo de Serviço</label>
                    <select id="service-type" name="service_type" required>
                        <option value="" disabled selected>Selecione o serviço...</option>
                        <option value="producao">Produção Musical Completa</option>
                        <option value="gravacao">Gravação de Vocais/Instrumentos</option>
                        <option value="mixagem">Mixagem</option>
                        <option value="masterizacao">Masterização</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="session-date">Data da Sessão</label>
                    <input type="date" id="session-date" name="session_date" required>
                </div>

                <div class="form-group">
                    <label for="session-time">Horário de Início</label>
                    <input type="time" id="session-time" name="session_time" min="09:00" max="18:00" required>
                    <small>Horários disponíveis das 09:00 às 18:00.</small>
                </div>
                
                <div class="form-group">
                    <label for="project-details">Detalhes do Projeto</label>
                    <textarea id="project-details" name="project_details" rows="4" placeholder="Fale um pouco sobre o que você precisa..."></textarea>
                </div>
                
                <button type="submit" class="cta-button">Confirmar Agendamento</button>
            </form>
        </section>
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