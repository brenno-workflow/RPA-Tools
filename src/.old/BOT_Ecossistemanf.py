from modulos.mylogger.mylogger import MyLogger
from modulos.mydriver.mydriver import MyDriver
from modulos.myweb.myweb import MyWeb
from procedimentos.ecossistemanf.controle import Controle_Fsist, Controle_Limpar
from procedimentos.ecossistemanf.ecossistemanf import Ecossistemanf_Chaves, Ecossistemanf_Servidor, Ecossistemanf_Unzip
from procedimentos.ecossistemanf.fsist import Fsist_Login, Fsist_Avisos, Fsist_Periodo, Fsist_Ciencia, Fsist_Relatorio, Fsist_Excel, Fsist_Notas, Fsist_Print
from procedimentos.ecossistemanf.mail import Mail_Ecossistemanf

# Variaveis gerais
status = False
sucesso = f'SUCESSO - {__name__}'
falha = f'FALHA - {__name__}'
erro = f'ERRO - {__name__}'

# Variaveis especificas
user = 'leonardo.vinci'
host = 'localhost'
database = 'ecossistemanf_db'

# Valores
id = 1
local = 'desktop'
module_controle = 'controle'
module_fsist = 'fsist'
name_sucesso = 'sucesso'
name_falha = 'falha'
name_erro = 'erro'
name_download = 'download'
name_fsist = 'fsist'
name_fncanceladas = 'fncancelada'
type_controle = 'controle'
type_subcontrole = 'subcontrole'
process = 'ecossistemanf'

# Colunas
coluna_user = 'user'
coluna_id = 'id'
coluna_login = 'login'
coluna_password = 'password'
coluna_module = 'module'
coluna_type = 'type'
coluna_name = 'name'
coluna_process = 'process'
coluna_subprocess = 'subprocess'
coluna_mail = 'mail'
coluna_url = 'url'
coluna_local = 'local'
coluna_path = 'path'
coluna_folder = 'folder'
coluna_departament = 'departament'
coluna_dias_ativas = 'dias_ativas'
coluna_dias_canceladas = 'dias_canceladas'
coluna_relatorio = 'relatorio'
coluna_chaves = 'chaves'
coluna_status = 'status'
coluna_xml = 'xml'
coluna_filtro = 'filtro'
coluna_filtro_ativas = 'filtro_ativas'
coluna_filtro_canceladas = 'filtro_canceladas'
coluna_filtro_tem_xml = 'filtro_tem_xml'
coluna_filtro_requests = 'filtro_requests'

# Tabelas
tabela_credenciais = 'credenciais'
tabela_emails = 'emails'
tabela_servidores = 'servidores'
tabela_controle_rpa = 'controle_rpa'
tabela_fsist_parametros = 'fsist_parametros'
tabela_fsist_relatorio = 'fsist_relatorio'
tabela_fsist_relatorio_temp = 'fsist_relatorio_temp'
tabela_ecossistemanf_chaves = 'ecossistemanf_chaves'
tabela_ecossistemanf_chaves_temp = 'ecossistemanf_chaves_temp'
tabela_sid_fncancelada_parametros = 'sid_fncancelada_parametros'

# Status procedimentos
status_procedimentos = None

# Instancias
# Instanciar é uma boa prática e necessário
# Não instaciar resulta na abertura de processo diferentes e erros
my_logger = MyLogger()
my_driver = MyDriver()

# Metodo de 'INJEÇÃO DE DEPENDENCIA'
# ref.: https://www.youtube.com/watch?v=5DBfVnQn1Ow
my_web = MyWeb(my_driver)
controle_fsist = Controle_Fsist.ControleFsist(
    user, host, database, name_sucesso, name_falha, name_erro, name_download, 
    coluna_module, coluna_name, coluna_path, coluna_folder, coluna_type, coluna_local, 
    module_controle, module_fsist, 
    type_controle, type_subcontrole, 
    tabela_controle_rpa
    )
controle_limpar = Controle_Limpar.ControleLimpar(
    user, host, database, module_fsist, type_subcontrole, name_download, name_sucesso, name_falha, name_erro,
    coluna_path, coluna_module, coluna_type, coluna_name, 
    tabela_controle_rpa
    )
