import os
import json
import configparser
from modules.mylogger.mylogger import MyLogger
from modules.mydriver.mydriver import MyDriver
from modules.myweb.myweb import MyWeb
from controllers.projects.fsist_xml.control import Control_Folder
from controllers.projects.fsist_xml.web import fsist_process
from controllers.print import Print_Screen
from controllers.projects.fsist_xml.mail import Mail
from datetime import datetime




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
folder_fsist = r'fsist'
folder_log = r'logs'

# src
folder_src = r'src'

# ------------------------- Extensão -------------------------

extension_ini = '.ini'
extension_json = '.json'
extension_js = '.js'
extension_log = '.log'
extension_png = '.png'
extension_pdf = '.pdf'
extension_xml = '.xml'


# ------------------------- Files -------------------------

# Connection
config_connection = 'connection'

# ------ Control ------

# Control
# ------ Control ------
config_control = 'control'
config_subcontrol = 'subcontrol'

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


config_web_fsist_login = 'fsist_login'
config_web_fsist_monitor_notas = 'fsist_monitor_notas'
config_web_sid_nfcancelada = 'sid_nfcancelada'
# --------- Mail ----------
config_mail_fsist = 'fsist'
# ------------------------- Path -------------------------

path_config = os.path.join(dir_path, folder_config)

# ------------------------- Parsen -------------------------

# ConfigParser
config = configparser.ConfigParser()

current_date = datetime.now().strftime("%d-%m-%Y")
log_folder_path = os.path.join(dir_path, folder_log)
log_subfolder_path = os.path.join(log_folder_path, current_date)
log_file_path = os.path.join(log_subfolder_path, (current_date + extension_log))
print(log_file_path)

# Connection
config.read(os.path.join(path_config, (os.path.join(folder_connection, (os.path.join(config_connection + extension_ini))))))
user = config[config_connection]['user_1']
password = config[config_connection]['password_1']
host = config[config_connection]['host_1']
database = config[config_connection]['db_1']

# ------------------------- Control -------------------------


# Control
config.read(os.path.join(path_config, (os.path.join(folder_control, (config_control + extension_ini)))))
folder_control_rpa = config[config_control]['control']
folder_sucesso = config[config_control]['sucesso']
folder_falha = config[config_control]['falha']
folder_erro = config[config_control]['erro']
folder_download = config[config_control]['download']

#--------Subcontrol---------
config.read(os.path.join(path_config, (os.path.join(folder_control, (os.path.join(folder_fsist, (config_subcontrol + extension_ini)))))))
folder_service = config[config_subcontrol]['service_1']

# ------------------------- Database -------------------------

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
column_id_servers = config[config_database_servers]['id']
table_servers = config[config_database_servers]['table']


# Credenciais
config.read(os.path.join(path_config, (os.path.join(folder_database, (os.path.join(folder_db, (config_database_credentials + extension_ini)))))))
column_login = config[config_database_credentials]['login']
column_password = config[config_database_credentials]['password']
table_credentials = config[config_database_credentials]['table']

# Sites
config.read(os.path.join(path_config, (os.path.join(folder_database, (os.path.join(folder_db, (config_database_sites + extension_ini)))))))
column_url = config[config_database_sites]['url']
column_sites_id = config[config_database_sites]['id']
table_sites = config[config_database_sites]['table']
id_fsist_sid = config[config_database_sites]['fsist_sid_nfautorizada']

# ------ Fluxos ------

