<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sonar Studio - Login</title>
    <link rel="icon" type="image/x-icon" href="/static/img/favicon.ico" />
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/static/css/portal.css">
</head>
<body>
    <div class="login-container">
        <div class="login-card">
            <h2>Bem-vindo</h2>
            <p class="logo-text">Acesse o Sonar Studio</p>

            % if edited:
                <p style="color: green;">Usuário {{edited}} editado com sucesso!</p>
            % end
            % if removed:
                <p style="color: orange;">Usuário {{removed}} removido com sucesso.</p>
            % end
            % if created:
                <p style="color: green;">Usuário {{created}} criado com sucesso!</p>
            % end
            
            <form action="/portal" method="POST">
                <div class="input-group">
                    <label for="username">Usuário</label>
                    <input type="text" id="username" name="username" placeholder="Digite seu usuário" required>
                </div>
                <div class="input-group">
                    <label for="password">Senha</label>
                    <input type="password" id="password" name="password" placeholder="Digite sua senha" required>
                </div>
                <button type="submit" class="login-button">Entrar</button>
            </form>

            <a href="/create" class="register-link">Ainda não tem conta? Crie uma aqui.</a>
        </div>
    </div>
</body>
</html>