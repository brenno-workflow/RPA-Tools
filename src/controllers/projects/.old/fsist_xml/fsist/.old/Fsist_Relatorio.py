from modulos.mylogger.mylogger import MyLogger
from modulos.mysql.mysql import MySQL
from modulos.myweb.myweb import MyWeb
import time

class FsistRelatorio:
        
    def __init__(self, 
                 my_driver, user, host, database, id, module_fsist, type_subcontrole, name_download, 
                 coluna_id, coluna_path, coluna_module, coluna_type, coluna_name, coluna_relatorio, 
                 tabela_controle_rpa, tabela_fsist_parametros, tabela_fsist_relatorio
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
        self.my_web = MyWeb(my_driver)

        # Variaveis especificas
        self.user = user
        self.host = host
        self.database = database

        # Valores
        self.id = id
        self.module = module_fsist
        self.type = type_subcontrole
        self.name = name_download

        # Colunas
        self.coluna_id = coluna_id
        self.coluna_path = coluna_path
        self.coluna_module = coluna_module
        self.coluna_type = coluna_type
        self.coluna_name = coluna_name
        self.coluna_relatorio = coluna_relatorio

        # Tabela
        self.tabela_controle = tabela_controle_rpa
        self.tabela_parametros = tabela_fsist_parametros
        self.tabela_relatorio = tabela_fsist_relatorio

    # Configurar caminho de donwload do fsist
    def fsist_relatorio(self):

        # Variaveis
        coluna_parametros = ['id_relatorio', 'xpath_relatorio_tem_xml', 'xpath_relatorio_gerar', 'id_relatorio_nome_arquivo']
        filtro_coluna = [self.coluna_module, self.coluna_type, self.coluna_name]
        filtro = [self.module, self.type, self.name]
                
        try:

            print('aquiiiiiiiiiiii')

            # SELECT - Controle
            status_mysql_controle = self.my_sql.mysql_select(
                self.user, 
                self.host,
                self.database,
                self.coluna_path, 
                self.tabela_controle, 
                filtro_coluna, 
                filtro
                )

            if status_mysql_controle['status']:

                print('não aquiiiiiiiiiiiii')
                
                # Pegar resultados
                path_download = status_mysql_controle['resultado'][0]
                print('path_download')
                print(path_download)

                # Atualizar diretorio de donwload
                status_navegador_download = self.my_web.browser_download(path_download)

                if status_navegador_download['status']:

                    # Parametros
                    status_mysql_parametros = self.my_sql.mysql_select(
                        self.user, 
                        self.host,
                        self.database,
                        coluna_parametros, 
                        self.tabela_parametros, 
                        self.coluna_id, 
                        self.id
                        )

                    if status_mysql_parametros['status']:

                        lista_parametros = status_mysql_parametros['resultado']
                        print('lista de parametros')
                        print(lista_parametros)

                        id_relatorio = lista_parametros[0]
                        xpath_relatorio_tem_xml = lista_parametros[1]
                        xpath_relatorio_gerar = lista_parametros[2]
                        id_relatorio_nome_arquivo = lista_parametros[3]

                        # Pesquisar e clicar
                        status_elemento = self.my_web.id_click(id_relatorio)

                        if status_elemento['status']:

                            # Verificar se a checkbox já está marcada
                            status_elemento = self.my_web.xpath_checkbox(xpath_relatorio_tem_xml)

                            if not status_elemento['status']:

                                status_elemento = self.my_web.xpath_click(xpath_relatorio_tem_xml)
                            
                            if status_elemento['status']:

                                # Buscar valor do elemento
                                status_elemento = self.my_web.id_value_text(id_relatorio_nome_arquivo)

                                if status_elemento['status']:

                                    # Pega o nome que terá o relatório baixado
                                    relatorio_name = status_elemento['resultado']

                                    # Update nome do relatorio no Banco de Dados
                                    status_mysql_controle = self.my_sql.mysql_update(
                                        self.user, 
                                        self.host,
                                        self.database,
                                        self.coluna_relatorio, 
                                        self.tabela_relatorio, 
                                        self.coluna_id, 
                                        self.id, 
                                        relatorio_name
                                        )

                                    if status_mysql_controle['status']:

                                        # Gerar relatorio
                                        status_elemento = self.my_web.xpath_click(xpath_relatorio_gerar)

                                        if status_elemento['status']:

                                            time.sleep(5)

                                            self.status = True
                                            print(self.sucesso)
                                        
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