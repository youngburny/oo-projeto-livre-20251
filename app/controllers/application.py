from app.controllers.datarecord import UserRecord, MessageRecord, SessionRecord
from bottle import template, redirect, request, response, Bottle, static_file, HTTPResponse
import os
import uuid

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
            'admin': self.admin,
            # 'admin_remove_usuarios_e_sessoes': self.admin_remove_user_and_sessions,
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

        # Rotas para o Admin: Remoção de usuários

        @self.app.route('/admin/confirmar-remocao-usuario/<username>', method='GET')
        def admin_confirmar_remocao_usuario_getter(username):
            current_user = self.getCurrentUserBySessionId()
            # Garante que apenas administradores possam acessar esta rota
            if not current_user or not current_user.isAdmin():
                self.feedback_message = "Acesso negado: Somente administradores podem remover usuários."
                return redirect('/home')
            
            # Não permitir que um admin tente se auto-deletar por aqui, ou deletar outro admin
            user_to_remove, user_type_to_remove = self.__users.getUserByUsername(username)
            if not user_to_remove or user_to_remove.isAdmin(): # Se não encontrar ou for admin
                    self.feedback_message = "Erro: Não é possível remover este usuário ou conta inexistente."
                    return redirect('/admin') # Redireciona de volta para o painel admin

            return template(
                'app/views/html/admin_confirmar_remocao_usuario',
                current_user=current_user, # O admin logado
                usuario_a_remover=user_to_remove, # O usuário que será removido
                transfered=True # Para renderizar o cabeçalho
            )

        @self.app.route('/admin/remover-usuario/<username>', method='POST')
        def admin_remover_usuario_action(username):
            print(username)
            current_user = self.getCurrentUserBySessionId()
            # Garante que apenas administradores possam executar esta ação
            if not current_user or not current_user.isAdmin():
                self.feedback_message = "Acesso negado: Somente administradores podem remover usuários."
                return redirect('/home')
            
            # Não permitir que um admin tente se deletar por aqui, ou deletar outro admin
            user_to_delete_obj, user_type_to_delete = self.__users.getUserByUsername(username)
            if not user_to_delete_obj or user_to_delete_obj.isAdmin() or user_to_delete_obj.username == current_user.username:
                self.feedback_message = "Erro: Não é possível remover este usuário."
                return redirect('/admin') # Redireciona de volta para o painel admin

            # Chama o método auxiliar para remover o usuário e suas sessões
            admin_remove_user_and_sessions(username)
            return redirect('/admin') # Redireciona de volta para o painel admin após a ação


        def admin_remove_user_and_sessions(username_to_delete):
            # Encontra o objeto do usuário para deletar
            user_obj, account_type = self.__users.getUserByUsername(username_to_delete)
            
            if not user_obj:
                self.feedback_message = f"Erro: Usuário '{username_to_delete}' não encontrado para remoção."
                return

            # Encontra e remove todas as sessões associadas a este usuário
            sessions_of_user = self.__sessions.getSessions(username=username_to_delete)
            sessions_removed_count = 0
            for session in sessions_of_user:
                removed_id = self.__sessions.removeSession(session.idSessao)
                if removed_id:
                    sessions_removed_count += 1
                else:
                    print(f"Atenção: Não foi possível remover a sessão ID {session.idSessao} para o usuário {username_to_delete}.")

            # Remove o usuário do sistema
            removed_user_name = self.__users.removeUser(user_obj) # user_obj é o objeto UserAccount

            if removed_user_name:
                self.feedback_message = f"Usuário '{removed_user_name}' e {sessions_removed_count} sessões associadas removidos com sucesso!"
                self.update_account_list() # Atualiza lista de usuários via WebSocket se necessário
            else:
                self.feedback_message = f"Erro: Não foi possível remover o usuário '{username_to_delete}'."

