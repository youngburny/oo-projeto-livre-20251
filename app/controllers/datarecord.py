from app.models.session import Session
from app.models.user_account import UserAccount, SuperAccount
from app.models.user_message import UserMessage
import json
import uuid


class MessageRecord():
    """Banco de dados JSON para o recurso: Mensagem"""

    def __init__(self):
        self.__user_messages= []
        self.read()

    def read(self):
        try:
            with open("app/controllers/db/user_messages.json", "r") as fjson:
                user_msg = json.load(fjson)
                self.__user_messages = [UserMessage(**msg) for msg in user_msg]
        except FileNotFoundError:
            print('Não existem mensagens registradas!')

    def __write(self):
        try:
            with open("app/controllers/db/user_messages.json", "w") as fjson:
                user_msg = [vars(user_msg) for user_msg in \
                self.__user_messages]
                json.dump(user_msg, fjson)
                print(f'Arquivo gravado com sucesso (Mensagem)!')
        except FileNotFoundError:
            print('O sistema não conseguiu gravar o arquivo (Mensagem)!')

    def book(self,username,content):
        new_msg= UserMessage(username,content)
        self.__user_messages.append(new_msg)
        self.__write()
        return new_msg

    def getUsersMessages(self):
        return self.__user_messages

# ------------------------------------------------------------------------------

class UserRecord():
    """Banco de dados JSON para o recurso: Usuário"""

    def __init__(self):
        self.__allusers= {'user_accounts': [], 'super_accounts': []}
        self.__authenticated_users = {}
        self.read('user_accounts')
        self.read('super_accounts')


    def read(self,database):
        account_class = SuperAccount if (database == 'super_accounts' ) else UserAccount
        try:
            with open(f"app/controllers/db/{database}.json", "r") as fjson:
                user_d = json.load(fjson)
                self.__allusers[database]= [account_class(**data) for data in user_d]
        except FileNotFoundError:
            self.__allusers[database].append(account_class('Guest', '000000'))

    def __write(self,database):
        try:
            with open(f"app/controllers/db/{database}.json", "w") as fjson:
                user_data = [vars(user_account) for user_account in \
                self.__allusers[database]]
                json.dump(user_data, fjson)
                print(f'Arquivo gravado com sucesso (Usuário)!')
        except FileNotFoundError:
            print('O sistema não conseguiu gravar o arquivo (Usuário)!')

    def setUser(self,username,password):
        for account_type in ['user_accounts', 'super_accounts']:
            for user in self.__allusers[account_type]:
                if username == user.username:
                    user.password= password
                    print(f'O usuário {username} foi editado com sucesso.')
                    self.__write(account_type)
                    return username
        print('O método setUser foi chamado, porém sem sucesso.')
        return None

    def removeUser(self, user):
        for account_type in ['user_accounts', 'super_accounts']:
            if user in self.__allusers[account_type]:
                print(f'O usuário {"(super) " if account_type == "super_accounts" else ""}{user.username} foi encontrado no cadastro.')
                self.__allusers[account_type].remove(user)
                print(f'O usuário {"(super) " if account_type == "super_accounts" else ""}{user.username} foi removido do cadastro.')
                self.__write(account_type)
                return user.username
        print(f'O usuário {user.username} não foi identificado!')
        return None


    def book(self, username, password, permissions):
        account_type = 'super_accounts' if permissions else 'user_accounts'
        account_class = SuperAccount if permissions else UserAccount
        new_user = account_class(username, password, permissions) if permissions else account_class(username, password)
        self.__allusers[account_type].append(new_user)
        self.__write(account_type)
        return new_user.username

    def getUserAccounts(self):
        return self.__allusers['user_accounts']

    def getCurrentUser(self,session_id):
        if session_id in self.__authenticated_users:
            return self.__authenticated_users[session_id]
        else:
            return None

    def getAuthenticatedUsers(self):
        return self.__authenticated_users

    def checkUser(self, username, password):
        for account_type in ['user_accounts', 'super_accounts']:
            for user in self.__allusers[account_type]:
                if user.username == username and user.password == password:
                    session_id = str(uuid.uuid4())  # Gera um ID de sessão único
                    self.__authenticated_users[session_id] = user
                    return session_id  # Retorna o ID de sessão para o usuário
        return None

    def logout(self, session_id):
        if session_id in self.__authenticated_users:
            del self.__authenticated_users[session_id] # Remove o usuário logado