# Fluxos
config.read(os.path.join(path_config, (os.path.join(folder_database, (os.path.join(folder_fluxos, (config_database_fluxos + extension_ini)))))))
column_fluxos_id = config[config_database_fluxos]['id']
param_web_fsist = config[config_database_fluxos]['web_fsist_login']
param_web_ecossistemanf_autorizada = config[config_database_fluxos]['sid_ecossistemanf_autorizada']
param_web_ecossistemanf_cancelada = config[config_database_fluxos]['sid_ecossistemanf_nfcancelada']
param_server_fsist = config[config_database_fluxos]['server_ecossistemanf']
param_control = config[config_database_fluxos]['control']
param_control_fsist = config[config_database_fluxos]['control_fsist']
param_control_fsist_sucesso = config[config_database_fluxos]['control_fsist_sucesso']
param_control_fsist_falha = config[config_database_fluxos]['control_fsist_falha']
param_control_fsist_erro = config[config_database_fluxos]['control_fsist_erro']
param_control_fsist_download = config[config_database_fluxos]['control_fsist_download']
param_mail_repositorio = config[config_database_fluxos]['mail_repositorio']
param_mail_ecossistemanf_sucesso = config[config_database_fluxos]['mail_ecossistemanf_sucesso']
param_mail_ecossistemanf_falha = config[config_database_fluxos]['mail_ecossistemanf_falha']
param_mail_ecossistemanf_erro = config[config_database_fluxos]['mail_ecossistemanf_erro']
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

# ------------------------- Web -------------------------


# FSIST_Login
config.read(os.path.join(path_config, (os.path.join(folder_web, (os.path.join(folder_fsist, (config_web_fsist_login + extension_ini)))))))
input_user = config[config_web_fsist_login]['element_user']
input_password = config[config_web_fsist_login]['element_password']
btn_login = config[config_web_fsist_login]['btn_entrar_inicio']
btn_entrar = config[config_web_fsist_login]['btn_entrar']

# FSIST_Monitor_Notas
config.read(os.path.join(path_config, (os.path.join(folder_web, (os.path.join(folder_fsist, (config_web_fsist_monitor_notas + extension_ini)))))), encoding='utf-8')
data_download = config[config_web_fsist_monitor_notas]['data_download']
element_msg = config[config_web_fsist_monitor_notas]['element_msg']
download_xml = config[config_web_fsist_monitor_notas]['download_xml']
btn_data = config[config_web_fsist_monitor_notas]['btn_data']
btn_select_all = config[config_web_fsist_monitor_notas]['btn_selecionar_todas']
btn_download = config[config_web_fsist_monitor_notas]['btn_download']
btn_ciencia = config[config_web_fsist_monitor_notas]['btn_ciencia']
btn_cancel = config[config_web_fsist_monitor_notas]['btn_cancel']
btn_sim = config[config_web_fsist_monitor_notas]['btn_sim']
dias_ativas = config[config_web_fsist_monitor_notas]['dias_ativas']
dias_cancelada = config[config_web_fsist_monitor_notas]['dias_cancelada']
data_inicial = config[config_web_fsist_monitor_notas]['btn_data_inicial']
btn_confirmar = config[config_web_fsist_monitor_notas]['btn_confirmar']
btn_relatorio = config[config_web_fsist_monitor_notas]['btn_relatorio']
checkbox_xml = config[config_web_fsist_monitor_notas]['checkbox_xml']
btn_gerar_relatorio = config[config_web_fsist_monitor_notas]['btn_gerar_relatorio']
barra_pesquisa = config[config_web_fsist_monitor_notas]['barra_pesquisa']
btn_buscar = config[config_web_fsist_monitor_notas]['btn_buscar']
btn_ok = config[config_web_fsist_monitor_notas]['btn_ok']
trocar_nome_arquivo = config[config_web_fsist_monitor_notas]['trocar_nome_arquivo']

# SID NFcancelada
config.read(os.path.join(path_config, (os.path.join(folder_web, (os.path.join(folder_sid, (config_web_sid_nfcancelada + extension_ini)))))))
chave_nfcancelada = config[config_web_sid_nfcancelada]['chave_nfcancelada']
password_nfcancelada = config[config_web_sid_nfcancelada]['password_nfcancelada']
btn_apontamento = config[config_web_sid_nfcancelada]['btn_apontamento']




with open(os.path.join(path_config, (os.path.join(folder_mail, (os.path.join(folder_fsist, (config_mail_fsist + extension_json)))))), 'r', encoding='utf-8') as file:
    config = json.load(file)
head_sucesso = config['head']['head_sucesso']
head_falha = config['head']['head_falha']
head_erro = config['head']['head_erro']
msg_sucesso = config['body']['msg_sucesso']
msg_falha = config['body']['msg_falha']
msg_erro = config['body']['msg_erro']

