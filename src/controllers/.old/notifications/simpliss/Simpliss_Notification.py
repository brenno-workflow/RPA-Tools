from modules.mylogger.mylogger import MyLogger
from modules.mysql.mysql import MySQL
from modules.myweb.myweb import MyWeb
from selenium.webdriver.common.keys import Keys
import time

class SimplissNotification():
        
    def __init__(self, 
                 webdriver,
                 input_banner, input_banner_close
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
        
        # Inputs
        self.input_banner = input_banner
        self.input_banner_close = input_banner_close
    
    # Função para verificar se existem arquivos com extensão no caminho  
    def banner(self):

        # TryCtach
        try:
                
            # Abrir site do SID
            status_banner = self.my_web.element(
                self.input_banner, 'id', 'find')

            if status_banner['status']:

                status_click_close = self.my_web.element(
                    self.input_banner_close, 'xpath', 'click')

                if status_click_close['status']:

                    time.sleep(5)

                    status_banner = self.my_web.element(
                        self.input_banner, 'id', 'find')

                    if status_banner['status'] == False:
                        self.status = True
                        mensagem = 'Sucesso em fechar as notificações.'
                        print(mensagem)
                            
                    else:
                        self.status = False
                        mensagem = 'Falha - Banner de notificações não foi fechado.'
                        print(mensagem)

                else:
                    self.status = False
                    mensagem = 'Falha em fechar as notificações.'
                    print(mensagem)

            else:
                self.status = True
                mensagem = 'Não existia um banner de notificações.'
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
            mensagem = 'Erro em fechar as notificações.'
            print(mensagem)
            print(aviso)

            # Alimentar o log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error(mensagem)
            self.my_logger.log_error(str(aviso))

        return{'status': self.status}