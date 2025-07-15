from app.controllers.datarecord import UserRecord, MessageRecord, SessionRecord
from bottle import template, redirect, request, response, Bottle, static_file
import socketio


class Application:

    def __init__(self):

        self.pages = {
            'portal': self.portal,
            'home': self.home,
            'agendar': self.agendar,
            'create': self.create,
            'delete': self.delete,
            'chat': self.chat,
            'edit': self.edit,
            'agendamento-sucesso': self.agendamento_sucesso,
            'minhas-sessoes': self.minhas_sessoes,
            'admin': self.admin
        }
        
        self.__users = UserRecord()
        self.__messages = MessageRecord()
        self.__sessions = SessionRecord()

        self.edited = None
        self.removed = None
        self.created= None
        self.feedback_message = None

        # Initialize Bottle app
        self.app = Bottle()
        self.setup_routes()

        # Initialize Socket.IO server
        self.sio = socketio.Server(async_mode='eventlet')
        self.setup_websocket_events()

        # Create WSGI app
        self.wsgi_app = socketio.WSGIApp(self.sio, self.app)

        self.sid_to_user = {} #Mapeamento sid para o usuário


    # estabelecimento das rotas
    def setup_routes(self):
        @self.app.route('/static/<filepath:path>')
        def serve_static(filepath):
            return static_file(filepath, root='./app/static')

        @self.app.route('/favicon.ico')
        def favicon():
            return static_file('favicon.ico', root='.app/static')
        
        @self.app.route('/admin', method='GET')
        def admin_getter():
            return self.render('admin')

        # ROTA DAS PÁGINAS
        @self.app.route('/home', method='GET')
        def home_getter():
            return self.render('home')
        
        @self.app.route('/agendar', method='GET')
        def agendar_getter():
            return self.render('agendar')
        
        @self.app.route('/agendar', method='POST')
        def agendar_action():
            current_user = self.getCurrentUserBySessionId()
            
            tipo_servico = request.forms.get('service_type')
            data_servico = request.forms.get('session_date')
            horario_servico = request.forms.get('session_time')
            detalhes = request.forms.get('project_details')
            cliente = current_user.username
        
            self.__sessions.bookSession(tipo_servico, data_servico, horario_servico, detalhes, cliente)
            
            return self.agendamento_sucesso(current_user=current_user)

        @self.app.route('/agendamento-sucesso', method='GET')
        def agendamento_sucesso_getter():
            return self.render('agendamento-sucesso')

        @self.app.route('/minhas-sessoes', method='GET')
        def minhas_sessoes_getter():
            return self.render('minhas-sessoes')
        
        # --- Rotas para Edição de Sessão ---
        @self.app.route('/editar-sessao/<idSessao>', method='GET')
        def editar_sessao_getter(idSessao):
            current_user = self.getCurrentUserBySessionId()
            if not current_user:
                return redirect('/portal')
            
            sessao_para_editar = self.__sessions.getSession(idSessao)
            
            # Permite acesso se for admin, ou se a sessão pertencer ao usuário
            if not sessao_para_editar or \
            (sessao_para_editar.cliente != current_user.username and not current_user.isAdmin()):
                return redirect('/minhas-sessoes') # Redireciona se não for dono nem admin
            
            return template(
                'app/views/html/editar_sessao', 
                current_user=current_user, 
                sessao=sessao_para_editar, 
                transfered=True
            )

        @self.app.route('/editar-sessao/<idSessao>', method='POST')
        def editar_sessao_action(idSessao):
            current_user = self.getCurrentUserBySessionId()
            if not current_user:
                return redirect('/portal')
            
            sessao_existente = self.__sessions.getSession(idSessao)

            # Verifica se a sessão existe e se o usuário é o dono ou um admin
            if not sessao_existente or \
            (sessao_existente.cliente != current_user.username and not current_user.isAdmin()):
                # Redireciona para a lista de sessões ou admin, dependendo de onde veio
                return redirect('/minhas-sessoes') # Ou para /admin se veio de lá

            # Pega os dados do formulário
            tipo_servico = request.forms.get('service_type')
            data_servico = request.forms.get('session_date')
            horario_servico = request.forms.get('session_time')
            detalhes = request.forms.get('project_details')

            # Se for admin, o cliente da sessão deve ser mantido como o original
            # Se for o próprio cliente editando, o cliente é o current_user.username
            cliente_para_atualizar = sessao_existente.cliente # Mantém o cliente original
           

            self.__sessions.setSession(
                idSessao=idSessao, 
                tipoServico=tipo_servico, 
                dataServico=data_servico, 
                horarioServico=horario_servico, 
                detalhes=detalhes,
                cliente=cliente_para_atualizar # Garante que o cliente da sessão não mude indevidamente
            )
            
            # Redireciona para a página de onde o usuário veio
            if current_user.isAdmin():
                redirect('/admin')
            else:
                redirect('/minhas-sessoes')


        # --- Rotas para Remoção de Sessão --------------------------------
        @self.app.route('/confirmar-remocao-sessao/<idSessao>', method='GET')
        def confirmar_remocao_sessao_getter(idSessao):
            current_user = self.getCurrentUserBySessionId()
            if not current_user:
                return redirect('/portal')
            
            sessao_para_remover = self.__sessions.getSession(idSessao)

            if not sessao_para_remover or \
            (sessao_para_remover.cliente != current_user.username and not current_user.isAdmin()):
                return redirect('/minhas-sessoes')
            
            return template(
                'app/views/html/confirmar_remocao_sessao',
                current_user=current_user,
                sessao=sessao_para_remover,
                transfered=True
            )

        @self.app.route('/remover-sessao/<idSessao>', method='POST')
        def remover_sessao_action(idSessao):
            current_user = self.getCurrentUserBySessionId()
            if not current_user:
                return redirect('/portal')
            
            sessao_existente = self.__sessions.getSession(idSessao)

            if not sessao_existente or \
            (sessao_existente.cliente != current_user.username and not current_user.isAdmin()):
                # Redireciona para a lista de sessões ou admin, dependendo de onde veio
                return redirect('/minhas-sessoes') # Ou para /admin se veio de lá

            self.__sessions.removeSession(idSessao)
            
            # Redireciona para a página de onde o usuário veio
            if current_user.isAdmin():
                redirect('/admin')
            else:
                redirect('/minhas-sessoes')

        
