from modulos.mylogger.mylogger import MyLogger
from modulos.mysql.mysql import MySQL
from modulos.myfolder.myfolder import MyFolder
from modulos.myzip.myzip import MyZip
from modulos.myfilter.myfilter import MyFilter
import os
import time

class EcossistemanfUnzip():
        
    def __init__(self, 
                 user, host, database, module_fsist, type_controle, type_subcontrole, process, name_download, 
                 coluna_module, coluna_type, coluna_process, coluna_name, coluna_path, 
                 tabela_servidores, tabela_controle):

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
        self.my_folder = MyFolder()
        self.my_zip = MyZip()
        self.my_filter = MyFilter()

        # Variaveis especificas
        self.user = user
        self.host = host
        self.database = database

        # Valores
        self.module = module_fsist
        self.type_controle = type_controle
        self.type_subcontrole = type_subcontrole
        self.process = process
        self.name = name_download
        self.extensao_pdf = '.pdf'
        self.extensao_xml = '.xml'
        self.extensao_zip = '.zip'

        # Colunas
        self.coluna_module = coluna_module
        self.coluna_type = coluna_type
        self.coluna_process = coluna_process
        self.coluna_name = coluna_name
        self.coluna_path = coluna_path
        
        # Tabela SELECT
        self.tabela_servidores = tabela_servidores
        self.tabela_controle = tabela_controle

    # Função para verificar se existem arquivos com extensão no caminho  
    def ecossistemanf_unzip(self):

        # Variaveis
        filtro_coluna_servidores = [self.coluna_module, self.coluna_type, self.coluna_process]
        filtro_servidores = [self.module, self.type_controle, self.process]
        filtro_coluna_controle = [self.coluna_module, self.coluna_type, self.coluna_name]
        filtro_controle = [self.module, self.type_subcontrole, self.name]

        # TryCtach
        try:

            # Buscar caminho da pasta download
            status_select_controle = self.my_sql.mysql_select(
                self.user, 
                self.host,
                self.database,
                self.coluna_path, 
                self.tabela_controle, 
                filtro_coluna_controle, 
                filtro_controle
                )

            if status_select_controle['status']:

                # Atualizar variaveis
                path_download = status_select_controle['resultado'][0]

                # Buscar informações do banco de dados
                status_select_servidores = self.my_sql.mysql_select(
                    self.user, 
                    self.host,
                    self.database,
                    self.coluna_path, 
                    self.tabela_servidores, 
                    filtro_coluna_servidores, 
                    filtro_servidores
                    )

                if status_select_servidores['status']:

                    # Atualizar variaveis
                    path_ecossistemanf = status_select_servidores['resultado'][0]

                    # Buscar a lista de arquivos da pasta Download
                    status_lista_arquivos_download = self.my_folder.listar_arquivos(path_download)

                    if status_lista_arquivos_download['status']:

                        lista_arquivos = status_lista_arquivos_download['resultado'][0]

                        # Filtrar por extensão
                        status_filtro_zip = self.my_filter.elemento_em_lista(lista_arquivos, self.extensao_zip)

                        if status_filtro_zip['status']:

                            # Verificar se foram baixadas novas notas
                            if status_filtro_zip['resultado'] == []:
                                self.status = True
                                print(self.sucesso)

                                # Atualizar log
                                self.my_logger.log_info('Nenhuma nova nota foi baixada.')

                            else:

                                # Atualizar variavel com o arquivo zip
                                arquivo_zip = status_filtro_zip['resultado'][0]

                                # Juntar o path com o arquivo
                                path_arquivo_zip = os.path.join(path_download, arquivo_zip)

                                # Extrair os arquivos
                                status_path_arquivo_unzip = self.my_zip.unzip(path_arquivo_zip, path_ecossistemanf)

                                time.sleep(20)

                                if status_path_arquivo_unzip['status']:
                                    self.status = True
                                    print(self.sucesso)
                                    self.my_logger.log_info('Sucesso na hora de realizar a descompactação do arquivo zip.')

                                else:
                                    self.status = False
                                    print(self.falha)
                                    self.my_logger.log_warn('Erro na hora de realizar a descompactação do arquivo zip.')
            
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