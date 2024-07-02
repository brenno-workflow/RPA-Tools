from modulos.mylogger.mylogger import MyLogger
from modulos.mysql.mysql import MySQL
from modulos.mypath.mypath import MyPath
import os

class ControleRPA:
        
    def __init__(self, 
                 user, host, database, module_controle, 
                 coluna_local, coluna_folder, coluna_module, coluna_path, 
                 tabela_controle):

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
        self.my_path = MyPath()

        # Variaveis especificas
        self.user = user
        self.host = host
        self.database = database

        # Valores
        self.module_controle = module_controle
        self.path = None

        # Colunas
        self.coluna_local = coluna_local
        self.coluna_folder = coluna_folder
        self.coluna_module = coluna_module
        self.coluna_path = coluna_path

        # Tabela controle 
        self.tabela_controle = tabela_controle

    # MySQL Controle
    def criar_controle_rpa(self):

        # Variaveis
        coluna_controle_list = [self.coluna_local, self.coluna_folder]

        # TryCtach
        try:
            
            # Tabela Controle
            status_mysql_select = self.my_sql.mysql_select(
                self.user, 
                self.host, 
                self.database, 
                coluna_controle_list, 
                self.tabela_controle, 
                self.coluna_module, 
                self.module_controle
                )

            if status_mysql_select['status']:
                
                # Pegar a lista da tabela
                lista_variaveis = status_mysql_select['resultado']

                print('lista variaveis')
                print(lista_variaveis)

                diretorio = lista_variaveis[0]
                controle = lista_variaveis[1]
                print(diretorio)
                print(controle)

                # Identificar caminho do usuário local
                path = os.path.expanduser('~')

                # Caminho do usuário local + diretorio + pasta
                #path_diretorio = os.path.join(path, diretorio)
                path_diretorio = os.path.join(os.path.join(path, diretorio), controle)
                print(path_diretorio)

                # Criar pasta crontrole no path especificado no MySQL
                status_mypath_path = self.my_path.criar_path(path_diretorio)

                if status_mypath_path['status']:

                    # Atualizar path no banco de dados
                    status_mysql_update = self.my_sql.mysql_update(
                        self.user,
                        self.host,
                        self.database, 
                        self.coluna_path, 
                        self.tabela_controle, 
                        self.coluna_module, 
                        self.module_controle, 
                        path_diretorio
                        )

                    if status_mysql_update['status']:
                        self.status = True
                        print(self.sucesso)

                    else:
                        self.status = False
                        print(self.falha)

                else:
                    self.status = False
                    print(self.falha)

            else:
                self.status = False
                print(self.falha)

            # Alimentar o log
            if self.status:
                self.my_logger.log_info(self.sucesso)
                self.my_logger.log_info('Criar pasta de Controle RPA')

            else:
                self.my_logger.log_warn(self.falha)
                self.my_logger.log_warn('Criar pasta de Controle RPA')

        except Exception as aviso:
            self.status = False
            print(self.erro)
            print(aviso)

            # Alimentar o log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error('Criar pasta de Controle RPA')
            self.my_logger.log_error(str(aviso))

        return{'status': self.status}
    
    