from modules.mylogger.mylogger import MyLogger
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
import os

class MyWeb:

    def __init__(self, webdriver):

        # Variaveis gerais
        self.status = False
        self.sucesso = f'SUCESSO - {__name__}'
        self.falha = f'FALHA - {__name__}'
        self.erro = f'ERRO - {__name__}'

        # Instancias
        # Instanciar é uma boa prática e necessário
        # Não instaciar resulta na abertura de processo diferentes e erros
        self.my_logger = MyLogger()
        
        # Metodo de 'INJEÇÃO DE DEPENDENCIA'
        # ref.: https://www.youtube.com/watch?v=5DBfVnQn1Ow
        self.webdriver: WebDriver = webdriver

        # Variaveis especificas
        self.resultado = None
        self.resultado_elemento = None
        self.status_elemento = None
        self.type = None
        self.action = None
        self.subaction = None
        self.condition = None
        self.key = None
    
    # ------------------------------------ NAVEGADOR ------------------------------------

    # Fechar navegador
    def browser(self, action, subaction = None, condition = None):

        """
        Ira realizar uma ação em um determinado elemento da pagina da web.

        Args:
            element (str): O elemento em sí.
            action (str): A ação que será realizada ['GET', 'QUIT', 'COMMAND_EXECUTOR', 'PRINT', 'MAXIMIZE'].
            subaction (str / opcional): A subação que irá realizar ['DOWNLOAD', 'SAVE'].
                obs.: Por padrão, será 'None'.
            condition (str, int / opcional): A condição para realizar a subação.
                obs.: Por padrão, será 'None'.
        """

        # Variaveis
        self.type = str(type)
        self.action = str(action)

        # TryCatch
        try:

            # ---------------------- SUBACTION ----------------------
                
            if subaction == None:
                self.subaction = None

            else:
                self.subaction = str(subaction)

            # ---------------------- ACTION ----------------------

            # ---------------------- GET ----------------------

            if self.action.lower() == 'get':
                self.webdriver.get(condition)

                # ---------------------- SUBACTION ---------------------- 

                # ---------------------- NONE ---------------------- 
                    
                if self.subaction == None:
                    self.status = True
                    print(self.sucesso)

                # ---------------------- ELSE ---------------------- 

                else:
                    self.status = False
                    mensagem = '"Subaction" não cadastrado.'
                    print(mensagem)

            # ---------------------- QUIT ----------------------

            elif self.action.lower() == 'quit':
                self.webdriver.quit()

                # ---------------------- SUBACTION ---------------------- 

                # ---------------------- NONE ---------------------- 
                    
                if self.subaction == None:
                    self.status = True
                    print(self.sucesso)

                # ---------------------- ELSE ----------------------

                else:
                    self.status = False
                    mensagem = '"Subaction" não cadastrado.'
                    print(mensagem)

            # ---------------------- command executor ----------------------

            elif self.action.lower() == 'command_executor':
                self.action = action

                # Configurar o command_executor dinamicamente
                self.webdriver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')

                # ---------------------- SUBACTION ---------------------- 

                # ---------------------- NONE ---------------------- 
                    
                if self.subaction == None:
                    self.status = True
                    print(self.sucesso)

                # ---------------------- DOWNLOAD ---------------------- 
                    
                if self.subaction.lower() == 'download':

                    # Criar dicionario de parametros
                    params = {
                        # Comando do protocolo DevTools do Chrome.
                        # cmd: Indica o comando específico que queremos enviar
                        'cmd': 'Browser.setDownloadBehavior',
                        # Dicionário contendo os parâmetros específicos para o comando
                        'params': {
                            # Permitir o comportamento de download
                            'behavior': 'allow',
                            # Definir novo caminho de download
                            'downloadPath': condition
                            }
                    }
                    # Executar atualização
                    self.webdriver.execute("send_command", params)

                    self.status = True
                    print(self.sucesso)

                # ---------------------- ELSE ----------------------

                else:
                    self.status = False
                    mensagem = '"Subaction" não cadastrado.'
                    print(mensagem)

            # ---------------------- PRINT ----------------------

            elif self.action.lower() == 'print':
                self.webdriver.save_screenshot(condition)

                # ---------------------- SUBACTION ---------------------- 

                # ---------------------- NONE ---------------------- 
                    
                if self.subaction == None:
                    self.status = True
                    print(self.sucesso)

                # ---------------------- SAVE ---------------------- 
                    
                if self.subaction.lower() == 'save':
                    self.webdriver.save_screenshot(condition)

                    self.status = True
                    print(self.sucesso)

                # ---------------------- ELSE ----------------------

                else:
                    self.status = False
                    mensagem = '"Subaction" não cadastrado.'
                    print(mensagem)
            
            # ---------------------- MAXIMIZE ----------------------

            elif self.action.lower() == 'maximize':
                self.webdriver.maximize_window()

                # ---------------------- SUBACTION ---------------------- 

                # ---------------------- NONE ---------------------- 
                    
                if self.subaction == None:
                    self.status = True
                    print(self.sucesso)

                # ---------------------- ELSE ----------------------

                else:
                    self.status = False
                    mensagem = '"Subaction" não cadastrado.'
                    print(mensagem)

            # ---------------------- ELSE ----------------------

            else:
                self.status = False
                mensagem = '"Type" especificado não cadastrado.'
                print(mensagem)

            # Atualizar o log
            if self.status:
                self.my_logger.log_info(self.sucesso)

            else:
                self.my_logger.log_warn(self.falha)
                self.my_logger.log_warn(mensagem)

        except Exception as aviso:
            self.status = False
            print(self.erro)
            print(aviso)

            # Alimentar log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error(str(aviso))

        return{'status': self.status, 'resultado': self.resultado}

    # ------------------------------------ ELEMENTOS ------------------------------------

    # Buscar elementos
    def element(self, element, type, action, subaction = None, condition = None):

        """
        Ira realizar uma ação em um determinado elemento da pagina da web.

        Args:
            element (str): O elemento em sí.
            type (str): O tipo de elemento a ser utilizado ['ID', 'CLASS', 'NAME', 'XPATH', 'CSS', 'TAG'].
            action (str): A ação que será realizada ['FIND', 'FIND_ELEMENTS', 'TEXT', 'SEND_KEYS', 'CHECKBOX', 'DROPDOWN', 'CLICK'].
            subaction (str / opcional): A subação que irá realizar ['INDEX', 'CLICK', 'VALUE', 'TEXT', 'LIST', 'SEND_KEYS', 'GET_ATTRIBUTE', 'IS_DISPLAYED', 'GET_VALUE'].
                obs.: Por padrão, será 'None'.
            condition (str, int / opcional): A condição para realizar a subação.
                obs.: Por padrão, será 'None'.
        """

        # Variaveis
        self.type = str(type)
        self.action = str(action)

        # TryCatch
        try:

            # ---------------------- TYPE ----------------------

            if self.type.lower() == 'id':
                self.type = By.ID

            elif self.type.lower() == 'class':
                self.type = By.CLASS_NAME

            elif self.type.lower() == 'name':
                self.type = By.NAME

            elif self.type.lower() == 'xpath':
                self.type = By.XPATH

            elif self.type.lower() == 'css':
                self.type = By.CLASS_NAME

            elif self.type.lower() == 'tag':
                self.type = By.TAG_NAME

            else:
                self.type = None

            # ---------------------- ACTION ----------------------
                
            if action == None:
                self.action = None

            else:
                self.action = str(action)

            # ---------------------- SUBACTION ----------------------
                
            if subaction == None:
                self.subaction = None

            else:
                self.subaction = str(subaction)

            # ---------------------- FUNCTION ----------------------

            # Verificar se possui TYPE
            if self.type is not None:

                # Buscar elemento
                self.resultado = self.webdriver.find_element(self.type, element)

                if self.resultado:

                    # ---------------------- ACTIONS ----------------------

                    # STATUS
                    if self.action is not None:
                        self.status = True
                        mensagem = '"Action" não é None.'
                        print(mensagem)

                        # FIND                         
                        if self.action.lower() == 'find':
                            self.resultado_elemento = self.resultado

                        # FIND ELEMENTS                         
                        elif self.action.lower() == 'find_elements':
                            self.resultado_elemento = self.webdriver.find_elements(self.type, element)

                        # CLICK
                        elif self.action.lower() == 'click':
                            
                            # Esperar até que o elemento seja clicavel
                            # '((tipo, elemento))' é uma tupla que contém outra tupla (tipo, elemento). 
                            # Função 'element_to_be_clickable' espera uma única tupla como argumento -  agrupar tipo e elemento em uma tupla externa.
                            status_click = WebDriverWait(self.webdriver, 10).until(EC.element_to_be_clickable((type, element)))

                            if status_click:
                                self.resultado.click()

                            else: 
                                self.status = False
                                mensagem = f'O elemento: "{self.resultado}" não está possível de ser clicado.'
                                print(mensagem)

                        # TEXT 
                        elif self.action.lower() == 'text':
                            self.resultado_elemento = self.resultado.text

                        # CHECKBOX
                        elif self.action.lower() == 'checkbox':
                            self.resultado_elemento = self.resultado

                        # DROPBOX
                        elif self.action.lower() == 'dropdown':
                            self.resultado_elemento = self.resultado                        
                        
                        # SEND KEYS
                        elif self.action.lower() == 'send_keys':
                            self.resultado.send_keys(condition)

                        else:
                            self.status = False
                            mensagem = '"Action" não cadastrada.'
                            print(mensagem)

                        # ---------------------- SUBACTION ----------------------
                            
                        # NONE
                        if self.subaction == None:
                            self.status = True
                            print(self.sucesso)

                        # CLICK
                        elif self.subaction.lower() == 'click':
                            status_click = WebDriverWait(self.webdriver, 10).until(EC.element_to_be_clickable((type, element)))

                            if status_click:
                                self.resultado.click()

                            else: 
                                self.status = False
                                mensagem = f'O elemento: "{self.resultado}" não está possível de ser clicado.'
                                print(mensagem)

                        # SEND_KEYS
                        elif self.subaction.lower() == 'send_keys':
                            self.resultado.clear()
                            self.resultado.send_keys(condition)

                        # GET_ATTIBUTE
                        elif self.subaction.lower() == 'get_attribute':
                            self.resultado_elemento = self.resultado.get_attribute(condition)

                        # IS_DISPLAYED
                        elif self.subaction.lower() == 'is_displayed':
                            self.resultado_elemento = self.resultado.is_displayed()

                            if self.resultado_elemento is False:
                                self.status = False
                                mensagem = f'O elemento: "{self.resultado_elemento}" não está disponivel.'
                                print(mensagem)

                        # IS_SELECTED
                        elif self.subaction.lower() == 'is_selected':
                            self.resultado_elemento = self.resultado.is_selected()

                            if self.resultado_elemento is False:
                                self.status = False
                                mensagem = f'O elemento: "{self.resultado_elemento}" não está selecionado.'
                                print(mensagem)

                        # TEXT                     
                        elif self.subaction.lower() == 'text':

                            # Inicializar Select
                            select = Select(self.resultado)

                            # Seleciona o texto visivel
                            self.resultado_elemento = select.select_by_visible_text(condition)

                            if self.resultado_elemento is False:
                                self.status = False
                                mensagem = f'O elemento: "{self.resultado_elemento}" não está visivel.'
                                print(mensagem)

                        # LIST
                        elif self.subaction.lower() == 'list':

                            # Inicializar Select
                            select = Select(self.resultado)

                            # Criar lista de resultados
                            dropdown_list = []

                            # Obter todas as opções de dropdown
                            dropdown_options = select.options

                            # Loop
                            for dropdown_options_count in dropdown_options:
                                dropdown_list.append(dropdown_options_count.text)

                            # Atualizar resultado
                            self.resultado_elemento = dropdown_list
                            
                        else:
                            self.status = False
                            mensagem = '"Subaction" não cadastrado.'
                            print(mensagem)

                    else:
                        self.status = False
                        mensagem = '"Action" não pode ser None.'
                        print(mensagem)

                else:
                    self.status = False
                    mensagem = '"Element" especificado não encontrado.'
                    print(mensagem)

            else:
                self.status = False
                mensagem = '"Type" especificado não cadastrado.'
                print(mensagem)

            # Atualizar o log
            if self.status:
                self.my_logger.log_info(self.sucesso)

            else:
                self.my_logger.log_warn(self.falha)
                self.my_logger.log_warn(mensagem)

        except Exception as aviso:
            self.status = False
            print(self.erro)
            print(aviso)

            # Alimentar log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error(str(aviso))

        return{'status': self.status, 'resultado': self.resultado_elemento}
    
    # ------------------------------------ JAVASCRIPT ------------------------------------

    def execute_script(self, script, *args):

        """
        Ira realizar uma ação em um determinado elemento da pagina da web.

        Args:
            script (str): O script em si.
            args (opcional): Argumentos para o JS.
        """

        # TryCatch
        try:

            # Executar script
            self.resultado = self.webdriver.execute_script(script, *args)

            # Verifica se existe elemento
            if self.resultado:   
                self.resultado_elemento = self.resultado             

                self.status = True
                print(self.sucesso)

            else:
                self.status = False
                print(self.falha)
                self.my_logger.log_warn(f'Falha ao executar o script: {script}')

        except Exception as aviso:
            self.status = False
            print(self.erro)
            print(aviso)

            # Alimentar log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error(str(aviso))

        return{'status': self.status, 'resultado': self.resultado_elemento}
    
    # ------------------------------------ PRINT ------------------------------------
    
    # Apertar ENTER
    def print(self, path, name = None, extension = None):

        """
        Função para tirar um print da pagina.

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
            
            # Digitar texto
            self.status_elemento = self.webdriver.print_page(path_name_extension)

            if self.status_elemento['status']:
                self.status = True
                print(self.sucesso)

            else:
                self.status = False
                print(self.falha)

        except Exception as aviso:
            self.status = False
            print(self.erro)
            print(aviso)

            # Alimentar log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error(str(aviso))

        return{'status': self.status, 'resultado': self.resultado}