from modules.mylogger.mylogger import MyLogger
import os
import zipfile
import shutil
from datetime import datetime

class MyFolder:
        
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
        self.data_atual = datetime.now().strftime('%Y-%m-%d')

    # ------------------------------------ FOLDER ------------------------------------

    # Manipular pasta
    def folder(self, action, subaction = None, condition = None, subcondition = None):

        """
        Função para manipular pastas dentro do código.

        Args:
            action (str): A ação que será realizada ['MAKE', 'REMOVE', 'LIST', 'MOVE', 'COPY', 'UNZIP'].
            subaction (str / opcional): A subação que irá realizar ['FILE', 'FOLDER'].
                obs.: Por padrão, será 'None'.
            condition (str, list, int / opcional): A condição para realizar a subação.
                obs.: Por padrão, será 'None'.
        """

        # Variaveis
        self.action = str(action)
        self.subaction = str(subaction)

        # TryCtach
        try:

            # ---------------------- ACTIONS ----------------------

           # STATUS
            if self.action is not None:
                self.status = True
                mensagem = '"Action" não é None.'

                # MAKE
                if self.action.lower() =='MAKE':
                    if not os.path.exists(condition):
                        os.makedirs(condition)

                        self.status = True
                        self.resultado = condition
                        mensagem = f'Sucesso ao criar a pasta: {condition}'
                    
                    else:
                        self.status = False
                        mensagem = f'Falha ao criar a pasta: {condition}'
                  
                # MOVE
                elif self.action.lower() == 'MOVE':
                    self.resultado_elemento = self.resultado.move()
                # CREATE TABLE
                elif self.action.lower() == 'REMOVE':
                    self.resultado_elemento = self.resultado

                elif self.action.lower() == 'LIST':
                    self.resultado_elemento = self.resultado.query(condition)

                elif self.action.lower() == 'COPY':
                    self.resultado_elemento = self.resultado.query(condition)

                elif self.action.lower() == 'UNZIP':
                    self.resultado_elemento = self.resultado.query(condition)

                else:
                    self.status = False
                    mensagem = '"Action" não cadastrada.'
                    print(mensagem)

            # ---------------------- MOVE ----------------------
                    
            elif self.action.lower() == 'move':

                # Verificar se possui ambos os caminhos
                if isinstance(condition, list):

                    # Paths
                    path_org = condition[0]
                    path_dst = condition[1]

                    # ---------------------- SUBACTION ----------------------
                            
                    # ---------------------- NONE ----------------------
                    
                    if subaction == None:
                        self.status = True
                        mensagem = f'Sucesso ao mover o arquivo/pasta.'
                        print(mensagem)
                        self.my_logger.log_info(mensagem)

                    # ---------------------- FILE ----------------------
                        
                    elif self.subaction.lower() == 'file':

                        # Mover
                        self.resultado = shutil.move(path_org, path_dst)
                        self.status = True
                        mensagem = f'Sucesso ao mover o arquivo para a pasta: {path_dst}.'
                        print(mensagem)
                        
                    # ---------------------- FOLDER ----------------------
                        
                    elif self.subaction.lower() == 'folder':
                        
                        # Mover
                        self.resultado = shutil.move(path_org, path_dst)
                        self.status = True
                        mensagem = f'Sucesso ao mover o arquivo para a pasta: {path_dst}.'
                        print(mensagem)

                    # ---------------------- ELSE ----------------------
                        
                    else:
                        self.status = False
                        mensagem = '"Subaction" não cadastrado.'
                        print(mensagem)

                else:
                    self.status = False
                    mensagem = '"Condition" não é uma lista com path de ORIGEM e DESTINO assim: condition=[org, dest].'
                    print(mensagem)

            # ---------------------- COPY ----------------------
                    
            elif self.action.lower() == 'copy':

                # Verificar se possui ambos os caminhos
                if isinstance(condition, list):

                    # Paths
                    path_org = condition[0]
                    path_dst = condition[1]

                    # ---------------------- SUBACTION ----------------------
                            
                    # ---------------------- NONE ----------------------
                    
                    if subaction == None:
                        self.status = True
                        mensagem = f'Sucesso ao mover o arquivo/pasta.'
                        print(mensagem)
                        self.my_logger.log_info(mensagem)

                    # ---------------------- FILE ----------------------
                        
                    elif self.subaction.lower() == 'file':

                        # Mover
                        self.resultado = shutil.copy(path_org, path_dst)
                        self.status = True
                        mensagem = f'Sucesso ao mover o arquivo para a pasta: {path_dst}.'
                        print(mensagem)
                        
                    # ---------------------- FOLDER ----------------------
                        
                    elif self.subaction.lower() == 'folder':
                        
                        # Mover
                        self.resultado = shutil.copy(path_org, path_dst)
                        self.status = True
                        mensagem = f'Sucesso ao mover o arquivo para a pasta: {path_dst}.'
                        print(mensagem)

                    # ---------------------- ELSE ----------------------
                        
                    else:
                        self.status = False
                        mensagem = '"Subaction" não cadastrado.'
                        print(mensagem)

                else:
                    self.status = False
                    mensagem = '"Condition" não é uma lista com path de ORIGEM e DESTINO assim: condition=[org, dest].'
                    print(mensagem)

            # ---------------------- REMOVE ----------------------
                    
            elif self.action.lower() == 'remove':

                # Listar
                self.resultado = os.listdir(condition)

                # Loop generico para todos os arquivos dentro da lista
                for file in self.resultado:

                    # Criar caminho para deletar
                    file_path = os.path.join(condition, file)

                    # ---------------------- SUBACTION ----------------------
                            
                    # ---------------------- NONE ----------------------
                    
                    if subaction == None:

                        if os.path.exists(file_path):
                            os.remove(file_path)

                            mensagem = f'Deletado o arquivo/pasta: {file} da pasta: {condition}.'
                            print(mensagem)
                            self.my_logger.log_info(mensagem)

                        self.status = True
                        print(self.sucesso)

                    # ---------------------- FILE ----------------------
                        
                    elif self.subaction.lower() == 'file':

                        if os.path.isfile(file_path):
                            os.remove(file_path)

                            mensagem = f'Deletado o arquivo: {file} da pasta: {condition}.'
                            print(mensagem)
                            self.my_logger.log_info(mensagem)

                        self.status = True
                        print(self.sucesso)
                        
                    # ---------------------- FOLDER ----------------------
                        
                    elif self.subaction.lower() == 'folder':

                        if os.path.isdir(file_path):
                            os.remove(file_path)

                            mensagem = f'Deletada a pasta: {file} da pasta: {condition}.'
                            print(mensagem)
                            self.my_logger.log_info(mensagem)

                        self.status = True
                        print(self.sucesso)

                    # ---------------------- ELSE ----------------------
                        
                    else:
                        self.status = False
                        mensagem = '"Subaction" não cadastrado.'
                        print(mensagem)

            # ---------------------- LIST ----------------------
                        
            elif self.action.lower() == 'list':
                self.resultado = os.listdir(condition)

                # Criar lista temporaria
                resultado_temp = []

                # ---------------------- SUBACTION ----------------------
                            
                # ---------------------- NONE ----------------------
                
                if subaction == None:
                    self.status = True
                    print(self.sucesso)

                # ---------------------- FILE ----------------------
                        
                elif self.subaction.lower() == 'file':

                    # Loop generico para todos os arquivos dentro da lista
                    for file in self.resultado:

                        # Criar caminho para deletar
                        file_path = os.path.join(condition, file)

                        if os.path.isfile(file_path):
                            resultado_temp.append(file)

                    # Atualizar variavel
                    self.resultado = resultado_temp
                    mensagem = f'Lista de arquivos: {self.resultado}'
                    self.my_logger.log_info(mensagem)

                    self.status = True
                    print(self.sucesso)
                    
                # ---------------------- FOLDER ----------------------
                    
                elif self.subaction.lower() == 'folder':

                    # Loop generico para todos os arquivos dentro da lista
                    for file in self.resultado:

                        # Criar caminho para deletar
                        file_path = os.path.join(condition, file)

                        if os.path.isdir(file_path):
                            resultado_temp.append(file)

                    # Atualizar variavel
                    self.resultado = resultado_temp
                    mensagem = f'Lista de pastas: {self.resultado}'
                    self.my_logger.log_info(mensagem)

                    self.status = True
                    print(self.sucesso)

            
                # ---------------------- ELSE ----------------------
                    
                else:
                    self.status = False
                    mensagem = '"Subaction" não cadastrado.'
                    print(mensagem)

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
            mensagem = f'Erro ao executar o módulo MyFolder.'
            print(self.erro)
            print(aviso)

            # Alimentar o log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error(mensagem)
            self.my_logger.log_error(str(aviso))

        return{'status': self.status, 'resultado': self.resultado}
    
    # ------------------------------------ ZIP ------------------------------------
    
    # Verificar se existem arquivos no caminho
    def unzip(self, path_arquivo, path_destino):

        """
        Função para descompactar um ou mais arquivos zip.

        Args:
            path_arquivo (str/list): Caminho(s) para o(s) arquivo(s) que deseja descompactar.
            path_destino (str): Local onde serão salvos os arquivos após descompactar.
        """

        # Variaveis
        path_arquivo_list = isinstance(path_arquivo, list)

        # TryCtach
        try:

            # Verificar se foi passado uma lista de arquivo para descompactar
            if path_arquivo_list:

                # Atualizar lista de paths
                paths = path_arquivo

            else:

                # Criar lista unica
                paths = [path_arquivo]

            # Gerar nova lista de resultados
            self.resultado = []
            
            for arquivo in paths:

                # Verifica se o caminho existe
                if os.path.exists(arquivo):
                
                    # Cria um objeto ZipFile
                    arquivo_zip = zipfile.ZipFile(arquivo, 'r')

                    # Descompacta o arquivo zip
                    arquivo_zip.extractall(path_destino)

                    # Listar o nome dos arquivos presentes no zip
                    arquivo_zip_list = arquivo_zip.namelist()

                    # Lista do nome dos arquivos extraidos
                    self.resultado.append(arquivo_zip.namelist())
                    print(self.resultado)

                    self.status = True
                    print(self.sucesso)

                else:
                    self.status = False
                    print(self.falha)
                    break

            # Atualizar log
            if self.status:
                self.my_logger.log_info('Lista de arquivos extraidos: ')
                self.my_logger.log_info(self.resultado)

            else:
                self.my_logger.log_warn('Arquivo insdiponivel para leitura.')

        except Exception as aviso:
            self.status = False
            print(self.erro)
            print(aviso)

            # Alimentar o log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error(str(aviso))

        return{'status': self.status}