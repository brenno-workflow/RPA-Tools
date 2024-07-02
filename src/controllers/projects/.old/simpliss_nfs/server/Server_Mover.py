from modules.mylogger.mylogger import MyLogger
from modules.myfolder.myfolder import MyFolder
import os

class ServerMover():
        
    def __init__(self,
                 file_name, file_path, file_path_old
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
        self.my_folder = MyFolder()

        # Metodo de 'INJEÇÃO DE DEPENDENCIA'
        # ref.: https://www.youtube.com/watch?v=5DBfVnQn1Ow

        # Variaveis especificas
        self.file_name = file_name
        self.file_path = file_path
        self.file_path_old = file_path_old

    # Função para listar os anexos 
    def server_mover(self):

        # TryCtach
        try:

            # Path atual
            file_path = os.path.join(self.file_path, self.file_name)

            # Path old
            file_path_old = os.path.join(self.file_name, self.file_path_old)

            # Condição
            paths = [file_path, file_path_old]
            
            # Fazer a movimentação
            status_myfolder_move = self.my_folder.folder('move', 'file', paths)

            if status_myfolder_move['status']:
                self.status = True
                mensagem = f'Sucesso ao movimentar o arquivo: {self.file_name} para a pasta: {self.file_path_old}'
                print(mensagem)

            else:
                self.status = False
                mensagem = f'Falha ao movimentar o arquivo: {self.file_name} para a pasta: {self.file_path_old}'
                print(mensagem)

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
            mensagem = f'Erro ao movimentar o arquivo: {self.file_name} para a pasta: {self.file_path_old}'
            print(mensagem)
            print(aviso)

            # Alimentar o log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error(mensagem)
            self.my_logger.log_error(str(aviso))

        return{'status': self.status}