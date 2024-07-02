from modulos.mylogger.mylogger import MyLogger
from modulos.mysql.mysql import MySQL
from modulos.myweb.myweb import MyWeb
from datetime import datetime, timedelta

class FsistPeriodo:
        
    def __init__(self, my_driver, 
                 user, host, database, id, module_fsist, type_subcontrole, 
                 coluna_id, coluna_module, coluna_type, coluna_dias_ativas, coluna_dias_canceladas,
                 tabela_fsist_parametros, tabela_fsist_relatorio):

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
        self.module = module_fsist
        self.type = type_subcontrole
        self.data_ativas = None
        self.data_canceladas = None

        # Colunas
        self.coluna_id = coluna_id
        self.coluna_module = coluna_module
        self.coluna_type = coluna_type
        self.coluna_dias_ativas = coluna_dias_ativas
        self.coluna_dias_canceladas = coluna_dias_canceladas

        # Tabelas
        self.tabela_parametros = tabela_fsist_parametros
        self.tabela_relatorio = tabela_fsist_relatorio

    # Datas
    def fsist_datas(self):

        # Query - Datas
        coluna_filtro_relatorio = [self.coluna_module, self.coluna_type]
        filtro_relatorio = [self.module, self.type]
        coluna_datas = [self.coluna_dias_ativas, self.coluna_dias_canceladas]

        # TryCtach
        try:
            
            # Datas
            status_mysql_datas = self.my_sql.mysql_select(
                self.user, 
                self.host,
                self.database,
                coluna_datas, 
                self.tabela_relatorio, 
                coluna_filtro_relatorio, 
                filtro_relatorio
                )

            if status_mysql_datas['status']:

                lista_datas = status_mysql_datas['resultado']

                dias_ativas = lista_datas[0]
                dias_canceladas = lista_datas[1]

                # Data atual
                data_atual = datetime.now()
                print(data_atual)

                # Data ativas
                self.data_ativas = (data_atual - timedelta(dias_ativas)).strftime('%d/%m/%Y')
                print(self.data_ativas)

                # Data ativas
                self.data_canceladas = (data_atual - timedelta(dias_canceladas)).strftime('%d/%m/%Y')
                print(self.data_canceladas)

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

        return{'status': self.status, 'data_ativas': self.data_ativas, 'data_canceladas': self.data_canceladas}

    # Periodo
    def fsist_periodo_ativas(self):

        # Query - Parametros
        coluna_parametros = ['id_periodo', 'id_data_inicial', 'xpath_periodo_confirmar']

        try:

            # Chamar a função de datas
            status_datas = self.fsist_datas()

            if status_datas['status']:

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

                    id_periodo = lista_parametros[0]
                    id_data_inicial = lista_parametros[1]
                    xpath_periodo_confirmar = lista_parametros[2]

                    # Pesquisar e clicar
                    status_elemento = self.my_web.id_click(id_periodo)

                    if status_elemento['status']:

                        status_elemento = self.my_web.id_click(id_data_inicial)

                        if status_elemento['status']:

                            status_elemento = self.my_web.type_text(self.data_ativas)
                            
                            if status_elemento['status']:

                                status_elemento = self.my_web.send_keys_enter()

                                if status_elemento['status']:

                                    status_elemento = self.my_web.xpath_click(xpath_periodo_confirmar)

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
    

    # Periodo
    def fsist_periodo_canceladas(self):

        # Query - Parametros
        coluna_parametros = ['id_periodo', 'id_data_inicial', 'xpath_periodo_confirmar']

        try:

            # Chamar a função de datas
            status_datas = self.fsist_datas()

            if status_datas['status']:

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

                    id_periodo = lista_parametros[0]
                    id_data_inicial = lista_parametros[1]
                    xpath_periodo_confirmar = lista_parametros[2]

                    # Pesquisar e clicar
                    status_elemento = self.my_web.id_click(id_periodo)

                    if status_elemento['status']:

                        status_elemento = self.my_web.id_click(id_data_inicial)

                        if status_elemento['status']:
                            
                            status_elemento = self.my_web.type_text(self.data_canceladas)

                            if status_elemento['status']:
                                
                                status_elemento = self.my_web.send_keys_enter()

                                if status_elemento['status']:

                                    status_elemento = self.my_web.xpath_click(xpath_periodo_confirmar)

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