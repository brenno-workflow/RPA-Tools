from modules.mylogger.mylogger import MyLogger
from modules.myfolder.myfolder import MyFolder
import os
import re

class ServerCopiar():
        
    def __init__(self,
                 file_name, file_folder, file_path
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
        self.file_folder = file_folder
        self.file_path = file_path

    # Função para listar os anexos 
    def server_copiar(self, path):

        """
        Ira realizar uma copia do arquivo.

        Args:
            path (str): O caminho que ira salvar a copia do arquivo.
        """

        # TryCtach
        try:

            # Pasta + modulo
            file_name = self.file_folder + " - " + self.file_name
            self.my_logger.log_info('file_name')
            self.my_logger.log_info(file_name)

            # Retirar caracters uft-8
            file_name_ok = re.sub(r'[^\x20-\x7E]', '', file_name)
            self.my_logger.log_info('file_name_ok')
            self.my_logger.log_info(file_name_ok)

            # Path atual
            file_path = os.path.join(self.file_path, self.file_name)

            # Path new
            file_path_copy = os.path.join(path, file_name_ok)

            # Condição
            paths = [file_path, file_path_copy]
            
            # Fazer a movimentação
            status_myfolder_move = self.my_folder.folder('copy', 'file', paths)

            if status_myfolder_move['status']:
                self.status = True
                mensagem = f'Sucesso ao copiar o arquivo: {self.file_name} para a pasta: {path}'
                print(mensagem)

            else:
                self.status = False
                mensagem = f'Falha ao copiar o arquivo: {self.file_name} para a pasta: {path}'
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
            mensagem = f'Erro ao movimentar o arquivo: {self.file_name} para a pasta: {path}'
            print(mensagem)
            print(aviso)

            # Alimentar o log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error(mensagem)
            self.my_logger.log_error(str(aviso))

        return{'status': self.status}