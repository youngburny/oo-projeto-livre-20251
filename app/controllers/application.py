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
            'minhas-sessoes': self.minhas_sessoes
        }
        
        self.__users = UserRecord()
        self.__messages = MessageRecord()
        self.__sessions = SessionRecord()

        self.edited = None
        self.removed = None
        self.created= None

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
            
            # Busca a sessão pelo ID para pré-preencher o formulário
            sessao_para_editar = self.__sessions.getSession(idSessao)
            
            if not sessao_para_editar or sessao_para_editar.cliente != current_user.username:
                # Se a sessão não existir ou não pertencer ao usuário logado, redireciona
                return redirect('/minhas-sessoes') # Ou uma página de erro/acesso negado
            
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
            
            # Pega os dados do formulário
            tipo_servico = request.forms.get('service_type')
            data_servico = request.forms.get('session_date')
            horario_servico = request.forms.get('session_time')
            detalhes = request.forms.get('project_details')

            # Tenta atualizar a sessão
            # O setSession promove o funcionamento de atualização
            # Passamos os dados que podem ter sido alterados
            self.__sessions.setSession(
                idSessao=idSessao, 
                tipoServico=tipo_servico, 
                dataServico=data_servico, 
                horarioServico=horario_servico, 
                detalhes=detalhes,
                cliente=current_user.username # Garantir que o cliente não mude indevidamente
            )
            
            redirect('/minhas-sessoes') # Redireciona de volta para a lista de sessões

        # --- Rotas para Remoção de Sessão --------------------------------
        @self.app.route('/confirmar-remocao-sessao/<idSessao>', method='GET')
        def confirmar_remocao_sessao_getter(idSessao):
            current_user = self.getCurrentUserBySessionId()
            if not current_user:
                return redirect('/portal')
            
            sessao_para_remover = self.__sessions.getSession(idSessao)

            if not sessao_para_remover or sessao_para_remover.cliente != current_user.username:
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
            
            # Verifica se a sessão realmente pertence ao usuário antes de remover
            sessao_existente = self.__sessions.getSession(idSessao)
            if sessao_existente and sessao_existente.cliente == current_user.username:
                self.__sessions.removeSession(idSessao)
            
            redirect('/minhas-sessoes')
        
#------------------------------------------------------------------------------------
        
        @self.app.route('/chat', method='GET')
        def chat_getter():
            return self.render('chat')

        @self.app.route('/')
        @self.app.route('/portal', method='GET')
        def portal_getter():
            return self.render('portal')

        @self.app.route('/edit', method='GET')
        def edit_getter():
            return self.render('edit')

        @self.app.route('/portal', method='POST')
        def portal_action():
            username = request.forms.get('username')
            password = request.forms.get('password')
            self.authenticate_user(username, password)

        @self.app.route('/edit', method='POST')
        def edit_action():
            username = request.forms.get('username')
            password = request.forms.get('password')
            print(username + ' sendo atualizado...')
            self.update_user(username, password)
            return self.render('edit')

        @self.app.route('/create', method='GET')
        def create_getter():
            return self.render('create')

        @self.app.route('/create', method='POST')
        def create_action():
            username = request.forms.get('username')
            password = request.forms.get('password')
            self.insert_user(username, password)
            return self.render('portal')

        @self.app.route('/logout', method='POST')
        def logout_action():
            self.logout_user()
            return self.render('portal')

        @self.app.route('/delete', method='GET')
        def delete_getter():
            return self.render('delete')

        @self.app.route('/delete', method='POST')
        def delete_action():
            self.delete_user()
            return self.render('portal')


    # método controlador de acesso às páginas:
    def render(self, page, parameter=None):
        content = self.pages.get(page, self.portal)
        if not parameter:
            return content()
        return content(parameter)

    # métodos controladores de páginas
    def getAuthenticatedUsers(self):
        return self.__users.getAuthenticatedUsers()

    def getCurrentUserBySessionId(self):
        session_id = request.get_cookie('session_id')
        return self.__users.getCurrentUser(session_id)

    ## PÁGINAS DE GESTÃO DE USUÁRIO PELO PORTAL
    def create(self):
        return template('app/views/html/create')

    def delete(self):
        current_user = self.getCurrentUserBySessionId()
        user_accounts= self.__users.getUserAccounts()
        return template('app/views/html/delete', user=current_user, accounts=user_accounts)

    def edit(self):
        current_user = self.getCurrentUserBySessionId()
        user_accounts= self.__users.getUserAccounts()
        return template('app/views/html/edit', user=current_user, accounts= user_accounts)

    def portal(self):
        current_user = self.getCurrentUserBySessionId()
        if current_user:
            portal_render = template('app/views/html/portal', \
            username=current_user.username, edited=self.edited, \
            removed=self.removed, created=self.created)
            self.edited = None
            self.removed= None
            self.created= None
            return portal_render
        portal_render = template('app/views/html/portal', username=None, \
        edited=self.edited, removed=self.removed, created=self.created)
        self.edited = None
        self.removed= None
        self.created= None
        return portal_render

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
            self.logout_user()
            response.set_cookie('session_id', session_id, httponly=True, secure=True, max_age=3600)
            redirect('/home')
        redirect('/portal')

    def delete_user(self):
        current_user = self.getCurrentUserBySessionId()
        self.logout_user()
        self.removed= self.__users.removeUser(current_user)
        self.update_account_list()
        print(f'Valor de retorno de self.removed: {self.removed}')
        redirect('/portal')

    def insert_user(self, username, password):
        self.created= self.__users.book(username, password,[])
        self.update_account_list()
        redirect('/portal')

    def update_user(self, username, password):
        self.edited = self.__users.setUser(username, password)
        redirect('/portal')

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
