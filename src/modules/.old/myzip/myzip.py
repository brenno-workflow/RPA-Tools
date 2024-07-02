from modules.mylogger.mylogger import MyLogger
import zipfile
import os

class MyZip:
        
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