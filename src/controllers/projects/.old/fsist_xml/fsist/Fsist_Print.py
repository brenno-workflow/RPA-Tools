from modules.mylogger.mylogger import MyLogger
from modules.mysql.mysql import MySQL
from modules.myweb.myweb import MyWeb
from datetime import datetime
import os

class FsistPrint:
        
    def __init__(self,
                 my_driver, 
                 user, password, host, database, 
                 table_control, table_fluxos, table_status, table_fluxoscontrol,
                 column_control_path, column_status_id, column_fluxos_id,
                 param_true, 
                 extension_png
                 ):

        # Variaveis gerais
        self.status = False
        self.sucesso = f'SUCESSO - {__name__}'
        self.falha = f'FALHA - {__name__}'
        self.erro = f'ERRO - {__name__}'

        # Instancias
        # Instanciar é uma boa prática e necessário
        # Não instanciar resulta na abertura de processo diferentes e erros
        self.my_logger = MyLogger()
        self.my_sql = MySQL()

        # Metodo de 'INJEÇÃO DE DEPENDENCIA'
        # ref.: https://www.youtube.com/watch?v=5DBfVnQn1Ow
        self.my_web = MyWeb(my_driver)

        # Variaveis especificas
        self.user = user
        self.password =  password
        self.host = host
        self.database = database
        
        # Colunas
        self.column_fluxos_id = column_fluxos_id
        self.column_status_id = column_status_id
        self.column_control_path = column_control_path

        # Tabela SELECT
        self.table_control = table_control
        self.table_fluxos = table_fluxos
        self.table_status = table_status
        self.table_fluxoscontrol = table_fluxoscontrol

        # Parametros
        self.param_true = param_true
        self.extension_png = extension_png

    # Configurar caminho de download do fsist
    def fsist_print(self, condition, subcondition = None):
        try:
            # Colunas de controle para a query
            column_id = [self.table_control, self.column_control_path]
            column_control_id = [column_id]

            # Lista de filtros
            column_id_fluxos = [self.table_fluxos, self.column_fluxos_id]
            column_id_status = [self.table_status, self.column_status_id]
            column_filter_id = [column_id_fluxos, column_id_status]

            # Lista de colunas e filtros
            filter_id = [condition, self.param_true]

            # SELECT - Controle
            status_mysql_controle = self.my_sql.mysql_select(
                self.user,
                self.password,
                self.host,
                self.database,
                self.table_fluxoscontrol,
                column_control_id,
                column_filter_id,
                filter_id,
                True
            )
            
            if status_mysql_controle['status']:
                resultado = status_mysql_controle['resultado']
                print(resultado)

                # Pasta de controle
                control_folder = resultado[0][0]

                # Nome do arquivo
                if subcondition is None:
                    nome_arquivo = datetime.now().strftime('%d_%m_%Hh%M')
                else:
                    nome_arquivo = subcondition    
                
                # Caminho completo do arquivo
                name_file = os.path.join(control_folder, (nome_arquivo + self.extension_png))
                
                # Capturar print da página
                status_print_web = self.my_web.browser('print', 'download', name_file)

                if status_print_web['status']:
                    self.status = True
                    print(self.sucesso)
                else:
                    self.status = False
                    print(self.falha)

            else:
                self.status = False
                print("Falha ao realizar consulta no banco de dados")

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

        return {'status': self.status}
