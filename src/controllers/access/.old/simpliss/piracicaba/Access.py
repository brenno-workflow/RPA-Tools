from modules.mylogger.mylogger import MyLogger
from modules.mysql.mysql import MySQL
from modules.myweb.myweb import MyWeb
from selenium.webdriver.common.keys import Keys
from controllers.access.simpliss import Notification
import time

class Access():
        
    def __init__(self, 
                 webdriver, user, password, host, database, 
                 web_url, web_login, web_password,
                 input_banner, input_banner_close, input_banner_hidden,
                 input_user, input_password, button_entrar, button_sair
                 ):

        # Variaveis gerais
        self.status = False
        self.sucesso = f'SUCESSO - {__name__}'
        self.falha = f'FALHA - {__name__}'
        self.erro = f'ERRO - {__name__}'

        # Instancias
        # Instanciar é uma boa prática e necessário
        # Não instaciar resulta na abertura de processo diferentes e erros
        self.my_logger = MyLogger()
        self.my_sql = MySQL()

        # Metodo de 'INJEÇÃO DE DEPENDENCIA'
        # ref.: https://www.youtube.com/watch?v=5DBfVnQn1Ow
        self.my_web = MyWeb(webdriver)
        self.notification = Notification.Notification(webdriver, input_banner, input_banner_close, input_banner_hidden)

        # Variaveis especificas
        self.user = user
        self.password = password
        self.host = host
        self.database = database

        # Paramentros
        self.web_url = web_url
        self.web_login = web_login
        self.web_password = web_password

        # Inputs
        self.input_user = input_user
        self.input_password = input_password

        # Buttons
        self.button_entrar = button_entrar
        self.button_sair = button_sair
    
    # Função para verificar se existem arquivos com extensão no caminho  
    def login(self):

        # TryCtach
        try:
                
            # Abrir site
            status_open_url = self.my_web.browser(
                'get', None, self.web_url)

            if status_open_url['status']:

                status_notification = self.notification.banner()

                if status_notification['status']:

                    status_type_login = self.my_web.element(
                        self.input_user, 'id', 'click', 'send_keys', self.web_login)

                    if status_type_login['status']:

                        status_type_password = self.my_web.element(
                            self.input_password, 'id', 'click', 'send_keys', self.web_password)

                        if status_type_password['status']:

                            status_entrar = self.my_web.element(
                                self.input_password, 'id', 'send_keys', None, Keys.ENTER)

                            if status_entrar['status']:
                                self.status = True
                                mensagem = f'Sucesso em fazer Login no site: "{self.web_url}", com o login: "{self.web_login}" e password: "{self.web_password}".'
                                print(mensagem)

                            else:
                                self.status = False
                                mensagem = f'Falha em fazer Login no site: "{self.web_url}", com o login: "{self.web_login}" e password: "{self.web_password}".'
                                print(mensagem)

                        else:
                            self.status = False
                            mensagem = f'Falha ao digitar a senha: "{self.web_password}".'
                            print(mensagem)                            
                            
                    else:
                        self.status = False
                        mensagem = f'Falha ao digitar o login: "{self.web_login}".'
                        print(mensagem)                        

                else:
                    self.status = False
                    mensagem = 'Falha ao fechar as notificações.'
                    print(mensagem)                    

            else:
                self.status = False
                mensagem = f'Falha ao abrir a url: "{self.web_url}".'
                print(mensagem)                

            # Alimentar o log
            if self.status:
                self.my_logger.log_info(self.sucesso)
                self.my_logger.log_info(mensagem)

            else:
                self.my_logger.log_warn(self.falha)
                self.my_logger.log_warn(mensagem)

        except Exception as aviso:
            self.status = False
            mensagem = f'Erro em fazer Login no site: "{self.web_url}", com o login: "{self.web_login}" e password: "{self.web_password}".'
            print(aviso)

            # Alimentar o log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error(mensagem)
            self.my_logger.log_error(str(aviso))

        return{'status': self.status}
    
    def logoff(self):

        # TryCtach
        try:

            # Abrir site
            status_open_url = self.my_web.browser(
                'get', None, self.web_url)
            
            if status_open_url['status']:
            
                status_button_sair = self.my_web.element(
                    self.button_sair, 'xpath', 'find')

                if status_button_sair['status']:

                    status_sair = self.my_web.element(
                        self.button_sair, 'xpath', 'click')

                    if status_sair['status']:
                        self.status = True
                        mensagem = 'Sucesso em fazer Logoff.'
                        print(mensagem)

                    else:
                        self.status = False
                        mensagem = f'Falha ao fazer o click no elemento: "{self.button_sair}".'
                        print(mensagem)                  

                else:
                    self.status = False
                    mensagem = f'Falha ao localizar o elemento: "{self.button_sair}".'
                    print(mensagem)   

            else:
                self.status = False
                mensagem = f'Falha ao abrir a url: "{self.web_url}".'
                print(mensagem)             

            # Alimentar o log
            if self.status:
                self.my_logger.log_info(self.sucesso)
                self.my_logger.log_info(mensagem)

            else:
                self.my_logger.log_warn(self.falha)
                self.my_logger.log_warn(mensagem)

        except Exception as aviso:
            self.status = False
            mensagem = 'Erro em fazer Logoff.'
            print(aviso)

            # Alimentar o log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error(mensagem)
            self.my_logger.log_error(str(aviso))

        return{'status': self.status}