from modules.mylogger.mylogger import MyLogger
from modules.mysql.mysql import MySQL
from modules.myweb.myweb import MyWeb
import time

class NFSTable():
        
    def __init__(self, 
                 webdriver, user, password, host, database, 
                 column_fluxos_id, column_status_id,
                 column_url,
                 table_fluxos, table_status, 
                 table_sites, table_fluxosweb, 
                 param_web_table, param_true
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
        self.webdriver = webdriver

        # Colunas
        self.column_url = column_url
        
        # ID
        self.column_fluxos_id = column_fluxos_id
        self.column_status_id = column_status_id
                
        # Tabela 
        self.table_fluxos = table_fluxos
        self.table_status = table_status
        self.table_sites = table_sites
        self.table_fluxosweb = table_fluxosweb

        # Parametros
        self.param_true = param_true
        self.param_web_table = param_web_table

    # Abrir tabela inicial
    def nfs_index_table(self):

        # TryCtach
        try:

            # Lista de colunas site e credenciais
            column_url = [self.table_sites, self.column_url]
            column_site_credential = [column_url]

            # Lista de filtros
            column_id_fluxos = [self.table_fluxos, self.column_fluxos_id]
            column_id_status = [self.table_status, self.column_status_id]
            column_filter_id = [column_id_fluxos, column_id_status]

            # Lista de colunas_filtro
            filter_id = [self.param_web_table, self.param_true]
            
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
                print('resultado')
                print(resultado)
                self.my_logger.log_info(f"resultado: {resultado}")

                # Atualizar variaveis
                url = resultado[0][0]
                print(url)

                status_table = self.my_web.browser('get', None, url)

                if status_table['status']:
                    self.status = True
                    print(self.sucesso)

                else:
                    self.status = False
                    mensagem = f"Falha ao abrir a url: '{url}'"

            else:
                self.status = False
                mensagem = f"Falha ao  fazer o SELECT da tabela: '{self.table_fluxosweb}'"

            # Alimentar o log
            if self.status:
                self.my_logger.log_info(self.sucesso)

            else:
                self.my_logger.log_warn(self.falha)
                self.my_logger.log_warn(mensagem)

        except Exception as aviso:
            self.status = False
            print(self.erro)
            print(aviso)

            # Alimentar o log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error(str(aviso))

        return{'status': self.status}
    
    # Abrir nova tabela clone
    def nfs_new_table(self):        

        # TryCtach
        try:

            status_current_url = self.my_web.browser('current_url')

            if status_current_url['status']:

                url = status_current_url['resultado']
                mensagem = f'---------------------------------------\nurl: "{url}"\n-----------------------------------'
                self.my_logger.log_info(mensagem)

                # Script para abrir uma nava guia especifica
                script_new_tab = f"window.open('{url}', '_blank');"

                status_new_tab = self.my_web.browser('execute_script', None, script_new_tab)

                if status_new_tab['status']:

                    status_new_tab_control = self.my_web.browser('switch_to', 'window', 0)

                    if status_new_tab_control['status']:
                        mensagem = f'---------------------------------------\nurl: "{url}"\n-----------------------------------'
                        self.my_logger.log_info(mensagem)
                        self.status = True
                        print(self.sucesso)

                    else:
                        self.status = False
                        mensagem = f"Falha ao trocar o controle para a nova guia"

                else:
                    self.status = False
                    mensagem = f"Falha ao carregar a url: '{url}'"

            else:
                self.status = False
                mensagem = "Falha ao buscar a url atual"

            # Alimentar o log
            if self.status:
                self.my_logger.log_info(self.sucesso)

            else:
                self.my_logger.log_warn(self.falha)
                self.my_logger.log_warn(mensagem)

        except Exception as aviso:
            self.status = False
            print(self.erro)
            print(aviso)

            # Alimentar o log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error(str(aviso))

        return{'status': self.status}
    
    # Fechar nova tabela clone
    def nfs_close_table(self):

        # TryCtach
        try:

            status_close_tab = self.my_web.browser('close')

            if status_close_tab['status']:

                status_switch_tab = self.my_web.browser('switch_to', 'window', 'main')

                if status_switch_tab['status']:
                    time.sleep(5)
                    self.status = True
                    print(self.sucesso)

                else:
                    self.status = False
                    mensagem = "Falha ao voltar na aba de INDEX no navegador"

            else:
                self.status = False
                mensagem = "Falha ao fechar a aba atual"

            # Alimentar o log
            if self.status:
                self.my_logger.log_info(self.sucesso)

            else:
                self.my_logger.log_warn(self.falha)
                self.my_logger.log_warn(mensagem)

        except Exception as aviso:
            self.status = False
            print(self.erro)
            print(aviso)

            # Alimentar o log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error(str(aviso))

        return{'status': self.status}