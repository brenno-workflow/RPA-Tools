from modules.mylogger.mylogger import MyLogger
from modules.mysql.mysql import MySQL
from modules.myfolder.myfolder import MyFolder
import os
import time

class EcossistemanfUnzip():
        
    def __init__(self, 
                 user, password, host, database, 
                 column_fluxos_id, column_status_id, column_server_id, column_server_path, column_control_path,
                 table_fluxos, table_status, table_fluxosserver, table_servers, table_control, table_fluxoscontrol,
                 param_server_ecossistema, param_control_download, param_true ):

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
        self.my_folder = MyFolder()

        # Variaveis especificas
        self.user = user
        self.password =  password
        self.host = host
        self.database = database

        # ID
        self.column_fluxos_id = column_fluxos_id
        self.column_status_id = column_status_id

        # Parametros        
        self.param_server_ecossistema = param_server_ecossistema
        self.param_control = param_control_download
        self.param_true = param_true

        # Tabelas
        self.table_fluxos = table_fluxos
        self.table_status = table_status
        self.table_fluxosserver = table_fluxosserver
        self.table_servers = table_servers
        self.table_control = table_control
        self.table_fluxoscontrol = table_fluxoscontrol
        # Colunas
        self.column_server_id = column_server_id
        self.column_server_path = column_server_path  
        self.column_control_path = column_control_path

    # Função para verificar se existem arquivos com extensão no caminho  
    def ecossistemanf_unzip(self):
        # TryCtach
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
                
                # Pegar resultados
                path_controle_download = status_mysql_controle['resultado'][0][0]
                print('path_download')
                print(path_controle_download)

                column_id = [self.table_servers, self.column_server_path]
                column_server_id = [column_id]

                # Lista de filtros
                column_id_fluxos = [self.table_fluxos, self.column_fluxos_id]
                column_id_status = [self.table_status, self.column_status_id]
                column_filter_id = [column_id_fluxos, column_id_status]


                # Lista de colunas_filtro
                filter_id = [self.param_server_ecossistema, self.param_true]

                # SELECT - Controle
                status_mysql_controle = self.my_sql.mysql_select(
                    self.user,
                    self.password,
                    self.host,
                    self.database,
                    self.table_fluxosserver,
                    column_server_id,
                    column_filter_id,
                    filter_id,
                    True
                    )
            
            else:
                self.status = False
                print(self.falha)
                self.my_logger.log_warn('Erro na hora de realizar a busca no banco de dados.')

            if status_mysql_controle['status']:

                # Atualizar variaveis
                path_servidor = status_mysql_controle['resultado'][0][0]
                print(path_servidor)
                status_list_download = self.my_folder.folder('list', 'file', path_controle_download)

                if status_list_download['status']:
                    lista_arquivos = status_list_download['resultado']
                    for arquivo in lista_arquivos:
                        if arquivo.endswith(".zip"):
                            caminho_arquivo_zip = os.path.join(path_controle_download, arquivo)
                            print(caminho_arquivo_zip)
                            break  # Para assim que encontrar o primeiro arquivo .xlsx
                        else:
                            continue
                else:
                    self.status = False
                    print(self.falha)
                    self.my_logger.log_warn('Erro na hora de retornar a lista das pastas.')

                status_unzip_folder = self.my_folder.folder('unzip', None, caminho_arquivo_zip, path_servidor)
                time.sleep(2)
                if status_unzip_folder['status']:
                    self.status = True
                    print(self.sucesso)
                    self.my_logger.log_info('Sucesso na hora de realizar a descompactação do arquivo zip.')

                else:
                    self.status = False
                    print(self.falha)
                    self.my_logger.log_warn('Erro na hora de realizar a descompactação do arquivo zip.')

            else:
                self.status = False
                print(self.falha)
                self.my_logger.log_warn('Erro na hora de realizar a busca no banco de dados.')

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