ecossistemanf_servidor = Ecossistemanf_Servidor.EcossistemanfServidor(
    user, host, database, module_fsist, type_subcontrole,
    coluna_module, coluna_type, coluna_path,
    tabela_servidores
    )
ecossistemanf_unzip = Ecossistemanf_Unzip.EcossistemanfUnzip(
    user, host, database, module_fsist, type_controle, type_subcontrole, process, name_download,
    coluna_module, coluna_type, coluna_process, coluna_name, coluna_path, 
    tabela_servidores, tabela_controle_rpa
    )
fsist_login = Fsist_Login.FsistLogin(
    my_driver, user, host, database, id, module_fsist, name_fsist, 
    coluna_id, coluna_user, coluna_module, coluna_name, coluna_url, coluna_login, coluna_password, 
    tabela_credenciais, tabela_fsist_parametros
    )
fsist_avisos = Fsist_Avisos.FsistAvisos(
    my_driver, user, host, database, id, 
    coluna_id, 
    tabela_fsist_parametros
    )
fsist_periodo = Fsist_Periodo.FsistPeriodo(
    my_driver, user, host, database, id, module_fsist, type_subcontrole, 
    coluna_id, coluna_module, coluna_type, coluna_dias_ativas, coluna_dias_canceladas, 
    tabela_fsist_parametros, tabela_fsist_relatorio
    )
fsist_ciencia = Fsist_Ciencia.FsistCiencia(
    my_driver, user, host, database, id, 
    coluna_id,
    tabela_fsist_parametros
    )
fsist_relatorio = Fsist_Relatorio.FsistRelatorio(
    my_driver, user, host, database, id, module_fsist, type_subcontrole, name_download, 
    coluna_id, coluna_path, coluna_module, coluna_type, coluna_name, coluna_relatorio, 
    tabela_controle_rpa, tabela_fsist_parametros, tabela_fsist_relatorio
    )
fsist_excel = Fsist_Excel.FsistExcel(
    user, host, database, id, module_fsist, type_subcontrole, name_download, 
    coluna_id, coluna_module, coluna_type, coluna_name, coluna_relatorio, coluna_path, coluna_chaves, coluna_status, coluna_xml, 
    tabela_controle_rpa, tabela_fsist_relatorio, tabela_fsist_relatorio_temp
    )
ecossistemanf_chaves = Ecossistemanf_Chaves.EcossistemanfChaves(
    user, host, database, module_fsist, process, 
    coluna_module, coluna_process, coluna_status, coluna_url, coluna_chaves, coluna_filtro, 
    tabela_ecossistemanf_chaves, tabela_ecossistemanf_chaves_temp
    )
fsist_notas = Fsist_Notas.FsistNotas(
    my_driver, user, host, database, id, module_fsist, name_fncanceladas, 
    coluna_url, coluna_password, coluna_id, coluna_user, coluna_module, coluna_name, coluna_chaves, coluna_status, coluna_xml, coluna_filtro_ativas, coluna_filtro_canceladas, coluna_filtro_tem_xml, 
    tabela_credenciais, tabela_fsist_parametros, tabela_sid_fncancelada_parametros, tabela_fsist_relatorio, tabela_fsist_relatorio_temp, tabela_ecossistemanf_chaves_temp
    )
fsist_print = Fsist_Print.FsistPrint(
    my_driver, user, host, database, module_fsist, type_subcontrole, name_falha, name_erro, 
    coluna_path, coluna_module, coluna_type, coluna_name, 
    tabela_controle_rpa
    )
mail_ecossistemanf = Mail_Ecossistemanf.MailEcossistemanf(
    user, host, database, module_fsist, type_subcontrole, name_sucesso, name_falha, name_erro,
    coluna_mail, coluna_module, coluna_type, coluna_name, coluna_path, 
    tabela_emails, tabela_controle_rpa, tabela_servidores
    )

