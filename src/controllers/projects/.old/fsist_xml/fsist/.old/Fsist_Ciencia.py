from modulos.mylogger.mylogger import MyLogger
from modulos.mysql.mysql import MySQL
from modulos.myweb.myweb import MyWeb

class FsistCiencia:
        
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

        # Valores
        self.id = id

        # Colunas
        self.coluna_id = coluna_id

        # Tabelas
        self.tabela_parametros = tabela_fsist_parametros

    # Ciencia
    def fsist_ciencia(self):

        # Query - Parametros
        coluna_parametros = ['id_selecionar_todas', 'id_download', 'class_mensagem', 'id_mensagem_sim', 'xpath_mensagem_efetuar_ciencia', 'xpath_mensagem_cancelar']

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

                id_selecionar_todas = lista_parametros[0]
                id_download = lista_parametros[1]
                class_mensagem = lista_parametros[2]
                id_mensagem_sim = lista_parametros[3]
                xpath_mensagem_efetuar_ciencia = lista_parametros[4]
                xpath_mensagem_cancelar = lista_parametros[5]

                # Pesquisar e clicar
                status_elemento = self.my_web.id_click(id_selecionar_todas)

                if status_elemento['status']:

                    status_elemento = self.my_web.id_click(id_download)

                    if status_elemento['status']:

                        status_elemento = self.my_web.class_find(class_mensagem)
                        
                        if status_elemento['status']:

                            # Se tiver, vai efetuar a ciencia
                            status_elemento = self.my_web.xpath_click(xpath_mensagem_efetuar_ciencia)

                            # Verifica se apareceu a mensagem para baixar
                            status_elemento = self.my_web.class_find(class_mensagem)
                        
                            if status_elemento['status']:

                                # Ira efetuar o cancelamento depois
                                status_elemento = self.my_web.xpath_click(xpath_mensagem_cancelar)

                                if status_elemento['status']:
                                    
                                    # Selecionar todas para limpar
                                    status_elemento = self.my_web.id_click(id_selecionar_todas)

                                    if status_elemento['status']:

                                        status_elemento = self.my_web.id_click(id_mensagem_sim)

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