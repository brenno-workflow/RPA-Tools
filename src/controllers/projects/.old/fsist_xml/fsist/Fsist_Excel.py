from modules.mylogger.mylogger import MyLogger
from modules.mysql.mysql import MySQL
from modules.mypandas.mypandas import MyPandas
import os
class FsistExcel:
        
    def __init__(self, 
                 user, password, host, database,
                 column_fluxos_id, column_status_id,
                 column_control_id, column_control_path,
                 table_fluxos, table_status, table_fluxoscontrol, table_control,
                 param_control, param_true,
                 folder_download,
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
        self.my_pandas = MyPandas()
        
        # Metodo de 'INJEÇÃO DE DEPENDENCIA'
        # ref.: https://www.youtube.com/watch?v=5DBfVnQn1Ow

        # Variaveis especificas
        self.user = user
        self.password = password
        self.host = host
        self.database = database

        # ID
        self.column_fluxos_id = column_fluxos_id
        self.column_status_id = column_status_id

        # Parametros        
        self.param_control = param_control
        self.param_true = param_true

        # Tabelas
        self.table_fluxos = table_fluxos
        self.table_status = table_status
        self.table_fluxoscontrol = table_fluxoscontrol
        self.table_control = table_control

        # Colunas
        self.column_control_id = column_control_id
        self.column_control_path = column_control_path        

        # Pastas
        self.folder = folder_download


    # Ciencia
    def excel(self, condition, subcondition):

        
        # Try Catch
        try:

            column_id = [self.table_control, self.column_control_path]
            column_control_id = [column_id]

            # Lista de filtros
            column_id_fluxos = [self.table_fluxos, self.column_fluxos_id]
            column_id_status = [self.table_status, self.column_status_id]
            column_filter_id = [column_id_fluxos, column_id_status]


            # Lista de colunas_filtro
            filter_id = [self.param_control, self.param_true]

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

                id_control = resultado[0][0]
                print(id_control)
                id_control = os.path.join(id_control, self.folder)
                for arquivo in os.listdir(id_control):
                    if arquivo.endswith(".xlsx"):
                        caminho_arquivo_xlsx = os.path.join(id_control, arquivo)
                        print(caminho_arquivo_xlsx)
                        break  # Para assim que encontrar o primeiro arquivo .xlsx

                status_planilha = self.my_pandas.table(caminho_arquivo_xlsx, 'excel', 'filter', 'index', condition, subcondition)
                if status_planilha['status']:
                    self.resultado = status_planilha['resultado']
                    self.my_logger.log_info(self.resultado)
                    self.status = True

                else:
                    self.status = False

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

        return{'status': self.status, 'resultado': self.resultado}