# Variaveis gerais
status = False
sucesso = f'SUCESSO - {__name__}'
falha = f'FALHA - {__name__}'
erro = f'ERRO - {__name__}'

# Status procedimentos
status_procedimentos = None

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


# Metodo de 'INJEÇÃO DE DEPENDENCIA'
# ref.: https://www.youtube.com/watch?v=5DBfVnQn1Ow
my_web = MyWeb(my_driver)
control_folder = Control_Folder.ControlFolder(
    user, password, host, database,
    column_fluxos_id, column_status_id,
    column_control_id, column_control_path,     
    table_fluxos, table_status, table_fluxoscontrol, table_control,
    param_true, param_control, param_control_fsist_sucesso, param_control_fsist_falha, param_control_fsist_erro, param_control_fsist_download,
    folder_control_rpa, folder_sucesso, folder_falha, folder_erro, folder_download,
    param_control_fsist, param_control_fsist,
    folder_service 
)
fsist_process = fsist_process.FsistProcess(
    webdriver,
    user, password, host, database,
    column_fluxos_id, column_status_id, column_url, column_login, column_password, column_control_id, column_control_path, column_path_servers, column_id_servers,
    table_fluxos, table_status, table_fluxosweb, table_sites, table_credentials, table_fluxoscontrol, table_control, table_fluxosserver, table_servers,
    param_web_fsist, param_true, param_control_fsist_download, param_web_ecossistemanf_autorizada, param_web_ecossistemanf_cancelada, param_control_fsist, param_server_fsist, param_control_fsist_sucesso, param_control_fsist_falha, param_control,
    input_user, input_password, btn_login, btn_entrar, btn_data, btn_confirmar, btn_sim, btn_download, btn_ciencia, btn_cancel, btn_select_all, btn_relatorio, btn_gerar_relatorio, btn_buscar, btn_ok, 
    dias_ativas, dias_cancelada, data_inicial, barra_pesquisa, element_msg, checkbox_xml, download_xml, chave_nfcancelada, password_nfcancelada, btn_apontamento, data_download,
    extension_png, 
    folder_download,
)
mail = Mail.Mail(
    user, password, host, database, 
    column_fluxos_id, column_status_id, 
    column_mail, column_login, column_password, column_control_path,
    table_status, table_fluxos, table_mail, table_fluxosmail, table_credentials, table_control, table_fluxoscontrol,
    param_true, param_mail_repositorio, param_mail_ecossistemanf_sucesso, param_mail_ecossistemanf_falha, param_control_fsist_erro, param_control_fsist_sucesso, param_control_fsist_falha, param_control_fsist_erro,
    head_sucesso, head_falha, head_erro, msg_sucesso, msg_falha, msg_erro, log_file_path
)
print_screen = Print_Screen.PrintScreen(
    user, password, host, database,
    column_fluxos_id, column_status_id, 
    column_control_path, 
    table_status, table_fluxos, table_control, table_fluxoscontrol,
    param_true, param_control_fsist_erro,
    extension_png
)
# TryCtach
try:
    # Control Folder
    status_control_folder = control_folder.control_folder
    # Process 
    status_process_nf = fsist_process.nf_process
    # Postman
    postman = mail.postman
    # Print geral
    print_screen = print_screen.print_screen

    lista_procedimentos = [
        status_control_folder,
        status_process_nf, 
        postman
    ]

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
                mensagem = mensagem_falha
                print(mensagem)
                print_screen()
                postman()
                break
            
            # Alimentar o log
            if status:
                my_logger.log_info(sucesso)
                my_logger.log_info(mensagem)

            else:
                my_logger.log_warn(falha)
                my_logger.log_warn(mensagem)
    else:
        status = False
        mensagem = 'Falha ao criar o WebDriver no módulo MyWeb.'
        print(mensagem)
        print_screen()
        postman()

       
        

   

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
    # Tirar um print da tela como um todo
   

    # Enviar e-mail de erros

# Para fazer uma lista das bibliotecas utilizadas até o momento:
# Abrir um novo terminal
# selecionar o __main__ (bot principal)
# digitar: pip freeze > requirements.txt
# Ira criar um arquivo txt de requerimentos