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
            action (str): A ação que será realizada ['MAKE', 'REMOVE', 'LIST', 'MOVE', 'COPY'].
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

            # ---------------------- ACTION ----------------------

            # ---------------------- MAKE ----------------------

            if self.action.lower() == 'make':

                # Criação da pasta de controle
                if not os.path.exists(condition):
                    os.makedirs(condition)

                # Verificação da pasta de controle
                if os.path.exists(condition):

                    self.resultado = condition
                    mensagem = f'Sucesso ao criar a pasta: {condition}'
                    print(mensagem)
                    self.my_logger.log_info(mensagem)

                    # ---------------------- SUBACTION ----------------------
                            
                    # ---------------------- NONE ----------------------
                    
                    if subaction == None:
                        self.status = True
                        print(self.sucesso)

                    # ---------------------- ELSE ----------------------
                        
                    else:
                        self.status = False
                        mensagem = '"Subaction" não cadastrado.'
                        print(mensagem)

                else:
                    self.status = False
                    mensagem = f'Falha ao criar a pasta: {condition}'
                    print(mensagem)

            # ---------------------- MOVE ----------------------
                    
            elif self.action.lower() == 'move':

                # Verificar se possui ambos os caminhos

                    # Paths
                    path_org = condition
                    path_dst = subcondition

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

                

            # ---------------------- COPY ----------------------
                    
            elif self.action.lower() == 'copy':

                # Verificar se possui ambos os caminhos
                if isinstance(condition, list):

                    # Paths
                    path_org = condition
                    path_dst = subcondition

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

            # ---------------------- UNZIP ----------------------
            elif self.action.lower() == 'unzip':

                if os.path.exists(condition):
                    with zipfile.ZipFile(condition, 'r') as zip_ref:
                        
                        if os.path.exists(subcondition):
                            zip_ref.extractall(subcondition)
                            print('arquivo encontrado')
                            self.my_logger.log_info('arquivo encontrado')
                            self.status = True
                            
                            mensagem = f'Arquivo {zip_ref} extraído com sucesso para a pasta {subcondition}'

                        else:
                            mensagem = f'Não foi possivel realizar a ação, o caminho de destino {subcondition} não foi encontrado/existe'
                            print(mensagem)
                            self.my_logger.log_warn(mensagem)
                            self.status = False

                        zip_ref.close()

                else:
                    mensagem = f'Não foi possivel realizar a ação, o caminho {condition} não foi encontrado/existe'
                    print(mensagem)
                    self.my_logger.log_warn(mensagem)
                    self.status = False

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
    
