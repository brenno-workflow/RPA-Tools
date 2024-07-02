from modules.mylogger.mylogger import MyLogger
from modules.mysql.mysql import MySQL
from modules.myweb.myweb import MyWeb
from selenium.webdriver.common.keys import Keys
import time

class SIDLogin():
        
    def __init__(self, 
                 webdriver, user, password, host, database, 
                 column_fluxos_id, column_status_id,
                 column_url, column_login, column_password,
                 table_fluxos, table_status, table_fluxosweb, table_sites, table_credentials,
                 param_sid, param_true,
                 input_user, input_password, button_entrar
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
        self.my_web = MyWeb(webdriver)

        # Variaveis especificas
        self.user = user
        self.password = password
        self.host = host
        self.database = database

        # Colunas
        self.column_url = column_url
        self.column_login = column_login
        self.column_password = column_password

        # ID
        self.column_fluxos_id = column_fluxos_id
        self.column_status_id = column_status_id
        
        # Tabela SELECT
        self.table_fluxos = table_fluxos
        self.table_status = table_status
        self.table_sites = table_sites
        self.table_credentials = table_credentials
        self.table_fluxosweb = table_fluxosweb
        
        # Parametros
        self.param_true = param_true
        self.param_sid = param_sid

        # Inputs
        self.input_user = input_user
        self.input_password = input_password

        # Buttons
        self.button_entrar = button_entrar
    
    # Função para verificar se existem arquivos com extensão no caminho  
    def sid_login(self):

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
            filter_id = [self.param_sid, self.param_true]
            
            # Buscar informações do banco de dados
            status_select_site_credenciais = self.my_sql.mysql_select(
                self.user,
                self.password, 
                self.host,
                self.database,
                self.table_fluxosweb,
                column_site_credential,
                column_filter_id,
                filter_id,
                True
                )

            if status_select_site_credenciais['status']:

                # Retorna a lista de resultados
                resultado = status_select_site_credenciais['resultado']
                print(resultado)

                # Atualizar variaveis
                url = resultado[0][0]
                login = resultado[1][0]
                password = resultado[2][0]
                
                # Abrir site do SID
                status_open_url = self.my_web.browser('get', None, url)

                if status_open_url:

                    status_type_login = self.my_web.element(self.input_user, 'id', 'click', 'send_keys', login)

                    if status_type_login:

                        status_type_password = self.my_web.element(self.input_password, 'id', 'click', 'send_keys', password)

                        if status_type_password:

                            status_entrar = self.my_web.element(self.input_password, 'id', 'send_keys', None, Keys.ENTER)
                            #status_entrar = self.my_web.element(self.button_entrar, 'class', 'click')

                            if status_entrar:
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