from modules.mylogger.mylogger import MyLogger
from modules.mysql.mysql import MySQL
from modules.myrequest.myrequest import MyRequest
import time

class EcossistemanfChaves:
        
    def __init__(self, 
                 user, password, host, database, 
                 column_fluxos_id, column_status_id,
                 column_url, column_login, column_password,
                 table_fluxos, table_status, table_fluxosweb, table_sites, table_credentials,
                 param_ecossistema, param_true,
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
        self.my_request = MyRequest()
        
        # Metodo de 'INJEÇÃO DE DEPENDENCIA'
        # ref.: https://www.youtube.com/watch?v=5DBfVnQn1Ow
        
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
        self.param_ecossistema = param_ecossistema
        

    # Função para fazer o quests das chaves ativas e canceldas do ecossistemanf
    def ecossistemanf_chaves(self):
        
        # TryCatch
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
            filter_id = [self.param_ecossistema, self.param_true]


                # Parametros
            status_mysql_parametros = self.my_sql.mysql_select(
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
            if status_mysql_parametros['status']:
                
            # Retorna a lista de resultados
                resultado = status_mysql_parametros['resultado']
                print(resultado)

                # Atualizar variaveis
                url = resultado[0][0]
                print(url)
                time.sleep(10)
                # Fazar os requests
                status_requests_ecossitemanf = self.my_request.requests_get(url, 'td')
                self.my_logger.log_info(status_requests_ecossitemanf['resultado'])
                if status_requests_ecossitemanf['status']:
                    # Pegar a lista de resulatdos
                    self.resultado = status_requests_ecossitemanf['resultado']
                    self.status = True
                
                else:
                    self.status = False
            
            else:
                self.status = False
                
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

        return{'status': self.status, 'resultado': self.resultado}

    