from modules.mylogger.mylogger import MyLogger
from modules.mysql.mysql import MySQL
from modules.myweb.myweb import MyWeb
from selenium.webdriver.common.keys import Keys
import time

class SIDPesquisar():
        
    def __init__(self, 
                 webdriver, 
                 file_name, 
                 input_pesquisar, button_gerir , button_buscar
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

        # Parametros
        self.file_name = file_name

        # WEB
        # Class
        self.input_search = input_pesquisar
        # Xpath
        self.button_gerir = button_gerir
        self.button_buscar = button_buscar
    
    # Função para verificar se existem arquivos com extensão no caminho  
    def sid_pesquisar(self):

        # TryCtach
        try:

            # Retirar a extensão do arquivo
            self.file_name = str(self.file_name)
            #file_name = self.file_name.split('.')[0]

            # Retirar a extensão do nome do arquivo
            position = self.file_name.rfind('.')
            result = self.file_name[:position]
            file_name = result

            # Clicar na barra de pesquisa
            status_search_bar = self.my_web.element(self.input_search, 'id', 'CLICK', 'send_keys', file_name)

            if status_search_bar['status']:

                # Digitar enter
                status_key_enter = self.my_web.element(self.button_buscar, 'xpath', 'click')

                if status_key_enter['status']:

                    time.sleep(1)

                    # Clickar no link do perfil
                    status_button_gerir = self.my_web.element(self.button_gerir, 'xpath', 'click')

                    if status_button_gerir['status']:

                        time.sleep(5)

                        self.status = True
                        print(self.sucesso)

                    else:
                        self.status = False
                        print(self.falha)

                else:
                    self.status = False
                    print(self.falha)

            else:
                self.status = False
                print(self.falha)

            # Alimentar o log
            if self.status:
                self.my_logger.log_info(self.sucesso)

            else:
                self.my_logger.log_warn(self.falha)

        except Exception as aviso:
            self.status = False
            print(self.erro)
            print(aviso)

            # Alimentar o log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error(str(aviso))

        return{'status': self.status}