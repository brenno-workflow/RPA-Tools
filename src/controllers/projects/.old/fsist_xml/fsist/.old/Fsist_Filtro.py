from modulos.mylogger.mylogger import MyLogger
from modulos.mysql.mysql import MySQL
from modulos.myfilter.myfilter import MyFilter
from modulos.myweb.myweb import MyWeb

class FsistFiltro:
        
    def __init__(self, 
                 my_driver, user, host, database, id, 
                 coluna_id, coluna_chaves, coluna_status, coluna_xml, coluna_filtro_ativas, coluna_filtro_canceladas, coluna_filtro_tem_xml,
                 tabela_fsist_relatorio, tabela_fsist_relatorio_temp, tabela_ecossistemanf_chaves_temp
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
        self.my_filter = MyFilter()
        
        # Metodo de 'INJEÇÃO DE DEPENDENCIA'
        # ref.: https://www.youtube.com/watch?v=5DBfVnQn1Ow
        self.my_web = MyWeb(my_driver)

        # Variaveis especificas
        self.user = user
        self.host = host
        self.database = database

        # Valores
        self.id = id
        self.resultado = None

        # Colunas
        self.coluna_id = coluna_id
        self.coluna_chaves = coluna_chaves
        self.coluna_status = coluna_status
        self.coluna_tem_xml = coluna_xml
        self.coluna_filtro_ativas = coluna_filtro_ativas
        self.coluna_filtro_canceladas = coluna_filtro_canceladas
        self.coluna_filtro_tem_xml = coluna_filtro_tem_xml

        # Tabelas
        self.tabela_relatorio = tabela_fsist_relatorio
        self.tabela_relatorio_temp = tabela_fsist_relatorio_temp
        self.tabela_ecossistemanf_temp = tabela_ecossistemanf_chaves_temp
    # ------------------------------------ FILTROS ------------------------------------
    
    # Fazer o filtro de chaves ativas
    def fsist_filtro_chaves(self, status):

        """
        Função para fazer um filtro especifico de duas tabelas.
        Sempre ira retornar uma lista de resultados.
        
        OBS.: A lista pode ser nula, no caso de ausencia de novas notas.

        Args:
            status (str): Determinar se deseja das notas ativas ou canceladas.
                Opções: 'ativas', 'canceladas'.
        """

        # Variaveis
        status_ativas = 'ativas'
        status_canceladas = 'canceladas'
        lista_coluna_relatorio = [self.coluna_filtro_ativas, self.coluna_filtro_canceladas, self.coluna_filtro_tem_xml]
        lista_coluna_filtros_relatorio = [self.coluna_status, self.coluna_tem_xml]

        # TryCatch
        try:

            # Fazer o select dos filtro no Banco de Dados
            status_mysql_relatorio = self.my_sql.mysql_select(
                self.user, 
                self.host,
                self.database,
                lista_coluna_relatorio, 
                self.tabela_relatorio, 
                self.coluna_id, 
                self.id
                )

            if status_mysql_relatorio['status']:

                # Pegar o nome das colunas no banco de dados
                lista_relatorio = status_mysql_relatorio['resultado']

                # Atualizar variaveis
                filtro_ativas = lista_relatorio[0]
                filtro_canceladas = lista_relatorio[1]
                filtro_tem_xml = lista_relatorio[2]

                if status_mysql_relatorio['status']:

                    if status == status_ativas:

                        # Atualizar o log
                        self.my_logger.log_info('Lista de chaves ativas presentes no servidor do Ecossistemanf.')

                        # Filtrar resultado com lista do ecossistemanf
                        status_ecossistemanf_filtro = self.my_sql.mysql_select(
                            self.user, 
                            self.host,
                            self.database,
                            self.coluna_chaves, 
                            self.tabela_ecossistemanf_temp, 
                            self.coluna_status, 
                            filtro_ativas
                            )

                        # Criar lista de filtros
                        lista_filtros_relatorio = [filtro_ativas, filtro_tem_xml]
                    
                    elif status == status_canceladas:

                        # Atualizar o log
                        self.my_logger.log_info('Lista de chaves canceladas presentes no servidor do Ecossistemanf.')

                        # Filtrar resultado com lista do ecossistemanf
                        status_ecossistemanf_filtro = self.my_sql.mysql_select(
                            self.user, 
                            self.host,
                            self.database,
                            self.coluna_chaves, 
                            self.tabela_ecossistemanf_temp, 
                            self.coluna_status, 
                            filtro_canceladas
                            )

                        # Criar lista de filtros
                        lista_filtros_relatorio = [filtro_canceladas, filtro_tem_xml]

                    else:
                        self.status = False
                        print(self.falha)

                    if status_ecossistemanf_filtro['status']:

                        # Atualizar variavel com a lista de chaves filtradas
                        ecossistemanf_chaves_filtro = status_ecossistemanf_filtro['resultado']

                        # Atualizar o log
                        self.my_logger.log_info('Lista de chaves presentes no relatorio do Fsist.')

                        # Chamar função para fazer filtros (lista de filtros) da tabela do relatorio no Banco de Dados
                        status_relatorio_filtro = self.my_sql.mysql_select(
                            self.user, 
                            self.host,
                            self.database,
                            self.coluna_chaves, 
                            self.tabela_relatorio_temp, 
                            lista_coluna_filtros_relatorio, 
                            lista_filtros_relatorio
                            )

                        if status_relatorio_filtro['status']:

                            # Atualizar variavel com a lista de chaves filtradas
                            relatorio_chaves_filtro = status_relatorio_filtro['resultado']

                            # Chamar função para fazer um filtro entre duas listas
                            status_filtro_lista = self.my_filter.lista_nao_lista(relatorio_chaves_filtro, ecossistemanf_chaves_filtro)

                            if status_filtro_lista['status']:

                                # Atualizar variavel com a lista de chaves filtradas
                                self.resultado = status_filtro_lista['resultado']

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

        return{'status': self.status, 'resultado': self.resultado}