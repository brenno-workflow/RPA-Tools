from modules.mylogger.mylogger import MyLogger
from modules.mysql.mysql import MySQL
from modules.myfolder.myfolder import MyFolder
import os

class ControlFolder():
        
    def __init__(self, 
                 user, password, host, database,
                 column_control_path, column_control_path_temp,
                 id_control, id_control_temp,
                 table_control, table_control_temp,
                 param_control,
                 folder_control
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

        # Variaveis especificas
        self.user = user
        self.password = password
        self.host = host
        self.database = database

        # Pastas
        self.folder = folder_control

        # Colunas
        self.column_control_path = column_control_path
        self.column_control_path_temp = column_control_path_temp

        # ID
        self.id_control = id_control
        self.id_control_temp = id_control_temp
                
        # Tabela 
        self.table_control = table_control
        self.table_control_temp = table_control_temp 

        # Parametros
        self.param_control = param_control
    
    # Função para verificar se existem arquivos com extensão no caminho  
    def control_folder(self):

        # TryCtach
        try:

            # Obtem o diretorio do projeto
            dir_path = os.path.dirname(os.path.realpath(__name__))

            # Cria o caminho para a pasta de controle
            folder_path = os.path.join(dir_path, self.folder)

            status_my_folder = self.my_folder.folder('make', 'folder', folder_path)

            # Limpar tabela temporaria
            if status_my_folder['status']:

                status_mysql_truncate = self.my_sql.mysql_truncate(
                    self.user,
                    self.password,
                    self.host,
                    self.database,
                    self.table_control_temp                    
                )

                # Zerar a tabela temporaria
                if status_mysql_truncate['status']:

                    status_mysql_insert = self.my_sql.mysql_insert(
                        self.user,
                        self.password,
                        self.host,
                        self.database,
                        self.table_control_temp,
                        self.column_control_path_temp,
                        folder_path
                    )

                    if status_mysql_insert['status']:

                        # Atualizar tabela dimensão
                        status_mysql_update = self.my_sql.mysql_update(
                            self.user,
                            self.password,
                            self.host,
                            self.database,
                            self.table_control,
                            self.column_control_path,
                            self.id_control,
                            self.param_control
                        )

                        if status_mysql_update['status']:
                            self.status = True
                            mensagem = f'Sucesso ao criar a pasta: {self.folder} no caminho: {folder_path}'
                            print(mensagem)

                        else:
                            self.status = False
                            mensagem = f'Falha ao fazer o UPDATE da tabela: {self.table_control}'
                            print(mensagem)

                    else:
                        self.status = False
                        mensagem = f'Falha ao fazer o INSERT da tabela: {self.table_control_temp}'
                        print(mensagem)

                else:
                    self.status = False
                    mensagem = f'Falha ao fazer o TRUNCATE da tabela: {self.table_control_temp}'
                    print(mensagem)

            else:
                self.status = False
                mensagem = f'Falha ao criar a pasta: {self.folder} no caminho: {folder_path}'
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
            mensagem = f'Erro ao criar a pasta: {self.folder} no caminho: {folder_path}'
            print(self.erro)
            print(mensagem)
            print(aviso)

            # Alimentar o log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error(mensagem)
            self.my_logger.log_error(str(aviso))

        return{'status': self.status, 'resultado': folder_path}