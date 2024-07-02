import configparser
import json
import os
from modules.mylogger.mylogger import MyLogger
from modules.mydriver.mydriver import MyDriver
from modules.myweb.myweb import MyWeb
from controllers.access.sid import SID_Login
from controllers.projects.sid_cliente_documentos.web.sid.cliente import SID_Documentos
from controllers.projects.sid_cliente_documentos.server import Server_Folder
from controllers.projects.sid_cliente_documentos.control import Control_Folder
from controllers.projects.sid_cliente_documentos.mail import Mail
from controllers.projects.sid_cliente_documentos.print import Print_Screen

# ------------------------- Name -------------------------

# Buscar o caminho da pasta principal ('RPA-Vincibot')
dir_path = os.path.dirname(os.path.realpath(__name__))

# ------------------------- Folders -------------------------

# Configs
folder_config = r'configs'
folder_connection = r'connection'
folder_control = r'control'
folder_database = r'database'
folder_web = r'web'
folder_db = r'db'
folder_fluxos = r'fluxos'
folder_sid = r'sid'
folder_mail = r'mail'

# src
folder_src = r'src'
folder_scripts = r'scripts'

# ------------------------- Extensão -------------------------

extension_ini = '.ini'
extension_json = '.json'
extension_js = '.js'
extension_png = '.png'

# ------------------------- Files -------------------------

# ------ Connection ------

# Connection
config_connection = 'connection'

# ------ Control ------

# Control
config_control = 'control'

# SID
config_control_service = 'control_service'
config_control_module = 'control_module'

# ------ Database ------

# Control
config_database_control = 'db_control'

# DB
config_database_status = 'db_status'
config_database_servers = 'db_servers'
config_database_credentials = 'db_credentials'
config_database_sites = 'db_sites'
config_database_mail = 'db_mail'

# Fluxos
config_database_fluxos = 'db_fluxos'
config_database_fluxosweb = 'db_fluxosweb'
config_database_fluxosserver = 'db_fluxosserver'
config_database_fluxoscontrol = 'db_fluxoscontrol'
config_database_fluxosmail = 'db_fluxosmail'

# Sid
config_database_sid_cliente_anexos = 'sid_cliente_anexos'
config_database_sid_cliente_anexos_temp = 'sid_cliente_anexos_temp'

# ------ Web ------

# SID
config_web_sid_login = 'sid_login'
config_web_sid_cliente = 'sid_cliente'

# ------ Scripts ------

# Sid
src_script_sid_cliente_anexos_table = 'sid_cliente_anexos_table'

# ------ Mail ------

# Sid
config_mail_sid_cliente = 'sid_cliente'

# ------------------------- Path -------------------------

path_config = os.path.join(dir_path, folder_config)
path_src = os.path.join(dir_path, folder_src)

# ------------------------- Parsen -------------------------

# ConfigParser
config = configparser.ConfigParser()

# ------------------------- Connection -------------------------

# Connection
config.read(os.path.join(path_config, (os.path.join(folder_connection, (os.path.join(config_connection + extension_ini))))))
user = config[config_connection]['user_1']
password = config[config_connection]['password_1']
host = config[config_connection]['host_1']
database = config[config_connection]['db_1']

# ------------------------- Control -------------------------

# ------ Control ------

# Control
config.read(os.path.join(path_config, (os.path.join(folder_control, (config_control + extension_ini)))))
folder_control_rpa = config[config_control]['control']

# ------ SID ------

# SID
config.read(os.path.join(path_config, (os.path.join(folder_control, (os.path.join(folder_sid, (config_control_service + extension_ini)))))))
folder_service = config[config_control_service]['service_1']

# SID_Cliente
config.read(os.path.join(path_config, (os.path.join(folder_control, (os.path.join(folder_sid, (config_control_module + extension_ini)))))))
folder_module = config[config_control_module]['module_1']
folder_sucesso = config[config_control_module]['sucesso']
folder_falha = config[config_control_module]['falha']
folder_erro = config[config_control_module]['erro']

# ------------------------- Database -------------------------

# ------ Control ------

# Control
config.read(os.path.join(path_config, (os.path.join(folder_database, (os.path.join(folder_control, (config_database_control + extension_ini)))))))
column_control_id = config[config_database_control]['id']
column_control_name = config[config_database_control]['name']
column_control_path = config[config_database_control]['path']
table_control = config[config_database_control]['table']

# ------ DB ------

