from modules.mylogger.mylogger import MyLogger
import os

class MyPath:
        
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

    # Verifica e cria um path
    def criar_path(self, path):

        # Variaveis
        path_list = isinstance(path, list)

        # TryCtach
        try:

            # Criar lsita de path
            if path_list:

                # Atualizar variavel com a lista
                paths = path

            else:

                # Criar lista unica
                paths = [path]

            for count in range(len(paths)):                

                # Verifica se o camiho já existe
                if os.path.exists(paths[count]):
                    self.status = True
                    print(self.sucesso)

                else:

                    # Cria o caminho especificado
                    os.makedirs(paths[count])

                    if os.path.exists(paths[count]):
                        self.status = True
                        print(self.sucesso)
                    
                    else:
                        self.status = False
                        print(self.falha)

        except Exception as aviso:
            self.status = False
            print(self.erro)
            print(aviso)

            # Alimentar o log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error(str(aviso))

        return{'status': self.status}

    # Verifica e cria um path
    def criar_path_folder(self, path, folder):

        # Variaveis
        folder_list = isinstance(folder, list)

        # TryCtach
        try:

            # Criar lista de pastas
            if folder_list:

                # Atualiza valor da lista
                folders = folder

            else:

                # Cria uma lista unica
                folders = [folder]

            # Atualizar lista de resultados
            self.lista_resultado = folders
            print('folders')
            print(folders)
            print(len(folders))

            for count in range(len(folders)):

                # Converter para um diretorio
                path_folder = os.path.join(path, folders[count])

                # Verifica se o camiho já existe
                if os.path.exists(path_folder):
                    self.status = True
                    print(self.sucesso)

                else:

                    # Cria o caminho especificado
                    os.makedirs(path_folder)

                    if os.path.exists(path_folder):
                        self.status = True
                        print(self.sucesso)
                    
                    else:
                        self.status = False
                        print(self.falha)

                # Fazer lista de resultados
                if self.status:
                    self.lista_resultado[count] = path_folder

            # Atualizar resultado
            if self.status:
                self.resultado = self.lista_resultado

            # Alimentar o log
            if self.status:
                self.my_logger.log_info(str(self.resultado))

        except Exception as aviso:
            self.status = False
            print(self.erro)
            print(aviso)

            # Alimentar o log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error(str(aviso))

        return{'status': self.status, 'resultado': self.resultado}