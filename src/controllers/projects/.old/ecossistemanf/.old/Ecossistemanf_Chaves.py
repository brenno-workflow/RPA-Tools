from modulos.mylogger.mylogger import MyLogger
from modulos.mysql.mysql import MySQL
from modulos.myrequest.myrequest import MyRequest

class EcossistemanfChaves:
        
    def __init__(self, 
                 user, host, database, module_fsist, process,  
                 coluna_module, coluna_process, coluna_status, coluna_url, coluna_chaves, coluna_filtro, 
                 tabela_ecossistemanf_chaves, tabela_ecossistemanf_chaves_temp
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
        self.my_request = MyRequest()
        
        # Metodo de 'INJEÇÃO DE DEPENDENCIA'
        # ref.: https://www.youtube.com/watch?v=5DBfVnQn1Ow
        
        # Variaveis especificas
        self.user = user
        self.host = host
        self.database = database

        # Valores
        self.module = module_fsist
        self.process = process

        # Colunas
        self.coluna_modules = coluna_module
        self.coluna_process = coluna_process
        self.coluna_status = coluna_status
        self.coluna_url = coluna_url
        self.coluna_chaves = coluna_chaves
        self.coluna_filtro = coluna_filtro

        # Tabelas
        self.tabela_chaves = tabela_ecossistemanf_chaves
        self.tabela_chaves_temp = tabela_ecossistemanf_chaves_temp

    # Função para fazer o quests das chaves ativas e canceldas do ecossistemanf
    def ecossistemanf_chaves(self):

        # Variaveis
        colunas_chaves = [self.coluna_status, self.coluna_url, self.coluna_filtro]
        coluna_chaves_temp = [self.coluna_chaves, self.coluna_status]
        
        # TryCatch
        try:

            # Fazer o select dos parametros no banco de dados 
            status_mysql_select = self.my_sql.mysql_select(
                self.user, 
                self.host,
                self.database,
                colunas_chaves, 
                self.tabela_chaves
                )

            if status_mysql_select['status']:

                # Pegar lista de resultados
                lista_resultado = status_mysql_select['resultado']

                # Atualizar variaveis com o resultado
                filtro_ativas = lista_resultado[0]
                filtro_canceladas = lista_resultado[1]
                urls_ativas = lista_resultado[2]
                urls_canceladas = lista_resultado[3]
                filtro_requests = lista_resultado[4]

                # Lista de urls
                lista_urls = [urls_ativas, urls_canceladas]
        
                # Fazar os requests
                status_requests_ecossitemanf = self.my_request.requests_get(lista_urls, filtro_requests)

                if status_requests_ecossitemanf['status']:

                    # Pegar a lista de resulatdos
                    lista_resultado = status_requests_ecossitemanf['resultado']

                    # Atualizar variaveis com o resultado
                    chaves_ativas = lista_resultado[0]
                    chaves_canceladas = lista_resultado[1]

                    # Criar listas para INSERT
                    lista_status_ativas = [f'{filtro_ativas}'] * len(chaves_ativas)
                    lista_status_canceladas = [f'{filtro_canceladas}'] * len(chaves_canceladas)

                    # Lista de valores
                    lista_chaves_ativas = [chaves_ativas, lista_status_ativas]
                    lista_chaves_canceladas = [chaves_canceladas, lista_status_canceladas]

                    # Faezr o truncate da tabela
                    status_mysql_truncate = self.my_sql.mysql_truncate(
                        self.user, 
                        self.host,
                        self.database,
                        self.tabela_chaves_temp
                        )

                    if status_mysql_truncate['status']:

                        # Fazer o insert das chaves ativas
                        status_mysql_inser_ativas = self.my_sql.mysql_insert(
                            self.user, 
                            self.host,
                            self.database,
                            coluna_chaves_temp, 
                            self.tabela_chaves_temp, 
                            lista_chaves_ativas
                            )

                        if status_mysql_inser_ativas['status']:

                            # Fazer o insert das chaves canceladas
                            status_mysql_inser_canceladas = self.my_sql.mysql_insert(
                                self.user, 
                                self.host,
                                self.database,
                                coluna_chaves_temp, 
                                self.tabela_chaves_temp, 
                                lista_chaves_canceladas
                                )
                            
                            if status_mysql_inser_canceladas['status']:
                                self.status = True
                                print(self.sucesso)

                            else:
                                self.status = False
                                print(self.falha)

                        else:
                            self.status = False
                            print(self.falha)

                    else:
                        self.status = False
                        print(self.falha)

                else:
                    self.status = False
                    print(self.falha)
            
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

    