# Status
config.read(os.path.join(path_config, (os.path.join(folder_database, (os.path.join(folder_db, (config_database_status + extension_ini)))))))
column_status_id = config[config_database_status]['id']
param_true = config[config_database_status]['true']
param_false = config[config_database_status]['false']
table_status = config[config_database_status]['table']

# Mail
config.read(os.path.join(path_config, (os.path.join(folder_database, (os.path.join(folder_db, (config_database_mail + extension_ini)))))))
column_mail = config[config_database_mail]['mail']
table_mail = config[config_database_mail]['table']

# Servers
config.read(os.path.join(path_config, (os.path.join(folder_database, (os.path.join(folder_db, (config_database_servers + extension_ini)))))))
column_path_servers = config[config_database_servers]['path']
table_servers = config[config_database_servers]['table']

# Credenciais
config.read(os.path.join(path_config, (os.path.join(folder_database, (os.path.join(folder_db, (config_database_credentials + extension_ini)))))))
column_login = config[config_database_credentials]['login']
column_password = config[config_database_credentials]['password']
table_credentials = config[config_database_credentials]['table']

# Sites
config.read(os.path.join(path_config, (os.path.join(folder_database, (os.path.join(folder_db, (config_database_sites + extension_ini)))))))
column_url = config[config_database_sites]['url']
table_sites = config[config_database_sites]['table']

# ------ Fluxos ------

# Fluxos
config.read(os.path.join(path_config, (os.path.join(folder_database, (os.path.join(folder_fluxos, (config_database_fluxos + extension_ini)))))))
column_fluxos_id = config[config_database_fluxos]['id']
param_web_sid = config[config_database_fluxos]['web_sid_login']
param_web_sid_cliente = config[config_database_fluxos]['web_sid_cliente_workflow']
param_server_sid_cliente_anexos = config[config_database_fluxos]['server_sid_cliente_anexos']
param_control = config[config_database_fluxos]['control']
param_control_sid = config[config_database_fluxos]['control_sid']
param_control_sid_cliente = config[config_database_fluxos]['control_sid_cliente']
param_control_sid_cliente_sucesso = config[config_database_fluxos]['control_sid_cliente_sucesso']
param_control_sid_cliente_falha = config[config_database_fluxos]['control_sid_cliente_falha']
param_control_sid_cliente_erro = config[config_database_fluxos]['control_sid_cliente_erro']
param_mail_repositorio = config[config_database_fluxos]['mail_repositorio']
param_mail_sid_cliente_sucesso = config[config_database_fluxos]['mail_sid_cliente_sucesso']
param_mail_sid_cliente_falha = config[config_database_fluxos]['mail_sid_cliente_falha']
param_mail_sid_cliente_erro = config[config_database_fluxos]['mail_sid_cliente_erro']
table_fluxos = config[config_database_fluxos]['table']

# FluxosWeb
config.read(os.path.join(path_config, (os.path.join(folder_database, (os.path.join(folder_fluxos, (config_database_fluxosweb + extension_ini)))))))
table_fluxosweb = config[config_database_fluxosweb]['table']

# FluxosServer
config.read(os.path.join(path_config, (os.path.join(folder_database, (os.path.join(folder_fluxos, (config_database_fluxosserver + extension_ini)))))))
table_fluxosserver = config[config_database_fluxosserver]['table']

# FluxosControl
config.read(os.path.join(path_config, (os.path.join(folder_database, (os.path.join(folder_fluxos, (config_database_fluxoscontrol + extension_ini)))))))
table_fluxoscontrol = config[config_database_fluxoscontrol]['table']

# FluxosMail
config.read(os.path.join(path_config, (os.path.join(folder_database, (os.path.join(folder_fluxos, (config_database_fluxosmail + extension_ini)))))))
table_fluxosmail = config[config_database_fluxosmail]['table']

# ------ SID ------

# SID_Cliente_Anexos
config.read(os.path.join(path_config, (os.path.join(folder_database, (os.path.join(folder_sid, (config_database_sid_cliente_anexos + extension_ini)))))))
column_anexo = config[config_database_sid_cliente_anexos]['anexo']
table_sid_cliente_anexos = config[config_database_sid_cliente_anexos]['table']

