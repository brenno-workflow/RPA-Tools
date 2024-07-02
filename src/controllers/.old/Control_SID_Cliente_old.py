from modules.mylogger.mylogger import MyLogger
from modules.mysql.mysql import MySQL
from modules.myfolder.myfolder import MyFolder
from src.controllers.control.Control import ControlFolder
import os

class SIDPesquisar():
        
    def __init__(self, 
                 user, password, host, database, 
                 folder_sid, folder_cliente, folder_sucesso, folder_falha, folder_erro
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
        self.my_folder = MyFolder()
        self.control_folder = ControlFolder()

        # Variaveis especificas
        self.user = user
        self.password = password
        self.host = host
        self.database = database

        # Pastas
        self.folder_sid = folder_sid
        self.folder_cliente = folder_cliente
        self.folder_sucesso = folder_sucesso
        self.folder_falha = folder_falha
        self.folder_erro = folder_erro
    
    # Função para verificar se existem arquivos com extensão no caminho  
    def control_sid(self):

        # TryCtach
        try:

            status_control_folder = self.control_folder.control_folder()

            if status_control_folder['status']:

                # Obtem o diretorio do projeto
                control_path = status_control_folder['resultado']

                # Cria o caminho para a pasta de controle
                folder_path_sid = os.path.join(control_path, self.folder_sid)

                status_folder_sid = self.my_folder.folder('make', 'folder', folder_path_sid)

                if status_folder_sid['status']:

                    # Cria o caminho para a pasta de controle
                    folder_path_cliente = os.path.join(control_path, self.folder_cliente)

                    status_folder_cliente = self.my_folder.folder('make', 'folder', folder_path_cliente)

                    if status_folder_cliente['status']:

                        # Listar subpastas para controle
                        subfolder_list = [self.folder_sucesso, self.folder_falha, self.folder_erro]

                        for subfolder_list_count in subfolder_list:

                            # Cria o caminho para a pasta de controle
                            subfolder_path = os.path.join(folder_path_cliente, subfolder_list_count)

                            status_subfolder = self.my_folder.folder('make', 'folder', subfolder_path)

                            if status_subfolder['status']:
                                self.status = True
                                mensagem = f'Sucesso ao criar a pasta: {subfolder_list_count} e {subfolder_path}'
                                print(mensagem)

                            else:
                                self.status = False
                                mensagem = f'Falha ao criar a pasta: {subfolder_list_count} e {subfolder_path}'
                                print(mensagem)
                                break

                    else:
                        self.status = False
                        mensagem = f'Falha ao criar a pasta: {self.folder_cliente} no caminho: {folder_path_cliente}'
                        print(mensagem)

            else:
                self.status = False
                mensagem = f'Falha ao criar a pasta: {self.folder_sid} no caminho: {folder_path_sid}'
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
            mensagem = f'Erro ao criar a pasta: {self.folder_sid} e {self.folder_cliente}'
            print(self.erro)
            print(mensagem)
            print(aviso)

            # Alimentar o log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error(mensagem)
            self.my_logger.log_error(str(aviso))

        return{'status': self.status}