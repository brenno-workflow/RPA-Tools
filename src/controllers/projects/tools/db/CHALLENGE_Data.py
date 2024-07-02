from modules.mylogger.mylogger import MyLogger
from modules.mypandas.mypandas import MyPandas

class CHALLENGEData():
        
    def __init__(self,
                 column_a, column_b, column_c, column_d, column_e, column_f, column_g,
                 path_challenge
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

        # Metodo de 'INJEÇÃO DE DEPENDENCIA'
        # ref.: https://www.youtube.com/watch?v=5DBfVnQn1Ow
        self.my_pandas = MyPandas()

        # Columns
        self.column_a = column_a
        self.column_b = column_b
        self.column_c = column_c
        self.column_d = column_d
        self.column_e = column_e
        self.column_f = column_f
        self.column_g = column_g
        # Path
        self.path_challenge = path_challenge
    
    # Função para buscar os dados presentes no excel
    def data(self):

        # TryCtach
        try:

            # Lista de colunas site e credenciais
            status_challenge_data = self.my_pandas.table(self.path_challenge, 'excel', 'read')

            if status_challenge_data['status']:

                # Retorna a lista de resultados
                resultado = status_challenge_data['resultado']
                mensagem = f"resultado: {resultado}"
                print('resultado')
                print(resultado)                

                self.status = True
                print(self.sucesso)

            else:
                self.status = False
                mensagem = f"Falha ao fazer ao buscar os dados na tabela: '{self.path_challenge}'"
                    
            # Alimentar o log
            if self.status:
                self.my_logger.log_info(self.sucesso)
                self.my_logger.log_info(mensagem)

            else:
                self.my_logger.log_warn(self.falha)
                self.my_logger.log_warn(mensagem)

        except Exception as aviso:
            self.status = False
            print(self.erro)
            print(aviso)

            # Alimentar o log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error(str(aviso))

        return{'status': self.status, 'resultado': resultado}