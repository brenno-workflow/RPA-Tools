from modulos.mylogger.mylogger import MyLogger
from modulos.mysql.mysql import MySQL
from modulos.myfolder.myfolder import MyFolder

class ControleLimpar:
        
    def __init__(self, 
                 user, host, database, module_fsist, type_subcontrole, name_download, name_sucesso, name_falha, name_erro,
                 coluna_path, coluna_module, coluna_type, coluna_name,
                 tabela_controle_rpa
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
        self.host = host
        self.database = database

        # Valores
        self.module = module_fsist
        self.type = type_subcontrole
        self.name_download = name_download
        self.name_sucesso = name_sucesso
        self.name_falha = name_falha
        self.name_erro = name_erro

        # Colunas
        self.coluna_path = coluna_path
        self.coluna_module = coluna_module
        self.coluna_type = coluna_type
        self.coluna_name = coluna_name

        # Tabela
        self.tabela_controle = tabela_controle_rpa

    # Configurar caminho de donwload do fsist
    def limpar_download(self):

        # Variaveis
        filtro_coluna = [self.coluna_module, self.coluna_type, self.coluna_name]
        filtro = [self.module, self.type, self.name_download]
        
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
                print('path_download')
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