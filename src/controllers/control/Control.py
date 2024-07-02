from modules.mylogger.mylogger import MyLogger
from modules.mysql.mysql import MySQL
from modules.myfolder.myfolder import MyFolder
import os

class Control():
        
    def __init__(self, 
                 user, password, host, database,
                 column_fluxos_id, column_status_id,
                 column_control_id, column_control_path,
                 table_fluxos, table_status, table_fluxoscontrol, table_control,
                 param_control, param_true,
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
        self.folder = folder_control
    
    # Função para verificar se existem arquivos com extensão no caminho  
    def control(self):

        # TryCtach
        try:

            # Lista de colunas site e credenciais
            column_id = [self.table_control, self.column_control_id]
            column_control_id = [column_id]

            # Lista de filtros
            column_id_fluxos = [self.table_fluxos, self.column_fluxos_id]
            column_id_status = [self.table_status, self.column_status_id]
            column_filter_id = [column_id_fluxos, column_id_status]

            # Lista de colunas_filtro
            filter_id = [self.param_control, self.param_true]

            # Fazer select para ID do control
            status_mysql_select = self.my_sql.mysql_select(
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

            if status_mysql_select['status']:

                # ID para atualizar a db_control
                resultado = status_mysql_select['resultado']
                print(resultado)

                id_control = resultado[0][0]

                # Obtem o diretorio do projeto
                dir_path = os.path.dirname(os.path.realpath(__name__))

                # Cria o caminho para a pasta de controle
                folder_path = os.path.join(dir_path, self.folder)

                status_my_folder = self.my_folder.folder('make', None, folder_path)

                # Limpar tabela temporaria
                if status_my_folder['status']:

                    # Atualizar tabela dimensão
                    status_mysql_update = self.my_sql.mysql_update(
                        self.user,
                        self.password,
                        self.host,
                        self.database,
                        self.table_control,
                        self.column_control_path,
                        self.column_control_id,
                        id_control,
                        folder_path
                    )

                    if status_mysql_update['status']:
                        self.status = True
                        mensagem = f'Sucesso ao criar a pasta: "{self.folder}" no path: "{folder_path}"'
                        print(mensagem)

                    else:
                        self.status = False
                        mensagem = f'Falha ao fazer o UPDATE do path: "{folder_path}" na tabela: "{self.table_control}"'
                        print(mensagem)

                else:
                    self.status = False
                    mensagem = f'Falha ao criar a pasta: "{self.folder}" no path: "{folder_path}"'
                    print(mensagem)

            else:
                self.status = False
                mensagem = f'Falha ao fazer o SELECT da tabela: "{self.table_fluxoscontrol}"'
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
            mensagem = f'Erro ao criar a pasta: "{self.folder}" no path: "{folder_path}"'
            print(self.erro)
            print(mensagem)
            print(aviso)

            # Alimentar o log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error(mensagem)
            self.my_logger.log_error(str(aviso))

        return{'status': self.status}