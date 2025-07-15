<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" type="image/x-icon" href="/static/img/favicon.ico" />
    <title>Crud de usuário</title>
    <link rel="stylesheet" type="text/css" href="/static/css/create.css">
    <script src="/static/js/create.js" defer></script>
</head>
<body>
    <div class="create-container">
        <div class="create-card">
            <h1>Seja bem-vindo ao BMVC! (Bottle Powered)</h1>
            <h4>Cadastre seu nome ou apelido e uma senha numérica de acesso com 6 dígitos:</h4>
            
            % if feedback_message:
                <p class="feedback-message {{ 'success' if 'sucesso' in feedback_message else 'error' }}">
                    {{ feedback_message }}
                </p>
            % end

            <form action="/create" method="post">
                <div class="input-group"> <label for="username">Nome:</label>
                    <input id="username" name="username" type="text" required />
                </div>
                <div class="input-group"> <label for="password">Senha:</label>
                    <input id="password" name="password" type="password" required />
                </div>
                <div class="button-container">
                    <input value="Criar" type="submit" class="create-button" /> </div>
            </form>
            <a href="/portal" class="back-to-portal">Portal</a>
        </div>
    </div>
</body>
</html>