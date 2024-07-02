from modules.mylogger.mylogger import MyLogger
from modules.mysql.mysql import MySQL
from modules.myweb.myweb import MyWeb
import time

class NFSDownload():
        
    def __init__(self, 
                 webdriver, user, password, host, database, 
                 column_fluxos_id, column_status_id,
                 column_control_path,
                 table_fluxos, table_status,
                 table_control, table_fluxoscontrol,
                 param_control_download, param_true,
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
        self.my_web = MyWeb(webdriver)

        # Variaveis especificas
        self.user = user
        self.password = password
        self.host = host
        self.database = database

        # Colunas
        self.column_control_path = column_control_path
        
        # ID
        self.column_fluxos_id = column_fluxos_id
        self.column_status_id = column_status_id
                
        # Tabela 
        self.table_fluxos = table_fluxos
        self.table_status = table_status
        self.table_control = table_control
        self.table_fluxoscontrol = table_fluxoscontrol

        # Parametros
        self.param_true = param_true
        self.param_control_download = param_control_download

        # Web
        # Table
        self.button_imprimir = button_imprimir
    
    # Baixar pdf da nota
    def nfs_download(self):

        # TryCtach
        try:

            # Lista de colunas site e credenciais
            column_control_path = [self.table_control, self.column_control_path]
            column_table_control_path = [column_control_path]

            # Lista de filtros
            column_id_fluxos = [self.table_fluxos, self.column_fluxos_id]
            column_id_status = [self.table_status, self.column_status_id]
            column_filter_id = [column_id_fluxos, column_id_status]

            # Lista de colunas_filtro
            filter_id = [self.param_control_download, self.param_true]
            
            # Buscar informações do banco de dados
            status_select_site_credenciais = self.my_sql.mysql_select(
                self.user,
                self.password, 
                self.host,
                self.database,
                self.table_fluxoscontrol,
                column_table_control_path,
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
                control_download_path = resultado[0][0]
                print(control_download_path)

                # Configurar o download
                status_nfs_browser_config = self.my_web.browser('command_executor', 'download', control_download_path)

                if status_nfs_browser_config['status']:
                    
                    # Baixar a nota
                    status_nfs_imprimir = self.my_web.element(self.button_imprimir, 'id', 'find', 'click')

                    if status_nfs_imprimir['status']:
                        time.sleep(5)
                        self.status = True
                        print(self.sucesso)

                    else:
                        self.status = False
                        mensagem = "Falha ao fazer download do arquivo em pdf do NFSe"
                    
                else:
                    self.status = False
                    mensagem = "Falha ao configurar o path do download no navegador"

            else:
                self.status = False
                mensagem = f"Falha ao fazer o SELECT na tabela: '{self.table_fluxoscontrol}'"
                    
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