from modules.mylogger.mylogger import MyLogger

class MyList:
        
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
    
    # Função para buscar os valores de determinada coluna em função da coluna (x)
    def lista_filtro(self, lista_principal, lista_filtro, filtro):

        # Variaveis
        lista_resultado = []

        # TryCtach
        try:

            # Contar elementos
            lista_principal_count = len(lista_principal)
            print('lista_principal_count')
            print(lista_principal_count)

            lista_filtro_count = len(lista_filtro)
            print('lista_filtro_count')
            print(lista_filtro_count)

            # Verificar se a quantidade bate
            if lista_principal_count == lista_filtro_count:

                # Laço de repetição:
                # Chamar as duas lista ao mesmo tempo no loop
                # 'zip' para iterar simultaneamente sobre as duas listas.
                for elemento_lista_principal, elemento_lista_filtro in zip(lista_principal, lista_filtro):

                    # Se o elemento (x) da 'lista_filtro' for igual ao 'filtro'
                    if elemento_lista_filtro == filtro:

                        # Atualiza a variavel
                        lista_resultado.append(elemento_lista_principal)
                        print('lista filtrada - mylist')
                        print(lista_resultado)

                    else:
                        self.status = False
                        print(self.falha)
                        break

                else:
                    self.status = False
                    print(self.falha)

                if lista_resultado:

                    # Atualizar variavael com a lista filtrada
                    self.resultado = lista_resultado

                    self.status = True
                    print(self.sucesso)

                else:
                    self.status = False
                    print(self.falha)

            # Alimentar o log
            if self.status:
                self.my_logger.log_info(self.resultado)

        except Exception as aviso:
            self.status = False
            print(self.erro)
            print(aviso)

            # Alimentar o log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error(str(aviso))

        return{'status': self.status, 'resultado': self.resultado}