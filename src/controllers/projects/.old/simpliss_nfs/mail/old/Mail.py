from modules.mylogger.mylogger import MyLogger
from modules.mysql.mysql import MySQL
from modules.mymail.mymail import MyMail
from modules.myfolder.myfolder import MyFolder

class Mail():
        
    def __init__(self, 
                 user, password, host, database, 
                 column_mail, column_login, column_password, column_control_path,
                 id_status, id_fluxos, 
                 table_status, table_fluxos, table_mail, table_fluxosmail, table_credentials, table_control, table_fluxoscontrol,
                 param_true, param_mail_repositorio, param_mail_sid_cliente_sucesso, param_mail_sid_cliente_falha, param_mail_sid_cliente_erro, param_control_sid_cliente_sucesso, param_control_sid_cliente_falha, param_control_sid_cliente_erro,
                 head_sucesso, head_falha, head_erro, msg_sucesso, msg_falha, msg_erro
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
        self.my_mail = MyMail()
        self.my_folder = MyFolder()

        # Metodo de 'INJEÇÃO DE DEPENDENCIA'
        # ref.: https://www.youtube.com/watch?v=5DBfVnQn1Ow

        # Variaveis especificas
        self.user = user
        self.password = password
        self.host = host
        self.database = database

        # Colunas
        self.column_mail = column_mail
        self.column_login = column_login
        self.column_password = column_password
        self.column_control_path = column_control_path

        # ID
        self.id_status = id_status
        self.id_fluxos = id_fluxos
        
        # Tabela SELECT
        self.table_status = table_status
        self.table_fluxos = table_fluxos
        self.table_credentials = table_credentials
        self.table_mail = table_mail
        self.table_fluxosmail = table_fluxosmail
        self.table_control = table_control
        self.table_fluxoscontrol = table_fluxoscontrol
        
        # Parametros
        self.param_true = param_true
        self.param_mail_repositorio = param_mail_repositorio
        self.param_mail_sid_cliente_sucesso = param_mail_sid_cliente_sucesso
        self.param_mail_sid_cliente_falha = param_mail_sid_cliente_falha
        self.param_mail_sid_cliente_erro = param_mail_sid_cliente_erro
        self.param_control_sid_cliente_sucesso = param_control_sid_cliente_sucesso
        self.param_control_sid_cliente_falha = param_control_sid_cliente_falha
        self.param_control_sid_cliente_erro = param_control_sid_cliente_erro

        # Head
        self.head_sucesso = head_sucesso
        self.head_falha = head_falha
        self.head_erro = head_erro

        # Body
        self.msg_sucesso = msg_sucesso
        self.msg_falha = msg_falha
        self.msg_erro = msg_erro
    
    # Função para verificar se existem arquivos com extensão no caminho  
    def mail(self, type):

        """
        Ira realizar um print da pagina da web.

        Args:
            type (str): O tipo de elemento a ser utilizado ['SUCESSO', 'FALHA', 'ERRO']
        """

        # Variaveis
        type = str(type)

        # TryCtach
        try:

            # Colunas Fluxosmail
            column_login = [self.table_credentials, self.column_login]
            column_password = [self.table_credentials, self.column_password]
            column_mail = [self.table_mail, self.column_mail]
            column_fluxosmail = [column_login, column_password, column_mail]

            # Colunas Control
            column_path = [self.table_control, self.column_control_path]
            column_control = [column_path]

            # Lista de colunas filtros
            column_id_fluxos = [self.table_fluxos, self.id_fluxos]
            column_id_status = [self.table_status, self.id_status]
            column_filter = [column_id_fluxos, column_id_status]

            # Lista de filtros            
            if type.lower() == 'sucesso':
                status_type = True

                # Mail
                filter_mail_repositorio = [self.param_mail_repositorio, self.param_true]
                filter_mail_sucesso = [self.param_mail_sid_cliente_sucesso, self.param_true]                
                filter_mail = [filter_mail_repositorio, filter_mail_sucesso]

                # Path
                filter_path = [self.param_control_sid_cliente_sucesso, self.param_true]

                ## Titulo
                head = self.head_sucesso

                # Corpo
                body = self.msg_sucesso

            elif type.lower() == 'falha':
                status_type = True

                # Mail
                filter_mail_repositorio = [self.param_mail_repositorio, self.param_true]
                filter_mail_falha = [self.param_mail_sid_cliente_falha, self.param_true]
                filter_mail = [filter_mail_repositorio, filter_mail_falha]

                # Path
                filter_path = [self.param_control_sid_cliente_falha, self.param_true]

                ## Titulo
                head = self.head_falha

                # Corpo
                body = self.msg_falha

            elif type.lower() == 'erro':
                status_type = True

                # Mail
                filter_mail_repositorio = [self.param_mail_repositorio, self.param_true]
                filter_mail_erro = [self.param_mail_sid_cliente_erro, self.param_true]
                filter_mail = [filter_mail_repositorio, filter_mail_erro]

                # Path
                filter_path = [self.param_control_sid_cliente_erro, self.param_true]

                ## Titulo
                head = self.head_erro

                # Corpo
                body = self.msg_erro

            else:
                status_type = False

            if status_type:                

                # Buscar paths
                status_mysql_path = self.my_sql.mysql_select(
                    self.user,
                    self.password,
                    self.host,
                    self.database,
                    self.table_fluxoscontrol,
                    column_control,
                    column_filter,
                    filter_path,
                    True
                )

                if status_mysql_path['status']:

                    # Listar path
                    resultado = status_mysql_path['resultado']
                    path = resultado[0][0]

                    status_myfolder_files = self.my_folder.folder('list', 'file', path)

                    if status_myfolder_files['status']:

                        # Listar file
                        resultado = status_myfolder_files['resultado']
                        file = resultado

                        # Lista de e-mails
                        mails = []
                        login = []
                        password = []

                        # Buscar os e-mails
                        for filter_mail_count in filter_mail:
                        
                            # Buscar informações do banco de dados
                            status_select_sucesso = self.my_sql.mysql_select(
                                self.user,
                                self.password, 
                                self.host,
                                self.database,
                                self.table_fluxosmail,
                                column_fluxosmail,
                                column_filter,
                                filter_mail_count,
                                True
                                )

                            if status_select_sucesso['status']:

                                # Retorna a lista de resultados
                                resultado = status_select_sucesso['resultado']
                                print('----------------- resultado ------------------------')
                                print(resultado)

                                # Retorna a lista de resultados
                                login.append(resultado[0][0])
                                print('login')
                                print(login)
                                password.append(resultado[1][0])
                                print('password')
                                print(password)
                                mails.append(resultado[2][0])
                                print('mails')
                                print(mails)
                                status_select = True  
                                mensagem = f'Sucesso ao fazer o SELECT da tabela: {self.table_fluxosmail}'
                                print(mensagem)              

                            else:
                                status_select = False
                                mensagem = f'Falha ao fazer o SELECT da tabela: {self.table_fluxosmail}'
                                print(mensagem)
                                break

                        if status_select:

                            # E-mails
                            #mail_repositorio = mails[0]
                            #mail_recipient = mails[1:]
                            # Identificar o indice de começo da contagem, retorna a lsita a partir da posição definida (var = var [1:])

                            # Enviar o e-mail:
                            status_mymail_send = self.my_mail.mail(
                                login[1],
                                password[1],
                                mails,
                                head,
                                body,
                                path,
                                file
                            )

                            if status_mymail_send['status']:
                                self.status = True
                                mensagem = f'Sucesso ao enviar o e-mail.'
                                print(mensagem)

                            else:
                                self.status = False
                                mensagem = f'Falha ao enviar o e-mail.'
                                print(mensagem)

                        else:
                            self.status = False
                            mensagem = f'Falha ao fazer o SELECT na tabela: {self.table_fluxosmail}.'
                            print(mensagem)

                    else:
                        self.status = False
                        mensagem = f'Falha ao listar os arquivos do path: {path}.'
                        print(mensagem)

                else:
                    self.status = False
                    mensagem = f'Falha ao fazer o SELECT na tabela: {self.table_fluxoscontrol}.'
                    print(mensagem)

            else:
                self.status = False
                mensagem = f'"TYPE" informado não cadastrado.'
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
            mensagem = 'Erro ao fazer ao enivar os e-mails.'
            print(aviso)

            # Alimentar o log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error(mensagem)
            self.my_logger.log_error(str(aviso))

        return{'status': self.status}
    
    # Função para verificar se existem arquivos com extensão no caminho  
    def mail_sucesso(self):

        """
        Ira enviar o e-mail de sucesso.
        """

        # TryCtach
        try:

            # Mail
            status_mail = self.mail('sucesso')

            if status_mail['status']:
                self.status = True
                mensagem = 'Sucesso ao encaminhar o e-mail.'
                print(mensagem)

            else:
                self.status = False
                mensagem = 'Falha ao encaminhar o e-mail.'
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
            mensagem = 'Erro ao encaminhar o e-mail.'
            print(mensagem)

            # Alimentar o log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error(mensagem)
            self.my_logger.log_error(str(aviso))

        return{'status': self.status}
    
    # Função para verificar se existem arquivos com extensão no caminho  
    def mail_falha(self):

        """
        Ira enviar o e-mail de falha.
        """

        # TryCtach
        try:

            # Mail
            status_mail = self.mail('falha')

            if status_mail['status']:
                self.status = True
                mensagem = 'Sucesso ao encaminhar o e-mail.'
                print(mensagem)

            else:
                self.status = False
                mensagem = 'Falha ao encaminhar o e-mail.'
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
            mensagem = 'Erro ao encaminhar o e-mail.'
            print(mensagem)

            # Alimentar o log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error(mensagem)
            self.my_logger.log_error(str(aviso))

        return{'status': self.status}
    
    # Função para verificar se existem arquivos com extensão no caminho  
    def mail_erro(self):

        """
        Ira enviar o e-mail de erro.
        """

        # TryCtach
        try:

            # Mail
            status_mail = self.mail('erro')

            if status_mail['status']:
                self.status = True
                mensagem = 'Sucesso ao encaminhar o e-mail.'
                print(mensagem)

            else:
                self.status = False
                mensagem = 'Falha ao encaminhar o e-mail.'
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
            mensagem = 'Erro ao encaminhar o e-mail.'
            print(mensagem)

            # Alimentar o log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error(mensagem)
            self.my_logger.log_error(str(aviso))

        return{'status': self.status}



