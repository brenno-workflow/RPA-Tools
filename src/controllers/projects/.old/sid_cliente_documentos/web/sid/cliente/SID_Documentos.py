from modules.mylogger.mylogger import MyLogger
from modules.mysql.mysql import MySQL
import time
from controllers.projects.sid_cliente_documentos.server import Server_Mover, Server_Copiar
from controllers.projects.sid_cliente_documentos.web.sid.cliente import SID_Workflow, SID_Pesquisar, SID_Verificar, SID_Anexar, SID_Print

class SIDDocumentos():
        
    def __init__(self, 
                 webdriver, user, password, host, database, 
                 column_fluxos_id, column_status_id,
                 column_url, column_file_name, column_file_folder, column_file_path, column_file_path_old, column_control_path,
                 table_fluxos, table_status, table_fluxosweb, table_sid_cliente_anexos_temp, table_control, table_fluxoscontrol, table_sites,
                 param_sid_cliente, param_true, param_control_sid_cliente_sucesso, param_control_sid_cliente_falha, param_control_sid_cliente_erro,
                 input_pesquisar, button_gerir, input_conteudo_anexos, button_anexos, button_anexar_documento, button_escolher_arquivo, input_data_acontecimento, input_observacao, button_tipo_anexo, button_selecionar_tipo, button_inserir, button_buscar,
                 js_sid_cliente_anexos_table,
                 extension_png
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

        # Variaveis especificas
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.webdriver = webdriver

        # Extensões
        self.extension_png = extension_png

        # Colunas
        self.column_url = column_url
        self.column_file_name = column_file_name
        self.column_file_folder = column_file_folder
        self.column_file_path = column_file_path
        self.column_file_path_old = column_file_path_old
        self.column_control_path = column_control_path
        
        # ID
        self.column_fluxos_id = column_fluxos_id
        self.column_status_id = column_status_id
                
        # Tabela 
        self.table_fluxos = table_fluxos
        self.table_status = table_status
        self.table_sites = table_sites
        self.table_fluxosweb = table_fluxosweb
        self.table_sid_cliente_anexos_temp = table_sid_cliente_anexos_temp
        self.table_control = table_control
        self.table_fluxoscontrol = table_fluxoscontrol

        # Parametros
        self.param_true = param_true
        self.param_sid_cliente = param_sid_cliente
        self.param_control_sid_cliente_sucesso = param_control_sid_cliente_sucesso
        self.param_control_sid_cliente_falha = param_control_sid_cliente_falha
        self.param_control_sid_cliente_erro = param_control_sid_cliente_erro

        # WEB
        self.input_pesquisar = input_pesquisar
        self.button_gerir = button_gerir
        self.input_conteudo_anexos = input_conteudo_anexos
        self.button_anexos = button_anexos
        self.button_anexar_documento = button_anexar_documento
        self.button_escolher_arquivo = button_escolher_arquivo
        self.input_data_acontecimento = input_data_acontecimento
        self.input_observacao = input_observacao
        self.button_tipo_anexo = button_tipo_anexo
        self.button_selecionar_tipo = button_selecionar_tipo
        self.button_inserir = button_inserir
        self.button_buscar = button_buscar

        # Scripts
        self.js_sid_cliente_anexos_table = js_sid_cliente_anexos_table
    
    # Função para verificar se existem arquivos com extensão no caminho  
    def sid_documentos(self):

        # Variaveis
        path_control_status = False
        path_control_list = []

        # TryCtach
        try:

            # Buscar as pastas de controle
            # Coluna Path
            column_path = [[self.table_control, self.column_control_path]]

            # Lista de colunas filtros
            column_id_fluxos = [self.table_fluxos, self.column_fluxos_id]
            column_id_status = [self.table_status, self.column_status_id]
            column_filter_id_fluxos = [column_id_fluxos, column_id_status]
            filter_id_fluxos_sucesso = [self.param_control_sid_cliente_sucesso, self.param_true]
            filter_id_fluxos_falha = [self.param_control_sid_cliente_falha, self.param_true]
            filter_id_fluxos_erro = [self.param_control_sid_cliente_erro, self.param_true]
            filter_id_fluxos = [filter_id_fluxos_sucesso, filter_id_fluxos_falha, filter_id_fluxos_erro]
            
            # Buscar informações do banco de dados
            for filter_id_fluxos_count in filter_id_fluxos:
                status_select_sucesso = self.my_sql.mysql_select(
                    self.user,
                    self.password, 
                    self.host,
                    self.database,
                    self.table_fluxoscontrol,
                    column_path,
                    column_filter_id_fluxos,
                    filter_id_fluxos_count,
                    True
                    )

                if status_select_sucesso['status']:

                    # Retorna a lista de resultados
                    resultado = status_select_sucesso['resultado']
                    print(resultado)

                    path_control_list.append(resultado[0][0])
                    path_control_status = True
                    print('path_control_list')
                    print(path_control_list)
                
                else:
                    path_control_status = False
                    break

            if path_control_status:

                # Lista de colunas - sid_cliente_anexos_temp
                column_file = [self.column_file_name, self.column_file_folder, self.column_file_path, self.column_file_path_old]
                
                # Buscar informações do banco de dados
                status_select_site_credenciais = self.my_sql.mysql_select(
                    self.user,
                    self.password, 
                    self.host,
                    self.database,
                    self.table_sid_cliente_anexos_temp,
                    column_file
                    )

                if status_select_site_credenciais['status']:

                    # Retorna a lista de resultados
                    resultado = status_select_site_credenciais['resultado']
                    print(resultado)

                    # Lista separadas
                    file_name_list = resultado[0]
                    file_folder_list = resultado[1]
                    file_path_list = resultado[2]
                    file_path_old_list = resultado[3]

                    for file_name_list_count, file_folder_list_count, file_path_list_count, file_path_old_list_count in zip(file_name_list, file_folder_list, file_path_list, file_path_old_list):

                        # Subistituir '-' por '/'
                        # Verifica se '-' está presente na string
                        if '-' in file_folder_list_count:
                            # Substitui '-' por '/'
                            file_folder_list_count_web = str(file_folder_list_count).replace('-', '/')
                        else:
                            # Se não houver '-', mantém a string como está
                            file_folder_list_count_web = file_folder_list_count

                        # Parametrizar as funções
                        sid_workflow = SID_Workflow.SIDWorkflow(
                            self.webdriver, self.user, self.password, self.host, self.database, 
                            self.column_fluxos_id, self.column_status_id,
                            self.column_url,
                            self.table_fluxos, self.table_status, self.table_fluxosweb, self.table_sites,
                            self.param_sid_cliente, self.param_true
                        )
                        sid_pesquisar = SID_Pesquisar.SIDPesquisar(
                            self.webdriver,
                            file_name_list_count, self.input_pesquisar, self.button_gerir, self.button_buscar
                        )
                        sid_verificar = SID_Verificar.SIDVerificar(
                            self.webdriver,
                            file_folder_list_count_web,
                            self.js_sid_cliente_anexos_table
                        )
                        sid_anexar = SID_Anexar.SIDAnexar(
                            self.webdriver,
                            file_name_list_count, file_folder_list_count_web, file_path_list_count, 
                            self.input_conteudo_anexos, self.button_anexos, self.button_anexar_documento, self.button_escolher_arquivo, self.input_data_acontecimento, self.input_observacao, self.button_tipo_anexo, self.button_selecionar_tipo, self.button_inserir
                        )
                        sid_print = SID_Print.SIDPrint(
                            self.webdriver, self.user, self.password, self.host, self.database, 
                            file_name_list_count, file_folder_list_count,
                            self.extension_png
                        )
                        sid_mover = Server_Mover.ServerMover(
                            file_name_list_count, file_path_list_count, file_path_old_list_count
                        )
                        sid_copiar = Server_Copiar.ServerCopiar(
                            file_name_list_count, file_folder_list_count, file_path_list_count
                        )

                        # Ir para o workflow
                        status_sid_workflow = sid_workflow.sid_workflow()

                        if status_sid_workflow['status']:
                        
                            # Pesquisar cliente no sid
                            status_sid_search = sid_pesquisar.sid_pesquisar()
                            
                            if status_sid_search['status']:
                                
                                # Verificar se pode anexar o arquivo
                                status_sid_verificar = sid_verificar.sid_verificar()

                                if status_sid_verificar['status']:

                                    # Anexar arquivos no sid
                                    status_sid_anexos = sid_anexar.sid_anexar()

                                    if status_sid_anexos['status']:

                                        # Tirar print
                                        status_sid_print = sid_print.print(path_control_list[0]) # sucesso

                                        if status_sid_print['status']:

                                            # Copiar o arquivo para pasta de controle 
                                            #status_sid_copiar = sid_copiar.server_copiar(path_control_list[0])

                                            #if status_sid_copiar['status']:
                                                                                               
                                                # Mover o arquivo para a pasta old
                                                status_sid_mover = sid_mover.server_mover()

                                                if status_sid_mover['status']:
                                                    self.status = True
                                                    mensagem = f'Sucesso ao mover o arquivo: {file_name_list_count} para a pasta: {file_path_old_list_count}'
                                                    print(self.sucesso)
                                                    print(mensagem)

                                                else:
                                                    self.status = False
                                                    mensagem = f'Falha ao mover o arquivo: {file_name_list_count} para a pasta: {file_path_old_list_count}'
                                                    print(self.falha)
                                                    print(mensagem)

                                            #else:
                                                #self.status = False
                                                #mensagem = f'Falha ao copiar o arquivo: {file_name_list_count} para a pasta: {path_control_list[0]}'
                                                #print(self.falha)
                                                #print(mensagem)

                                        else:
                                            self.status = False
                                            mensagem = f'Falha ao tirar print do arquivo: {file_name_list_count} e salvar na pasta: {path_control_list[0]}'
                                            print(self.falha)                                            
                                            print(mensagem)

                                    else:
                                        
                                        # Tirar print
                                        status_sid_print = sid_print.print(path_control_list[1]) # falha

                                        if status_sid_print['status']:
                                            
                                            # Copiar o arquivo para pasta de controle
                                            #status_sid_copiar = sid_copiar.server_copiar(path_control_list[1])

                                            #if status_sid_copiar['status']:
                                                
                                                # Mover o arquivo para a pasta old + cópia por e-mail                                    
                                                #status_sid_mover = sid_mover.server_mover()
                                                
                                                #if status_sid_mover['status']:                                                    
                                                    #self.status = True
                                                    #mensagem = f'Sucesso ao mover o arquivo: {file_name_list_count} para a pasta: {file_path_old_list_count}'
                                                    #print(self.sucesso)
                                                    #print(mensagem)

                                                #else:
                                                    #self.status = False
                                                    #mensagem = f'Falha ao mover o arquivo: {file_name_list_count} para a pasta: {file_path_old_list_count}'
                                                    #print(self.falha)
                                                    #print(mensagem)
                                                
                                                #self.status = True
                                                #mensagem = f'Sucesso ao copiar o arquivo: {file_name_list_count} para a pasta: {path_control_list[1]}'
                                                #print(self.falha)
                                                #print(mensagem)

                                            #else:
                                                #self.status = False
                                                #mensagem = f'Falha ao copiar o arquivo: {file_name_list_count} para a pasta: {path_control_list[1]}'
                                                #print(self.falha)
                                                #print(mensagem)
                                            
                                            self.status = True
                                            mensagem = f'Sucesso ao tirar print do arquivo: {file_name_list_count} e salvar na pasta: {path_control_list[1]}'
                                            print(self.falha)                                            
                                            print(mensagem)

                                        else:
                                            self.status = False
                                            mensagem = f'Falha ao tirar print do arquivo: {file_name_list_count} e salvar na pasta: {path_control_list[1]}'
                                            print(self.falha)                                            
                                            print(mensagem)

                                else:

                                    # Tirar print
                                    status_sid_print = sid_print.print(path_control_list[1]) # falha

                                    if status_sid_print['status']:
                                        
                                        # Copiar o arquivo para pasta de controle
                                        #status_sid_copiar = sid_copiar.server_copiar(path_control_list[1])

                                        #if status_sid_copiar['status']:
                                            
                                            # Mover o arquivo para a pasta old + cópia por e-mail                                    
                                            #status_sid_mover = sid_mover.server_mover()
                                            
                                            #if status_sid_mover['status']:                                                    
                                                #self.status = True
                                                #mensagem = f'Sucesso ao mover o arquivo: {file_name_list_count} para a pasta: {file_path_old_list_count}'
                                                #print(self.sucesso)
                                                #print(mensagem)

                                            #else:
                                                #self.status = False
                                                #mensagem = f'Falha ao mover o arquivo: {file_name_list_count} para a pasta: {file_path_old_list_count}'
                                                #print(self.falha)
                                                #print(mensagem)
                                            
                                            #self.status = True
                                            #mensagem = f'Sucesso ao copiar o arquivo: {file_name_list_count} para a pasta: {path_control_list[1]}'
                                            #print(self.falha)
                                            #print(mensagem)

                                        #else:
                                            #self.status = False
                                            #mensagem = f'Falha ao copiar o arquivo: {file_name_list_count} para a pasta: {path_control_list[1]}'
                                            #print(self.falha)
                                            #print(mensagem)
                                        
                                        self.status = True
                                        mensagem = f'Sucesso ao tirar print do arquivo: {file_name_list_count} e salvar na pasta: {path_control_list[1]}'
                                        print(self.falha)                                            
                                        print(mensagem)

                                    else:
                                        self.status = False
                                        mensagem = f'Falha ao tirar print do arquivo: {file_name_list_count} e salvar na pasta: {path_control_list[1]}'
                                        print(self.falha)                                            
                                        print(mensagem)

                            else:

                                # Tirar print
                                status_sid_print = sid_print.print(path_control_list[1]) # falha

                                if status_sid_print['status']:

                                    # Copiar o arquivo para pasta de controle
                                    #status_sid_copiar = sid_copiar.server_copiar(path_control_list[1])

                                    #if status_sid_copiar['status']:
                                        
                                        # Mover o arquivo para a pasta old + cópia por e-mail                                    
                                        #status_sid_mover = sid_mover.server_mover()
                                        
                                        #if status_sid_mover['status']:                                                    
                                            #self.status = True
                                            #mensagem = f'Sucesso ao mover o arquivo: {file_name_list_count} para a pasta: {file_path_old_list_count}'
                                            #print(self.sucesso)
                                            #print(mensagem)

                                        #else:
                                            #self.status = False
                                            #mensagem = f'Falha ao mover o arquivo: {file_name_list_count} para a pasta: {file_path_old_list_count}'
                                            #print(self.falha)
                                            #print(mensagem)
                                        
                                        #self.status = True
                                        #mensagem = f'Sucesso ao copiar o arquivo: {file_name_list_count} para a pasta: {path_control_list[1]}'
                                        #print(self.falha)
                                        #print(mensagem)

                                    #else:
                                        #self.status = False
                                        #mensagem = f'Falha ao copiar o arquivo: {file_name_list_count} para a pasta: {path_control_list[1]}'
                                        #print(self.falha)
                                        #print(mensagem)
                                    
                                    self.status = True
                                    mensagem = f'Sucesso ao tirar print do arquivo: {file_name_list_count} e salvar na pasta: {path_control_list[1]}'
                                    print(self.falha)                                            
                                    print(mensagem)

                                else:
                                    self.status = False
                                    mensagem = f'Falha ao tirar print do arquivo: {file_name_list_count} e salvar na pasta: {path_control_list[1]}'
                                    print(self.falha)                                            
                                    print(mensagem)

                        else:
                            self.status = False
                            mensagem = 'Falha ao tentar acessar o website do WORKFLOW'
                            print(self.falha)
                            print(mensagem)
                
                else:
                    self.status = False
                    mensagem = 'Falha ao fazer o SELECT dos Anexos'
                    print(self.falha)
                    print(mensagem)

            else:
                self.status = False
                mensagem = 'Falha ao fazer o SELECT da pasta Control'
                print(self.falha)
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
            mensagem = 'Erro ao fazer a manutenção dos documentos'
            print(self.erro)
            print(mensagem)
            print(aviso)

            # Tentativas
            sid_print.print(path_control_list[2])

            # Alimentar o log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error(mensagem)
            self.my_logger.log_error(str(aviso))            

        return{'status': self.status}