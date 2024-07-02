from modulos.mylogger.mylogger import MyLogger
from modulos.mysql.mysql import MySQL
from modulos.myexcel.myexcel import MyExcel
import os

class FsistExcel:
        
    def __init__(self, 
                 user, host, database, id, module_fsist, type_subcontrole, name_download, 
                 coluna_id, coluna_module, coluna_type, coluna_name, coluna_relatorio, coluna_path, coluna_chaves, coluna_status, coluna_xml, 
                 tabela_controle_rpa, tabela_fsist_relatorio, tabela_fsist_relatorio_temp
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
        self.my_excel = MyExcel()
        
        # Metodo de 'INJEÇÃO DE DEPENDENCIA'
        # ref.: https://www.youtube.com/watch?v=5DBfVnQn1Ow

        # Variaveis especificas
        self.user = user
        self.host = host
        self.database = database

        # Valores
        self.id = id
        self.module = module_fsist
        self.type = type_subcontrole
        self.name_download = name_download

        # Colunas
        self.coluna_id = coluna_id
        self.coluna_module = coluna_module
        self.coluna_type = coluna_type
        self.coluna_name = coluna_name
        self.coluna_relatorio = coluna_relatorio
        self.coluna_path = coluna_path
        self.coluna_chaves = coluna_chaves
        self.coluna_status = coluna_status
        self.coluna_tem_xml = coluna_xml

        # Tabelas
        self.tabela_controle = tabela_controle_rpa
        self.tabela_relatorio = tabela_fsist_relatorio
        self.tabela_relatorio_temp = tabela_fsist_relatorio_temp

    # Ciencia
    def excel_relatorio(self):

        # Variaveis
        filtro_coluna_controle = [self.coluna_module, self.coluna_type, self.coluna_name]
        filtro_controle = [self.module, self.type, self.name_download]
        colunas_relatorio = [self.coluna_chaves, self.coluna_status, self.coluna_tem_xml, self.coluna_relatorio]
        filtro_coluna_relatorio = [self.coluna_module, self.coluna_type]
        filtro_relatorio = [self.module, self.type]
        colunas_relatorio_temp = [self.coluna_chaves, self.coluna_status, self.coluna_tem_xml]
        
        # Try Catch
        try:

            # Buscar caminho do relatorio baixado
            status_mysql_controle = self.my_sql.mysql_select(
                self.user, 
                self.host,
                self.database,
                self.coluna_path, 
                self.tabela_controle, 
                filtro_coluna_controle, 
                filtro_controle
                )

            if status_mysql_controle['status']:

                path_download = status_mysql_controle['resultado'][0]
                
                # Buscar parmetros para filtrar o excel
                status_mysql_relatorio = self.my_sql.mysql_select(
                    self.user, 
                    self.host,
                    self.database,
                    colunas_relatorio, 
                    self.tabela_relatorio, 
                    filtro_coluna_relatorio, 
                    filtro_relatorio
                    )

                if status_mysql_relatorio['status']:

                    # Pegar o nome das colunas no banco de dados
                    lista_relatorio = status_mysql_relatorio['resultado']

                    # Atualizar variaveis
                    coluna_chaves = lista_relatorio[0]
                    coluna_status = lista_relatorio[1]
                    coluna_tem_xml = lista_relatorio[2]
                    relatorio_name = lista_relatorio[3]

                    # Lista de colunas
                    lista_colunas = [coluna_chaves, coluna_status, coluna_tem_xml]

                    # Caminho do relatorio
                    path_download_relatorio = os.path.join(path_download, relatorio_name)

                    # Criar filtro no excel
                    status_myexcel_lista = self.my_excel.excel_leitura(path_download_relatorio, lista_colunas)

                    if status_myexcel_lista['status']:

                        # Pegar lista de resultados
                        lista_resultado = status_myexcel_lista['resultado']
                        
                        # Atualizar variaveis
                        lista_chaves = lista_resultado[0]
                        lista_status = lista_resultado[1]
                        lista_tem_xml = lista_resultado[2]

                        # Chamar função de truncar (limpar os dados)
                        status_mysql_truncate = self.my_sql.mysql_truncate(
                            self.user, 
                            self.host,
                            self.database,
                            self.tabela_relatorio_temp
                            )

                        if status_mysql_truncate['status']:

                            # Lista de valores
                            lista_valores = [lista_chaves, lista_status, lista_tem_xml]

                            # Filtrar colunas ativas (com XML)
                            status_mysql_insert = self.my_sql.mysql_insert(
                                self.user, 
                                self.host,
                                self.database,
                                colunas_relatorio_temp, 
                                self.tabela_relatorio_temp, 
                                lista_valores
                                )

                            if status_mysql_insert['status']:
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