# ------------------------------------------------------------------------------


class SessionRecord():
    """Banco de dados JSON para o recurso: Sessão"""

    def __init__(self):
        self.__sessions= []
        self.read()

    def read(self):
        try:
            with open(f"app/controllers/db/sessions.json", "r") as fjson:
                session_d = json.load(fjson)
                self.__sessions= [Session(**data) for data in session_d]
        except FileNotFoundError:
            self.__sessions.append(Session(0, 'Servico Teste', '2020-02-02', '10:00', 'Teste de servico solicitado', 'Fulano'))

    def __write(self):
        try:
            with open(f"app/controllers/db/sessions.json", "w") as fjson:
                session_data = [vars(session_content) for session_content in \
                self.__sessions]
                json.dump(session_data, fjson)
                print(f'Arquivo gravado com sucesso (Sessão)!')
        except FileNotFoundError:
            print('O sistema não conseguiu gravar o arquivo (Sessão)!')

    def setSession(self, idSessao, tipoServico=None, dataServico=None, horarioServico=None, detalhes=None, cliente=None):
        for session in self.__sessions:
            if idSessao == session.idSessao:
                session.tipoServico= tipoServico if tipoServico else session.tipoServico
                session.dataServico= dataServico if dataServico else session.dataServico
                session.horarioServico= horarioServico if horarioServico else session.horarioServico
                session.detalhes= detalhes if detalhes else session.detalhes
                session.cliente= cliente if cliente else session.cliente
                
                self.__write()
                print(f'A Sessão {session} foi editado com sucesso.')
                return session
                    
        print('O método setSession foi chamado, porém sem sucesso.')
        return None

    def removeSession(self, idSessao):
        for session in self.__sessions:
            if idSessao == session.idSessao:
                print(f'A Sessão {idSessao} foi encontrada!')
                self.__sessions.remove(session)
                print(f'A Sessão {idSessao} foi removida!')
                self.__write()
                return session.idSessao
        print(f'A Sessão {idSessao} não foi encontrada!')
        return None

    def bookSession(self, tipoServico=None, dataServico=None, horarioServico=None, detalhes=None, cliente=None):      
        new_session = Session(str(uuid.uuid4()), tipoServico, dataServico, horarioServico, detalhes, cliente)
        self.__sessions.append(new_session)
        self.__write()
           
        return new_session.idSessao

    def getSession(self, idSessao):
        for session in self.__sessions:
            if idSessao == session.idSessao:
                return session

    def getSessions(self, username=None):
        if not username:
            return self.__sessions
        else:
            return [sessao for sessao in self.__sessions if sessao.cliente == username]
        
        
#-------------------------------------------------------------------------------


    def getCurrentUser(self,session_id):
        if session_id in self.__authenticated_users:
            return self.__authenticated_users[session_id]
        else:
            return None

    def getAuthenticatedUsers(self):
        return self.__authenticated_users

    def checkUser(self, username, password):
        for account_type in ['user_accounts', 'super_accounts']:
            for user in self.__allusers[account_type]:
                if user.username == username and user.password == password:
                    session_id = str(uuid.uuid4())  # Gera um ID de sessão único
                    self.__authenticated_users[session_id] = user
                    return session_id  # Retorna o ID de sessão para o usuário
        return None

    def logout(self, session_id):
        if session_id in self.__authenticated_users:
            del self.__authenticated_users[session_id] # Remove o usuário logado
