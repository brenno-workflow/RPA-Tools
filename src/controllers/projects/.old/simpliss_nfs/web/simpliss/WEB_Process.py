from modules.mylogger.mylogger import MyLogger
from modules.mysql.mysql import MySQL
from controllers.access.simpliss.piracicaba import Access
from controllers.projects.simpliss_nfs.web.simpliss.piracicaba import NFS_Index, NFS_Credentials, NFS_Nota

class WEBProcess():
        
    def __init__(self, 
                 webdriver, user, password, host, database, 
                 column_fluxos_id, column_status_id,
                 column_url, column_login, column_password, column_control_path,
                 table_fluxos, table_status, 
                 table_credentials, table_sites, table_fluxosaccess, table_fluxosweb, table_control, table_fluxoscontrol,
                 param_web_access, param_true, param_web_table, param_control_download,
                 input_banner, input_banner_close, input_banner_hidden,
                 input_user, input_password, button_entrar, button_sair,
                 input_coluna_numero, button_coluna_proximo,
                 button_imprimir
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
        self.nfs_credentials = NFS_Credentials.NFSCredentials(
            webdriver, user, password, host, database, 
            column_fluxos_id, column_status_id,
            column_url, column_login, column_password,
            table_fluxos, table_status, 
            table_credentials, table_sites, table_fluxosaccess,
            param_web_access, param_true
        )
        self.nfs_nota = NFS_Nota.NFSNota(
            webdriver, user, password, host, database, 
            column_fluxos_id, column_status_id,
            column_url,
            table_fluxos, table_status, 
            table_sites, table_fluxosweb, 
            param_web_table, param_true,
            input_coluna_numero, button_coluna_proximo,
            button_imprimir
        )        

        # Variaveis especificas
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.webdriver = webdriver

        # Web
        # Notifications
        self.input_banner = input_banner
        self.input_banner_close = input_banner_close
        self.input_banner_hidden = input_banner_hidden
        # Login
        self.input_user = input_user
        self.input_password = input_password
        self.button_entrar = button_entrar
        self.button_sair = button_sair
    
    # Função para verificar se existem arquivos com extensão no caminho  
    def web_process(self):

        # Variaveis
        web_table = {'id': 'tb_Pesquisa'}
        filter_ativas = 'Status == "Normal"'
        filter_canceladas = 'Status == "Cancelada"'
        column_numero = 'Número'
        column_cnpj = 'CPF/CNPJ Prestador'

        # TryCtach
        try:

            # Fazer select das credentials
            status_select_site_credenciais = self.nfs_credentials.nfs_credentials()            

            if status_select_site_credenciais['status']:

                # Retorna a lista de resultados
                resultado = status_select_site_credenciais['resultado']

                # Atualizar variaveis
                url = resultado[0]
                login = resultado[1]
                password = resultado[2]

                for url_count, login_count, password_count in zip(url, login, password):

                    # Parametrizar as funções
                    web_access = Access.Access(
                        self.webdriver, self.user, self.password, self.host, self.database, 
                        url_count, login_count, password_count,
                        self.input_banner, self.input_banner_close, self.input_banner_hidden,
                        self.input_user, self.input_password, self.button_entrar, self.button_sair
                    )

                    # Passo a passo
                    # 1) Função para verificar todas as notas ativas (elemento selenium, número nota)
                    # 2) Função para verificar todas as notas canceladas (número nota)
                    # 3) Função para verificar notas que já foram registardas (SID) (CONPJ + nº Nota)
                    # 4) Função para verificar baixar notas que ainda não foram registradas (SID) (elemento selenium clica, baixa PDF e gera XML - nome padrão = CNPJ + nº Nota)
                    # 5) Função para cancelar as notas canceladas (CNPJ, nº Nota, senha do SID)

                    # Login
                    status_simpliss_login = web_access.login()

                    if status_simpliss_login['status']:
                        
                        # Lista notas ativas
                        status_nfs_ativas = self.nfs_nota.nfs_notas(web_table, filter_ativas, columns=[column_numero, column_cnpj])

                        if status_nfs_ativas['status']:

                            resultado = status_nfs_ativas['resultado']

                            # Baixar nota + xml
                    
                            # Logoff
                            status_simpliss_logoff = web_access.logoff()
                            
                            if status_simpliss_logoff['status']:
                                self.status = True
                                print(self.sucesso)

                            else:
                                self.status = False
                                print(self.falha)
                                break

                    else:
                        self.status = False
                        print(self.falha)
                        break
            
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