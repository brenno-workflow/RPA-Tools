import configparser
import json
import os
from modules.mylogger.mylogger import MyLogger
from modules.mydriver.mydriver import MyDriver
from modules.myweb.myweb import MyWeb
from controllers.projects.simpliss_nfs.web.simpliss.piracicaba import Simpliss_Procedimento
from controllers.projects.simpliss_nfs.control import Control_Folder
from controllers.projects.simpliss_nfs.mail import Mail

# ------------------------- Name -------------------------

# Buscar o caminho da pasta principal ('RPA-Vincibot')
dir_path = os.path.dirname(os.path.realpath(__name__))
print('dir_path')
print(dir_path)

# ------------------------- Folders -------------------------

# Configs
folder_config = r'configs'
folder_connection = r'connection'
folder_control = r'control'
folder_database = r'database'
folder_bigdata = r'bigdata'
folder_web = r'web'
folder_db = r'db'
folder_fluxos = r'fluxos'
folder_simpliss = r'simpliss'
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

# Simpliss
config_control_simpliss = 'control_simpliss'
config_control_simpliss_piracicaba = 'control_simpliss_piracicaba'

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

# ------ Web ------

# Simpliss
config_web_simpliss_access = 'simpliss_access'
config_web_simpliss_notification = 'simpliss_notification'

# ------ Scripts ------


# ------ Mail ------

config_mail_simpliss = 'simpliss_piracicaba'

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

# ------ Simpliss ------

# Simpliss
config.read(os.path.join(path_config, (os.path.join(folder_control, (os.path.join(folder_simpliss, (config_control_simpliss + extension_ini)))))))
folder_service = config[config_control_simpliss]['service']

# Simpliss_Piracicaba
config.read(os.path.join(path_config, (os.path.join(folder_control, (os.path.join(folder_simpliss, (config_control_simpliss_piracicaba + extension_ini)))))))
folder_module = config[config_control_simpliss_piracicaba]['module']
folder_sucesso = config[config_control_simpliss_piracicaba]['sucesso']
folder_falha = config[config_control_simpliss_piracicaba]['falha']
folder_erro = config[config_control_simpliss_piracicaba]['erro']

# ------------------------- Database -------------------------

# ------ Control ------

# Control
config.read(os.path.join(path_config, (os.path.join(folder_database, (os.path.join(folder_control, (config_database_control + extension_ini)))))))
id_control = config[config_database_control]['id']
column_control_name = config[config_database_control]['name']
column_control_path = config[config_database_control]['path']
param_control = config[config_database_control]['control']
param_control_service = config[config_database_control]['control_simpliss']
param_control_service_module = config[config_database_control]['control_simpliss_piracicaba']
param_control_service_module_sucesso = config[config_database_control]['control_simpliss_piracicaba_sucesso']
param_control_service_module_falha = config[config_database_control]['control_simpliss_piracicaba_falha']
param_control_service_module_erro = config[config_database_control]['control_simpliss_piracicaba_erro']
param_control_service_module_download = config[config_database_control]['control_simpliss_piracicaba_erro']
table_control = config[config_database_control]['table']

# ------ DB ------

# Status
config.read(os.path.join(path_config, (os.path.join(folder_database, (os.path.join(folder_db, (config_database_status + extension_ini)))))))
id_status = config[config_database_status]['id']
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
id_fluxos = config[config_database_fluxos]['id']
param_simpliss = config[config_database_fluxos]['web_simpliss_piracicaba_login']
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

# ------ Simpliss ------

# ------------------------- Web -------------------------

# Simpliss_Login
config.read(os.path.join(path_config, (os.path.join(folder_web, (os.path.join(folder_simpliss, (config_web_simpliss_access + extension_ini)))))))
input_user = config[config_web_simpliss_access]['user']
input_password = config[config_web_simpliss_access]['password']
button_entrar = config[config_web_simpliss_access]['entrar']
button_sair = config[config_web_simpliss_access]['sair']

# Simpliss_Notification
config.read(os.path.join(path_config, (os.path.join(folder_web, (os.path.join(folder_simpliss, (config_web_simpliss_notification + extension_ini)))))))
input_banner = config[config_web_simpliss_notification]['banner']
input_banner_close = config[config_web_simpliss_notification]['banner_close']

# ------------------------- Scripts -------------------------


# ------------------------- Mail -------------------------

# Simpliss_Mail
with open(os.path.join(path_config, (os.path.join(folder_mail, (os.path.join(folder_simpliss, (config_mail_simpliss + extension_json)))))), 'r', encoding='utf-8') as file:
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
    column_control_path,
    id_control,
    table_control,
    param_control, param_control_sid, param_control_sid_cliente, param_control_sid_cliente_sucesso, param_control_sid_cliente_falha, param_control_sid_cliente_erro,
    folder_control_rpa, folder_service, folder_module, folder_sucesso, folder_falha, folder_erro
)
simpliss_procedimento = Simpliss_Procedimento.SimplissProcedimento(
    webdriver, user, password, host, database, 
    column_url, column_login, column_password,
    id_fluxos, id_status,
    table_fluxos, table_status, table_credentials, table_sites, table_fluxosweb,
    param_simpliss, param_true, 
    input_banner, input_banner_close,
    input_user, input_password, button_entrar, button_sair
)
mail = Mail.Mail(
    user, password, host, database, 
    column_mail, column_login, column_password, column_control_path,
    id_status, id_fluxos, 
    table_status, table_fluxos, table_mail, table_fluxosmail, table_credentials, table_control, table_fluxoscontrol,
    param_true, param_mail_repositorio, param_mail_sid_cliente_sucesso, param_mail_sid_cliente_falha, param_mail_sid_cliente_erro, param_control_sid_cliente_sucesso, param_control_sid_cliente_falha, param_control_sid_cliente_erro,
    head_sucesso, head_falha, head_erro, msg_sucesso, msg_falha, msg_erro
)

# TryCtach
try:

    # ------------------------- Procedimentos -------------------------

    # Criar pastas de controle
    control_folder = control_folder.control_folder
    # Fazer login no SID
    simpliss_procedimento = simpliss_procedimento.procedimento
    # Enviar sucesso
    email_sucesso = mail.mail_sucesso
    # Enviar falha
    email_falha = mail.mail_falha

    # ------------------------- Lista de Procedimentos -------------------------

    # Criar lista de ações a serem executadas
    lista_procedimentos = [
        control_folder,
        #simpliss_procedimento,
        #email_sucesso
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
                #email_falha()
                break

    else:
        status = False
        mensagem = 'Falha ao criar o WebDriver no módulo MyWeb.'
        print(mensagem)

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

# Para fazer uma lista das bibliotecas utilizadas até o momento:
# Abrir um novo terminal
# selecionar o __main__ (bot principal)
# digitar: pip freeze > requirements.txt
# Ira criar um arquivo txt de requerimentos