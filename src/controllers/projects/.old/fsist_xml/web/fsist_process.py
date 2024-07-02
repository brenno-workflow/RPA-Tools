from modules.mylogger.mylogger import MyLogger
from modules.myfolder.myfolder import MyFolder
from modules.myweb.myweb import MyWeb
from modules.mysql.mysql import MySQL
from controllers.projects.fsist_xml.control import Controle_Limpar
from controllers.projects.fsist_xml.ecossistemanf import Ecossistemanf_Servidor, Ecossistemanf_Chaves, Ecossistemanf_Unzip
from controllers.projects.fsist_xml.fsist import Fsist_Ciencia, Fsist_Periodo, Fsist_Relatorio, Fsist_Print, Fsist_Login, Fsist_Notas
import os
class FsistProcess():
    def __init__(self, 
                 webdriver, 
                 user, password, host, database, 
                 column_fluxos_id, column_status_id, column_url, column_login, column_password, column_control_id, column_control_path, column_path_servers, column_id_servers,
                 table_fluxos, table_status, table_fluxosweb, table_sites, table_credentials, table_fluxoscontrol, table_control, table_fluxosserver, table_servers,
                 param_web_fsist, param_true, param_control_fsist_download, param_web_ecossistemanf_autorizada, param_web_ecossistemanf_cancelada, param_control_fsist, param_server_fsist, param_control_fsist_sucesso, param_control_fsist_falha, param_control,
                 input_user, input_password, 
                 btn_login, btn_entrar, btn_data,  btn_confirmar, btn_sim, btn_download, btn_ciencia, btn_cancel, btn_select_all, btn_relatorio, btn_gerar_relatorio, btn_buscar, btn_ok,
                 dias_ativas, dias_cancelada, data_inicial, barra_pesquisa, element_msg, checkbox_xml, download_xml, chave_nfcancelada, password_nfcancelada, btn_apontamento, data_download, extensao_png,
                 folder_download
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
        self.my_folder = MyFolder()
        self.my_sql = MySQL()

        # Metodo de 'INJEÇÃO DE DEPENDENCIA'
        # ref.: https://www.youtube.com/watch?v=5DBfVnQn1Ow
        self.my_web = MyWeb(webdriver)

        self.fsist_login = Fsist_Login.FsistLogin(
        webdriver, 
        user, password, host, database, 
        column_fluxos_id, column_status_id,
        column_url, column_login, column_password,
        table_fluxos, table_status, table_fluxosweb, table_sites, table_credentials,
        param_web_fsist, param_true,
        input_user, input_password, btn_login, btn_entrar
        )
        self.fsist_periodo = Fsist_Periodo.FsistPeriodo(
        webdriver, 
        dias_ativas, dias_cancelada, btn_data, data_inicial, btn_confirmar, barra_pesquisa
        )
        self.fsist_ciencia = Fsist_Ciencia.FsistCiencia(
        webdriver, 
        btn_select_all, btn_download, element_msg, btn_ciencia, btn_cancel, btn_sim, btn_ok, data_download
        )
        self.fsist_relatorio = Fsist_Relatorio.FsistRelatorio(
        webdriver,
        user, password, host, database,
        btn_select_all, btn_relatorio, checkbox_xml, btn_gerar_relatorio, btn_sim,
        column_fluxos_id, column_status_id, column_control_id, column_control_path,
        table_fluxos, table_status, table_fluxoscontrol, table_control, 
        param_control_fsist_download, param_true, folder_download,
        )
        self.fsist_notas = Fsist_Notas.FsistNotas(
        webdriver, 
        user, password, host, database, 
        column_fluxos_id, column_status_id, column_url, column_login, 
        column_password, column_control_id, column_control_path, 
        table_fluxos, table_status, table_fluxoscontrol, table_control, table_fluxosweb, table_sites, table_credentials, 
        param_control_fsist , param_true, param_web_ecossistemanf_autorizada, param_web_ecossistemanf_cancelada, param_control_fsist_sucesso, folder_download,
        barra_pesquisa, btn_buscar, btn_select_all, btn_download, download_xml, btn_apontamento, password_nfcancelada, chave_nfcancelada,
        )
        self.controle_limpar = Controle_Limpar.ControleLimpar(
        user, password, host, database, 
        column_fluxos_id, column_status_id,
        column_control_id, column_control_path,
        table_fluxos, table_status, table_fluxoscontrol, table_control,
        param_control_fsist_download, param_true,
        )
        self.ecossistema_chaves = Ecossistemanf_Chaves.EcossistemanfChaves(
        user, password, host, database, 
        column_fluxos_id, column_status_id,
        column_url, column_login, column_password,
        table_fluxos, table_status, table_fluxosweb, table_sites, table_credentials,
        param_web_ecossistemanf_autorizada, param_true,
        
        )
        self.fsist_verificar_arquivos = Ecossistemanf_Servidor.EcossistemanfServidor(
        user, password, host, database, 
        column_fluxos_id, column_status_id, column_path_servers, 
        table_fluxos, table_status, table_fluxosserver, table_servers, param_true, param_server_fsist,
        )
        self.ecossistema_unzip = Ecossistemanf_Unzip.EcossistemanfUnzip(
        user, password, host, database, 
        column_fluxos_id, column_status_id, column_id_servers, column_path_servers, column_control_path, 
        table_fluxos, table_status, table_fluxosserver, table_servers, table_control, table_fluxoscontrol, 
        param_server_fsist, param_control_fsist_download, param_true,
        )
        self.fsist_print = Fsist_Print.FsistPrint(
        webdriver, 
        user, password, host, database, 
        table_control, table_fluxos, table_status, table_fluxoscontrol,
        column_control_path, column_status_id, column_fluxos_id,
        param_true,
        extensao_png
        )
        
        # Variaveis especificas
        self.user = user
        self.password =  password
        self.host = host
        self.database = database

        # Table
        self.table_fluxoscontrol = table_fluxoscontrol
        self.table_status = table_status
        self.table_fluxos = table_fluxos
        self.table_control = table_control

        # Columns
        self.column_fluxos_id = column_fluxos_id
        self.column_status_id = column_status_id
        self.column_control_path = column_control_path

        # Parametros
        self.param_control_fsist_sucesso = param_control_fsist_sucesso
        self.param_control_fsist_falha = param_control_fsist_falha
        self.param_control_fsist = param_control_fsist
        self.param_control = param_control
        self.param_true = param_true



    def process_fsist_nfativa(self):
        
        try:    
            # Periodo Fsist Ativas
            status_fsist_periodo_ativas = self.fsist_periodo.fsist_periodo_ativas
            #  Ciencia Fsist
            status_fsist_ciencia = self.fsist_ciencia.fsist_ciencia
            # Relatorio Fsist
            status_fsist_relatorio = self.fsist_relatorio.fsist_relatorio
            # Chaves Fsist Ativas
            status_fsist_notas_ativas = self.fsist_notas.fsist_notas_ativas
            # Unzip folder
            status_ecossistemanf_unzip = self.ecossistema_unzip.ecossistemanf_unzip
            # Limpeza Download Folder
            status_limpeza_download = self.controle_limpar.limpar_download


            lista_procedimentos = [
                status_fsist_periodo_ativas,
                status_fsist_ciencia,
                status_fsist_relatorio,
                status_fsist_notas_ativas,
                status_ecossistemanf_unzip,
                status_limpeza_download,
            ]
            
            # Loop de procediemntos 
            for procedimento in lista_procedimentos:

                # Pegar o nome do procedimento
                # VERIFICAR DE USAR O MYNAME PARA ISSO DEPOIS!!!!!!!!!
                procedimento_nome = getattr(procedimento, '__qualname__', str(procedimento))

                # Mensagens
                mensagem_inicial = f'Iniciando o processo do bot: {procedimento_nome}'
                mensagem_sucesso = f'Sucesso ao rodar o bot {procedimento_nome}'
                mensagem_falha = f'Falha ao rodar o bot {procedimento_nome}'
                mensagem_erro = f'Erro ao rodar o bot {procedimento_nome}'

                # Informar qual arquivo está sendo executado no momento
                break_line = '\n--------------------------------------------------------------------------------------------------------------------------------------------------'
                mensagem = mensagem_inicial
                print(mensagem_inicial)
                self.my_logger.log_info(break_line)
                self.my_logger.log_info(mensagem)
                
                # Executar procedimentos em ordem
                status_procedimento = procedimento()

                if status_procedimento['status']:
                    self.status = True
                    mensagem = mensagem_sucesso
                    print(mensagem)

                else:
                    self.status = False
                    mensagem - mensagem_falha
                    print(mensagem)
                    
                    break
                
                # Alimentar o log
                if self.status:
                    self.my_logger.log_info(self.sucesso)
                    self.my_logger.log_info(mensagem)

                else:
                    self.my_logger.log_warn(self.falha)
                    self.my_logger.log_warn(mensagem)

        except Exception as aviso:
            status = False
            mensagem = mensagem_erro
            print(self.erro)
            print(mensagem)
            print(aviso)

            # Alimentar o log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error(mensagem)
            self.my_logger.log_error(str(aviso))

        return{'status': self.status}

    def process_fsist_nfcancelada(self):
        try:    


            # Periodo Fsist Canceladas
            status_fsist_periodo_cancelada = self.fsist_periodo.fsist_periodo_canceladas
            # Relatorio Fsist
            status_fsist_relatorio = self.fsist_relatorio.fsist_relatorio
            # Chaves Fsist Canceladas
            status_fsist_notas_canceladas = self.fsist_notas.fsist_notas_canceladas
            # Limpeza Download Folder
            status_limpeza_download = self.controle_limpar.limpar_download



            lista_procedimentos = [
                status_fsist_periodo_cancelada,
                status_fsist_relatorio,
                status_fsist_notas_canceladas,
                status_limpeza_download,
            ]
            
            # Loop de procediemntos
            for procedimento in lista_procedimentos:

                # Pegar o nome do procedimento
                # VERIFICAR DE USAR O MYNAME PARA ISSO DEPOIS!!!!!!!!!
                procedimento_nome = getattr(procedimento, '__qualname__', str(procedimento))

                # Mensagens
                mensagem_inicial = f'Iniciando o processo do bot: {procedimento_nome}'
                mensagem_sucesso = f'Sucesso ao rodar o bot {procedimento_nome}'
                mensagem_falha = f'Falha ao rodar o bot {procedimento_nome}'
                mensagem_erro = f'Erro ao rodar o bot {procedimento_nome}'

                # Informar qual arquivo está sendo executado no momento
                break_line = '\n--------------------------------------------------------------------------------------------------------------------------------------------------'
                mensagem = mensagem_inicial
                print(mensagem_inicial)
                self.my_logger.log_info(break_line)
                self.my_logger.log_info(mensagem)
                
                # Executar procedimentos em ordem
                status_procedimento = procedimento()

                if status_procedimento['status']:
                    self.status = True
                    mensagem = mensagem_sucesso
                    print(mensagem)

                else:
                    self.status = False
                    mensagem - mensagem_falha
                    print(mensagem)
                    
                    break
                
                # Alimentar o log
                if self.status:
                    self.my_logger.log_info(self.sucesso)
                    self.my_logger.log_info(mensagem)

                else:
                    self.my_logger.log_warn(self.falha)
                    self.my_logger.log_warn(mensagem)

        except Exception as aviso:
            self.status = False
            mensagem = mensagem_erro
            print(self.erro)
            print(mensagem)
            print(aviso)

            # Alimentar o log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error(mensagem)
            self.my_logger.log_error(str(aviso))

        return{'status': self.status}
    
    def nf_process(self):
        try:
            cancelada = 'nf_cancelada'
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
                # Path pasta sucesso controle
                resultado = status_mysql_controle['resultado']
                print(resultado)

                sucess_control_folder = resultado[0][0]

                filter_id = [self.param_control_fsist_falha, self.param_true]
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
                    # Path Falha controle
                    fail_control_folder = resultado[0][0]

                    # Função para verificar se existem arquivos nas pastas ['PDFs', 'XMLs']
                    status_verificar_arquivos = self.fsist_verificar_arquivos.verficar_arquivos()

                    if status_verificar_arquivos['status']:
                        # Função de Login no fsist
                        fsist_login = self.fsist_login.fsist_login()

                        if fsist_login['status']:
                            # Processo NF Ativa
                            status_nf_ativa = self.process_fsist_nfativa()

                            if status_nf_ativa['status']:
                                self.my_logger.log_info('status')
                                self.my_logger.log_info(status_nf_ativa['status'])
                                # Print de sucesso NF Ativa
                                status_print_fsist = self.fsist_print.fsist_print(self.param_control_fsist_sucesso, 'nf_ativa')

                                if status_print_fsist['status']:
                                    self.status = True
                                else:
                                    self.status = False

                            else:
                                # Print de falha NF Ativa

                                status_print_fsist = self.fsist_print.fsist_print(self.param_control_fsist_falha, 'nf_ativa')
                                if status_print_fsist['status']:
                                    self.status = True

                                else:
                                    self.status = False
                                sucess_control_folder_ativa = os.path.join(sucess_control_folder,'chaves_ativas.txt')
                                # Mover txt para pasta de falhas
                                status_move_txt = self.my_folder.folder('move', 'folder', sucess_control_folder_ativa, fail_control_folder,  )
                            # Processo NF Cancelada
                            status_nf_cancelada = self.process_fsist_nfcancelada()
                            if status_nf_cancelada['status']:
                                # Print de sucesso nf cancelada
                                status_print_fsist = self.fsist_print.fsist_print(self.param_control_fsist_sucesso, cancelada)

                                if status_print_fsist['status']:
                                    self.status = True
                                else:
                                    self.status = False

                            else:
                                # Print de falha NF Cancelada
                                status_print_fsist = self.fsist_print.fsist_print(self.param_control_fsist_falha, cancelada)

                                if status_print_fsist['status']:
                                    self.status = True
                                else:
                                    self.status = False
                        else:
                            self.status = False
                            self.my_logger.log_warn("Não foi possivel fazer o login")

                    else:
                        # Função de Login no fsist
                        fsist_login = self.fsist_login.fsist_login()

                        if fsist_login['status']:
                            status_print_fsist = self.fsist_print.fsist_print(self.param_control_fsist_falha, 'servidor_com_arquivos')
                            # Processo NF Cancelada
                            status_nf_cancelada = self.process_fsist_nfcancelada()

                            if status_nf_cancelada['status']:
                                # Print de sucesso NF Cancelada
                                status_print_fsist = self.fsist_print.fsist_print(self.param_control_fsist_sucesso, cancelada)
                                if status_print_fsist['status']:
                                    self.status = True
                                else:
                                    self.status = False

                            else:
                                # Print de falha NF Cancelada
                                status_print_fsist = self.fsist_print.fsist_print(self.param_control_fsist_falha, cancelada)
                                if status_print_fsist['status']:
                                    self.status = True
                                else:
                                    self.status = False
                                    
                                sucess_control_folder_cancelada = os.path.join(sucess_control_folder,'chaves_canceladas.txt')
                                # Move txt para pasta de falhas
                                status_move_png = self.my_folder.folder('move', 'file', sucess_control_folder_cancelada, fail_control_folder)
                                        
                        
                        else:
                            self.status = False
                            self.my_logger.log_warn("Não foi possivel fazer o login")


        except Exception as aviso:
            print(self.erro)
            print(aviso)
        return{'status': self.status}
            

