from modules.mylogger.mylogger import MyLogger

class MyFilter:
        
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
        self.resultado = None
        self.lista_resultado = None
    
    # Função para buscar os valores da lista principal na lista filtro
    def lista_nao_lista(self, lista_principal, lista_filtro):

        """
        Módulo para fazer um FILTRO entre duas listas.
        Sempre irá retornar uma lista de resultados -> resultado = [lista]

        Args:
            lista_principal (list): Lista que contem os valores desejados.
            lista_filtro (list): Lista com todos os valores antigos para realizar o filtro.
        """

        # Variaveis
        self.lista_resultado = []

        # TryCatch
        try:

            for valor in lista_principal:

                # Fazer o filtro 
                if valor not in lista_filtro:

                    # Atualizar lista de resultados
                    self.lista_resultado.append(valor)
                    print('self.lista_resultado')
                    print(self.lista_resultado)
            
            # Atualizar variavel de retorno
            self.resultado = self.lista_resultado
            print('self.resultado')
            print(self.resultado)

            self.status = True
            print(self.sucesso)
            
            # Alimentar o log
            if self.status:
                self.my_logger.log_info('Filtro dos elementos da lista_principal que não estavam presentes na lista_filtro:')
                self.my_logger.log_info(self.resultado)

        except Exception as aviso:
            self.status = False
            print(self.erro)
            print(aviso)

            # Alimentar o log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error(str(aviso))

        return{'status': self.status, 'resultado': self.resultado}
    
    # Função para buscar uma extensão na lista filtro
    def elemento_em_lista(self, lista_filtro, elemento):

        """
        Módulo para fazer um FILTRO de elemento(s) em uma lista.
        Sempre irá retornar uma lista de resultados -> resultado = [lista]

        Args:
            elemento (str/list): Valor(es) desejado(s).
                obs: Se for uma extensão, passar como elemento='.{extensao}'
            lista_filtro (list): Lista com todos os valores antigos para realizar o filtro.
        """

        # Variaveis
        elemento_list = isinstance(elemento, list)

        # TryCatch
        try:

            # Verifica se corresponde a uma lista de extensões
            if elemento_list:

                # Atualiza o valor da lista desejada
                elementos = elemento

            else:

                # Cria uma lista unica
                elementos = [elemento]

            # Criar uma nova lista zerada
            self.lista_resultado = []

            for valor in elementos:

                # Fazer o filtro 
                for arquivo in lista_filtro:

                    # Preciso especificar que se trata de um 'str' para utilizar: 'startwith', 'endswith', etc
                    arquivo = str(arquivo)
                    valor = str(valor)

                    # Verifica se o valor é uma extensão
                    if valor.startswith('.'):

                        # Verificar se o arquivo termina com a extensao informada
                        if arquivo.endswith(valor):

                            # Atualizar lista de resultados
                            self.lista_resultado.append(arquivo)
                            print('self.lista_resultado')
                            print(self.lista_resultado)

                    else:

                        # Verifica se o arquivo é igual ao valor da lista
                        if arquivo == valor:

                            # Atualizar lista de resultados
                            self.lista_resultado.append(arquivo)
                            print('self.lista_resultado')
                            print(self.lista_resultado)

            # Atualizar variavel de retorno
            self.resultado = self.lista_resultado
            print('self.resultado')
            print(self.resultado)

            self.status = True
            print(self.sucesso)
            
            # Alimentar o log
            if self.status:
                self.my_logger.log_info('Elementos que estavam presentes na lista:')
                self.my_logger.log_info(self.resultado)

        except Exception as aviso:
            self.status = False
            print(self.erro)
            print(aviso)

            # Alimentar o log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error(str(aviso))

        return{'status': self.status, 'resultado': self.resultado}
    
    # Função para buscar uma extensão na lista filtro
    def elemento_nao_lista(self, lista_filtro, elemento):

        """
        Módulo para fazer um FILTRO de elemento(s) em uma lista.
        Sempre irá retornar uma lista de resultados -> resultado = [lista]

        Args:
            elemento (str/list): Valor(es) desejado(s).
                obs: Se for uma extensão, passar como elemento='.{extensao}'
            lista_filtro (list): Lista com todos os valores antigos para realizar o filtro.
        """

        # Variaveis
        elemento_list = isinstance(elemento, list)

        # TryCatch
        try:

            # Verifica se corresponde a uma lista de extensões
            if elemento_list:

                # Atualiza o valor da lista desejada
                elementos = elemento

            else:

                # Cria uma lista unica
                elementos = [elemento]

            # Criar uma nova lista zerada
            self.lista_resultado = []

            for valor in elementos:

                # Fazer o filtro 
                for arquivo in lista_filtro:

                    # Preciso especificar que se trata de um 'str' para utilizar: 'startwith', 'endswith', etc
                    arquivo = str(arquivo)
                    valor = str(valor)

                    # Verifica se o valor é uma extensão
                    if valor.startswith('.'):

                        # Verificar se o arquivo termina com a extensao informada
                        if not arquivo.endswith(valor):

                            # Atualizar lista de resultados
                            self.lista_resultado.append(arquivo)
                            print('self.lista_resultado')
                            print(self.lista_resultado)

                    else:

                        # Verifica se o arquivo é igual ao valor da lista
                        if not arquivo == valor:

                            # Atualizar lista de resultados
                            self.lista_resultado.append(arquivo)
                            print('self.lista_resultado')
                            print(self.lista_resultado)

            # Atualizar variavel de retorno
            self.resultado = self.lista_resultado
            print('self.resultado')
            print(self.resultado)

            self.status = True
            print(self.sucesso)
            
            # Alimentar o log
            if self.status:
                self.my_logger.log_info('Elementos que estavam presentes na lista:')
                self.my_logger.log_info(self.resultado)

        except Exception as aviso:
            self.status = False
            print(self.erro)
            print(aviso)

            # Alimentar o log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error(str(aviso))

        return{'status': self.status, 'resultado': self.resultado}