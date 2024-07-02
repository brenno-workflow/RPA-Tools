from modulos.mylogger.mylogger import MyLogger
from modulos.mysql.mysql import MySQL
from modulos.myweb.myweb import MyWeb

class FsistAvisos:
        
    def __init__(self, 
                 my_driver, user, host, database, id, 
                 coluna_id, 
                 tabela_fsist_parametros):

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

        # Variaveis especificas
        self.user = user
        self.host = host
        self.database = database

        # valores
        self.id = id

        # Colunas
        self.coluna_id = coluna_id

        # Tabelas
        self.tabela_parametros = tabela_fsist_parametros

    # Avisos que impedem o clique da pagina
    def fsist_avisos(self):

        # Query - Parametros
        coluna_parametros = ['class_mensagem', 'xpath_mensagem_fechar']

        try:

            # Parametros
            status_mysql_parametros = self.my_sql.mysql_select(
                self.user, 
                self.host,
                self.database,
                coluna_parametros, 
                self.tabela_parametros, 
                self.coluna_id, self.id
                )

            if status_mysql_parametros['status']:

                lista_parametros = status_mysql_parametros['resultado']

                class_mensagem = lista_parametros[0]
                xpath_mensagem_fechar = lista_parametros[1]

                # Pesquisar e clicar
                status_elemento = self.my_web.class_find(class_mensagem)

                if status_elemento['status']:

                    status_elemento = self.my_web.xpath_click(xpath_mensagem_fechar)
                    
                    if status_elemento['status']:

                        self.status = True
                        print(self.sucesso)

                else:
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
    
    # Avisos que impedem o clique da pagina
    def aviso_site_falso(self):

        # Query - Parametros
        coluna_parametros = ['class_mensagem', 'id_mensagem_ok']

        try:

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

                class_mensagem = lista_parametros[0]
                id_mensagem_ok = lista_parametros[1]

                # Pesquisar e clicar
                status_elemento = self.my_web.class_find(class_mensagem)

                if status_elemento['status']:

                    status_elemento = self.my_web.id_click(id_mensagem_ok)
                    
                    if status_elemento['status']:

                        self.status = True
                        print(self.sucesso)

                    else:
                        self.status = False
                        print(self.falha)

                else:
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