# TryCtach
try:

    # Procedimentos
    # Criar pastas de controle
    criar_controle_fsist = controle_fsist.criar_controle_fsist
    # Limpar pastas do controle
    controle_limpar_download = controle_limpar.limpar_download
    controle_limpar_sucesso = controle_limpar.limpar_sucesso
    controle_limpar_falha = controle_limpar.limpar_falha
    controle_limpar_erro = controle_limpar.limpar_erro
    # Verificar se não existem arquivos na pasta do servidor
    servidor_sem_arquivos = ecossistemanf_servidor.ecossistemanf_sem_arquivos
    # Verificar se existem arquivos na pasta do servidor
    servidor_com_arquivos = ecossistemanf_servidor.ecossistemanf_com_arquivos
    # Extrair os arquivos zip na pasta do servidor (eco)
    servidor_unzip = ecossistemanf_unzip.ecossistemanf_unzip
    # Iniciar driver
    iniciar_driver = my_driver.driver_chrome
    # Login Fsist
    fsist_login = fsist_login.fsist_login
    # Dispensar notificações/avisos na pagina
    fsist_avisos = fsist_avisos.fsist_avisos
    # Periodo de notas ativas            
    fsist_periodo_ativas = fsist_periodo.fsist_periodo_ativas
    # Periodo de notas canceladas            
    fsist_periodo_canceladas = fsist_periodo.fsist_periodo_canceladas
    # Ciencia de notas
    fsist_ciencia = fsist_ciencia.fsist_ciencia
    # Gerar relatorio
    fsist_relatorio = fsist_relatorio.fsist_relatorio
    # Atualizar os dados do excel no Banco de Dados
    fsist_excel = fsist_excel.excel_relatorio
    # Buscar as notas já lançadas e canceladas no Ecossistemanf
    ecossistemanf_chaves = ecossistemanf_chaves.ecossistemanf_chaves
    # Fazer o filtro de chaves ativas
    fsist_notas_baixar = fsist_notas.fsist_notas_ativas
    # Fazer o filtro de chaves canceladas
    fsist_notas_cancelar = fsist_notas.fsist_notas_canceladas
    # Tirar print de falhas na web
    fsist_print_falha = fsist_print.fsist_print_falha
    # Tirar print de erros no geral
    fsist_print_erro = fsist_print.fsist_print_erro
    # Encaminhar e-mails
    mail_verificar = mail_ecossistemanf.mail_verificar
    mail_sucesso = mail_ecossistemanf.mail_sucesso
    mail_falha = mail_ecossistemanf.mail_falha
    mail_erro = mail_ecossistemanf.mail_erro

    # Criar lista de ações a serem executadas
    lista_procedimentos = [
        criar_controle_fsist,
        servidor_sem_arquivos,
    ]

    # Loop de procediemntos
    for procedimento in lista_procedimentos:

        # Pegar o nome do procedimento
        # VERIFICAR DE USAR O MYNAME PARA ISSO DEPOIS!!!!!!!!!
        procedimento_nome = getattr(procedimento, '__qualname__', str(procedimento))

        # Informar qual arquivo está sendo executado no momento
        my_logger.log_info(f'Iniciando o processo do bot: {procedimento_nome}')
        print(f'Iniciando o processo do bot: {procedimento_nome}')
        
        # Executar procedimentos em ordem
        status_procedimento = procedimento()

        if status_procedimento['status']:
            status = True
            print(sucesso)

        else:
            status = False
            print(falha)
        
        # Alimentar o log
        if status:
            my_logger.log_info(f'Sucesso ao rodar o bot {procedimento_nome}')
            print(f'Sucesso ao rodar o bot {procedimento_nome}')

        else:
            my_logger.log_warn(f'Falha ao rodar o bot {procedimento_nome}')
            print(f'Falha ao rodar o bot {procedimento_nome}')

            # Tirar print da falha
            fsist_print_falha()
            break

    if status:    

        # Criar lista de ações a serem executadas
        lista_procedimentos = [
            iniciar_driver,
            fsist_login,
            fsist_periodo_ativas,
            fsist_ciencia,
            controle_limpar_download,
            fsist_relatorio,
            fsist_excel,
            ecossistemanf_chaves,
            fsist_notas_baixar,
            servidor_unzip,
            fsist_periodo_canceladas,
            controle_limpar_download,
            fsist_relatorio,
            fsist_excel,
            fsist_notas_cancelar,
            controle_limpar_download
        ]

        # Loop de procediemntos
        for procedimento in lista_procedimentos:

            # Pegar o nome do procedimento
            # VERIFICAR DE USAR O MYNAME PARA ISSO DEPOIS!!!!!!!!!
            procedimento_nome = getattr(procedimento, '__qualname__', str(procedimento))

            # Informar qual arquivo está sendo executado no momento
            my_logger.log_info(f'Iniciando o processo do bot: {procedimento_nome}')
            print(f'Iniciando o processo do bot: {procedimento_nome}')
            
            # Executar procedimentos em ordem
            status_procedimento = procedimento()

            if status_procedimento['status']:
                status = True
                print(sucesso)

            else:
                status = False
                print(falha)
            
            # Alimentar o log
            if status:
                my_logger.log_info(f'Sucesso ao rodar o bot {procedimento_nome}')
                print(f'Sucesso ao rodar o bot {procedimento_nome}')

            else:
                my_logger.log_warn(f'Falha ao rodar o bot {procedimento_nome}')
                print(f'Falha ao rodar o bot {procedimento_nome}')

                # Tirar print da falha
                fsist_print_falha()
                break

    else:

        # E-mail de verificação
        status_mail = mail_verificar()

        if status_mail['status']:
            print('Sucesso ao enviar o e-mail de verificação.')

            status = True
            print(sucesso)

        else:
            status = False
            print(falha)

    # Alimentar o log
    if status:
        my_logger.log_info(sucesso)

    else:
        my_logger.log_warn(falha)

    # Enviar e-mails
    if status:

        # E-mail de sucesso
        status_mail = mail_sucesso()

        if status_mail['status']:
            print('Sucesso ao enviar o e-mail de sucesso.')
            
            status_controle_limpar = controle_limpar_sucesso()

            if status_controle_limpar['status']:
                print('Sucesso ao limpar a pasta de sucesso.')

            else:
                print('Falha ao limpar a pasta de sucesso.')
                my_logger.log_warn('Falha ao limpar a pasta de sucesso.')

        else:
            print('Falha ao enviar o e-mail de sucesso.')
            my_logger.log_warn('Falha ao enviar o e-mail de sucesso.')

    else:

        # E-mail de falhas
        status_mail = mail_falha()

        if status_mail['status']:
            print('Sucesso ao enviar o e-mail de falhas.')
            
            status_controle_limpar = controle_limpar_falha()

            if status_controle_limpar['status']:
                print('Sucesso ao limpar a pasta de falhas.')

            else:
                print('Falha ao limpar a pasta de falhas.')
                my_logger.log_warn('Falha ao limpar a pasta de falhas.')

        else:
            print('Falha ao enviar o e-mail de falhas.')
            my_logger.log_warn('Falha ao enviar o e-mail de falhas.')

except Exception as aviso:
    status = False
    print(erro)
    print(aviso)

    # Alimentar o log
    my_logger.log_error(erro)
    my_logger.log_error(str(aviso))

    # Tirar um print da tela como um todo
    fsist_print_erro()

    # Enviar e-mail de erros
    status_mail = mail_erro()

    if status_mail['status']:
        print('Sucesso ao enviar o e-mail de erros.')
        
        status_controle_limpar = controle_limpar_falha()

        if status_controle_limpar['status']:
            print('Sucesso ao limpar a pasta de erros.')

        else:
            print('Falha ao limpar a pasta de erros.')
            my_logger.log_warn('Falha ao limpar a pasta de erros.')

    else:
        print('Falha ao enviar o e-mail de erros.')
        my_logger.log_warn('Falha ao enviar o e-mail de erros.')

# Para fazer uma lista das bibliotecas utilizadas até o momento:
# Abrir um novo terminal
# selecionar o __main__ (bot principal)
# digitar: pip freeze > requirements.txt
# Ira criar um arquivo txt de requerimentos