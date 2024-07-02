from modules.mylogger.mylogger import MyLogger
from modules.mysql.mysql import MySQL
from modules.myprint.myprint import MyPrint
import datetime

class PrintScreen():
        
    def __init__(self, 
                 user, password, host, database,
                 column_fluxos_id, column_status_id, 
                 column_control_path,
                 table_status, table_fluxos, table_control, table_fluxoscontrol,
                 param_true, param_control_folder,
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
        self.my_print = MyPrint()

        # Variaveis especificas
        self.user = user
        self.password = password
        self.host = host
        self.database = database

        # Extensões
        self.extension_png = extension_png

        # Colunas
        self.column_control_path = column_control_path
        
        # ID
        self.column_fluxos_id = column_fluxos_id
        self.column_status_id = column_status_id
                
        # Tabela 
        self.table_fluxos = table_fluxos
        self.table_status = table_status
        self.table_control = table_control
        self.table_fluxoscontrol = table_fluxoscontrol

        # Parametros
        self.param_true = param_true
        self.param_control_folder = param_control_folder
    
    # Função para verificar se existem arquivos com extensão no caminho  
    def print_screen(self):

        # Variaveis
        file_name = datetime.datetime.now()

        # TryCtach
        try:

            # Buscar as pastas de controle
            # Coluna Path
            column_path = [[self.table_control, self.column_control_path]]

            # Lista de colunas filtros
            column_id_fluxos = [self.table_fluxos, self.column_fluxos_id]
            column_id_status = [self.table_status, self.column_status_id]
            column_filter_id_fluxos = [column_id_fluxos, column_id_status]

            # Filtros
            filter_id_fluxos = [self.param_control_folder, self.param_true]
            
            # Buscar informações do banco de dados
            status_select_sucesso = self.my_sql.mysql_select(
                self.user,
                self.password, 
                self.host,
                self.database,
                self.table_fluxoscontrol,
                column_path,
                column_filter_id_fluxos,
                filter_id_fluxos,
                True
                )

            if status_select_sucesso['status']:

                # Retorna a lista de resultados
                resultado = status_select_sucesso['resultado']
                print(resultado)

                path_control = resultado[0][0]

                status_print_screen = self.my_print.print_screen(path_control, file_name, self.extension_png)

                if status_print_screen['status']:
                    self.status = True
                    mensagem = 'Sucesso ao tirar o PRINT da tela de ERRO geral'
                    print(mensagem)

                else:
                    self.status = False
                    mensagem = 'Falha ao tirar o PRINT da tela de ERRO geral'
                    print(mensagem)

            else:
                self.status = False
                mensagem = f'Falha ao fazer o select da tabela: "{self.table_fluxoscontrol}"'
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
            mensagem = f'Erro ao tirar o PRINT da tela de ERRO geral.'
            print(self.erro)
            print(mensagem)
            print(aviso)

            # Alimentar o log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error(mensagem)
            self.my_logger.log_error(str(aviso))

        return{'status': self.status}