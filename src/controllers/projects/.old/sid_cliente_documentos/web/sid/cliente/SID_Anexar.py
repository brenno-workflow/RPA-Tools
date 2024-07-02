from modules.mylogger.mylogger import MyLogger
from modules.mysql.mysql import MySQL
from modules.myweb.myweb import MyWeb
import os
import time
import datetime

class SIDAnexar():
        
    def __init__(self, 
                 webdriver,
                 file_name, file_folder, file_path, 
                 input_conteudo_anexos, button_anexos, button_anexar_documento, button_escolher_arquivo, input_data_acontecimento, input_observacao, button_tipo_anexo, button_selecionar_tipo, button_inserir
                 ):

        # Variaveis gerais
        self.status = False
        self.sucesso = f'SUCESSO - {__name__}'
        self.falha = f'FALHA - {__name__}'
        self.erro = f'ERRO - {__name__}'
        self.mensagem = None

        # Instancias
        # Instanciar é uma boa prática e necessário
        # Não instaciar resulta na abertura de processo diferentes e erros
        self.my_logger = MyLogger()
        self.my_sql = MySQL()

        # Metodo de 'INJEÇÃO DE DEPENDENCIA'
        # ref.: https://www.youtube.com/watch?v=5DBfVnQn1Ow
        self.my_web = MyWeb(webdriver)

        # Variaveis especificas
        self.file_name = file_name
        self.file_folder = file_folder
        self.file_path = file_path
        self.dt_atual = datetime.datetime.now().strftime('%d-%m-%Y')

        # --- WEB ---

        # ID
        self.input_conteudo_anexo = input_conteudo_anexos
        self.button_escolher_arquivo = button_escolher_arquivo
        self.button_tipo_anexo = button_tipo_anexo
        self.button_selecionar_tipo = button_selecionar_tipo
        self.button_inserir = button_inserir
        self.input_dt_acontecimento = input_data_acontecimento
        self.input_observacao = input_observacao
        
        # XPATH
        self.button_anexos = button_anexos
        self.button_anexar_documento = button_anexar_documento
    
    # Função para verificar se existem arquivos com extensão no caminho  
    def sid_anexar(self):

        # TryCtach
        try:

            # Abrir anexos
            status_button_anexos = self.my_web.element(self.button_anexos, 'xpath', 'click')

            if status_button_anexos['status']:

                status_button_anexar_documento = self.my_web.element(self.button_anexar_documento, 'xpath', 'click')

                if status_button_anexar_documento['status']:

                    print('self.button_escolher_arquivo')
                    print(self.button_escolher_arquivo)
                    print('self.file_path')
                    print(self.file_path)

                    time.sleep(5)

                    # Criar caminho do arquivo
                    file_path = os.path.join(self.file_path, self.file_name)

                    status_escolher_arquivo = self.my_web.element(self.button_escolher_arquivo, 'id', 'find', 'send_keys', file_path)
                    time.sleep(1)

                    if status_escolher_arquivo['status']:

                        status_dt_acontecimento = self.my_web.element(self.input_dt_acontecimento, 'id', 'click', 'send_keys', self.dt_atual)
                        time.sleep(1)                        

                        if status_dt_acontecimento['status']:

                            status_tipo_anexo = self.my_web.element(self.button_tipo_anexo, 'id', 'dropdown', 'text', self.file_folder)
                            time.sleep(1)

                            if status_tipo_anexo['status']:

                                status_selecionar_tipo = self.my_web.element(self.button_selecionar_tipo, 'id', 'click')
                                time.sleep(1)

                                if status_selecionar_tipo['status']:

                                    status_inserir = self.my_web.element(self.button_inserir, 'id', 'click')
                                    time.sleep(1)

                                    if status_inserir['status']:

                                        time.sleep(5)

                                        self.status = True
                                        print(self.sucesso)

                                    else:
                                        self.status = False
                                        self.mensagem = 'Falha ao clicar no botão "Inserir".'
                                        print(self.mensagem)

                                else:
                                    self.status = False
                                    self.mensagem = 'Falha ao clicar no botão "Selecionar Tipo".'
                                    print(self.mensagem)

                            else:
                                self.status = False
                                self.mensagem = 'Falha ao inserir o tipo de anexo no botão "Tipo Anexo".'
                                print(self.mensagem)

                        else:
                            self.status = False
                            self.mensagem = 'Falha ao escrever a data atual no campo "Data Acontecimento".'
                            print(self.mensagem)

                    else:
                        self.status = False
                        self.mensagem = 'Falha ao inserir o arquivo no botão "Escolher Arquivo".'
                        print(self.mensagem)

                else:
                    self.status = False
                    self.mensagem = 'Falha ao fazer o click no botão de "Anexar Documentos".'
                    print(self.mensagem)

            else:
                self.status = False
                self.mensagem = 'Falha ao fazer o click no menu de "Anexos".'
                print(self.mensagem)

            # Alimentar o log
            if self.status:
                self.my_logger.log_info(self.sucesso)

            else:
                self.my_logger.log_warn(self.falha)
                self.my_logger.log_warn(self.mensagem)

        except Exception as aviso:
            self.status = False
            print(self.erro)
            print(aviso)

            # Alimentar o log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error(str(aviso))

        return{'status': self.status}