#------------------------------------------------------------------------------------

        # Rota para upload de arquivos no websocket

        @self.app.route('/upload-file', method='POST')
        def upload_file_action():
            current_user = self.getCurrentUserBySessionId()
            if not current_user:
                return HTTPResponse(status=401, body={'message': 'Não autorizado'})
            
            upload = request.files.get('file')
            if not upload:
                return HTTPResponse(status=400, body={'message': 'Nenhum arquivo enviado'})
            
            upload_dir = './app/static/uploads'
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir) # Se não existir, cria o diretório, mas ele existe. (?)

            file_extension = os.path.splitext(upload.filename)[1]
            unique_filename = str(uuid.uuid4()) + file_extension
            file_path = os.path.join(upload_dir, unique_filename)

            try:
                upload.save(file_path)
                file_url = f'/static/uploads/{unique_filename}'

                self.sio.emit('message', {
                    'type': 'file',
                    'url': file_url,
                    'filename': upload.filename,
                    'username': current_user.username,
                    'content': f"Enviou um arquivo: {upload.filename}"})

                return HTTPResponse(status=200, body={'message': 'Arquivo enviado e notificado com sucesso', 'file_url': file_url})
        
            except Exception as e:

                print(f"Erro ao salvar o arquivo: {e}")
                return HTTPResponse(status=500, body={'message': 'Erro ao salvar o arquivo'})

        
        @self.app.route('/chat', method='GET')
        def chat_getter():
            return self.render('chat')

        @self.app.route('/')
        @self.app.route('/portal', method='GET')
        def portal_getter():
            message = self.feedback_message
            self.feedback_message = None

            current_session_id_on_portal_load = request.get_cookie('session_id')
            current_user_on_portal_load = None
            if current_session_id_on_portal_load:
                current_user_on_portal_load = self.__users.getCurrentUser(current_session_id_on_portal_load)
            
            print(f"\n--- DEBUG: Carregando Portal (GET /portal) ---")
            print(f"  Cookie session_id no request: {current_session_id_on_portal_load}")
            print(f"  Usuário associado ao cookie: {current_user_on_portal_load.username if current_user_on_portal_load else 'NÃO AUTENTICADO'}")
            print(f"--------------------------------------------------\n")
            # ----------------------------------------

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
        
        # if current_user:
        #     print(f"DEBUG: Usuário '{current_user.username}' já está logado no portal.")
        #     return redirect('/home') # Redireciona para home se já estiver logado 
            
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
        print(f"\n--- DEBUG: Início da autenticação para {username} ---")
        
        # Verifica o usuário no banco de dados
        new_session_id = self.__users.checkUser(username, password)
        
        if new_session_id: # Autenticação bem-sucedida
            # Deletando explicitamente o cookie antigo para a raiz do domínio
            old_session_id_from_cookie = request.get_cookie('session_id')
            if old_session_id_from_cookie:
                response.delete_cookie('session_id', path='/')
                print(f"DEBUG: Cookie antigo '{old_session_id_from_cookie}' deletado.")
                
                # Limpa a sessão antiga do dicionário de usuários autenticados no servidor
                if old_session_id_from_cookie in self.__users.getAuthenticatedUsers():
                    del self.__users.getAuthenticatedUsers()[old_session_id_from_cookie]
                    print(f"DEBUG: Sessão '{old_session_id_from_cookie}' removida de __authenticated_users.")

            # Definindo o novo cookie com path explícito para a raiz
            response.set_cookie('session_id', new_session_id, httponly=True, max_age=3600, path='/')
            print(f"DEBUG: Novo cookie '{new_session_id}' setado para {username}.")
            
            self.feedback_message = f"Bem-vindo, {username}!" # Mensagem de sucesso no login
            print(f"DEBUG: Autenticado {username}. Redirecionando para /home.")
            redirect('/home')
        else: # Se a autenticação falhar
            self.feedback_message = "Usuário ou senha inválidos."
            print(f"DEBUG: Falha na autenticação para {username}. Redirecionando para /portal.")
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
        print("\n--- DEBUG: Início do logout ---")

        session_id = request.get_cookie('session_id')
        if session_id:
            if session_id in self.__users.getAuthenticatedUsers():
                logged_out_username = self.__users.getAuthenticatedUsers()[session_id].username
                del self.__users.getAuthenticatedUsers()[session_id]
                print(f"DEBUG: Sessão '{session_id}' para '{logged_out_username}' removida de __authenticated_users.")
            
            response.delete_cookie('session_id', path='/') # Deleta o cookie do navegador
            print(f"DEBUG: Cookie '{session_id}' deletado do navegador.")
        else:
            print("DEBUG: Nenhum session_id encontrado no cookie para fazer logout.")
        
        self.update_users_list() # Notifica clientes sobre atualização da lista de usuários
        print("--- DEBUG: Fim do logout ---")

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
                    break

            user = None
            if session_id:
                user = self.__users.getCurrentUser(session_id)
                if user:
                    # Mapeia o SID do WebSocket para o objeto de usuário autenticado
                    self.sid_to_user[sid] = user
                    print(f'DEBUG: WS Client conectado: SID={sid}, Usuário={user.username}, SessionID={session_id}.')
                    self.sio.emit('connected', {'data': f'Conectado como {user.username}!'}, room=sid)
                    self.update_users_list() # Atualiza lista de online para todos
                else:
                    print(f'DEBUG: WS Client conectado: SID={sid}, SessionID={session_id}, mas sem usuário ativo no servidor. Cookie antigo?')
                    self.sio.emit('connected', {'data': 'Sessão inválida. Faça login novamente.'}, room=sid)
            else:
                print(f'DEBUG: WS Client conectado: SID={sid}, sem cookie de sessão. Conectado como visitante.')
                self.sio.emit('connected', {'data': 'Conectado. Faça login para acesso completo.'}, room=sid)

                
        @self.sio.event
        def disconnect(sid):
            if sid in self.sid_to_user:
                disconnected_user = self.sid_to_user[sid].username
                del self.sid_to_user[sid]
                print(f'Cliente desconectado: {sid}, usuário: {disconnected_user}')
            else:
                print(f'Client desconectado: {sid} (Usuário não autenticado.)')

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
    def update_users_list(self): # Este método é da classe, então usa 'self'
        print("DEBUG: update_users_list chamado.")
    
        connected_users_set = set()
        for sid, user_obj in self.sid_to_user.items():
            if user_obj: 
                connected_users_set.add(user_obj.username)

        
        users_list_for_js = [{'username': username} for username in connected_users_set]
        
        print(f"DEBUG: update_users_list - Usuários para emitir: {users_list_for_js}")
        self.sio.emit('update_users_event', {'users': users_list_for_js})

    # este método permite que o controller se comunique diretamente com todos
    # os clientes conectados. Sempre que algum usuários se removerem
    # este método vai comunicar todos os Administradores ativos.
    def update_account_list(self):
        print('Atualizando a lista de usuários cadastrados...')
        users = self.__users.getUserAccounts()
        users_list = [{'username': user.username} for user in users]
        self.sio.emit('update_account_event', {'accounts': users_list})
