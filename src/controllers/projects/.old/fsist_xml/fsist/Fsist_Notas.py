from modules.mylogger.mylogger import MyLogger
from controllers.projects.fsist_xml.ecossistemanf.Ecossistemanf_Chaves import EcossistemanfChaves
from controllers.projects.fsist_xml.fsist.Fsist_Excel import FsistExcel
from modules.mysql.mysql import MySQL
from modules.myfile.myfile import MyFile
from modules.myweb.myweb import MyWeb
import time

class FsistNotas:
        
    def __init__(self, 
                 my_driver,user, password, host, database,
                 column_fluxos_id, column_status_id, column_url, column_login, column_password,
                 column_control_id, column_control_path,
                 table_fluxos, table_status, table_fluxoscontrol, table_control, table_fluxosweb, table_sites, table_credentials,
                 param_control, param_true, param_ecossistema_ativas, param_ecossistemanf_cancelada, param_control_fsist_sucesso, folder_download,
                 barra_pesquisa, btn_buscar, btn_select_all, btn_download, download_xml, btn_apontamento, password_nfcancelada, chave_nfcancelada
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
        self.my_file = MyFile()
        # Metodo de 'INJEÇÃO DE DEPENDENCIA'
        # ref.: https://www.youtube.com/watch?v=5DBfVnQn1Ow
        self.my_web = MyWeb(my_driver)
        self.fsist_excel = FsistExcel(user, password, host, database,
                 column_fluxos_id, column_status_id,
                 column_control_id, column_control_path,
                 table_fluxos, table_status, table_fluxoscontrol, table_control,
                 param_control, param_true,
                 folder_download)
        self.chaves = EcossistemanfChaves(user, password, host, database, 
                 column_fluxos_id, column_status_id,
                 column_url, column_login, column_password,
                 table_fluxos, table_status, table_fluxosweb, table_sites, table_credentials,
                 param_ecossistema_ativas, param_true)
        
         # Variaveis especificas
        self.user = user
        self.password = password
        self.host = host
        self.database = database

        # Colunas
        self.column_url = column_url
        self.column_login = column_login
        self.column_password = column_password
        self.column_control_path = column_control_path

        # ID
        self.column_fluxos_id = column_fluxos_id
        self.column_status_id = column_status_id
        
        # Tabela SELECT
        self.table_fluxos = table_fluxos
        self.table_status = table_status
        self.table_sites = table_sites
        self.table_credentials = table_credentials
        self.table_fluxosweb = table_fluxosweb
        self.table_control = table_control
        self.table_fluxoscontrol = table_fluxoscontrol

        self.ecossistema_cancelada = param_ecossistemanf_cancelada
        self.param_true = param_true
        self.param_control_fsist_sucesso = param_control_fsist_sucesso

        self.barra_pesquisa = barra_pesquisa
        self.btn_buscar = btn_buscar
        self.btn_select_all = btn_select_all    
        self.btn_download = btn_download
        self.download_xml = download_xml
        self.btn_apontamento = btn_apontamento
        self.password_nfcancelada = password_nfcancelada
        self.chave_nfcancelada = chave_nfcancelada
    # ------------------------------------ CHAVES ATIVAS ------------------------------------
    
    # Fazer o filtro de chaves ativas e deixar na caixa de busca
    def fsist_notas_ativas(self):

        # Try Catch
        try:
            column_id = [self.table_control, self.column_control_path]
            column_control_id = [column_id]

            # Lista de filtros
            column_id_fluxos = [self.table_fluxos, self.column_fluxos_id]
            column_id_status = [self.table_status, self.column_status_id]
            column_filter_id = [column_id_fluxos, column_id_status]

            # Lista de colunas_filtro
            filter_id = [self.param_control_fsist_sucesso, self.param_true]

            # SELECT - Controle
            status_mysql_controle = self.my_sql.mysql_select(
                self.user,
                self.password,
                self.host,
                self.database,
                self.table_fluxoscontrol,
                column_control_id,
                column_filter_id,
                filter_id,
                True
                )
            if status_mysql_controle['status']:
                resultado = status_mysql_controle['resultado']
                print(resultado)
                
                sucess_control = resultado[0][0]
                self.my_logger.log_info(sucess_control)
                condition = 'Status == "Autorizada" and `Tem XML` == "Sim"'
                subcondition = 'Chave'
                status_excel_fsist = self.fsist_excel.excel(condition, subcondition)
                
                if status_excel_fsist['status']:
                    # Pegar lista de resultados
                    resultados_excel = status_excel_fsist['resultado']
                    print(resultados_excel)

                    # Verificar se não houveram novas
                    status_ecossistema_chaves = self.chaves.ecossistemanf_chaves()
                    resultado_chaves = status_ecossistema_chaves['resultado']
                    
                    novas_chaves = []
                    if status_ecossistema_chaves['status']:
                        for i in resultados_excel:
                            if i not in resultado_chaves:
                                novas_chaves.append(i)
                            else:
                                continue
                
                        status_txt_chaves = self.my_file.files(sucess_control, '.txt', 'write', None, novas_chaves, 'chaves_ativas')
                        if status_txt_chaves['status']:
                            if novas_chaves != []:
                                self.my_logger.log_info(novas_chaves)

                                lista_chaves = ', '.join(novas_chaves)            
                                status_barra_pesquisar = self.my_web.element(self.barra_pesquisa, 'id', 'click', 'send_keys', lista_chaves)
                                if status_barra_pesquisar['status']:
                                    status_btn_buscar = self.my_web.element(self.btn_buscar, 'id', 'find', 'click')
                
                                    if status_btn_buscar['status']:
                                        status_select_all = self.my_web.element(self.btn_select_all, 'id', 'find', 'click')

                                        if status_select_all['status']:
                                            status_btn_download = self.my_web.element(self.btn_download, 'id', 'find', 'click')
                                            
                                            if status_btn_download['status']:
                                                status_download_xml = self.my_web.element(self.download_xml, 'xpath', 'find', 'click')

                                                time.sleep(8)
                                                if status_download_xml['status']:
                                                    self.status = True
                                                else:
                                                    self.status = False
                                            else:
                                                self.status = False
                                        else:
                                            self.status = False
                                    else:
                                        self.status = False
                                else:
                                    self.status = False            
                            else:
                                mensagem = 'Não foi encontrado nenhuma nova chave'
                                self.my_logger.log_info(mensagem)
                                self.status = True
                        else:
                            mensagem = 'txt com as chaves não foi criado'
                            print(mensagem)
                            self.my_logger.log_warn(mensagem)
                            self.status = False
                else:     
                    self.status = False

            else:
                self.status = False
            
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

        return {'status': self.status}
    
    # ------------------------------------ CHAVES CANCELADAS ------------------------------------

    # Fazer o filtro de chaves ativas e deixar na caixa de busca
    def fsist_notas_canceladas(self):

        # Try Catch
        try:
            column_id = [self.table_control, self.column_control_path]
            column_control_id = [column_id]

            # Lista de filtros
            column_id_fluxos = [self.table_fluxos, self.column_fluxos_id]
            column_id_status = [self.table_status, self.column_status_id]
            column_filter_id = [column_id_fluxos, column_id_status]

            # Lista de colunas_filtro
            filter_id = [self.param_control_fsist_sucesso, self.param_true]

            # SELECT - Controle
            status_mysql_controle = self.my_sql.mysql_select(
                self.user,
                self.password,
                self.host,
                self.database,
                self.table_fluxoscontrol,
                column_control_id,
                column_filter_id,
                filter_id,
                True
                )
            if status_mysql_controle['status']:
                resultado = status_mysql_controle['resultado']
                print(resultado)

                sucess_control = resultado[0][0]
                # Lista de colunas site e credenciais
                column_url = [self.table_sites, self.column_url]
                column_password = [self.table_credentials, self.column_password]
                column_site_credential = [column_url, column_password]

                # Lista de filtros
                column_id_fluxos = [self.table_fluxos, self.column_fluxos_id]
                column_id_status = [self.table_status, self.column_status_id]
                column_filter_id = [column_id_fluxos, column_id_status]

                # Lista de colunas_filtro
                filter_id = [self.ecossistema_cancelada, self.param_true]

                # Parametros
                status_mysql_parametros = self.my_sql.mysql_select(
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
                if status_mysql_parametros['status']:
                    resultado = status_mysql_parametros['resultado']
                    print(resultado)

                    # Atualizar variaveis
                    url = resultado[0][0]
                    password = resultado[1][0]
            
                    condition = 'Status == "Cancelada"'
                    subcondition = 'Chave'
                    status_excel_fsist = self.fsist_excel.excel(condition, subcondition)

                    if status_excel_fsist['status']:
                        status_web_cancelada = self.my_web.browser('get', None, url)
                        if status_web_cancelada['status']:
                            chaves_canceladas = status_excel_fsist['resultado']
                            status_txt_chaves = self.my_file.files(sucess_control, '.txt', 'write', None, chaves_canceladas, "chaves_canceladas")

                            if status_txt_chaves['status']:
                                for i in chaves_canceladas:
                                    status_elemento = self.my_web.element(self.chave_nfcancelada, 'id', 'find', 'send_keys', i)
                                    if status_elemento['status']:
                                        status_elemento = self.my_web.element(self.password_nfcancelada, 'id', 'find', 'send_keys', password)
                                        if status_elemento['status']:
                                            status_elemento = self.my_web.element(self.btn_apontamento, 'id', 'find', 'click')
                                            self.status = True
                                        else:
                                            self.status = False
                                            break    
                            else:
                                mensagem = 'Não foi possivel criar o txt com as chaves canceladas'
                                print(mensagem)
                                self.my_logger.log_warn(mensagem)
                                self.status = False
                        else:
                            mensagem = f'Não foi possivel acessar a url: {url}'
                            self.status = False
                    else:
                        self.status = False
                        mensagem = 'Erro ao selecionar chaves no excel' 

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

        return {'status': self.status}