#------------------------------------------------------------------------------------
        
        @self.app.route('/chat', method='GET')
        def chat_getter():
            return self.render('chat')

        @self.app.route('/')
        @self.app.route('/portal', method='GET')
        def portal_getter():
            message = self.feedback_message # Pega a mensagem do atributo da aplicação
            self.feedback_message = None # Limpa para não ser exibida em futuras requisições GET sem post
            return self.render('portal', feedback_message=message)

        @self.app.route('/edit', method='GET')
        def edit_getter():
       
            message = self.feedback_message
            self.feedback_message = None
            return self.render('edit', feedback_message=message)
        
        @self.app.route('/portal', method='POST')
        def portal_action():
            username = request.forms.get('username')
            password = request.forms.get('password')
            self.authenticate_user(username, password)

        @self.app.route('/edit', method='POST')
        def edit_action():
            current_user_obj = self.getCurrentUserBySessionId()
            if not current_user_obj:
                return redirect('/portal')

            old_username = current_user_obj.username # Nome de usuário atual do usuário logado
            new_username = request.forms.get('username')
            new_password = request.forms.get('password')

            self.update_user(old_username, new_username, new_password)
            return redirect('/home') 

        @self.app.route('/create', method='GET')
        def create_getter():
            message = self.feedback_message
            self.feedback_message = None
            return self.render('create', feedback_message=message) 
        
        @self.app.route('/create', method='POST')
        def create_action():
            username = request.forms.get('username')
            password = request.forms.get('password')
            
            # Altera como insert_user é chamado, pois ele agora retorna None em caso de falha
            self.insert_user(username, password)
            # O redirecionamento será tratado dentro de insert_user
            return redirect('/portal') #

        @self.app.route('/logout', method='POST')
        def logout_action():
            self.logout_user()
            return self.render('portal')

        @self.app.route('/delete', method='GET')
        def delete_getter():
          
            message = self.feedback_message
            self.feedback_message = None
            return self.render('delete', feedback_message=message)

        @self.app.route('/delete', method='POST')
        def delete_action():
            self.delete_user()
            return self.render('portal')


    # método controlador de acesso às páginas:

    def admin(self, feedback_message=None):
        current_user = self.getCurrentUserBySessionId()

        print(f"\n--- Tentando acessar /admin ---")
        print(f"  current_user: {current_user.username if current_user else 'NÃO LOGADO'}")
        if current_user:
            print(f"  current_user.isAdmin(): {current_user.isAdmin()}")
        print("----------------------------\n")

        if current_user and current_user.isAdmin():
            todas_sessoes = self.__sessions.getSessions()
            todos_usuarios = self.__users.getUserAccounts()

            return template(
                'app/views/html/admin', 
                current_user=current_user,
                sessoes=todas_sessoes,
                usuarios=todos_usuarios,
                transfered=True,
                feedback_message=feedback_message # Passa a mensagem de feedback
            )
        else:
            self.feedback_message = "Acesso negado: Você precisa ser um administrador."
            return redirect('/home')

    def render(self, page_name, **kwargs):
        content_method = self.pages.get(page_name, self.portal)

        return content_method(**kwargs)

    # métodos controladores de páginas
    def getAuthenticatedUsers(self):
        return self.__users.getAuthenticatedUsers()

    def getCurrentUserBySessionId(self):
        session_id = request.get_cookie('session_id')
        return self.__users.getCurrentUser(session_id)

    ## PÁGINAS DE GESTÃO DE USUÁRIO PELO PORTAL
    def create(self, feedback_message=None): 
        return template('app/views/html/create', feedback_message=feedback_message)

    def delete(self, feedback_message=None): 
        current_user = self.getCurrentUserBySessionId()
        if not current_user:
            return redirect('/portal')
        return template('app/views/html/delete', current_user=current_user, feedback_message=feedback_message)

    def edit(self, feedback_message=None): # Defina feedback_message como None por padrão
        current_user = self.getCurrentUserBySessionId()
        if not current_user:
            return redirect('/portal')
        
        return template('app/views/html/edit', current_user=current_user, feedback_message=feedback_message)

    def portal(self, feedback_message=None): # feedback_message virá de portal_getter ou de redirects
        current_user = self.getCurrentUserBySessionId()
        
        # Prioriza a mensagem que vem diretamente como argumento da rota GET
        # Senão, pega a mensagem da instância da aplicação (feedback_message setado por redirects POST)
        final_message_to_display = feedback_message
        if not final_message_to_display:
            final_message_to_display = self.feedback_message

        # Limpa a mensagem da instância após ela ter sido recuperada para esta requisição
        self.feedback_message = None 
        
        # Limpa as flags antigas de 'edited', 'removed', 'created'
        self.edited = None
        self.removed = None
        self.created = None

        if current_user:
            return template('app/views/html/portal', 
                            username=current_user.username, 
                            feedback_message=final_message_to_display)
        
        return template('app/views/html/portal', 
                        username=None, 
                        feedback_message=final_message_to_display) 

    ## PÁGINAS DA APLICAÇÃO
    def home(self):
        self.update_users_list()
        current_user = self.getCurrentUserBySessionId()
        if current_user:
            return template('app/views/html/home', transfered=True, current_user=current_user)
        return template('app/views/html/portal', transfered=False)
    
    def agendar(self):
        self.update_users_list()
        current_user = self.getCurrentUserBySessionId()
        if current_user:
            return template('app/views/html/agendar', transfered=True, current_user=current_user)
        return template('app/views/html/portal', transfered=False)

    def minhas_sessoes(self):
        self.update_users_list()
        current_user = self.getCurrentUserBySessionId()
        if current_user:
            
            if not current_user:
                return redirect('/portal') 
            
            nome_usuario = current_user.username
            
            # Usa o método que criamos no Passo 1 para buscar os dados
            lista_de_sessoes = self.__sessions.getSessions(nome_usuario)
            
            # Renderiza o novo template, passando a lista de sessões para ele
            return template(
                'app/views/html/minhas_sessoes', 
                sessoes=lista_de_sessoes,
                current_user=current_user,
                transfered=True
            )

        return template('app/views/html/portal', transfered=False)
    
    def agendamento_sucesso(self, current_user):
        return template('app/views/html/agendamento-sucesso', transfered=True, current_user=current_user)   
        
    ## ROTAS DE USUÁRIOS
    def is_authenticated(self, username):
        current_user = self.getCurrentUserBySessionId()
        if current_user:
            return username == current_user.username
        return False

    def authenticate_user(self, username, password):
        session_id = self.__users.checkUser(username, password)
        if session_id:
            print(f'Usuário {username} autenticado com sucesso!')
            self.logout_user()
            response.set_cookie('session_id', session_id, httponly=True, secure=True, max_age=3600)
            redirect('/home')
        redirect('/portal')

    def delete_user(self):
        current_user = self.getCurrentUserBySessionId()
        if not current_user:
            self.feedback_message = "Erro: Não há usuário logado para deletar."
            redirect('/portal')
            return 

        removed_username = self.__users.removeUser(current_user) 
        self.logout_user() # Desloga o usuário após tentar a remoção
        self.update_account_list() # Atualiza lista de usuários (para WebSocket)

        if removed_username:
            self.feedback_message = f"Conta '{removed_username}' excluída com sucesso!"
        else:
            self.feedback_message = "Erro ao excluir conta. Usuário não encontrado no sistema."
        
        # Redireciona sempre para o portal após a tentativa de exclusão
        redirect('/portal')

    def insert_user(self, username, password):
        creation_result = self.__users.book(username, password, [])
        if creation_result:
            self.feedback_message = f"Conta '{username}' criada com sucesso! Faça login."
            self.update_account_list()
            redirect('/portal')
        else:
            self.feedback_message = "Erro ao criar conta: Nome de usuário já em uso."
            redirect('/create')

    def update_user(self, old_username, new_username, new_password):
        updated_user_obj = self.__users.setUser(old_username, new_username, new_password)
        if updated_user_obj:
            session_id = request.get_cookie('session_id')
            if session_id and session_id in self.__users.getAuthenticatedUsers():
                self.__users.getAuthenticatedUsers()[session_id] = updated_user_obj
            self.feedback_message = "Perfil atualizado com sucesso!"
            redirect('/home')
        else:
            self.feedback_message = "Erro: Nome de usuário já em uso ou outro erro ocorreu."
            redirect('/edit')

    def logout_user(self):
        session_id = request.get_cookie('session_id')
        self.__users.logout(session_id)
        response.delete_cookie('session_id')
        self.update_users_list()

    def chat(self):
        current_user = self.getCurrentUserBySessionId()
        if current_user:
            messages = self.__messages.getUsersMessages()
            auth_users= self.__users.getAuthenticatedUsers().values()
            return template('app/views/html/chat', current_user=current_user, \
            messages=messages, auth_users=auth_users)
        redirect('/portal')

    def newMessage(self, message):
        try:
            content = message
            current_user = self.getCurrentUserBySessionId()
            return self.__messages.book(current_user.username, content)
        except UnicodeEncodeError as e:
            print(f"Encoding error: {e}")
            return "An error occurred while processing the message."

    # Websocket:

    def setup_websocket_events(self):

        @self.sio.event
        def connect(sid, environ):
            cookies = environ.get('HTTP_COOKIE', '')
            session_id = None
            for cookie in cookies.split(';'):
                if 'session_id=' in cookie:
                    session_id = cookie.strip().split('=')[1]
            user = self.__users.getCurrentUser(session_id)
            if user:
                self.sid_to_user[sid] = user
                print(f'Client connected: {sid}, user: {getattr(user, 'username', None)}')
                self.sio.emit('connected', {'data': 'Connected'}, room=sid)

        @self.sio.event
        def disconnect(sid):
            if sid in self.sid_to_user:
                del self.sid_to_user[sid]
            print(f'Client disconnected: {sid}')

        @self.sio.event
        def message(sid, data):
            user = self.sid_to_user.get(sid)
            if user:
                objdata = self.__messages.book(user.username, data)
                self.sio.emit('message', {'content': objdata.content, 'username': objdata.username})
            else:
                self.sio.emit('message', {'content' : 'Usuário não autenticado', 'username': 'Desconhecido'})
                      

        # @self.sio.event
        # async def connect(sid, environ):
        #     print(f'Client connected: {sid}')
        #     self.sio.emit('connected', {'data': 'Connected'}, room=sid)

        # @self.sio.event
        # async def disconnect(sid):
        #     print(f'Client disconnected: {sid}')

        # # recebimento de solicitação de cliente para atualização das mensagens
        # @self.sio.event
        # def message(sid, data):
        #     objdata = self.newMessage(data)
        #     self.sio.emit('message', {'content': objdata.content, 'username': objdata.username})

        # solicitação para atualização da lista de usuários conectados. Quem faz
        # esta solicitação é o próprio controlador. Ver update_users_list()
        @self.sio.event
        def update_users_event(sid, data):
            self.sio.emit('update_users_event', {'content': data})

        # solicitação para atualização da lista de usuários conectados. Quem faz
        # esta solicitação é o próprio controlador. Ver update_users_list()
        @self.sio.event
        def update_account_event(sid, data):
            self.sio.emit('update_account_event', {'content': data})

    # este método permite que o controller se comunique diretamente com todos
    # os clientes conectados. Sempre que algum usuários LOGAR ou DESLOGAR
    # este método vai forçar esta atualização em todos os CHATS ativos. Este
    # método é chamado sempre que a rota ''
    def update_users_list(self):
        print('Atualizando a lista de usuários conectados...')
        users = self.__users.getAuthenticatedUsers()
        users_list = [{'username': user.username} for user in users.values()]
        self.sio.emit('update_users_event', {'users': users_list})

    # este método permite que o controller se comunique diretamente com todos
    # os clientes conectados. Sempre que algum usuários se removerem
    # este método vai comunicar todos os Administradores ativos.
    def update_account_list(self):
        print('Atualizando a lista de usuários cadastrados...')
        users = self.__users.getUserAccounts()
        users_list = [{'username': user.username} for user in users]
        self.sio.emit('update_account_event', {'accounts': users_list})
