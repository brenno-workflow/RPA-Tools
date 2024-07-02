from modulos.mylogger.mylogger import MyLogger
from modulos.mymail.mymail import MyMail
from modulos.mysql.mysql import MySQL
from modulos.myfolder.myfolder import MyFolder

class MailEcossistemanf():
        
    def __init__(self, 
                 user, host, database, module_fsist, type_subcontrole, name_sucesso, name_falha, name_erro, 
                 coluna_mail, coluna_module, coluna_type, coluna_name, coluna_path,
                 tabela_emails, tabela_controle_rpa, tabela_servidores):

        # Variaveis gerais
        self.status = False
        self.sucesso = f'SUCESSO - {__name__}'
        self.falha = f'FALHA - {__name__}'
        self.erro = f'ERRO - {__name__}'

        # Instancias
        # Instanciar é uma boa prática e necessário
        # Não instaciar resulta na abertura de processo diferentes e erros
        self.my_logger = MyLogger()
        self.my_mail = MyMail()
        self.my_sql = MySQL()
        self.my_folder = MyFolder()

        # Variaveis especificas
        self.user = user
        self.host = host
        self.database = database

        # Valores
        self.module_fsist = module_fsist
        self.type_subcontrole = type_subcontrole
        self.name_sucesso = name_sucesso
        self.name_falha = name_falha
        self.name_erro = name_erro
        
        # Colunas
        self.coluna_mail = coluna_mail
        self.coluna_module = coluna_module
        self.coluna_type = coluna_type
        self.coluna_name = coluna_name
        self.coluna_path = coluna_path

        # Tabelas
        self.tabela_emails = tabela_emails
        self.tabela_controle = tabela_controle_rpa
        self.tabela_servidores = tabela_servidores
    
    # E-mail para informar que ainda existem arquivos na pasta
    def mail_verificar(self):

        # Variaveis
        colunas_filtros = [self.coluna_module, self.coluna_type]
        filtros = [self.module_fsist, self.type_subcontrole]
        titulo = '[RPA] [ECOSSISTEMANF] E-mail de notificação - Servidor'

        # TryCatch
        try:

            # Fazer select para buscar e-mails
            status_mail_select = self.my_sql.mysql_select(
                self.user, 
                self.host, 
                self.database, 
                self.coluna_mail, 
                self.tabela_emails
                )

            if status_mail_select['status']:

                destinatarios = status_mail_select['resultado']

                # Fazer select para buscar path de pastas no servidor
                status_path_select = self.my_sql.mysql_select(
                    self.user, 
                    self.host,
                    self.database,
                    self.coluna_path,
                    self.tabela_servidores,
                    colunas_filtros,
                    filtros                    
                )

                if status_path_select['status']:

                    lista_resultado = status_path_select['resultado']

                    # Listar os arquivos presentes nas pastas do servidor
                    status_listar_arquivos = self.my_folder.listar_arquivos(lista_resultado)

                    if status_listar_arquivos['status']:

                        listas_resulatdos = status_listar_arquivos['resultado']
                        
                        arquivos_pdf = listas_resulatdos[0]
                        arquivos_xml = listas_resulatdos[1]

                        corpo = (
                            'Olá, aqui é o Leonardo Vinci, BOT de automação da Cataguá. \n'
                            'Este é um e-mail de notificação sobre arquivos presentes no servidor. \n'
                            'Por conta de existirem arquivos ainda presentes na pasta, não foram inseridas novas notas. \n'                          
                            'Segue lista de arquivos presentes nos servidores: \n'
                            f'XMLs = {arquivos_xml}. \n'
                            f'PDFs = {arquivos_pdf}. \n'                          
                            'Grato pela atenção.'
                        )

                        status_mail_enviar = self.my_mail.mail_enviar(
                            self.user,
                            destinatarios,
                            titulo,
                            corpo
                        )

                        if status_mail_enviar['status']:
                            self.status = True
                            print(self.sucesso)

                        else:
                            self.status = False
                            print(self.falha)
                            self.my_logger.log_warn('Falha ao enviar o e-mail de comunicação de arquivos na pasta.')

                    else:
                        self.status = False
                        print(self.falha)
                        self.my_logger.log_warn('Falha ao listar os arquivos das pastas do servidor.')

                else:
                    self.status = False
                    print(self.falha)
                    self.my_logger.log_warn('Falha ao fazer o select das pastas do servidor.')

            else:
                self.status = False
                print(self.falha)
                self.my_logger.log_warn('Falha ao fazer o select dos e-mails.')

        except Exception as aviso:
            self.status = False
            print(self.erro)
            print(aviso)

            # Alimentar o log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error(str(aviso))

        return{'status': self.status}
    
    # E-mail para informar sucesso
    def mail_sucesso(self):

         # Variaveis
        titulo = '[RPA] [ECOSSISTEMANF] E-mail de notificação - Sucesso'

        # TryCatch
        try:

            # Fazer select para buscar e-mails
            status_mail_select = self.my_sql.mysql_select(
                self.user, 
                self.host, 
                self.database, 
                self.coluna_mail, 
                self.tabela_emails
                )

            if status_mail_select['status']:

                destinatario = status_mail_select['resultado'][0]

                corpo = (
                    'Olá, aqui é o Leonardo Vinci, BOT de automação da Cataguá. \n'
                    'Este é um e-mail de notificação sobre o sucesso da execução do BOT_Ecossistemanf. \n'
                    'Grato pela atenção.'
                )

                status_mail_enviar = self.my_mail.mail_enviar(
                    self.user,
                    destinatario,
                    titulo,
                    corpo,
                )

                if status_mail_enviar['status']:
                    self.status = True
                    print(self.sucesso)

                else:
                    self.status = False
                    print(self.falha)
                    self.my_logger.log_warn('Falha ao enviar o e-mail de comunicação de sucesso dp BOT_Ecossistemanf.')

            else:
                self.status = False
                print(self.falha)
                self.my_logger.log_warn('Falha ao fazer o select dos e-mails.')

        except Exception as aviso:
            self.status = False
            print(self.erro)
            print(aviso)

            # Alimentar o log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error(str(aviso))

        return{'status': self.status}
    
    # E-mail para informar falha
    def mail_falha(self):

         # Variaveis
        colunas_filtros = [self.coluna_module, self.coluna_type, self.coluna_name]
        filtros = [self.module_fsist, self.type_subcontrole, self.name_falha]
        titulo = '[RPA] [ECOSSISTEMANF] E-mail de notificação - Falha'

        # TryCatch
        try:

            # Fazer select para buscar e-mails
            status_mail_select = self.my_sql.mysql_select(
                self.user, 
                self.host, 
                self.database, 
                self.coluna_mail, 
                self.tabela_emails
                )

            if status_mail_select['status']:

                destinatario = status_mail_select['resultado'][0]

                # Fazer select para buscar path de pastas no servidor
                status_path_select = self.my_sql.mysql_select(
                    self.user, 
                    self.host,
                    self.database,
                    self.coluna_path,
                    self.tabela_controle,
                    colunas_filtros,
                    filtros 
                )

                if status_path_select['status']:

                    path = status_path_select['resultado'][0]

                    # Listar os arquivos presentes nas pastas do servidor
                    status_listar_arquivos = self.my_folder.listar_arquivos(path)

                    if status_listar_arquivos['status']:

                        arquivos = status_listar_arquivos['resultado'][0]

                        corpo = (
                            'Olá, aqui é o Leonardo Vinci, BOT de automação da Cataguá. \n'                           
                            'Este é um e-mail de notificação sobre algumas falhas que ocorreram no processo de download de notas do Fsist. \n'
                            'Por conta de das falhas ocorridas, não foram inseridas novas notas. \n'
                            'Segue em anexo, os prints da tela onde ocorreu o impedimento. \n'
                            'Grato pela atenção.'
                        )

                        status_mail_enviar = self.my_mail.mail_enviar(
                            self.user,
                            destinatario,
                            titulo,
                            corpo,
                            path, 
                            arquivos
                        )

                        if status_mail_enviar['status']:
                            self.status = True
                            print(self.sucesso)

                        else:
                            self.status = False
                            print(self.falha)
                            self.my_logger.log_warn('Falha ao enviar o e-mail de comunicação com os print de falhas ocorridas no Fsist.')

                    else:
                        self.status = False
                        print(self.falha)
                        self.my_logger.log_warn('Falha ao listar os arquivos da pasta de falhas do Fsist.')

                else:
                    self.status = False
                    print(self.falha)
                    self.my_logger.log_warn('Falha ao fazer o select da pasta de falhas do Fsist.')

            else:
                self.status = False
                print(self.falha)
                self.my_logger.log_warn('Falha ao fazer o select dos e-mails.')

        except Exception as aviso:
            self.status = False
            print(self.erro)
            print(aviso)

            # Alimentar o log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error(str(aviso))

        return{'status': self.status}
    
    # E-mail para informar erro
    def mail_erro(self):

         # Variaveis
        colunas_filtros = [self.coluna_module, self.coluna_type, self.coluna_name]
        filtros = [self.module_fsist, self.type_subcontrole, self.name_erro]
        titulo = '[RPA] [ECOSSISTEMANF] E-mail de notificação - Erro'

        # TryCatch
        try:

            # Fazer select para buscar e-mails
            status_mail_select = self.my_sql.mysql_select(
                self.user, 
                self.host, 
                self.database, 
                self.coluna_mail, 
                self.tabela_emails
                )

            if status_mail_select['status']:

                destinatario = status_mail_select['resultado'][0]

                # Fazer select para buscar path de pastas no servidor
                status_path_select = self.my_sql.mysql_select(
                    self.user, 
                    self.host,
                    self.database,
                    self.coluna_path,
                    self.tabela_controle,
                    colunas_filtros,
                    filtros 
                )

                if status_path_select['status']:

                    path = status_path_select['resultado'][0]

                    # Listar os arquivos presentes nas pastas do servidor
                    status_listar_arquivos = self.my_folder.listar_arquivos(path)

                    if status_listar_arquivos['status']:

                        arquivos = status_listar_arquivos['resultado'][0]

                        corpo = (
                            'Olá, aqui é o Leonardo Vinci, BOT de automação da Cataguá. \n'
                            'Este é um e-mail de notificação sobre um erro que ocorreu na execução do BOT_Ecossistemanf. \n'
                            'Segue em anexo, o print da tela completa do erro. \n'
                            'Grato pela atenção.'
                        )

                        status_mail_enviar = self.my_mail.mail_enviar(
                            self.user,
                            destinatario,
                            titulo,
                            corpo,
                            path, 
                            arquivos
                        )

                        if status_mail_enviar['status']:
                            self.status = True
                            print(self.sucesso)

                        else:
                            self.status = False
                            print(self.falha)
                            self.my_logger.log_warn('Falha ao enviar o e-mail de comunicação com os print de erros ocorridos na execução do BOT_Ecossistemanf.')

                    else:
                        self.status = False
                        print(self.falha)
                        self.my_logger.log_warn('Falha ao listar os arquivos da pasta de erros do Fsist.')

                else:
                    self.status = False
                    print(self.falha)
                    self.my_logger.log_warn('Falha ao fazer o select da pasta de erros do Fsist.')

            else:
                self.status = False
                print(self.falha)
                self.my_logger.log_warn('Falha ao fazer o select dos e-mails.')

        except Exception as aviso:
            self.status = False
            print(self.erro)
            print(aviso)

            # Alimentar o log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error(str(aviso))

        return{'status': self.status}

    # Função para verificar se existem arquivos com extensão no caminho  
    def mail_teste(self):

        # Variaveis
        destinatario1 = 'brenno.brossi@catagua.com.br'
        destinatario2 = 'rayssa.souza@catagua.com.br'
        destinatario3 = 'leonardo.vinci@catagua.com.br'
        destinatario4 = 'adriano.gimenes@catagua.com.br'
        destinatario_list = [destinatario1, destinatario2, destinatario3, destinatario4]
        titulo = 'E-mail de teste - 15/01/2024'
        corpo = 'Teste de mensagem'
        path = r'C:\Users\brossi.brenno\Desktop\[RPA] Controle\[RPA] Fsist\[RPA] Download'
        path1 = r'C:\Users\brossi.brenno\Desktop\[RPA] Controle\[RPA] Fsist\[RPA] Download\teste1.txt'
        path2 = r'C:\Users\brossi.brenno\Desktop\[RPA] Controle\[RPA] Fsist\[RPA] Download\teste2.log'
        path_list = [path1, path2]
        arquivo1 = 'teste1.txt'
        arquivo2 = 'teste2.log'
        arquivo_list = [arquivo1, arquivo2]

        # TryCtach
        try:

            # Buscar caminho da pasta download
            status_mail_enviar = self.my_mail.mail_enviar(self.user, destinatario1, titulo, corpo, path, arquivo_list)

            if status_mail_enviar['status']:
                self.status = True
                print(self.sucesso)

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