# SID_Cliente_Anexos_Temp
config.read(os.path.join(path_config, (os.path.join(folder_database, (os.path.join(folder_sid, (config_database_sid_cliente_anexos_temp + extension_ini)))))))
folder_server_old = config[config_database_sid_cliente_anexos_temp]['old']
column_file_name = config[config_database_sid_cliente_anexos_temp]['file']
column_file_folder = config[config_database_sid_cliente_anexos_temp]['folder']
column_file_path = config[config_database_sid_cliente_anexos_temp]['path']
column_file_path_old = config[config_database_sid_cliente_anexos_temp]['path_old']
table_sid_cliente_anexos_temp = config[config_database_sid_cliente_anexos_temp]['table']

# ------------------------- Web -------------------------

# SID_Login
config.read(os.path.join(path_config, (os.path.join(folder_web, (os.path.join(folder_sid, (config_web_sid_login + extension_ini)))))))
input_user = config[config_web_sid_login]['user']
input_password = config[config_web_sid_login]['password']
button_entrar = config[config_web_sid_login]['entrar']

# SID_Cliente
config.read(os.path.join(path_config, (os.path.join(folder_web, (os.path.join(folder_sid, (config_web_sid_cliente + extension_ini)))))))
# Workflow
input_pesquisar = config[config_web_sid_cliente]['pesquisar']
button_gerir = config[config_web_sid_cliente]['gerir']
button_buscar = config[config_web_sid_cliente]['buscar']
# Anexos
input_conteudo_anexos = config[config_web_sid_cliente]['conteudo_anexos']
button_anexos = config[config_web_sid_cliente]['anexos']
button_anexar_documento = config[config_web_sid_cliente]['anexar_documento']
button_escolher_arquivo = config[config_web_sid_cliente]['escolher_arquivo']
input_data_acontecimento = config[config_web_sid_cliente]['data_acontecimento']
input_observacao = config[config_web_sid_cliente]['observacao']
button_tipo_anexo = config[config_web_sid_cliente]['tipo_anexo']
button_selecionar_tipo = config[config_web_sid_cliente]['selecionar_tipo']
button_inserir = config[config_web_sid_cliente]['inserir']

# ------------------------- Scripts -------------------------

# SID_Cliente_Anexos
with open(os.path.join(path_src, (os.path.join(folder_scripts, (os.path.join(folder_sid, (src_script_sid_cliente_anexos_table + extension_js)))))), 'r') as file:

    # Ler o arquivo
    js_sid_cliente_anexos_table = file.read()

# ------------------------- Mail -------------------------

# SID_Cliente
with open(os.path.join(path_config, (os.path.join(folder_mail, (os.path.join(folder_sid, (config_mail_sid_cliente + extension_json)))))), 'r', encoding='utf-8') as file:
    config = json.load(file)
head_sucesso = config['head']['head_sucesso']
head_falha = config['head']['head_falha']
head_erro = config['head']['head_erro']
msg_sucesso = config['body']['msg_sucesso']
msg_falha = config['body']['msg_falha']
msg_erro = config['body']['msg_erro']

# ------------------------- Procedimentos -------------------------

# Variaveis gerais
status = False
sucesso = f'SUCESSO - {__name__}'
falha = f'FALHA - {__name__}'
erro = f'ERRO - {__name__}'

# Status procedimentos
status_procedimentos = False

# Instancias
# Instanciar é uma boa prática e necessário
# Não instaciar resulta na abertura de processo diferentes e erros
my_logger = MyLogger()
my_driver = MyDriver()

# ------------------------- Driver -------------------------

status_my_driver = my_driver.driver_chrome()

if status_my_driver['status']:
    webdriver = status_my_driver['resultado']

else:
    webdriver = None

# ------------------------- Instancias -------------------------

