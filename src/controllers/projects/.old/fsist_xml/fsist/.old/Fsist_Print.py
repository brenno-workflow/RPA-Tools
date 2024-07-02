from modulos.mylogger.mylogger import MyLogger
from modulos.mysql.mysql import MySQL
from modulos.myweb.myweb import MyWeb
from modulos.myprint.myprint import MyPrint
import datetime

class FsistPrint:
        
    def __init__(self, 
                 my_driver, user, host, database, module_fsist, type_subcontrole, name_falha, name_erro, 
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
        self.my_print = MyPrint()
        
        # Metodo de 'INJEÇÃO DE DEPENDENCIA'
        # ref.: https://www.youtube.com/watch?v=5DBfVnQn1Ow
        self.my_web = MyWeb(my_driver)

        # Variaveis especificas
        self.user = user
        self.host = host
        self.database = database

        # Valores
        self.extension = '.png'
        self.module = module_fsist
        self.type = type_subcontrole
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
    def fsist_print_falha(self):

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

                # Nome do arquivo
                name = datetime.datetime.now().strftime('%Y-%m-%d - %H-%M-%S')

                # Capturar pagina que apresentou a falha
                status_print_web = self.my_web.print_web(path, name, self.extension)

                if status_print_web['status']:
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
    
    # Configurar caminho de donwload do fsist
    def fsist_print_erro(self):

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

                # Nome do arquivo
                name = datetime.datetime.now().strftime('%Y-%m-%d - %H-%M-%S')

                # Capturar pagina que apresentou a falha
                status_print_web = self.my_print.print_screen(path, name, self.extension)

                if status_print_web['status']:
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