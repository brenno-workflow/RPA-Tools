from modules.mylogger.mylogger import MyLogger
import pandas

class MyExcel:
        
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

    # Função para buscar os valores de determinada coluna em função da coluna (x)
    def excel_leitura(self, path_arquivo, coluna):

        """
        Módulo para ler uma coluna do excel.
        Sempre irá retornar uma lista de resultados por coluna -> resultado = [[lista1], [lista2]]

        Args:
            path_arquivo (str): Caminho com o nome do arquivo excel.
            coluna (str/list): Nome da coluna a ser lida.
        """

        # Variaveis
        coluna_list = isinstance(coluna, list)

        # TryCtach
        try:

            # Verifica se a variavel é uma lista
            if coluna_list:

                # Atualizar variavel com a lista
                colunas = coluna

            else:

                # Criar uma lista unica
                colunas = [coluna]

            # Carrega arquivo excel em um DataFrame
            excel = pandas.read_excel(path_arquivo)

            # Criar lista de resultados
            self.resultado = []

            for elemento in colunas:

                # Verificar se a coluna existe:
                if elemento in excel.columns:

                    # Retorna uma lista das informações da coluna
                    self.lista_resultado = excel[elemento].tolist()

                    self.resultado.append(self.lista_resultado)
                    print('self.resultado')
                    print(self.resultado)

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