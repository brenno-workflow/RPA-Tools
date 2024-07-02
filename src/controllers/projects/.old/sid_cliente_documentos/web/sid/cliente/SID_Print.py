from modules.mylogger.mylogger import MyLogger
from modules.mysql.mysql import MySQL
from modules.myweb.myweb import MyWeb
from modules.myprint.myprint import MyPrint
import os
import re

class SIDPrint():
        
    def __init__(self, 
                 webdriver, user, password, host, database, 
                 file_name, file_folder,
                 extension_png
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
        self.my_print = MyPrint()

        # Variaveis especificas
        self.user = user
        self.password = password
        self.host = host
        self.database = database

        # Variaveis
        self.file_name = file_name
        self.file_folder = file_folder

        # Extensões
        self.extension_png = extension_png    
    
    # Função para verificar se existem arquivos com extensão no caminho  
    def print(self, path):

        """
        Ira realizar um print da pagina da web.

        Args:
            path (str): O caminho que ira salvar o arquivo.
        """
                
        # TryCtach
        try:

            # Nome do arquivo
            print_name = self.file_folder + " - " + self.file_name + self.extension_png
            self.my_logger.log_info('print_name')
            self.my_logger.log_info(print_name)

            # Retirar caracters uft-8
            print_name_ok = re.sub(r'[^\x20-\x7E]', '', print_name)
            self.my_logger.log_info('print_name_ok')
            self.my_logger.log_info(print_name_ok)

            # Caminho completo
            print_path = os.path.join(path, print_name_ok)

            status_myweb_print = self.my_web.browser('print', 'save', print_path)

            if status_myweb_print['status']:
                self.status = True
                mensagem = f'Sucesso ao realizar o PRINT e salvar no path: {path}'
                print(mensagem)

            else:

                # Tirar print da tela inteira
                status_myprint_print = self.my_print.print_screen(print_path)

                if status_myprint_print['status']:
                    self.status = True
                    mensagem = f'Sucesso ao realizar o PRINT SCREEN e salvar no path: {path}'
                    print(mensagem)

                else:
                    self.status = False
                    mensagem = f'Falha ao realizar o PRINT SCREEN e salvar no path: {path}'
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
            print(self.erro)
            mensagem = f'Erro ao fazer o PRINT do arquivo: {self.file_name}'
            print(aviso)

            # Alimentar o log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error(mensagem)
            self.my_logger.log_error(str(aviso))

        return{'status': self.status}

