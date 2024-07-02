from modules.mylogger.mylogger import MyLogger
import os

class MyControl:
        
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
        self.folder_control = '[rpa] control'
        self.action = None
        self.path = None

    # Verificar se existe a pasta de controle
    def control(self):

        """
        Função para criar a pasta de controle dos processos em RPA.
        """

        # TryCtach
        try:

            # Obtem o diretorio do projeto
            dir_path = os.path.dirname(os.path.realpath(__name__))

            # Cria o caminho para a pasta de controle
            folder_control_path = os.path.join(dir_path, self.folder_control)

            # Criação da pasta de controle
            if not os.path.exists(folder_control_path):
                os.makedirs(folder_control_path)

            # Verificação da pasta de controle
            if os.path.exists(folder_control_path):

                self.resultado = folder_control_path

                self.status = True
                mensagem = f'Sucesso ao criar a pasta: {self.folder_control}'
                print(mensagem)

            else:
                self.status = False
                mensagem = f'Falha ao criar a pasta: {self.folder_control}'
                print(mensagem)

            # Atualizar log
            if self.status:
                self.my_logger.log_info(self.sucesso)
                self.my_logger.log_info(mensagem)

            else:
                self.my_logger.log_warn(self.falha)
                self.my_logger.log_warn(mensagem)

        except Exception as aviso:
            self.status = False
            mensagem = f'Erro ao criar a pasta: {self.folder_control}'
            print(self.erro)
            print(aviso)

            # Alimentar o log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error(mensagem)
            self.my_logger.log_error(str(aviso))

        return{'status': self.status, 'resultado': self.resultado}
    
    # Função para criar pastas dentro do controle
    def folder(self, action, subaction = None, condition = None):

        """
        Função para criar a pasta de controle dos processos em RPA.

        Args:
            action (str): A ação que será realizada ['CREATE', 'DELETE', 'CLEAR'].
            condition (str): O caminho para a pasta.
        """

        # Variaveis
        self.action = str(action)
        self.path = condition

        # TryCtach
        try:

            # ---------------------- FUNCTION ----------------------

            # ---------------------- ACTION ----------------------

            if self.action.lower() == 'create':

                # Criação da pasta de controle
                if not os.path.exists(condition):
                    os.makedirs(condition)

                # Verificação da pasta de controle
                if os.path.exists(condition):

                    self.resultado = condition
                    
                    self.status = True
                    mensagem = f'Sucesso ao criar a pasta: {self.folder_control}'
                    print(mensagem)

                else:
                    self.status = False
                    mensagem = f'Falha ao criar a pasta: {self.folder_control}'
                    print(mensagem)

            elif self.action.lower() == 'delete':

                teste = 1

            elif self.action.lower() == 'clear':

                teste = 1

            else:
                self.status = False
                mensagem = '"Action" especificado não cadastrada.'
                print(mensagem)

            # Atualizar log
            if self.status:
                self.my_logger.log_info(self.sucesso)
                self.my_logger.log_info(mensagem)

            else:
                self.my_logger.log_warn(self.falha)
                self.my_logger.log_warn(mensagem)

        except Exception as aviso:
            self.status = False
            mensagem = f'Erro ao criar a pasta: {self.folder_control}'
            print(self.erro)
            print(aviso)

            # Alimentar o log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error(mensagem)
            self.my_logger.log_error(str(aviso))

        return{'status': self.status, 'resultado': self.resultado}