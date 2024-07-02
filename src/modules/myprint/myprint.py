from modules.mylogger.mylogger import MyLogger
import pyautogui
import os

class MyPrint:
        
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
    def print_screen(self, path, name = None, extension = None):

        """
        Função para tirar um print da tela atual.

        Args:
            path(str): Caminho aonde deseja salvar o print.
                obs: Pode ser o caminho já com o nome que deseja salvar o arquivo e extensão.
            name(str, opcional): Nome que desja salvar o arquivo.
                obs: Por regra, o arquivo será salvo com o nome presente no caminho.
                        Pode incluir a extensão desejada no nome.
            extension (str, opcional): Tipo da extensão em que deseja salvar o print.
                obs: Por regra, o nome do arquivo ou o path completo já possui a extensão desejada.
        """

        # TryCatch
        try:

            if not extension == None:

                # Informar que é uma str para fazer a formula
                valor = str(extension)

                # Verifica se o valor está em formato de extensão
                if valor.startswith('.'):

                    # Atualiza variavel com o mesmo valor
                    extension_new = valor

                else: 

                    # Adiciona o '.' no final da extensão
                    extension_new = f'.{valor}'

                if not name == None:

                    # Juntar nome e extensão
                    name_extension = name + extension_new

                    # Fazer path completo com caminho, nome e extensão
                    path_name_extension = os.path.join(path, name_extension)

                else:

                    # Separar o caminho do nome do arquivo
                    diretorio, nome_arquivo = os.path.split(path)

                    # Separar o nome do arquivo do arquivo da extensão
                    name_path, extension_old = os.path.splitext(nome_arquivo)

                    # Juntar nom e extensão
                    name_extension = name_path + extension_new

                    # Fazer path completo com caminho, nome e extensão
                    path_name_extension = os.path.join(diretorio, name_extension)

            elif not name == None:

                # Atualizar caminho com o nome do arquivo
                path_name_extension = os.path.join(path, name)

            else:
                
                # Atualizar caminho informado como total
                path_name_extension = path
            
            # Capturar a tela
            screenshot = pyautogui.screenshot()

            # Salvar a captura no caminho informado
            screenshot.save(path_name_extension)

            self.status = True
            print(self.sucesso)

        except Exception as aviso:
            self.status = False
            print(self.erro)
            print(aviso)

            # Alimentar log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error(str(aviso))

        return{'status': self.status}