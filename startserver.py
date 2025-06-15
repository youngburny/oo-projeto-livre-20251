import eventlet.wsgi
from app.controllers.application import Application
import eventlet




# Inicialize a aplicação
app = Application()


# executa a aplicação
if __name__ == '__main__':

    
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 8080)), app.wsgi_app)
