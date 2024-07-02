import os

class MyFile():
    def __init__(self):
        self.status = False
        self.falha = "Falha"
        self.sucesso = "Sucesso"
        self.erro = "Erro"

    def verify_file(self, path, filename):
        
        """
        Verifica a existencia de arquivos
        Args:
            path (str/list): Caminho da pasta de destino. Pode ser uma str[caminho_destino] ou uma list[caminho, destino]
            filename (str/list): Nome do arquivo que será verificado. Pode ser uma str[nome_extensão] ou uma list[nome, extensão]
        """

        #Verificar lista
        path_list = isinstance(path, list)
        filename_list = isinstance(filename, list)

        try:
            if path_list:
                path_okay = os.path.join(path[0], path[1])

            else: 
                path_okay = path

            if filename_list:
                filename_okay = filename[0] + filename[1]   
                
            else: 
                filename_okay = filename
    
            caminho = os.path.join(path_okay, filename_okay)
            if os.path.exists(caminho):
                self.status = True
                print("O arquivo existe")
            else:
                self.status = False
                print("O arquivo não existe")
        except Exception as aviso:
            self.status = False
            print(self.falha)
            print(aviso)
        return {'status' : self.status}
    
    def write_file(self, type, path, element,  filename,  action = None):
        """
        cria e define o que será escrito(Dados textuais ou não textuais)
        Args:
            type(str): parametro type recebe o tipo da escrita [w, wb] podendo ser textual ou não
            path(str): parametro path recebe o caminho onde o arquivo será salvo
            element(str): parametro element recebe o elemento(podendo ser uma imagem, texto, audio e etc...) que será escrito
            filename(str): parametro filename é o nome do arquivo que será criado
            action(str): define a ação (se necessário) que o element vai receber 
        """
        try:
            if type.lower() == "w":
                type = 'w'

            elif type.lower() == "wb":
                type = 'wb'
            else:
                type = None
 
            if type ==  None:
                print(self.falha)
                self.status = False
            else:
                if action == None:
                    self.status = True
                    action_result = element
                    
                elif action.lower() == "screenshot_as_png": 
                    action_result = element.screenshot_as_png
                else:
                    self.status = False
                    print(self.falha)

            caminho = os.path.join(path, filename)
            with open(caminho, type) as arquivo:
                    arquivo.write(action_result)

            if os.path.exists(caminho):
                self.status = True
                print("O arquivo foi criado")
            else:
                self.status = False
                print("O arquivo não foi criado")

        except Exception as aviso:
            self.status = False
            print(self.falha)
            print(aviso)

        return {'status' : False}

    def delete_file(self, path, filename):
        path_list = isinstance(path, list)
        filename_list = isinstance(filename, list)
        
        try:
            if path_list:
                path_okay = os.path.join(path[0], path[1])

            else: 
                path_okay = path

            if filename_list:
                filename_okay = filename[0] + filename[1]   

            else: 
                filename_okay = filename   
            caminho = os.path.join(path_okay, filename_okay)
            if os.path.exists(caminho):
                os.remove(caminho)
                self.status = True
                print("O arquivo foi deletado")
            else:
                self.status = True
                print("O arquivo não existe")
        except Exception as aviso:
            self.status = False
            print(self.falha)
            print(aviso)
        return {'status' : self.status}