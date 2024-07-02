from modules.mylogger.mylogger import MyLogger
from modules.mysql.mysql import MySQL
from modules.myfolder.myfolder import MyFolder
import os

class EcossistemanfServidor():
        
    def __init__(self, 
                 user, password, host, database, 
                 column_fluxos_id, column_status_id, column_path,
                 table_fluxos, table_status, table_fluxosserver, table_servers,
                 param_true, param_server_fsist):
        # Inicialização de variáveis gerais
        self.status = False
        self.sucesso = f'SUCESSO - {__name__}'
        self.falha = f'FALHA - {__name__}'
        self.erro = f'ERRO - {__name__}'

        # Inicialização das instâncias de logger, MySQL e gerenciamento de pastas
        self.my_logger = MyLogger()
        self.my_sql = MySQL()
        self.my_folder = MyFolder()

        # Configurações de conexão
        self.user = user
        self.password = password
        self.host = host
        self.database = database

        # Configurações de colunas e tabelas
        self.column_path = column_path
        self.column_fluxos_id = column_fluxos_id
        self.column_status_id = column_status_id
        self.table_fluxos = table_fluxos
        self.table_status = table_status
        self.table_fluxosserver = table_fluxosserver
        self.table_servers = table_servers

        # Parâmetros específicos
        self.param_true = param_true
        self.param_server_fsist = param_server_fsist
        
    # Função para verificar se existem arquivos em um caminho específico
    def verficar_arquivos(self):
        try:
            # Configuração das colunas para consulta no banco de dados
            column_path = [self.table_servers, self.column_path]
            column_path_server = [column_path]

            # Configuração dos filtros para consulta
            column_id_fluxos = [self.table_fluxos, self.column_fluxos_id]
            column_id_status = [self.table_status, self.column_status_id]
            column_filter_id = [column_id_fluxos, column_id_status]
            filter_id = [self.param_server_fsist, self.param_true]

            # Execução da consulta no banco de dados
            status_mysql_select = self.my_sql.mysql_select(
                self.user,
                self.password, 
                self.host,
                self.database,
                self.table_fluxosserver,
                column_path_server,
                column_filter_id,
                filter_id,
                True
            )

            if status_mysql_select['status']:
                # Recuperação do resultado da consulta
                resultado = status_mysql_select['resultado']
                path_fsist = resultado[0][0]
                path_pdf = os.path.join(path_fsist, 'PDFs')
                path_xml = os.path.join(path_fsist, 'XMLs') 
                path_list = [path_pdf, path_xml]

                # Verificação de arquivos nas pastas listadas
                for i in path_list:
                    status_folders = self.my_folder.folder('list', 'file', i)
                    if status_folders['status']:
                        if status_folders['resultado'] == []:
                            self.status = True
                            continue
                        else:
                            self.status = False
                            break
                    else:
                        self.status = False
                        break      
            else:
                self.status = False

            # Log do resultado da operação
            if self.status:
                self.my_logger.log_info(self.sucesso)
            else:
                self.my_logger.log_warn(self.falha)
            
        except Exception as aviso:
            self.status = False
            # Log de erro
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error(str(aviso))

        return {'status': self.status}
