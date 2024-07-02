import mysql.connector
from modules.mylogger.mylogger import MyLogger

class MySQL():

    def __init__(self):

        # Variaveis gerais
        self.status = False
        self.sucesso = f'SUCESSO - {__name__}'
        self.falha = f'FALHA - {__name__}'
        self.erro = f'ERRO - {__name__}'

        # Instancias
        # Instanciar é uma boa prática e necessário
        # Não instaciar resulta na abertura de processo diferentes e erros
        self.my_logger = MyLogger()

        # Variaveis especificas
        self.cursos = None
        self.connection = None
        self.resultado = None
        self.resultado_temp = None
        self.lista_resultado = None
    
    # ------------------------------------ CONNECTION ------------------------------------
    
    # Função para conectar, executar query e desconectar da base de dados do MySQL
    def mysql_connection(self, user, password, host, database):

        """
        Módulo para criar um curso e permitir a realização do QUERY no banco de dados MySQL.
        NÃO IRÁ RETORNAR NENHUM RESULTADO

        Args:
            user (str): Nome do usuário no banco.
            password (str): Senha do usuário do banco.
            host (str): Endereçamento onde está localizado o banco.
            database (str): Nome do banco que deseja pesquisar.            
        """

        # TryCatch
        try:
            
            # Conexão com o banco de dados MySQL
            # Sempre colocar as credencias entre virgulas
            self.connection = mysql.connector.connect(
                user = user,
                password = password,
                host = host,
                database = database,
                charset = 'utf8mb4'
            )

            # Atribuir cursos
            self.cursor = self.connection.cursor()

            # Verificar conexão
            if self.connection.is_connected():
                self.status = True
                print(self.sucesso)

            else:
                self.status = False
                print(self.falha)
            
            # Alimentar log
            if self.status:
                self.my_logger.log_info(self.sucesso)
                self.my_logger.log_info('Sucesso ao conectar no Banco de Dados')

            else:
                self.my_logger.log_warn(self.falha)
                self.my_logger.log_warn('Falha ao conectar no Banco de Dados')

        except Exception as aviso:
            self.status = False
            print(self.erro)
            print(aviso)

            # Alimentar log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error('Erro ao conectar no Banco de Dados')
            self.my_logger.log_error(str(aviso))

        return{'status': self.status}
    
    # ------------------------------------ JOIN ------------------------------------
    
    # Função para realizar um JOIN de forma automatica
    def mysql_join(self, user, password, host, database, tabela, elemento_id = None):
            
        """
        Função para fazer um SELECT no banco de dados MySQL.
        Sempre irá retornar uma lista de resultados -> resultado = [[resultado_1], [resultado_2]]

        Args:
            user (str): Nome do usuário no banco.
            password (str): Senha do usuário do banco.
            host (str): Endereçamento onde está localizado o banco.
            database (str): Nome do banco que deseja pesquisar.
            tabela (str): Nome da tabela onde se econtra(m) a(s) coluna(s).
            elemento_id (str/list, opcional): Caso tenha alguma outra identificação da colunas relacionadas, pode passar a forma de identificação coluna = tabela
                obs.: Por padrão, irá identificar se possui algum dos elementos: 'id', 'id_', '_id', '_id_'
            join_type (str): Tipo de junção a ser aplicada na consulta (ex: 'INNER JOIN', 'LEFT JOIN', etc.).
                - Se especificado, será realizado um join entre a tabela principal e outra tabela.
                - Pode ser 'INNER JOIN', 'LEFT JOIN', 'RIGHT JOIN', etc.
        """

        # Variaveis
        id_list = ['id', 'id_', '_id', '_id_']

        # TryCatch
        try:

            # ------------------------- VERIFICAR NOVOS ELEMENTOS -------------------------

            # Verificar se existem elemento novos a serem pesquisados
            if elemento_id == None:

                # Seguir com os elementos da lista padrão
                elementos_id = id_list

            else:

                # Adicionar os novos elementos se não estiverem presentes na lista padrão
                elementos_id = id_list.append(elemento for elemento in elemento_id if not elemento in id_list)

            # ------------------------- CONECTAR NO BANCO DE DADOS -------------------------
                
            # Chamar função mysql_query
            status_mysql_connection = self.mysql_connection(user, password, host, database)

            if status_mysql_connection['status']:

                # ------------------------- SHOW TABLES -------------------------

                # Criar lista de resultados
                tabelas_banco = []

                # Listar todas as tabelas no banco de dados selecionado
                query_tabelas_banco ="SHOW TABLES"

                # Executar query
                self.cursor.execute(query_tabelas_banco)

                # Obtem as tabelas presentes no banco
                for tabelas_cursor in self.cursor:

                    # Fazer a TUPLA para retornar valor correto
                    tabelas_cursor_list = tabelas_cursor[0]
                    print('tabelas_cursor_list')
                    print(tabelas_cursor_list)

                    # Retornar o valor em um append
                    tabelas_banco.append(tabelas_cursor_list)
                    print('tabelas_banco')
                    print(tabelas_banco)

                if len(tabelas_banco) > 0:

                    tabelas_list = [tabela]         
                    tabelas_select = []
                    colunas_select = []
                    colunas_id = []
                    tabelas_join = []
                    colunas_join = []

                    # ------------------------- WHILE -------------------------

                    while len(tabelas_list) > 0:
                    #for tabelas_list_count in tabelas_list:

                        # Lista de colunas
                        colunas_describe = []
                        
                        # Query DESCRIBE
                        query_describe = f'DESCRIBE {tabelas_list[0]}'

                        # Executar query
                        self.cursor.execute(query_describe)

                        # Obtem os resultado no caso de DESCRIBE
                        query_describe_resultado = self.cursor.fetchall()

                        # Verifica se tem algum resultado/valor
                        if query_describe_resultado:

                            for valor in query_describe_resultado:

                                # Fazer a TUPLA para retornar valor correto
                                lista_query_describe_resultado = valor[0]
                                print('lista_query_describe_resultado')
                                print(lista_query_describe_resultado)

                                # Retornar o valor em um append
                                colunas_describe.append(lista_query_describe_resultado)
                                print('colunas_describe')
                                print(colunas_describe)

                            # ------------------------- SELECT LISTA -------------------------
                            # Lista utilizada para fazer o nome das colunas da nova tabela virtual
                            # Esquema do SELECT - 'SELECT {tabelas_join_select}_{colunas_join_select}'

                            # Coluna = [[lista], [lista]]
                            colunas_select.append(colunas_describe)
                            print('colunas_select')
                            print(colunas_select)

                            # Tabela = [tabela]
                            tabelas_select.append(tabelas_list[0])
                            print('tabelas_select')
                            print(tabelas_select)

                            # ------------------------- JOIN LISTA -------------------------
                            # Lista utilizada para fazer o JOIN das colunas da nova tabela virtual
                            # Esquema do JOIN - 'JOIN {tabelas_join_colunas} on {tabelas_join_select}.{colunas_join_tabelas} = {tabelas_join_colunas}.{colunas_join_id}'

                            # Filtrando as colunas que possuem os elementos do elementos_id
                            colunas_describe_id = [colunas_describe_count for colunas_describe_count in colunas_describe if any(id_ in colunas_describe_count for id_ in elementos_id)]
                            print('colunas_describe_id')
                            print(colunas_describe_id)

                            # ------------------------- COLUNA PK -------------------------
                            # Lista utilizada para buscar as colunas de FOREIGN KEY para a nova tabela virtual

                            # Filtrando as colunas que possuem os elementos MUL (Chave Multipla - Chave Estrangeira)
                            # Filtrando coluna primary_key da tabelas atual com o SHOW COLUMNS
                            query_show_columns = f'SHOW COLUMNS FROM {tabelas_list[0]}'

                            # Executar query
                            self.cursor.execute(query_show_columns)

                            # Obtem os resultado no caso de SELECT
                            query_show_columns_resultado = self.cursor.fetchall()
                            print('query_show_columns_resultado')
                            print(query_show_columns_resultado)

                            # Verifica se tem algum resultado/valor
                            if query_show_columns_resultado:

                                # Verificar todas as colunas
                                for resultado_count_mul in query_show_columns_resultado:
                                    
                                    # Se localizar a função de FOREIGN KEYS
                                    if 'MUL' in resultado_count_mul[3]:
                                        
                                        # Verifica se já não existe a coluna na lista de colunas_id
                                        if resultado_count_mul[0] not in colunas_describe_id:

                                            # Coluna da Chave Multipla (Estrangeira)
                                            colunas_describe_id.append(resultado_count_mul[0])

                            print('----------------- AQUI AGIRA NOW -------------------------------')
                            
                            print('colunas_describe_id')
                            print(colunas_describe_id)

                            # Pesquisar se coluna com 'id' é uma tabela
                            if len(colunas_describe_id) > 0:

                                # Itera sobre cada coluna em colunas_describe_id
                                for colunas_describe_id_count in colunas_describe_id:

                                    # Passar como str para fazer o replace
                                    colunas_describe_id_count = str(colunas_describe_id_count)

                                    for elementos_id_count in elementos_id:

                                        # Fazer a lista de possiveis tabelas existentes para verificar com a lista de tabelas real
                                        tabelas_possiveis = colunas_describe_id_count.replace(elementos_id_count, '')
                                        
                                        # Print de controle
                                        print('tabelas_possiveis')
                                        print(tabelas_possiveis)
                                        print('tabelas_banco')
                                        print(tabelas_banco)

                                        # Verificar se possivel tabela está no banco
                                        if tabelas_possiveis in tabelas_banco and tabelas_possiveis not in tabelas_list:
                                            
                                            # Se estiver, inserir a coluna e a tabela nas listas para fazer o join
                                            #tabelas_join.append(tabelas_possiveis)
                                            tabelas_join.append(tabelas_list[0])
                                            tabelas_list.append(tabelas_possiveis)
                                            colunas_join.append(colunas_describe_id_count)

                                # Print de controle
                                print('tabelas_join')
                                print(tabelas_join)
                                print('tabelas_list')
                                print(tabelas_list)
                                print('colunas_join')
                                print(colunas_join)
                                print('tabelas_banco')
                                print(tabelas_banco)

                                # ------------------------- COLUNA PK -------------------------
                                # Lista utilizada para buscar as colunas de PRIMARY KEY para a nova tabela virtual
                                                                
                                # Variaveis de controle temporario
                                coluna_join_pk = None
                                status_query_pk = False

                                # Verifica se tem algum resultado/valor
                                if query_show_columns_resultado:

                                    # Verificar todas as colunas
                                    for resultado_count_pk in query_show_columns_resultado:
                                        
                                        # Se localizar a função de PRIMARY KEY
                                        if 'PRI' in resultado_count_pk[3]:

                                            # Coluna da Chave Primaria (Primary Key)
                                            coluna_join_pk = resultado_count_pk[0]

                                            # Atualizar status
                                            status_query_pk = True

                                            print('coluna_join_pk')
                                            print(coluna_join_pk)
                                            print('Coluna da QUERY do ID')

                                        else:

                                            # Atualizar status
                                            status_query_pk = False

                                else:

                                    # Atualizar status
                                    status_query_pk = False

                                # Se não tiver, setar com a primeira coluna da tabela
                                if not status_query_pk:

                                    # Coluna da Chave Primaria (Primary Key)
                                    # Query DESCRIBE
                                    query_describe = f'DESCRIBE {tabelas_list[0]}'

                                    # Executar query
                                    self.cursor.execute(query_describe)

                                    # Obtem os resultado no caso de DESCRIBE
                                    query_describe_resultado = self.cursor.fetchall()

                                    # Verifica se tem algum resultado/valor
                                    if query_describe_resultado:

                                        coluna_join_pk = query_describe_resultado[0][0]

                                        # Print de controle
                                        print('coluna_join_pk')
                                        print(coluna_join_pk)
                                        print('Coluna de DESCRIBE do ID')

                                    else:
                                        
                                        coluna_join_pk = 'id'

                                        # Print de controle
                                        print('coluna_join_pk')
                                        print(coluna_join_pk)
                                        print('Coluna manual do ID')

                                # Atualizando listas de coluna_id
                                colunas_id.append(coluna_join_pk)

                            else:

                                # Informar que não existem colunas com o elemento id no banco (LOG)
                                print(f'Não existem os elementos: {elementos_id} nas colunas: {colunas_describe} presentes na tabela: {tabelas_list[0]} do Banco de Dados: {database}.')
                                self.my_logger.log_info(f'Não existem os elementos: {elementos_id} nas colunas: {colunas_describe} presentes na tabela: {tabelas_list[0]} do Banco de Dados: {database}.')

                        else:

                            # Informar que não foi possivel fazer o DESCRIBE
                            print(f'Falha ao realizar o DESCRIBE na tabela: {tabelas_list[0]} do Banco de Dados: {database}.')
                            self.my_logger.log_warn(f'Falha ao realizar o DESCRIBE na tabela: {tabelas_list[0]} do Banco de Dados: {database}.')
                            break

                        # Print de controle
                        print('----------------------------------------------------------------------')
                        print('tabelas_list')
                        print(tabelas_list)

                        # Retirar o primeiro elemento da lisa geral de tabelas
                        del tabelas_list[0]

                        # Print de controle
                        print('tabelas_list')
                        print(tabelas_list)

                    print('--------------------------------- MENUS ----------------------------------')

                    # Verificar se possui alguma tabela para dar JOIN
                    if len(tabelas_select) > 0:

                        # ------------------------- WRITE JOIN -------------------------
                        
                        # WRITE SELECT
                        # Esquema - 'SELECT {tabelas_join_select}_{colunas_join_select}'
                        
                        # Criar primeiros registros zerados
                        join_select = ''
                        join_on = ''

                        # Loop para pegar varias colunas de uma unica tabela
                        for count in range(len(colunas_select)):

                            join_select_count = ', '.join([f'{tabelas_select[count]}.{colunas_join_select_count} AS {tabelas_select[count]}_{colunas_join_select_count}' 
                                                     for colunas_join_select_count in colunas_select[count]])

                            # Adicionar uma virgula no final da da sentença da tabela + pular linha
                            join_select = join_select + join_select_count + ', ' + '\n'

                            # Print de controle
                            print('join_select')
                            print(join_select)

                        # Retirar ultima virgula do texto
                        join_select = join_select[:-3] + '\n'

                        # Print de controle
                        print('join_select')
                        print(join_select)
                        print('-------------------- PRINTS ------------------------------')
                        print('tabelas_join')
                        print(tabelas_join)
                        print('tabelas_select')
                        print(tabelas_select)
                        print('colunas_join')
                        print(colunas_join)
                        print('colunas_id')
                        print(colunas_id)
                        print('------------------------------------------------------')

                        # Realizar o delete dos primeiros elemtos da tabela select e colunas_id
                        del tabelas_select[0]
                        del colunas_id[0]

                        # Print de controle
                        print('tabelas_select')
                        print(tabelas_select)
                        print('colunas_id')
                        print(colunas_id)
                        
                        # WRITE JOIN
                        # Esquema - 'JOIN {tabelas_join_colunas} on {tabelas_join_select}.{colunas_join_tabelas} = {tabelas_join_colunas}.{colunas_join_id}'
                        
                        join_on = ' '.join([f'LEFT JOIN {tabelas_join_select_count} ON {tabelas_join_colunas_count_2}.{colunas_join_tabelas_count} = {tabelas_join_select_count}.{colunas_join_id_count} \n' 
                                            for tabelas_join_colunas_count_2, tabelas_join_select_count, colunas_join_tabelas_count, colunas_join_id_count in zip(tabelas_join, tabelas_select, colunas_join, colunas_id)])

                        # Print de controle
                        print('----------------------- SELECT --------------------------------')

                        # WRITE SELECT JOIN
                        # Esquema - 'SELECT {join_select} FROM {tabela} {join_on}'
                        select_join_on = f'SELECT {join_select} FROM {tabela} {join_on}'

                        # Print de controle
                        print(select_join_on)
                        print('-------------------------------------------------------')

                        # Atualizar resultado
                        self.resultado = select_join_on
                        mensagem = f'Este é o query para o JOIN:\n "{self.resultado}"'                    
                        self.my_logger.log_info(mensagem)
                        print(mensagem)

                    else:
                        self.status = False
                        print(self.falha)
                        print('Não existem tabelas para realizar o JOIN.')

                        # Alimentar log
                        self.my_logger.log_warn(self.falha)
                        self.my_logger.log_warn('Não existem tabelas para realizar o JOIN.')

                else:
                    self.status = False
                    print(self.falha)
                    print('Banco de Dados não possui tabelas para listar.')

                    # Alimentar log
                    self.my_logger.log_warn(self.falha)
                    self.my_logger.log_warn('Banco de Dados não possui tabelas para listar.')
            
            else:
                self.status = False
                print(self.falha)
            
            # Alimentar log
            if self.status:
                self.my_logger.log_info(self.sucesso)
                self.my_logger.log_info('Sucesso ao fazer o SELECT')
                #self.my_logger.log_info(str(self.resultado))

            else:
                self.my_logger.log_warn(self.falha)
                self.my_logger.log_warn('Falha ao fazer o SELECT')
        
        except Exception as aviso:
            self.status = False
            print(self.erro)
            print(aviso)

            # Alimentar log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error('Erro ao fazer o SELECT')
            self.my_logger.log_error(str(aviso))

        finally:
            # Sempre desconectar do banco de dados após o query
            self.cursor.close()
            self.connection.close()

        return{'status': self.status, 'resultado': self.resultado}
    
    # ------------------------------------ SELECT ------------------------------------
    
    # SELECT
    def mysql_select(self, user, password, host, database, tabela, coluna_principal, coluna_filtro = None, filtro = None, join = None):

        """
        Função para fazer um SELECT no banco de dados MySQL.
        Sempre irá retornar uma lista de resultados -> resultado = [resultado_1, resultado_2]

        Args:
            user (str): Nome do usuário no banco.
            password (str): Senha do usuário do banco.
            host (str): Endereçamento onde está localizado o banco.
            database (str): Nome do banco que deseja pesquisar.
            tabela (str): Nome da tabela onde se econtra(m) a(s) coluna(s).
            coluna_principal (str/list): Nome(s) da(s) coluna(s) que deseja obter os dados.
                - No caso de colunas para JOIN, seguir a ordem: coluna_principal = [[tabela_dimensão(str), coluna_dimensão(str)]].
            coluna_filtro (str/list, opcional): Nome(s) da(s) coluna(s) a ser(em) utilizada(s) como filtro na consulta.
                - Se uma lista for fornecida, a filtragem será aplicada a múltiplas colunas simultaneamente.
                - No caso de colunas para JOIN, seguir a ordem: coluna_filtro = [[tabela_dimensão(str), coluna_dimensão(str)]].
            filtro (str/list, opcional): Valor(es) correspondente(s) à(s) coluna(s) de filtro.
                - Se uma lista for fornecida, cada valor será utilizado como filtro para a(s) coluna(s) correspondente(s).
            join (str, opcional): Informar se gostaria de realizar o JOIN da tabela principal ('TRUE').
                - Se especificado, será realizado um join entre a tabela principal e demais tabelas necessárias.

        Returns:
            list: Lista de resultados da consulta.
        """

        # Variaveis
        coluna_principal_list = isinstance(coluna_principal, list)
        coluna_filtro_list = isinstance(coluna_filtro, list)
        
        # TryCatch
        try:

            # Verificar se tem JOIN
            if join == None:

                select_join = None

            else:

                # Chamar função para fazer JOIN
                status_mysql_join = self.mysql_join(user, password, host, database, tabela)

                if status_mysql_join['status']:

                    # Atualizar lista de select
                    select_join = status_mysql_join['resultado']

                else:
                    select_join = None

            # Chamar função mysql_query
            status_mysql_connection = self.mysql_connection(user, password, host, database)

            if status_mysql_connection['status']:

                # Criar lista de filtros
                if coluna_filtro == None:

                    # Atualiza que não existem nenhum filtro
                    filtros = None
                
                elif coluna_filtro_list:
                    
                    # Criar lista vazia
                    coluna_filtros_join = []

                    # Fazer loop para verificar necessidade de JOIN
                    for coluna_filtro_count in coluna_filtro:
                        
                        # Se existir sublista para JOIN
                        if isinstance(coluna_filtro_count, list):
                            
                            # Juntar no formato padrão do JOIN - Nome da coluna no JOIN: 'tabela_dimensão'.'coluna_dimensão' AS 'tabela_dimensão'_'coluna_dimensão'
                            coluna_filtros_join.append('_'.join(coluna_filtro_count))

                        else:

                            # Juntar a coluna normalmente
                            coluna_filtros_join.append(coluna_filtro_count)

                    # Criar os filtros de acordo com a quantidade passada na lista
                    filtros = ' AND '. join([f'{coluna} = "{valor}"' for coluna, valor in zip(coluna_filtros_join, filtro)])

                else:

                    # Criar filtro unico
                    filtros = f'{coluna_filtro} = "{filtro}"'

                # Criar lista de colunas
                if coluna_principal_list:
                    
                    # Criar lista vazia
                    colunas = []

                    # Fazer loop para verificar necessidade de JOIN
                    for coluna_principal_count in coluna_principal:
                        
                        # Se existir sublista para JOIN
                        if isinstance(coluna_principal_count, list):
                            
                            # Juntar no formato padrão do JOIN - Nome da coluna no JOIN: 'tabela_dimensão'.'coluna_dimensão' AS 'tabela_dimensão'_'coluna_dimensão'
                            colunas.append('_'.join(coluna_principal_count))

                        else:

                            # Juntar a coluna normalmente
                            colunas.append(coluna_principal_count)

                else:

                    # Criar lista unica
                    colunas = [coluna_principal]

                # Criar lista de resultados
                self.resultado = []

                # Laço de repetição 
                for colunas_count in colunas:

                    if filtros == None:

                        if select_join == None:

                            # Query - SELECT
                            query = f'SELECT {colunas_count} FROM {tabela}'

                        else:

                            # Query - SELECT + JOIN
                            query = f'WITH Tabela_Virtual AS ({select_join}) SELECT {colunas_count} FROM Tabela_Virtual'

                    else:

                        if select_join == None:
                    
                            # Query - SELECT
                            query = f'SELECT {colunas_count} FROM {tabela} WHERE {filtros}'

                        else:

                            # Query - SELECT + JOIN
                            query = f'WITH Tabela_Virtual AS ({select_join}) SELECT {colunas_count} FROM Tabela_Virtual WHERE {filtros}'

                    print('-------------------------------')
                    print(select_join)
                    print(colunas_count)
                    print(filtros)
                    print(query)
                    print('-------------------------------')

                    mensagem = f'Este é o query para o SELECT:\n "{query}"'                    
                    self.my_logger.log_info(mensagem)
                    print(mensagem)

                    # Executar query
                    self.cursor.execute(query)

                    # Obtem os resultado no caso de SELECT
                    resultado = self.cursor.fetchall()
                    print('resultado')
                    print(resultado)

                    # Verifica se tem algum resultado/valor
                    if resultado:

                        # Criar lista zerada
                        self.resultado_temp = []

                        for valor in resultado:

                            # Fazer a TUPLA para retornar valor correto
                            self.lista_resultado = valor[0]
                            print('lista_resultado')
                            print(self.lista_resultado)

                            # Retornar o valor em um append
                            self.resultado_temp.append(self.lista_resultado)
                            print('resultado_temp')
                            print(self.resultado_temp)

                        self.resultado.append(self.resultado_temp)
                        print('resultado')
                        print(self.resultado)

                        self.status = True
                        print(self.sucesso)

                    else:
                        self.status = False
                        print(self.falha)

            else:
                self.status = False
                print(self.falha)
            
            # Alimentar log
            if self.status:
                self.my_logger.log_info(self.sucesso)
                self.my_logger.log_info('Sucesso ao fazer o SELECT')
                self.my_logger.log_info(str(self.resultado))

            else:
                self.my_logger.log_warn(self.falha)
                self.my_logger.log_warn('Falha ao fazer o SELECT')

        except Exception as aviso:
            self.status = False
            print(self.erro)
            print(aviso)

            # Alimentar log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error('Erro ao fazer o SELECT')
            self.my_logger.log_error(str(aviso))

        finally:
            # Sempre desconectar do banco de dados após o query
            self.cursor.close()
            self.connection.close()

        return{'status': self.status, 'resultado': self.resultado}
    
    # ------------------------------------ UPDATE ------------------------------------
    
    # UPDATE
    def mysql_update(self, user, password, host, database, tabela, coluna_principal, coluna_filtro, filtro, update):

        """
        Função para fazer um UPDATE no banco de dados MySQL.
        Não suporta Tabelas Virtuais (CTEs).

        Args:
            user (str): Nome do usuário no banco.
            password (str): Senha do usuário do banco.
            host (str): Endereçamento onde está localizado o banco.
            database (str): Nome do banco que deseja pesquisar.
            tabela (str): Nome da tabela onde se econtra(m) a(s) coluna(s).
            coluna_principal (str/list): Nome(s) da(s) coluna(s) que deseja atualizar os dados.            
            coluna_filtro (str/list): Nome(s) da(s) coluna(s) para utilizar como filtro.
            filtro (str/list): Nome(s) do(s) elemento(s) que correspende(m) a coluna_filtro.
            join (str, opcional): Informar se gostaria de realizar o JOIN da tabela principal ('TRUE').
                - Se especificado, será realizado um join entre a tabela principal e demais tabelas necessárias.
        """

        # Variaveis
        coluna_principal_list = isinstance(coluna_principal, list)
        coluna_filtro_list = isinstance(coluna_filtro, list)

        # TryCatch
        try:

            # Chamar função mysql_query
            status_mysql_connection = self.mysql_connection(user, password, host, database)

            if status_mysql_connection['status']:

                # Criar lista de filtros
                if coluna_filtro_list:

                    # Criar os filtros de acordo com a quantidade passada na lista
                    filtros = ' AND '. join([f'{coluna} = "{valor}"' for coluna, valor in zip(coluna_filtro, filtro)])
                    
                else:
                    # Criar filtro unico
                    filtros = f'{coluna_filtro} = "{filtro}"'

                # Verificar se coluna_principal é uma lista
                if coluna_principal_list:

                    # Identificar nova variavel de colunas
                    colunas = coluna_principal

                else:

                    # Criar lista unica
                    colunas = [coluna_principal]

                # Laço de repetição 
                for count in range(len(colunas)):
                    
                    # Query - SELECT
                    query = f'UPDATE {tabela} SET {colunas[count]} = %s WHERE {filtros}'
                    mensagem = f'Este é o query para o UPDATE:\n "{query}"'                    
                    self.my_logger.log_info(mensagem)
                    print(mensagem)

                    # Executar query
                    self.cursor.execute(query, (update, ))

                    # Confirma a atualização no banco de dados
                    self.connection.commit()

                    self.status = True
                    print(self.sucesso)

            else:
                self.status = False
                print(self.falha)
            
            # Alimentar log
            if self.status:
                self.my_logger.log_info(self.sucesso)
                self.my_logger.log_info('Sucesso ao fazer o UPDATE')
                self.my_logger.log_info(str(update))

            else:
                self.my_logger.log_warn(self.falha)
                self.my_logger.log_warn('Falha ao fazer o UPDATE')

        except Exception as aviso:
            self.status = False
            print(self.erro)
            print(aviso)

            # Alimentar log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error('Erro ao fazer o UPDATE')
            self.my_logger.log_error(str(aviso))

        finally:
            # Sempre desconectar do banco de dados após o query
            self.cursor.close()
            self.connection.close()

        return{'status': self.status}
    
    # ------------------------------------ INSERT ------------------------------------
    
    # INSERT
    def mysql_insert(self, user, password, host, database, tabela, coluna, valor):

        """
        Função para fazer um INSERT no banco de dados MySQL.
        Não suporta Tabelas Virtuais (CTEs).

        Args:
            user (str): Nome do usuário no banco.
            password (str): Senha do usuário do banco.
            host (str): Endereçamento onde está localizado o banco.
            database (str): Nome do banco que deseja pesquisar.
            tabela (str): Nome da tabela onde se econtra(m) a(s) coluna(s).
            coluna (str/list): Nome(s) da(s) coluna(s) que deseja inserir os dados.
            valor (str/list): Nome(s) do(s) valor(s) para inserir na(s) coluna(s).
        """

        # Variaveis
        coluna_list = isinstance(coluna, list)
        valor_list = isinstance(valor, list)

        # TryCatch
        try:

            # Chamar função mysql_query
            status_mysql_connection = self.mysql_connection(user, password, host, database)

            if status_mysql_connection['status']:

                # Criar lista de colunas
                if coluna_list:

                    # Identificar nova variavel de colunas
                    colunas = ', '.join(coluna)

                else:

                    # Criar lista unica
                    colunas = coluna

                # Criar lista de valores
                if valor_list:
                    
                    # Identificar nova variavel de valores
                    #valores = ', '.join("'" + item + "'" for item in valor)
                    valores = ', '.join(['%s'] * len(valor))

                else:

                    # Criar lista unica
                    valores = '%s'
                    valor = [valor]

                # Query - INSERT
                query = f'INSERT INTO {tabela} ({colunas}) VALUES ({valores})'
                mensagem = f'Este é o query para o INSERT:\n "{query}"'                    
                self.my_logger.log_info(mensagem)
                print(mensagem)

                # Executar query
                self.cursor.execute(query, valor)

                # Confirma a atualização no banco de dados
                self.connection.commit()

                self.status = True
                print(self.sucesso)
                self.my_logger.log_info(str(valores))

            else:
                self.status = False
                print(self.falha)
            
            # Alimentar log
            if self.status:
                self.my_logger.log_info(self.sucesso)
                self.my_logger.log_info('Sucesso ao fazer o INSERT')

            else:
                self.my_logger.log_warn(self.falha)
                self.my_logger.log_warn('Falha ao fazer o INSERT')

        except Exception as aviso:
            self.status = False
            print(self.erro)
            print(aviso)

            # Alimentar log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error('Erro ao fazer o INSERT')
            self.my_logger.log_error(str(aviso))

        finally:
            # Sempre desconectar do banco de dados após o query
            self.cursor.close()
            self.connection.close()

        return{'status': self.status}
    
    # ------------------------------------ CREATE TABLE ------------------------------------
    
    # CREATE TABLE
    def mysql_create_table(self, user, password, host, database, tabela, coluna):

        """
        Módulo para criar uma nova tabela no banco de dados MySQL.
        Não suporta Tabelas Virtuais (CTEs).

        Args:
            user (str): Nome do usuário no banco.
            password (str): Senha do usuário do banco.
            host (str): Endereçamento onde está localizado o banco.
            database (str): Nome do banco que deseja pesquisar.
            tabela (str): Nome da tabelaque deseja criar.
            coluna (str/list): Nome(s) da(s) coluna(s) que deseja adicionar na nova tabela.
        """

        # Variaveis
        coluna_list = isinstance(coluna, list)

        # TryCatch
        try:

            # Chamar função mysql_query
            status_mysql_connection = self.mysql_connection(user, password, host, database)

            if status_mysql_connection['status']:

                # Criar lista de colunas
                if coluna_list:

                    # Identificar nova variavel de colunas
                    colunas = ', '.join(coluna)

                else:

                    # Criar coluna unica
                    colunas = coluna

                # Query
                query = f'CREATE TABLE IF NOT EXISTS {tabela} ({colunas}) DEFAULT CHARSET = utf8mb4'
                mensagem = f'Este é o query para o CREATE TABLE:\n "{query}"'                    
                self.my_logger.log_info(mensagem)
                print(mensagem)

                # Executar query
                self.cursor.execute(query)

                # Confirma a atualização no banco de dados
                self.connection.commit()

                self.status = True
                print(self.sucesso)

            else:
                self.status = False
                print(self.falha)
            
            # Alimentar log
            if self.status:
                self.my_logger.log_info(self.sucesso)
                self.my_logger.log_info('Sucesso ao fazer o CREATE TABLE')

            else:
                self.my_logger.log_warn(self.falha)
                self.my_logger.log_warn('Falha ao fazer o CREATE TABLE')

        except Exception as aviso:
            self.status = False
            print(self.erro)
            print(aviso)

            # Alimentar log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error('Erro ao fazer o CREATE TABLE')
            self.my_logger.log_error(str(aviso))

        finally:
            # Sempre desconectar do banco de dados após o query
            self.cursor.close()
            self.connection.close()

        return{'status': self.status}
    
    # ------------------------------------ TRUNCATE ------------------------------------
    
    # TRUNCATE
    def mysql_truncate(self, user, password, host, database, tabela):

        """
        Módulo para fazer um TRUNCATE no banco de dados MySQL.
        Irá apagar todos os dados da(s) coluna(s) presentes na tabela informada.
        Não suporta Tabelas Virtuais (CTEs).

        Args:
            user (str): Nome do usuário no banco.
            password (str): Senha do usuário do banco.
            host (str): Endereçamento onde está localizado o banco.
            database (str): Nome do banco que deseja pesquisar.
            tabela (str): Nome da tabela onde se econtra(m) o(s) dado(s) que deseja apagar.
        """

        # Variaveis
        tabela_list = isinstance(tabela, list)

        # TryCatch
        try:

            # Chamar função mysql_query
            status_mysql_connection = self.mysql_connection(user, password, host, database)

            if status_mysql_connection['status']:

                if tabela_list:

                    # Identificar nova variavel de tabelas
                    tabelas = tabela

                else:

                    # Criar lista unica
                    tabelas = [tabela]

                # Loop para inserir todos os valores
                for count in range(len(tabelas)):

                    # Query
                    query = f'truncate {tabelas[count]}'
                    mensagem = f'Este é o query para o TRUNCATE:\n "{query}"'                    
                    self.my_logger.log_info(mensagem)
                    print(mensagem)
                    
                    # Executar query
                    self.cursor.execute(query)

                    # Confirma a atualização no banco de dados
                    self.connection.commit()

                    self.status = True
                    print(self.sucesso)

            else:
                self.status = False
                print(self.falha)
            
            # Alimentar log
            if self.status:
                self.my_logger.log_info(self.sucesso)
                self.my_logger.log_info('Sucesso ao fazer o TRUNCATE')

            else:
                self.my_logger.log_warn(self.falha)
                self.my_logger.log_warn('Falha ao fazer o TRUNCATE')

        except Exception as aviso:
            self.status = False
            print(self.erro)
            print(aviso)

            # Alimentar log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error('Erro ao fazer o TRUNCATE')
            self.my_logger.log_error(str(aviso))

        finally:
            # Sempre desconectar do banco de dados após o query
            self.cursor.close()
            self.connection.close()

        return{'status': self.status}
    
    # ------------------------------------ DESCRIBE ------------------------------------
    
    # DESCRIBE
    def mysql_describe(self, user, password, host, database, tabela):

        """
        Módulo para informar todas as colunas presentes em uma tabela no banco de dados MySQL.
        Sempre irá retornar uma lista de resultados -> resultado = [resultado_1, resultado_2]

        Args:
            user (str): Nome do usuário no banco.
            password (str): Senha do usuário do banco.
            host (str): Endereçamento onde está localizado o banco.
            database (str): Nome do banco que deseja pesquisar.
            tabela (str): Nome da tabelaque deseja obter as colunas.
        """

        # TryCatch
        try:

            # Chamar função mysql_query
            status_mysql_connection = self.mysql_connection(user, password, host, database)

            if status_mysql_connection['status']:

                # Query
                query = f'DESCRIBE {tabela}'

                # Executar query
                self.cursor.execute(query)

                # Obtem os resultado no caso de DESCRIBE
                resultado = self.cursor.fetchall()

                # Verifica se tem algum resultado/valor
                if resultado:

                    for valor in resultado:

                        # Fazer a TUPLA para retornar valor correto
                        self.lista_resultado = valor[0]
                        print('lista_resultado')
                        print(self.lista_resultado)

                        # Retornar o valor em um append
                        self.resultado.append(self.lista_resultado)
                        print('resultado')
                        print(self.resultado)

                        self.status = True
                        print(self.sucesso)

                else:
                    self.status = False
                    print(self.falha)

            else:
                self.status = False
                print(self.falha)
            
            # Alimentar log
            if self.status:
                self.my_logger.log_info(self.sucesso)
                self.my_logger.log_info('Sucesso ao fazer o DESCRIBE.')

            else:
                self.my_logger.log_warn(self.falha)
                self.my_logger.log_warn('Falha ao fazer o DESCRIBE.')

        except Exception as aviso:
            self.status = False
            print(self.erro)
            print(aviso)

            # Alimentar log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error('Erro ao fazer o DESCRIBE.')
            self.my_logger.log_error(str(aviso))

        finally:
            # Sempre desconectar do banco de dados após o query
            self.cursor.close()
            self.connection.close()

        return{'status': self.status, 'resultado': self.resultado}
    
    # ------------------------------------ INFORMATION SCHEMA ------------------------------------

    # INFORMATION SCHEMA
    def mysql_information_schema(self, user, password, host, database):

        """
        Módulo para informar todas as tabelas presentes em um banco de dados MySQL.
        Sempre irá retornar uma lista de resultados -> resultado = [resultado_1, resultado_2]

        Args:
            user (str): Nome do usuário no banco.
            password (str): Senha do usuário do banco.
            host (str): Endereçamento onde está localizado o banco.
            database (str): Nome do banco que deseja pesquisar.
        """

        # TryCatch
        try:

            # Chamar função mysql_query
            status_mysql_connection = self.mysql_connection(user, host, database)

            if status_mysql_connection['status']:

                # Query
                query = f'SELECT table_name FROM information_schema.tables WHERE table_schema = {database}'

                # Executar query
                self.cursor.execute(query)

                # Obtem os resultado no caso de DESCRIBE
                resultado = self.cursor.fetchall()

                # Verifica se tem algum resultado/valor
                if resultado:

                    for valor in resultado:

                        # Fazer a TUPLA para retornar valor correto
                        self.lista_resultado = valor[0]
                        print('lista_resultado')
                        print(self.lista_resultado)

                        # Retornar o valor em um append
                        self.resultado.append(self.lista_resultado)
                        print('resultado')
                        print(self.resultado)

                        self.status = True
                        print(self.sucesso)

                else:
                    self.status = False
                    print(self.falha)

            else:
                self.status = False
                print(self.falha)
            
            # Alimentar log
            if self.status:
                self.my_logger.log_info(self.sucesso)
                self.my_logger.log_info('Sucesso ao fazer o DESCRIBE.')

            else:
                self.my_logger.log_warn(self.falha)
                self.my_logger.log_warn('Falha ao fazer o DESCRIBE.')

        except Exception as aviso:
            self.status = False
            print(self.erro)
            print(aviso)

            # Alimentar log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error('Erro ao fazer o DESCRIBE.')
            self.my_logger.log_error(str(aviso))

        finally:
            # Sempre desconectar do banco de dados após o query
            self.cursor.close()
            self.connection.close()

        return{'status': self.status, 'resultado': self.resultado}