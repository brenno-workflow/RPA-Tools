from modules.mylogger.mylogger import MyLogger
import os
from datetime import datetime

class MyFile():
    def __init__(self):
        self.status = False
        self.falha = "Falha"
        self.sucesso = "Sucesso"
        self.erro = "Erro"

       # Instâncias
        self.my_logger = MyLogger()
    
    def files(self, element, type, action, subaction=None, condition=None, subcondition=None):
        """
        Irá realizar uma ação em um arquivo (txt, json, etc.).

        Args:
            element (str): O caminho do arquivo a ser criado.
            type (str): O tipo do arquivo ['.txt', '.json', '.html', etc.].
            action (str): Ação a ser realizada ['write', 'append', 'delete'].
            subaction (str, opcional): Subação a ser realizada. Por padrão, é None.
            condition (str, opcional): Conteúdo a ser escrito no arquivo. Por padrão, é None.
            subcondition (str, opcional): Subcondição para a subação. Por padrão, é None.

        """
        
        try:
            # ---------------------- TYPE ----------------------
            if type is None:
                self.type = None
            else:
                self.type = str(type)

            # ---------------------- ACTION ----------------------
            if action is None:
                self.action = None
            else:
                self.action = str(action)

            # ---------------------- SUBACTION ----------------------
            if subaction is None:
                self.subaction = None
            else:
                self.subaction = str(subaction)

            if subcondition is None:
                self.element = element
            else:
                self.subcondition = subcondition + self.type
                self.element = os.path.join(element, self.subcondition)

            # Verificação do tipo de arquivo
            if self.type is not None:
                # Ações
                if self.type.lower() == '.txt':
                    if self.action.lower() == 'write':
                        with open(self.element, 'w') as file:
                            file.write(str(condition))
                        self.status = True
                    elif self.action.lower() == 'append':
                        with open(self.element, 'a') as file:
                            file.write(condition)
                        self.status = True
                    elif self.action.lower() == 'delete':
                        os.remove(self.element)
                        self.status = True
                    else:
                        mensagem = "Ação inválida para arquivo txt"
                        
            else:
                self.status = False
                self.resultado = None
                mensagem = '"Type" não definido.'
                self.my_logger.log_error(mensagem)
                print(mensagem)
            
            if self.status:
                mensagem = f"Ação '{self.action}' realizada com sucesso no arquivo '{self.element}'."
                self.my_logger.log_info(mensagem)
                print(mensagem)
            else:
                self.my_logger.log_warn("Ação falhou.")

        except Exception as aviso:
            self.status = False
            self.resultado = None
            mensagem = f"Erro: {aviso}"
            self.my_logger.log_error(mensagem)
            print(mensagem)

        return {'status': self.status}
