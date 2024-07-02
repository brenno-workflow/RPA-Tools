from modules.mylogger.mylogger import MyLogger
from modules.mysql.mysql import MySQL
from modules.myweb.myweb import MyWeb
import time

class SIDCliente():
        
    def __init__(self, 
                 webdriver, user, password, host, database, 
                 column_url,
                 id_fluxos, id_status,
                 table_fluxos, table_status, table_fluxosweb, table_sites,
                 param_sid_cliente, param_true
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

        # ID
        self.id_fluxos = id_fluxos
        self.id_status = id_status
                
        # Tabela SELECT
        self.table_fluxos = table_fluxos
        self.table_status = table_status
        self.table_sites = table_sites
        self.table_fluxosweb = table_fluxosweb

        # Parametros
        self.param_true = param_true
        self.param_sid_cliente = param_sid_cliente
    
    # Função para verificar se existem arquivos com extensão no caminho  
    def sid_cliente(self):

        # TryCtach
        try:

            # Lista de colunas site e credenciais
            column_url = [self.table_sites, self.column_url]
            column_site_credential = [column_url]

            # Lista de filtros
            column_id_fluxos = [self.table_fluxos, self.id_fluxos]
            column_id_status = [self.table_status, self.id_status]
            column_filter_id = [column_id_fluxos, column_id_status]

            # Filtos
            filter_id = [self.param_sid_cliente, self.param_true]
            
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

                # Abrir site do SID
                status_open_url = self.my_web.browser('get', None, url)

                if status_open_url:

                    time.sleep(5)

                    self.status = True
                    print(self.sucesso)

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