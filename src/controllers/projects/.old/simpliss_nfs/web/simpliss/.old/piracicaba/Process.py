from modules.mylogger.mylogger import MyLogger
from modules.mysql.mysql import MySQL
from controllers.access.simpliss.piracicaba import Access
from controllers.projects.simpliss_nfs.web.simpliss.nfs import NFS_Index

class Process():
        
    def __init__(self, 
                 webdriver, user, password, host, database, 
                 column_fluxos_id, column_status_id,
                 column_url, column_login, column_password, column_control_path,
                 table_fluxos, table_status, 
                 table_credentials, table_sites, table_fluxosaccess, table_fluxosweb, table_control, table_fluxoscontrol,
                 param_web_access, param_true, param_web_table, param_control_download,
                 input_banner, input_banner_close, input_banner_hidden,
                 input_user, input_password, button_entrar, button_sair,
                 input_coluna_numero, button_coluna_proximo,
                 button_imprimir
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

        # Metodo de 'INJEÇÃO DE DEPENDENCIA'
        # ref.: https://www.youtube.com/watch?v=5DBfVnQn1Ow

        # Variaveis especificas
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.webdriver = webdriver

        # Colunas
        self.column_url = column_url
        self.column_login = column_login
        self.column_password = column_password
        self.column_control_path = column_control_path
        
        # ID
        self.column_fluxos_id = column_fluxos_id
        self.column_status_id = column_status_id
                
        # Tabela 
        self.table_fluxos = table_fluxos
        self.table_status = table_status
        self.table_credentials = table_credentials
        self.table_sites = table_sites
        self.table_fluxosaccess = table_fluxosaccess
        self.table_fluxosweb = table_fluxosweb
        self.table_control = table_control
        self.table_fluxoscontrol = table_fluxoscontrol

        # Parametros
        self.param_true = param_true
        self.param_web_access = param_web_access
        self.param_web_table = param_web_table
        self.param_control_download = param_control_download

        # Web
        # Notifications
        self.input_banner = input_banner
        self.input_banner_close = input_banner_close
        self.input_banner_hidden = input_banner_hidden
        # Login
        self.input_user = input_user
        self.input_password = input_password
        self.button_entrar = button_entrar
        self.button_sair = button_sair
        # Table
        self.input_coluna_numero = input_coluna_numero
        self.button_coluna_proximo = button_coluna_proximo
        # NFSe
        self.button_imprimir = button_imprimir
    
    # Função para verificar se existem arquivos com extensão no caminho  
    def process(self):

        # TryCtach
        try:

           # Lista de colunas site e credenciais
            column_url = [self.table_sites, self.column_url]
            column_login = [self.table_credentials, self.column_login]
            column_password = [self.table_credentials, self.column_password]
            column_site_credential = [column_url, column_login, column_password]

            # Lista de filtros
            column_id_fluxos = [self.table_fluxos, self.column_fluxos_id]
            column_id_status = [self.table_status, self.column_status_id]
            column_filter_id = [column_id_fluxos, column_id_status]

            # Lista de colunas_filtro
            filter_id = [self.param_web_access, self.param_true]
            
            # Buscar informações do banco de dados
            status_select_site_credenciais = self.my_sql.mysql_select(
                self.user,
                self.password, 
                self.host,
                self.database,
                self.table_fluxosaccess,
                column_site_credential,
                column_filter_id,
                filter_id,
                True
                )

            if status_select_site_credenciais['status']:

                # Retorna a lista de resultados
                resultado = status_select_site_credenciais['resultado']
                print('resultado')
                print(resultado)

                # Atualizar variaveis
                url = resultado[0]
                login = resultado[1]
                password = resultado[2]
                
                print(url)
                print(login)
                print(password)

                for url_count, login_count, password_count in zip(url, login, password):

                    # Parametrizar as funções
                    web_access = Access.Access(
                        self.webdriver, self.user, self.password, self.host, self.database, 
                        url_count, login_count, password_count,
                        self.input_banner, self.input_banner_close, self.input_banner_hidden,
                        self.input_user, self.input_password, self.button_entrar, self.button_sair
                    )
                    web_page = NFS_Index.NFSIndex(
                        self.webdriver, self.user, self.password, self.host, self.database,
                        self.column_fluxos_id, self.column_status_id,
                        self.column_url, self.column_control_path,
                        self.table_fluxos, self.table_status, 
                        self.table_sites, self.table_fluxosweb, self.table_control, self.table_fluxoscontrol,
                        self.param_web_table, self.param_true, self.param_control_download,
                        self.input_coluna_numero, self.button_coluna_proximo,
                        self.button_imprimir
                    )

                    # Passo a passo
                    # 1) Função para verificar todas as notas ativas (elemento selenium, número nota)
                    # 2) Função para verificar todas as notas canceladas (número nota)
                    # 3) Função para verificar notas que já foram registardas (SID) (CONPJ + nº Nota)
                    # 4) Função para verificar baixar notas que ainda não foram registradas (SID) (elemento selenium clica, baixa PDF e gera XML - nome padrão = CNPJ + nº Nota)
                    # 5) Função para cancelar as notas canceladas (CNPJ, nº Nota, senha do SID)

                    # Login
                    status_simpliss_login = web_access.login()

                    if status_simpliss_login['status']:

                        status_nfs_index = web_page.nfs_index()

                        if status_nfs_index['status']:
                    
                            # Logoff
                            status_simpliss_logoff = web_access.logoff()
                            
                            if status_simpliss_logoff['status']:
                                self.status = True
                                print(self.sucesso)

                            else:
                                self.status = False
                                print(self.falha)
                                break

                    else:
                        self.status = False
                        print(self.falha)
                        break
            
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