from modules.mylogger.mylogger import MyLogger
from modules.mysql.mysql import MySQL
from modules.myweb.myweb import MyWeb
import time

class NFSIndex():
        
    def __init__(self, 
                 webdriver, user, password, host, database, 
                 column_fluxos_id, column_status_id,
                 column_url,
                 table_fluxos, table_status, 
                 table_sites, table_fluxosweb,
                 param_web_table, param_true, 
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

        # Web
    
    # Função para verificar se existem arquivos com extensão no caminho  
    def nfs_index(self):

        # Variaveis
        disable = 'disable'

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

                    while True:

                        status_table_rows = self.my_web.element('sorting_1', 'class', 'find_elements')

                        if status_table_rows['status']:

                            resultado = status_table_rows['resultado']
                            rows = resultado

                            print(f'rows: {rows}')
                            mensagem = f'rows: {rows}'
                            self.my_logger.log_info(mensagem)

                            for rows_count in rows:

                                #status_nfs_click = self.my_web.element(rows_count, 'class', 'click')

                                break

                                count = 0
                                print(f'contagem: {count + 1}')
                                mensagem = f'contagem: {count + 1} \n rows = {len(rows)}'
                                self.my_logger.log_info(mensagem)
                                #self.my_logger.log_info(f'rowns_count:{rows_count}')

                                status_next_button = self.my_web.element('tb_Pesquisa_next', 'id', 'find', 'get_attribute', 'class')

                                if status_next_button['status']:

                                    next_button_attribute = status_next_button['resultado']
                                    print(f'next_button_attribute: {next_button_attribute}')
                                    mensagem = f'next_button_attribute: {next_button_attribute}'
                                    self.my_logger.log_info(mensagem)
                                    
                                    if disable in next_button_attribute:
                                        break

                                    else:
                                        break

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