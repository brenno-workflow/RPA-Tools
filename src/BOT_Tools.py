# Modules
from modules.mylogger.mylogger import MyLogger
from modules.mydriver.mydriver import MyDriver
from modules.myweb.myweb import MyWeb

# Controllers
from controllers.projects.tools.web import WEB_Process

# Libraries
import configparser
import os

# ------------------------- Name -------------------------

# Buscar o caminho da pasta principal ('RPA-Vincibot')
dir_path = os.path.dirname(os.path.realpath(__name__))

# ------------------------- Folders -------------------------

# Configs
folder_config = r'configs'
folder_web = r'web'
folder_tools = r'tools'
folder_db = r'db'
folder_challenge = r'challenge'
folder_excel = r'excel'

# src
folder_src = r'src'

# ------------------------- Extensão -------------------------

extension_ini = '.ini'
extension_excel = '.xlsx'

# ------------------------- Configs -------------------------

# ------ Web ------
config_web_home = 'home'

# ------ DB ------
config_db_excel = 'excel'

# ------------------------- Challenge -------------------------
db_challenge = 'challenge'

# ------------------------- Path -------------------------

# ------ Path ------ 
path_config = os.path.join(dir_path, folder_config)
path_src = os.path.join(dir_path, folder_src)
path_challenge = os.path.join(dir_path, (os.path.join(folder_db, (os.path.join(folder_challenge, (os.path.join(folder_excel, (db_challenge + extension_excel))))))))

# ------------------------- Parsen -------------------------

# ------ ConfigParsen ------ 
config = configparser.ConfigParser()

# ------------------------- DB -------------------------

# ------ Challenge ------ 
config.read(os.path.join(path_config, (os.path.join(folder_db, (os.path.join(folder_challenge, (config_db_excel + extension_ini)))))))
column_a = config[config_db_excel]['column_a']
column_b = config[config_db_excel]['column_b']
column_c = config[config_db_excel]['column_c']
column_d = config[config_db_excel]['column_d']
column_e = config[config_db_excel]['column_e']
column_f = config[config_db_excel]['column_f']
column_g = config[config_db_excel]['column_g']

# ------------------------- Web -------------------------

# ------ Home ------ 
config.read(os.path.join(path_config, (os.path.join(folder_web, (os.path.join(folder_tools, (config_web_home + extension_ini)))))))
url_rpachallenge = config[config_web_home]['url']
input_fname = config[config_web_home]['fname']
input_lname = config[config_web_home]['lname']
input_company = config[config_web_home]['company']
input_role = config[config_web_home]['role']
input_adress = config[config_web_home]['adress']
input_email = config[config_web_home]['email']
input_phone = config[config_web_home]['phone']
button_submit = config[config_web_home]['submit']

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
web_process = WEB_Process.WEBProcess(
    webdriver, 
    url_rpachallenge,
    input_fname, input_lname, input_company, input_role, input_adress, input_email, input_phone,
    button_submit,
    column_a, column_b, column_c, column_d, column_e, column_f, column_g,
    path_challenge
)

# ------------------------- Procedimentos -------------------------
# Web Process
web_process = web_process.web_process

# ------------------------- Lista de Procedimentos -------------------------

# Criar lista de ações a serem executadas
lista_procedimentos = [
    web_process
]

# ------------------------- Loop -------------------------

# TryCtach
try:    

    if webdriver is not None:

        # Loop de procediemntos
        for procedimento in lista_procedimentos:

            # Pegar o nome do procedimento
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