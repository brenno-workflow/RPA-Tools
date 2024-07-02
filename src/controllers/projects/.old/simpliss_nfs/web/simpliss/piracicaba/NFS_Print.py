from modules.mylogger.mylogger import MyLogger
from modules.mysql.mysql import MySQL
from modules.myweb.myweb import MyWeb
import os

class NFSPrint():
        
    def __init__(self, 
                 webdriver, user, password, host, database, 
                 file_name_list_count,
                 column_control_path, 
                 id_status, id_fluxos, 
                 table_status, table_fluxos, table_control, table_fluxoscontrol,
                 param_true, param_control_sid_cliente_sucesso, param_control_sid_cliente_falha, param_control_sid_cliente_erro,
                 extension_png
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

        # Variaveis
        self.file_name = file_name_list_count

        # Extensões
        self.extension_png = extension_png

        # Colunas
        self.column_control_path = column_control_path

        # ID
        self.id_status = id_status
        self.id_fluxos = id_fluxos
        
        # Tabela SELECT
        self.table_status = table_status
        self.table_fluxos = table_fluxos
        self.table_control = table_control
        self.table_fluxoscontrol = table_fluxoscontrol
        
        # Parametros
        self.param_true = param_true
        self.param_control_sid_cliente_sucesso = param_control_sid_cliente_sucesso
        self.param_control_sid_cliente_falha = param_control_sid_cliente_falha
        self.param_control_sid_cliente_erro = param_control_sid_cliente_erro
    
    # Função para verificar se existem arquivos com extensão no caminho  
    def print(self, type):

        """
        Ira realizar um print da pagina da web.

        Args:
            type (str): O tipo de elemento a ser utilizado ['SUCESSO', 'FALHA', 'ERRO']
        """

        # Variaveis
        type = str(type)

        # TryCtach
        try:

            # Coluna Path
            column_path = [[self.table_control, self.column_control_path]]

            # Lista de colunas filtros
            column_id_fluxos = [self.table_fluxos, self.id_fluxos]
            column_id_status = [self.table_status, self.id_status]
            column_filter_id_fluxos = [column_id_fluxos, column_id_status]

            # Lista de filtros
            if type.lower() == 'sucesso':
                filter_id_fluxos = [self.param_control_sid_cliente_sucesso, self.param_true]

            elif type.lower() == 'falha':
                filter_id_fluxos = [self.param_control_sid_cliente_falha, self.param_true]

            elif type.lower() == 'erro':
                filter_id_fluxos = [self.param_control_sid_cliente_erro, self.param_true]
            
            # Buscar informações do banco de dados
            status_select_sucesso = self.my_sql.mysql_select(
                self.user,
                self.password, 
                self.host,
                self.database,
                self.table_fluxoscontrol,
                column_path,
                column_filter_id_fluxos,
                filter_id_fluxos,
                True
                )

            if status_select_sucesso['status']:

                # Retorna a lista de resultados
                resultado = status_select_sucesso['resultado'][0][0]
                print(resultado)

                # Caminho completo
                print_path = os.path.join(resultado, (self.file_name + self.extension_png))

                status_myweb_print = self.my_web.browser('print', 'save', print_path)

                if status_myweb_print['status']:
                    self.status = True
                    mensagem = f'Sucesso ao realizar o PRINT e salvar no path: {resultado}'
                    print(mensagem)

                else:
                    self.status = False
                    mensagem = f'Falha ao realizar o PRINT e salvar no path: {resultado}'
                    print(mensagem)
            
            else:
                self.status = False
                mensagem = f'Falha ao fazer o SELECT da tabela: {self.table_fluxoscontrol}'
                print(mensagem)

            # Alimentar o log
            if self.status:
                self.my_logger.log_info(self.sucesso)
                self.my_logger.log_info(mensagem)

            else:
                self.my_logger.log_warn(self.falha)
                self.my_logger.log_warn(mensagem)

        except Exception as aviso:
            self.status = False
            print(self.erro)
            mensagem = f'Erro ao fazer o SELECT da tabela: {self.table_fluxoscontrol}'
            print(aviso)

            # Alimentar o log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error(mensagem)
            self.my_logger.log_error(str(aviso))

        return{'status': self.status}

