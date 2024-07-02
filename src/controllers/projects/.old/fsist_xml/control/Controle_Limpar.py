from modules.mylogger.mylogger import MyLogger
from modules.mysql.mysql import MySQL
from modules.myfolder.myfolder import MyFolder

class ControleLimpar:
        
    def __init__(self, 
                 user, password, host, database, 
                 column_fluxos_id, column_status_id,
                 column_control_id, column_control_path,
                 table_fluxos, table_status, table_fluxoscontrol, table_control,
                 param_control, param_true,

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
        self.user = user
        self.password =  password
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

    # Configurar caminho de donwload do fsist
    def limpar_download(self):
        
        # TryCath
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
                path = status_mysql_controle['resultado'][0][0]
                print('path_download')
                print(path)
                

                # Limpar arquivos da pasta de download
                status_limpar_pasta = self.my_folder.folder('remove', 'file', path)

                if status_limpar_pasta['status']:
                    self.status = True
                    print(self.sucesso)
                
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

        return{'status': self.status}
    
    # Configurar caminho de sucesso do fsist
    def limpar_sucesso(self):

        # Variaveis
        filtro_coluna = [self.coluna_module, self.coluna_type, self.coluna_name]
        filtro = [self.module, self.type, self.name_sucesso]
        
        # TryCath
        try:

            # SELECT - Controle
            status_mysql_controle = self.my_sql.mysql_select(
                self.user, 
                self.host,
                self.database,
                self.coluna_path, 
                self.tabela_controle, 
                filtro_coluna, filtro
                )

            if status_mysql_controle['status']:
                
                # Pegar resultados
                path = status_mysql_controle['resultado'][0]
                print('path_sucesso')
                print(path)

                # Limpar arquivos da pasta de download
                status_limpar_pasta = self.my_folder.limpar_pasta(path)

                if status_limpar_pasta['status']:
                    self.status = True
                    print(self.sucesso)
                
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

        return{'status': self.status}
    
    # Configurar caminho de falha do fsist
    def limpar_falha(self):

        # Variaveis
        filtro_coluna = [self.coluna_module, self.coluna_type, self.coluna_name]
        filtro = [self.module, self.type, self.name_falha]
        
        # TryCath
        try:

            # SELECT - Controle
            status_mysql_controle = self.my_sql.mysql_select(
                self.user, 
                self.host,
                self.database,
                self.coluna_path, 
                self.tabela_controle, 
                filtro_coluna, filtro
                )

            if status_mysql_controle['status']:
                
                # Pegar resultados
                path = status_mysql_controle['resultado'][0]
                print('path_falha')
                print(path)

                # Limpar arquivos da pasta de download
                status_limpar_pasta = self.my_folder.limpar_pasta(path)

                if status_limpar_pasta['status']:
                    self.status = True
                    print(self.sucesso)
                
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

        return{'status': self.status}
    
    # Configurar caminho de erro do fsist
    def limpar_erro(self):

        # Variaveis
        filtro_coluna = [self.coluna_module, self.coluna_type, self.coluna_name]
        filtro = [self.module, self.type, self.name_erro]
        
        # TryCath
        try:

            # SELECT - Controle
            status_mysql_controle = self.my_sql.mysql_select(
                self.user, 
                self.host,
                self.database,
                self.coluna_path, 
                self.tabela_controle, 
                filtro_coluna, filtro
                )

            if status_mysql_controle['status']:
                
                # Pegar resultados
                path = status_mysql_controle['resultado'][0]
                print('path_erro')
                print(path)

                # Limpar arquivos da pasta de download
                status_limpar_pasta = self.my_folder.limpar_pasta(path)

                if status_limpar_pasta['status']:
                    self.status = True
                    print(self.sucesso)
                
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

        return{'status': self.status}