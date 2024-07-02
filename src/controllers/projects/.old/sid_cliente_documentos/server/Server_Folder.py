import os
from modules.mylogger.mylogger import MyLogger
from modules.mysql.mysql import MySQL
from modules.myfolder.myfolder import MyFolder

class ServerFolder():
        
    def __init__(self,
                 user, password, host, database, 
                 column_fluxos_id, column_status_id,
                 column_path, column_anexo, column_file_temp, column_folder_temp, column_path_temp, column_path_temp_old,
                 table_fluxos, table_status, table_fluxosserver, table_servers, table_sid_cliente_anexos, table_sid_cliente_anexos_temp,
                 param_true, param_server_sid_cliente,
                 folder_server_old
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
        self.my_folder = MyFolder()

        # Metodo de 'INJEÇÃO DE DEPENDENCIA'
        # ref.: https://www.youtube.com/watch?v=5DBfVnQn1Ow

        # Variaveis especificas

        # Connection
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.folder_old = folder_server_old

        # Colunas
        self.column_path = column_path
        self.column_anexo = column_anexo
        self.column_file_temp = column_file_temp
        self.column_folder_temp = column_folder_temp
        self.column_path_temp = column_path_temp
        self.column_path_temp_old = column_path_temp_old

        # ID
        self.column_fluxos_id = column_fluxos_id
        self.column_status_id = column_status_id
        
        # Tabela SELECT
        self.table_fluxos = table_fluxos
        self.table_status = table_status
        self.table_fluxosserver = table_fluxosserver
        self.table_servers = table_servers
        self.table_sid_cliente_anexos = table_sid_cliente_anexos
        self.table_sid_cliente_anexos_temp = table_sid_cliente_anexos_temp
        
        # Parametros
        self.param_true = param_true
        self.param_server_sid_cliente = param_server_sid_cliente

    # Função para listar os anexos 
    def sid_cliente_anexos(self):

        # TryCtach
        try:

            # Coluna Anexos
            column_sid_cliente_anexo = self.column_anexo
            
            # Buscar informações do banco de dados
            status_mysql_select = self.my_sql.mysql_select(
                self.user,
                self.password, 
                self.host,
                self.database,
                self.table_sid_cliente_anexos,
                column_sid_cliente_anexo
                )

            if status_mysql_select['status']:

                # Retorna a lista de resultados
                resultado = status_mysql_select['resultado']

                # Lista de anexos
                anexo_list = resultado[0]

                self.status = True
                print(self.sucesso)
                print(f'Lista de anexos da tabela: {self.table_sid_cliente_anexos}')
                print(f'{anexo_list}')

            else:
                self.status = False
                print(self.falha)
                print(f'Falha ao buscar a lista da tabela: {self.table_sid_cliente_anexos}')

            # Alimentar o log
            if self.status:
                self.my_logger.log_info(self.sucesso)
                self.my_logger.log_info(f'Lista de anexos da tabela: {self.table_sid_cliente_anexos}')
                self.my_logger.log_info(f'{anexo_list}')

            else:
                self.my_logger.log_warn(self.falha)
                self.my_logger.log_warn(f'Falha ao buscar a lista de anexos da tabela: {self.table_sid_cliente_anexos}')

        except Exception as aviso:
            self.status = False
            print(self.erro)
            print(aviso)

            # Alimentar o log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error(str(aviso))

        return{'status': self.status, 'resultado':anexo_list}
    
    # Função para listar as pastas
    def server_sid_cliente_folders(self):

        # TryCtach
        try:

            # Lista de colunas site e credenciais
            column_path = [self.table_servers, self.column_path]
            column_path_server = [column_path]

            # Lista de filtros
            column_id_fluxos = [self.table_fluxos, self.column_fluxos_id]
            column_id_status = [self.table_status, self.column_status_id]
            column_filter_id = [column_id_fluxos, column_id_status]

            # Lista de colunas_filtro
            filter_id = [self.param_server_sid_cliente, self.param_true]
            
            # Buscar informações do banco de dados
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

                # Retorna a lista de resultados
                resultado = status_mysql_select['resultado']

                path_sid_cliente = resultado[0][0]
                print('path_sid_cliente')
                print(path_sid_cliente)
                
                # Abrir site do SID
                status_folders = self.my_folder.folder('list', 'folder', path_sid_cliente)

                if status_folders['status']:

                    # Lista de pastas/arquivos
                    folder_list = status_folders['resultado']
                    print('folder_list')
                    print(folder_list)

                    self.status = True
                    print(self.sucesso)

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

        return{'status': self.status, 'resultado': folder_list, 'path': path_sid_cliente}
    
    # Função para verificar se existem arquivos nas pastas
    def server_sid_cliente_files(self):

        # Variaveis
        status_list = False

        # TryCtach
        try:

            # Lista de anexos
            status_anexos_list = self.sid_cliente_anexos()

            if status_anexos_list['status']:

                # Lista de anexos
                anexos_list = status_anexos_list['resultado']
                

                # Lista de pastas
                status_folders_list = self.server_sid_cliente_folders()

                if status_folders_list['status']:

                    # Listas de pastas
                    folder_list = status_folders_list['resultado']

                    # Caminho das pastas
                    path_sid_cliente = status_folders_list['path']

                    # Status list
                    status_list = True

            if status_list:

                status_mysql_truncate = self.my_sql.mysql_truncate(
                    self.user,
                    self.password,
                    self.host,
                    self.database,
                    self.table_sid_cliente_anexos_temp
                )

                if status_mysql_truncate['status']:
            
                    for folder_list_count in folder_list:

                        if folder_list_count in anexos_list:

                            # Caminho da pasta
                            path_folder = os.path.join(path_sid_cliente, folder_list_count)
                            print('path_folder')
                            print(path_folder)

                            # Buscar arquivos na pasta
                            status_myfolder_file_list = self.my_folder.folder('list', 'file', path_folder)

                            if status_myfolder_file_list['status']:

                                # Lista de arquivos dentro da pasta
                                file_list = status_myfolder_file_list['resultado']
                                print('file_list')
                                print(file_list)

                                if len(file_list) > 0:

                                    for file_list_count in file_list:
                                        
                                        # Path folder old
                                        path_folder_old = os.path.join(path_folder, self.folder_old)
                                        print('path_folder_old')
                                        print(path_folder_old)

                                        # Colunas
                                        column_insert_list = [self.column_file_temp, self.column_folder_temp, self.column_path_temp, self.column_path_temp_old]
                                        print('column_insert_list')
                                        print(column_insert_list)

                                        # Valores
                                        value_insert_list = [file_list_count, folder_list_count, path_folder, path_folder_old]
                                        print('value_insert_list')
                                        print(value_insert_list)                                        

                                        # Inserir na tabela temp
                                        status_mysql_insert = self.my_sql.mysql_insert(
                                            self.user,
                                            self.password,
                                            self.host,
                                            self.database,
                                            self.table_sid_cliente_anexos_temp,
                                            column_insert_list,
                                            value_insert_list
                                        )

                                        if status_mysql_insert['status']:
                                            self.status = True
                                            print(self.sucesso)

                                        else:
                                            self.status = False
                                            print(self.falha)

                                else:
                                    self.status = True
                                    print(self.sucesso)

                            else:
                                self.status = False
                                print(self.falha)
                            
                        else:
                            self.status = True
                            print(self.sucesso)

                else:
                    self.status = False
                    print(self.falha)
                    print(f'Falha ao realizar o truncate na tabela: {self.table_sid_cliente_anexos_temp}.')
            
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

        return{'status': self.status, 'resultado': folder_list}