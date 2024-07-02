from modules.mylogger.mylogger import MyLogger
from modules.mysql.mysql import MySQL
from modules.myweb.myweb import MyWeb
import time
import os

class FsistRelatorio:
        
    def __init__(self, 
                 driver, 
                 user, password, host, database, 
                 btn_select_all, btn_relatorio, checkbox_xml, btn_gerar_relatorio, btn_sim,
                 column_fluxos_id, column_status_id,
                 column_control_id, column_control_path,
                 table_fluxos, table_status, table_fluxoscontrol, table_control,
                 param_control, param_true,
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
        self.my_sql = MySQL()
        
        # Metodo de 'INJEÇÃO DE DEPENDENCIA'
        # ref.: https://www.youtube.com/watch?v=5DBfVnQn1Ow
        self.my_web = MyWeb(driver)

        # Variaveis especificas
        self.user = user
        self.password =  password
        self.host = host
        self.database = database

        # ID
        self.column_fluxos_id = column_fluxos_id
        self.column_status_id = column_status_id

        # Parametros        
        self.param_control = param_control
        self.param_true = param_true

        # Tabelas
        self.table_fluxos = table_fluxos
        self.table_status = table_status
        self.table_fluxoscontrol = table_fluxoscontrol
        self.table_control = table_control

        # Colunas
        self.column_control_id = column_control_id
        self.column_control_path = column_control_path        

        # Pastas
        self.folder = folder_download
        self.btn_select_all = btn_select_all
        self.btn_relatorio = btn_relatorio
        self.checkbox_xml = checkbox_xml
        self.btn_gerar_relatorio = btn_gerar_relatorio 
        self.btn_sim = btn_sim

    # Configurar caminho de donwload do fsist
    def fsist_relatorio(self):
    
                
        try:
            column_id = [self.table_control, self.column_control_path]
            column_control_id = [column_id]

            # Lista de filtros
            column_id_fluxos = [self.table_fluxos, self.column_fluxos_id]
            column_id_status = [self.table_status, self.column_status_id]
            column_filter_id = [column_id_fluxos, column_id_status]


            # Lista de colunas_filtro
            filter_id = [self.param_control, self.param_true]

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

                id_control = resultado[0][0]
                print(id_control)
                download_path = id_control
                # Atualizar diretorio de donwload
                status_navegador_download = self.my_web.browser('command_executor', 'download', download_path)
                self.my_logger.log_info(status_navegador_download['resultado'])
                
                if status_navegador_download['status']:
                    status_elemento = self.my_web.element(self.btn_select_all, 'id', 'find', 'click')

                    if status_elemento['status']:
                        # Pesquisar e clicar
                        status_elemento = self.my_web.element(self.btn_relatorio, 'id', 'find', 'click')
                        if status_elemento['status']:

                            # Verificar se a checkbox já está marcada
                            time.sleep(0.2)
                            status_elemento = self.my_web.element(self.checkbox_xml, 'xpath', 'checkbox', 'is_selected')

                            if status_elemento['status']:
                                print(self.btn_gerar_relatorio)
                                status_elemento_relatorio = self.my_web.element(self.btn_gerar_relatorio, 'xpath', 'find', 'click')

                            else:
                                time.sleep(2)
                                print(self.checkbox_xml)
                                status_elemento = self.my_web.element(self.checkbox_xml, 'xpath', 'find', 'click')

                                if status_elemento['status']:
                                    status_elemento_relatorio = self.my_web.element(self.btn_gerar_relatorio, 'xpath', 'find', 'click')
                                    if status_elemento_relatorio['status']:
                                        pass

                                    else:
                                        self.status = False
                                else:
                                    mensagem = "Falha ao selecionar a checkbox"
                                    self.status = False

                            if status_elemento_relatorio['status']:
                                status_elemento = self.my_web.element(self.btn_select_all, 'id', 'find', 'click')
                                
                                if status_elemento['status']:
                                    status_elemento = self.my_web.element(self.btn_sim, 'id', 'click')
                                    
                                    if status_elemento['status']:
                                        mensagem = "todas as etapas foram concluidas"
                                        self.status = True
                                    else:
                                        mensagem = "Falha ao tirar a seleção das notas"
                                        self.status = False
                                        
                            else:
                                mensagem = "Falha ao baixar o relatório"                                
                                self.status = False
                                
                        else:
                            mensagem = "Erro ao localizar elemento web"
                            self.status = False
                    
                    else:
                        mensagem = "Erro ao localizar elemento web"
                        self.status = False
                else:
                    mensagem = "Erro ao definir diretório de download"
                    self.status = False

            else:
                mensagem = "Não foi possivel realizar a consulta SQL"
                self.status = False
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
            print(aviso)

            # Alimentar o log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error(str(aviso))

        return{'status': self.status}