# Metodo de 'INJEÇÃO DE DEPENDENCIA'
# ref.: https://www.youtube.com/watch?v=5DBfVnQn1Ow
my_web = MyWeb(
    webdriver
)
control_folder = Control_Folder.ControlFolder(
    user, password, host, database,
    column_fluxos_id, column_status_id,
    column_control_id, column_control_path,     
    table_fluxos, table_status, table_fluxoscontrol, table_control,
    param_true, param_control, param_control_sid_cliente_sucesso, param_control_sid_cliente_falha, param_control_sid_cliente_erro,
    folder_control_rpa, folder_sucesso, folder_falha, folder_erro,
    param_control_sid, param_control_sid_cliente,
    folder_service, folder_module
)
sid_login = SID_Login.SIDLogin(
    webdriver, user, password, host, database, 
    column_fluxos_id, column_status_id,
    column_url, column_login, column_password,
    table_fluxos, table_status, table_fluxosweb, table_sites, table_credentials,
    param_web_sid, param_true,
    input_user, input_password, button_entrar
)
server_sid_cliente = Server_Folder.ServerFolder(
    user, password, host, database, 
    column_fluxos_id, column_status_id,
    column_path_servers, column_anexo, column_file_name, column_file_folder, column_file_path, column_file_path_old, 
    table_fluxos, table_status, table_fluxosserver, table_servers, table_sid_cliente_anexos, table_sid_cliente_anexos_temp,
    param_true, param_server_sid_cliente_anexos,
    folder_server_old
)
sid_cliente_documentos = SID_Documentos.SIDDocumentos(
    webdriver, user, password, host, database, 
    column_fluxos_id, column_status_id,
    column_url, column_file_name, column_file_folder, column_file_path, column_file_path_old, column_control_path,
    table_fluxos, table_status, table_fluxosweb, table_sid_cliente_anexos_temp, table_control, table_fluxoscontrol, table_sites,
    param_web_sid_cliente, param_true, param_control_sid_cliente_sucesso, param_control_sid_cliente_falha, param_control_sid_cliente_erro,
    input_pesquisar, button_gerir, input_conteudo_anexos, button_anexos, button_anexar_documento, button_escolher_arquivo, input_data_acontecimento, input_observacao, button_tipo_anexo, button_selecionar_tipo, button_inserir, button_buscar,
    js_sid_cliente_anexos_table,
    extension_png
)
mail = Mail.Mail(
    user, password, host, database, 
    column_fluxos_id, column_status_id, 
    column_mail, column_login, column_password, column_control_path,
    table_status, table_fluxos, table_mail, table_fluxosmail, table_credentials, table_control, table_fluxoscontrol,
    param_true, param_mail_repositorio, param_mail_sid_cliente_sucesso, param_mail_sid_cliente_falha, param_mail_sid_cliente_erro, param_control_sid_cliente_sucesso, param_control_sid_cliente_falha, param_control_sid_cliente_erro,
    head_sucesso, head_falha, head_erro, msg_sucesso, msg_falha, msg_erro
)
print_screen = Print_Screen.PrintScreen(
    user, password, host, database,
    column_fluxos_id, column_status_id, 
    column_control_path, 
    table_status, table_fluxos, table_control, table_fluxoscontrol,
    param_true, param_control_sid_cliente_erro,
    extension_png
)

# TryCtach
try:

    # ------------------------- Procedimentos -------------------------

    # Criar pastas de controle
    control_folder = control_folder.control_folder
    # Verificar Server
    server_sid_cliente_files = server_sid_cliente.server_sid_cliente_files
    # Fazer login no SID
    sid_login = sid_login.sid_login
    # Anexar documentos
    sid_documentos = sid_cliente_documentos.sid_documentos
    # Enviar sucesso
    postman = mail.postman
    # Print geral
    print_screen = print_screen.print_screen

    # ------------------------- Lista de Procedimentos -------------------------

    # Criar lista de ações a serem executadas
    lista_procedimentos = [
        control_folder,
        server_sid_cliente_files,
        sid_login,
        sid_documentos,
        postman
    ]

    # ------------------------- Loop -------------------------

    if webdriver is not None:

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
            my_logger.log_info(break_line)
            my_logger.log_info(mensagem)
            
            # Executar procedimentos em ordem
            status_procedimento = procedimento()

            if status_procedimento['status']:
                status = True
                mensagem = mensagem_sucesso
                print(mensagem)

            else:
                status = False
                mensagem - mensagem_falha
                print(mensagem)
                print_screen()
                postman()
                break

    else:
        status = False
        mensagem = 'Falha ao criar o WebDriver no módulo MyWeb.'
        print(mensagem)

        # Tentar e-mail
        print_screen()
        postman()

    # Alimentar o log
    if status:
        my_logger.log_info(sucesso)
        my_logger.log_info(mensagem)

    else:
        my_logger.log_warn(falha)
        my_logger.log_warn(mensagem)

except Exception as aviso:
    status = False
    mensagem = mensagem_erro
    print(erro)
    print(mensagem)
    print(aviso)

    # Alimentar o log
    my_logger.log_error(erro)
    my_logger.log_error(mensagem)
    my_logger.log_error(str(aviso))

    # Tentar e-mail
    print_screen()
    postman()

# Para fazer uma lista das bibliotecas utilizadas até o momento:
# Abrir um novo terminal
# selecionar o __main__ (bot principal)
# digitar: pip freeze > requirements.txt
# Ira criar um arquivo txt de requerimentos