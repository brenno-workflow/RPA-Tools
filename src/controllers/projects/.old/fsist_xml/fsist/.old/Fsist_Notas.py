from modulos.mylogger.mylogger import MyLogger
from procedimentos.ecossistemanf.fsist.Fsist_Filtro import FsistFiltro
from modulos.mysql.mysql import MySQL
from modulos.myweb.myweb import MyWeb
import time

class FsistNotas:
        
    def __init__(self, 
                 my_driver, user, host, database, id, module_fsist, name_fncanceladas, 
                 coluna_url, coluna_password, coluna_id, coluna_user, coluna_module, coluna_name, coluna_chaves, coluna_status, coluna_xml, coluna_filtro_ativas, coluna_filtro_canceladas, coluna_filtro_tem_xml, 
                 tabela_credenciais, tabela_fsist_parametros, tabela_fncancelada_parametros, tabela_fsist_relatorio, tabela_fsist_relatorio_temp, tabela_ecossistemanf_chaves_temp
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
        self.fsist_filtro = FsistFiltro(
            my_driver, user, host, database, id, 
            coluna_id, coluna_chaves, coluna_status, coluna_xml, coluna_filtro_ativas, coluna_filtro_canceladas, coluna_filtro_tem_xml, 
            tabela_fsist_relatorio, tabela_fsist_relatorio_temp, tabela_ecossistemanf_chaves_temp
            )
        
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
        self.name = name_fncanceladas

        # Colunas
        self.coluna_url = coluna_url
        self.coluna_password = coluna_password
        self.coluna_id = coluna_id
        self.coluna_user = coluna_user
        self.coluna_module = coluna_module
        self.coluna_name = coluna_name
        self.coluna_fsist = ['id_busca', 'id_selecionar_todas', 'id_download', 'class_mensagem', 'xpath_xml_pdf']
        self.colunas_fncanceladas = ['id_chave', 'id_password', 'id_apontamento']

        # Tabelas
        self.tabela_credenciais = tabela_credenciais
        self.tabela_fsist_parametros = tabela_fsist_parametros
        self.tabela_fncanceladas_parametros = tabela_fncancelada_parametros

    # ------------------------------------ CHAVES ATIVAS ------------------------------------
    
    # Fazer o filtro de chaves ativas e deixar na caixa de busca
    def fsist_notas_ativas(self):

        # Variaveis
        status = 'ativas'

        # Try Catch
        try:

            # Chamar função para filtrar chaves ativas
            status_filtro_chaves = self.fsist_filtro.fsist_filtro_chaves(status)

            if status_filtro_chaves['status']:

                # Pegar lista de resultados
                lista_resultados = status_filtro_chaves['resultado']
                print('Aqui -------------- lista de resultados')
                print(lista_resultados)

                # Verificar se não houveram novas
                if lista_resultados == []:
                    self.status = True
                    print(self.sucesso)

                else:

                    # Fazer o select dos paramentros
                    status_mysql_parametros = self.my_sql.mysql_select(
                        self.user, 
                        self.host,
                        self.database,
                        self.coluna_fsist, 
                        self.tabela_fsist_parametros, 
                        self.coluna_id, 
                        self.id
                        )

                    if status_mysql_parametros['status']:

                        # Pegar o nome das colunas no banco de dados
                        id_busca = status_mysql_parametros['resultado'][0]
                        id_selecionar_todas = status_mysql_parametros['resultado'][1]
                        id_download = status_mysql_parametros['resultado'][2]
                        class_mensagem = status_mysql_parametros['resultado'][3]
                        xpath_xml_pdf = status_mysql_parametros['resultado'][4]

                        # Clicar na aba de busca
                        status_elemento = self.my_web.id_click(id_busca)

                        if status_elemento['status']:

                            # Digitar chave
                            status_elemento = self.my_web.type_text(lista_resultados)

                            if status_elemento['status']:

                                status_elemento = self.my_web.send_keys_enter()

                                if status_elemento['status']:

                                    time.sleep(5)

                                    status_elemento = self.my_web.id_click(id_selecionar_todas)

                                    if status_elemento['status']:

                                        status_elemento = self.my_web.id_click(id_download)

                                        if status_elemento['status']:

                                            status_elemento = self.my_web.class_find(class_mensagem)

                                            if status_elemento['status']:

                                                status_elemento = self.my_web.xpath_click(xpath_xml_pdf)

                                                if status_elemento['status']:

                                                    time.sleep(5)

                                                    # Clicar na aba de busca
                                                    status_elemento = self.my_web.id_click(id_busca)

                                                    if status_elemento['status']:

                                                        # Criar texto de espaço
                                                        espaco = ' '

                                                        # Digitar espaço para limpar a caixa
                                                        status_elemento = self.my_web.type_text(espaco)

                                                        if status_elemento['status']:

                                                            status_elemento = self.my_web.send_keys_enter()

                                                            if status_elemento['status']:

                                                                time.sleep(2)
                                                    
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
    
    # ------------------------------------ CHAVES CANCELADAS ------------------------------------

    # Fazer o filtro de chaves ativas e deixar na caixa de busca
    def fsist_notas_canceladas(self):

        # Variaveis
        status = 'canceladas'
        colunas_credenciais = [self.coluna_url, self.coluna_password]
        filtro_colunas_credenciais = [self.coluna_module, self.coluna_name]
        filtro_credenciais = [self.module, self.name]

        # Try Catch
        try:

            # Chamar função para filtrar chaves ativas
            status_filtro_chaves = self.fsist_filtro.fsist_filtro_chaves(status)

            if status_filtro_chaves['status']:

                # Pegar lista de resultados
                lista_resultados = status_filtro_chaves['resultado']
                print('lista_resultados')
                print(lista_resultados)

                # Verificar se não houveram novas
                if lista_resultados == []:
                    self.status = True
                    print(self.sucesso)

                else:

                    # Fazer o select das credenciais
                    status_mysql_credenciais = self.my_sql.mysql_select(
                        self.user, 
                        self.host,
                        self.database,
                        colunas_credenciais, 
                        self.tabela_credenciais, 
                        filtro_colunas_credenciais, 
                        filtro_credenciais
                        )

                    if status_mysql_credenciais['status']:

                        url = status_mysql_credenciais['resultado'][0]
                        password = status_mysql_credenciais['resultado'][1]

                        # Fazer o select dos paramentros
                        status_mysql_parametros = self.my_sql.mysql_select(
                            self.user, 
                            self.host,
                            self.database,
                            self.colunas_fncanceladas, 
                            self.tabela_fncanceladas_parametros, 
                            self.coluna_id, 
                            self.id
                            )

                        if status_mysql_parametros['status']:

                            # Pegar o nome das colunas no banco de dados
                            id_chave = status_mysql_parametros['resultado'][0]
                            id_password = status_mysql_parametros['resultado'][1]
                            id_apontamento = status_mysql_parametros['resultado'][2]

                            for chave in lista_resultados:

                                # Abrir fncancelada
                                abrir_navegador = self.my_web.browser_open(url)

                                if abrir_navegador['status']:

                                    # Clicar na aba de chave
                                    status_elemento = self.my_web.id_click(id_chave)

                                    if status_elemento['status']:

                                        # Digitar a chave
                                        status_elemento = self.my_web.type_text(chave)

                                        if status_elemento['status']:

                                            # Clicar na aba de password
                                            status_elemento = self.my_web.id_click(id_password)

                                            if status_elemento ['status']:

                                                # Digitar a chave
                                                status_elemento = self.my_web.type_text(password)

                                                if status_elemento['status']:

                                                    # Clicar no apontamento
                                                    status_elemento = self.my_web.id_click(id_apontamento)

                                                    if status_elemento['status']:
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
    
