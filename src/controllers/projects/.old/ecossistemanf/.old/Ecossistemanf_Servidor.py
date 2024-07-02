from modulos.mylogger.mylogger import MyLogger
from modulos.mysql.mysql import MySQL
from modulos.myfolder.myfolder import MyFolder
from procedimentos.ecossistemanf.mail.Mail_Ecossistemanf import MailEcossistemanf

class EcossistemanfServidor():
        
    def __init__(self, 
                 user, host, database, module_fsist, type_subcontrole,
                 coluna_module, coluna_type, coluna_path,
                 tabela_servidores
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
        self.host = host
        self.database = database

        # Valores
        self.module = module_fsist
        self.type = type_subcontrole
        self.extensao_pdf = '.pdf'
        self.extensao_xml = '.xml'
        self.path_pdf = None
        self.path_xml = None
       
        # Colunas
        self.coluna_module = coluna_module
        self.coluna_type = coluna_type
        self.coluna_path = coluna_path
        
        # Tabela SELECT
        self.tabela_servidores = tabela_servidores
    
    # Função para verificar se existem arquivos com extensão no caminho  
    def ecossistemanf_sem_arquivos(self):

        # Variaveis
        filtro_coluna_servidores = [self.coluna_module, self.coluna_type]
        filtro_servidores = [self.module, self.type]

        # TryCtach
        try:

            # Buscar informações do banco de dados
            status_mysql_select = self.my_sql.mysql_select(
                self.user, 
                self.host, 
                self.database,
                self.coluna_path, 
                self.tabela_servidores, 
                filtro_coluna_servidores, 
                filtro_servidores
                )

            if status_mysql_select['status']:

                # Retorna a lista de resultados
                lista_resultados = status_mysql_select['resultado']
                print(lista_resultados)

                # Atualizar variaveis
                path_pdf = lista_resultados[0]
                path_xml = lista_resultados[1]

                # Chamar função para verificar se existe arquivo com a extensão especificada no caminho expecificado
                status_existe_pdf = self.my_folder.extensao_nao_existe(path_pdf, self.extensao_pdf)

                # Inverter a lógica para rodar apenas se não tiver arquivos na pasta
                if status_existe_pdf['status']:

                    # Chamar função para verificar se existe arquivo com a extensão especificada no caminho expecificado
                    status_existe_xml = self.my_folder.extensao_nao_existe(path_xml, self.extensao_xml)

                    # Inverter a lógica para rodar apenas se não tiver arquivos na pasta
                    if status_existe_xml['status']:
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
    
    # Função para verificar se existem arquivos com extensão no caminho  
    def ecossistemanf_com_arquivos(self):

        # Variaveis
        filtro_coluna_servidores = [self.coluna_module, self.coluna_type]
        filtro_servidores = [self.module, self.type]

        # TryCtach
        try:

            # Buscar informações do banco de dados
            status_mysql_select = self.my_sql.mysql_select(
                self.user, 
                self.host, 
                self.database,
                self.coluna_path, 
                self.tabela_servidores, 
                filtro_coluna_servidores, 
                filtro_servidores
                )

            if status_mysql_select['status']:

                # Retorna a lista de resultados
                lista_resultados = status_mysql_select['resultado']
                print(lista_resultados)

                # Atualizar variaveis
                path_pdf = lista_resultados[0]
                path_xml = lista_resultados[1]

                # Chamar função para verificar se existe arquivo com a extensão especificada no caminho expecificado
                status_existe_pdf = self.my_folder.extensao_existe(path_pdf, self.extensao_pdf)

                # Inverter a lógica para rodar apenas se não tiver arquivos na pasta
                if status_existe_pdf['status']:

                    # Chamar função para verificar se existe arquivo com a extensão especificada no caminho expecificado
                    status_existe_xml = self.my_folder.extensao_existe(path_xml, self.extensao_xml)

                    # Inverter a lógica para rodar apenas se não tiver arquivos na pasta
                    if status_existe_xml['status']:
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