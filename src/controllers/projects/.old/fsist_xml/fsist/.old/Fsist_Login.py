from modulos.mylogger.mylogger import MyLogger
from modulos.mysql.mysql import MySQL
from modulos.myweb.myweb import MyWeb
from procedimentos.ecossistemanf.fsist.Fsist_Avisos import FsistAvisos

class FsistLogin():
        
    def __init__(self, my_driver, 
                 user, host, database, id, module_fsist, name_fsist, 
                 coluna_id, coluna_user, coluna_module, coluna_name, coluna_url, coluna_login, coluna_password,
                 tabela_credenciais, tabela_fsist_parametros):

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
        self.my_web = MyWeb(my_driver)
        self.fsist_avisos = FsistAvisos(my_driver, user, host, database, id, coluna_id, tabela_fsist_parametros)

        # Variaveis especificas
        self.user = user
        self.host = host
        self.database = database

        # Valores
        self.id = id
        self.module_fsist = module_fsist
        self.name_fsist = name_fsist

        # Colunas
        self.coluna_id = coluna_id
        self.coluna_user = coluna_user
        self.coluna_module = coluna_module
        self.coluna_name = coluna_name
        self.coluna_url = coluna_url
        self.coluna_login = coluna_login
        self.coluna_password = coluna_password

        # Tabelas
        self.tabela_credenciais = tabela_credenciais
        self.tabela_parametros = tabela_fsist_parametros
    
    # Função para fazer o SELECT
    def fsist_login(self):

        # Variaveis
        coluna_parametros = ['class_entrar', 'id_usuario', 'id_senha', 'id_entrar']
        coluna_credenciais = [self.coluna_url, self.coluna_login, self.coluna_password]
        filtro_coluna_fsist = [self.coluna_user, self.coluna_module, self.coluna_name]
        filtro_fsist = [self.user, self.module_fsist, self.name_fsist]

        # TryCtach
        try:

            # Credenciais
            status_mysql_credenciais = self.my_sql.mysql_select(
                self.user, 
                self.host,
                self.database,
                coluna_credenciais, 
                self.tabela_credenciais, 
                filtro_coluna_fsist, 
                filtro_fsist
                )

            if status_mysql_credenciais['status']:

                lista_credenciais = status_mysql_credenciais['resultado']

                url = lista_credenciais[0]
                login = lista_credenciais[1]
                senha = lista_credenciais[2]

                # Parametros
                status_mysql_parametros = self.my_sql.mysql_select(
                    self.user, 
                    self.host,
                    self.database,
                    coluna_parametros, 
                    self.tabela_parametros, 
                    self.coluna_id, 
                    self.id
                    )

                if status_mysql_parametros['status']:

                    lista_parametros = status_mysql_parametros['resultado']

                    class_entrar = lista_parametros[0]
                    id_usuario = lista_parametros[1]
                    id_senha = lista_parametros[2]
                    id_entrar = lista_parametros[3]

                    print('url')
                    print(url)
                    print('lista_parametros')
                    print(lista_parametros)

                    # Abrir navegador
                    status_navegador_abrir = self.my_web.browser_open(url)
                    
                    if status_navegador_abrir['status']:

                        # Verificar mensagem de site falso
                        status_mensagem_site_falso = self.fsist_avisos.aviso_site_falso()

                        if status_mensagem_site_falso['status']:

                            # Pesquisar e clicar
                            status_elemento = self.my_web.class_click(class_entrar)

                            if status_elemento['status']:

                                status_elemento = self.my_web.id_click(id_usuario)

                                if status_elemento['status']:

                                    # Digitar texto
                                    status_elemento = self.my_web.type_text(login)

                                    if status_elemento['status']:

                                        status_elemento = self.my_web.id_click(id_senha)

                                        if status_elemento['status']:

                                            status_elemento = self.my_web.type_text(senha)

                                            if status_elemento['status']:

                                                status_elemento = self.my_web.id_click(id_entrar)

                                                if status_elemento['status']:
                                                    
                                                    self.status = True
                                                    print(self.sucesso)
                                            
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