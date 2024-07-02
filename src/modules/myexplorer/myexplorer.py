from modules.mylogger.mylogger import MyLogger
import os
import zipfile
import shutil
from datetime import datetime

class MyExplorer:
        
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
    def explorer(self, element, type, action, subaction = None, condition = None, subcondition = None):

        """
        Função para manipular pastas dentro do código.

        Args:
            element (str): O caminho do arquivo a ser criado.
            type (str): O tipo do arquivo ['FILE', 'FOLDER', 'ELEMENT'].
            action (str): A ação que será realizada ['MAKE', 'REMOVE', 'LIST', 'MOVE', 'COPY'].
            subaction (str / opcional): A subação que irá realizar ['FILE', 'FOLDER'].
                obs.: Por padrão, será 'None'.
            condition (str, list, int / opcional): A condição para realizar a subação.
                obs.: Por padrão, será 'None'.
        """

        # Variaveis
        self.action = str(action)
        self.subaction = str(subaction)
        self.element = self.element
        self.type = str(type)
        # TryCtach
        try:
            # ---------------------- TYPE ----------------------
            if self.type.lower() == 'file':
                self.type = 'file'
                
            elif self.type.lower() == 'folder':
                self.type = 'folder'

            elif self.type.lower() == 'element':
                self.type = 'element'

            else:
                self.type = None
                
                
            # ---------------------- ACTION ----------------------

            if self.type is not None:
                
                if self.action is not None:
                    self.status = True

                    # ---------------------- MAKE ----------------------

                    if self.action.lower() == 'make':
                        # Verificar Type
                        if self.type == 'file':
                            file = os.path.join(self.element, condition) 
                            # Criação do arquivo de controle
                            with open (file, 'w') as self.file:
                                self.file.write('')
                                
                        elif self.type == 'folder':
                            # Criação da pasta de controle
                            if not os.path.exists(condition):
                                os.makedirs(condition)

                        else:
                            
                            self.file = element
                    
                    # ---------------------- MOVE ----------------------

                    elif self.action.lower() == 'move':
                        
                        # Paths
                        path_org = condition
                        path_dst = subcondition
                            
                        # Mover
                        self.resultado = shutil.move(path_org, path_dst)
                        self.status = True
                        mensagem = f'Sucesso ao mover ao mover da: "{path_org}", para a: "{path_dst}".'
                        print(mensagem)

                    # ---------------------- COPY ----------------------

                    elif self.action.lower() == 'copy':
                        
                        # Paths
                        path_org = condition
                        path_dst = subcondition

                        # Mover
                        self.resultado = shutil.copy(path_org, path_dst)
                        self.status = True
                        mensagem = f'Sucesso ao copiar para a pasta: {path_dst}.'
                        print(mensagem)
                        

                    # ---------------------- REMOVE ----------------------
                            
                    elif self.action.lower() == 'remove':
                        if subcondition is not None:
                            file = os.path.join(self.element, subcondition)
                        
                        else:
                            file = self.element
                            
                        # Listar
                        if os.path.exists(file):
                            os.remove(file)
                            

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
                        for file in self.resultado:

                            if self.type == 'file':
                                # Criar caminho para deletar
                                file_path = os.path.join(condition, file)

                                if os.path.isfile(file_path):
                                    resultado_temp.append(file)
                                    self.status = True

                            elif self.type == 'folder':
                               # Criar caminho para deletar
                                file_path = os.path.join(condition, file)

                                if os.path.isdir(file_path):
                                    resultado_temp.append(file)
                                    self.status = True
                            else:
                                self.resultado = self.resultado
                                self.status = False
                        
                    else:
                        self.status = False
                        mensagem = '"Subaction" não cadastrado.'
                        print(mensagem)

                else:
                    self.status = False
                    mensagem = '"Action" especificado não cadastrada.'
                    print(mensagem)

            else:
                self.status = False
                mensagem = "Type não definido no código"
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
    
