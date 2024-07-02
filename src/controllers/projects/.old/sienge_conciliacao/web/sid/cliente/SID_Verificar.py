from modules.mylogger.mylogger import MyLogger
from modules.mysql.mysql import MySQL
from modules.myweb.myweb import MyWeb
from modules.myrequest.myrequest import MyRequest
import time


class SIDVerificar():
        
    def __init__(self, 
                 webdriver,
                 file_folder,
                 js_sid_cliente_anexos_table
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
        self.my_request = MyRequest()

        # Metodo de 'INJEÇÃO DE DEPENDENCIA'
        # ref.: https://www.youtube.com/watch?v=5DBfVnQn1Ow
        self.my_web = MyWeb(webdriver)

        # Variaveis especificas
        self.file_folder = file_folder

        #Scripts
        self.js_sid_cliente_anexos_table = js_sid_cliente_anexos_table
    
    # Função para verificar se existem arquivos com extensão no caminho  
    def sid_verificar(self):

        # Variaveis
        dataAcontecimento = []
        dataOperacao = []
        linkAnexo = []
        observacao = []
        tipoAnexo = []
        usuario = []

        # TryCtach
        try:

            # Encontrar a tabela de anexos
            status_conteudo_anexos = self.my_web.execute_script(self.js_sid_cliente_anexos_table)

            if status_conteudo_anexos['status']:

                # Tabela de anexos
                table_files = status_conteudo_anexos['resultado']
                print('table_files')
                print(table_files)

                # Loop da lista de dicionários
                for table_files_count in table_files:

                    dataAcontecimento.append(table_files_count['dataAcontecimento'])
                    dataOperacao.append(table_files_count['dataOperacao'])
                    linkAnexo.append(table_files_count['linkAnexo'])
                    observacao.append(table_files_count['observacao'])
                    tipoAnexo.append(table_files_count['tipoAnexo'])
                    usuario.append(table_files_count['usuario'])

                    # Exibir os resultados
                    print("dataAcontecimento =", dataAcontecimento)
                    print("dataOperacao =", dataOperacao)
                    print("linkAnexo =", linkAnexo)
                    print("observacao =", observacao)
                    print("tipoAnexo =", tipoAnexo)
                    print("usuario =", usuario)

                # Verificar se o arquivo já foi anexado
                if self.file_folder not in tipoAnexo:
                    self.status = True
                    print(self.sucesso)

                else:
                    self.status = False
                    print(self.falha)

            else:
                self.status = False
                self.mensagem = f'Falha ao fazer o rodar o script {self.js_sid_cliente_anexos_table}.'
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