from modules.mylogger.mylogger import MyLogger
from bs4 import BeautifulSoup
import pandas as pd
import os
import charset_normalizer
import chardet

class MyPandas:

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
        
        # Metodo de 'INJEÇÃO DE DEPENDENCIA'
        # ref.: https://www.youtube.com/watch?v=5DBfVnQn1Ow
        # Variaveis especificas
        self.resultado = None
        self.resultado_elemento = None
        self.type = None
        self.action = None
        self.subaction = None
    
    # ------------------------------------ ELEMENTOS ------------------------------------

    # Buscar elementos
    def table(self, element, type, action, subaction = None, condition = None, subcondition = None):

        """
        Ira realizar uma ação em um determinado elemento da pagina da web.

        Args:
            element (str): O elemento em sí.
            type (str): O tipo de elemento a ser utilizado ['EXCEL', 'CSV', 'ELEMENT'].
            action (str): A ação que será realizada ['READ', 'CREATE_TABLE'].
            subaction (str / opcional): A subação que irá realizar ['QUERY', 'INDEX', 'HTML_PARSER', 'ASTYPE'].
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

            if self.type.lower() == 'excel':
                self.resultado = pd.read_excel(element)

            elif self.type.lower() == 'csv':
                self.resultado = pd.read_csv(element)

            elif self.type.lower() == 'element':
                self.resultado = element

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

                # Verifica se fez a leitura
                if self.resultado is not None:
                    
                    # ---------------------- ACTIONS ----------------------

                    # STATUS
                    if self.action is not None:
                        self.status = True
                        mensagem = '"Action" não é None.'

                        # READ
                        if self.action.lower() =='read':
                            self.resultado_elemento = self.resultado

                        # CREATE TABLE
                        elif self.action.lower() == 'create_table':
                            self.resultado_elemento = self.resultado

                        elif self.action.lower() == 'filter':
                            self.resultado_elemento = self.resultado.query(condition)

                        else:
                            self.status = False
                            mensagem = '"Action" não cadastrada.'
                            print(mensagem)

                        # ---------------------- SUBACTION ----------------------
                            
                        # NONE
                        if self.subaction == None:
                            self.status = True
                            print(self.sucesso)
                        
                    

                        # STATUS
                        else:
                            self.status = True
                            mensagem = '"Subaction" não é None.'

                            # INDEX
                            if self.subaction.lower() == 'index':
                                self.resultado_elemento = self.resultado_elemento[subcondition]

                            # ASTYPE
                            elif self.subaction.lower() == 'astype':
                                self.resultado_elemento = self.resultado.astype(condition)

                            # SHAPE
                            elif self.subaction.lower() == 'astype':
                                self.resultado_elemento = self.resultado.shape[0]

                            # CONCAT
                            elif self.subaction.lower() == 'concat':
                                self.resultado_elemento = self.resultado.apply(lambda row: f'{subcondition}'.join(row[condition_count] for condition_count in condition), axis=1).tolist()

                            # HTML PARSER
                            elif self.subaction.lower() == 'html_parser':

                                # Detectar a codificação do HTML
                                html_bytes = self.resultado.encode()
                                detected_encoding = chardet.detect(html_bytes)['encoding']

                                # Criando o objeto BeautifulSoup
                                soup = BeautifulSoup(self.resultado, 'html.parser', from_encoding=detected_encoding)

                                # Encontrando a tabela
                                table = soup.find('table', condition)

                                # Extraindo os dados da tabela
                                headers = [header.text for header in table.find_all('th')]

                                rows = []
                                for row in table.find_all('tr')[1:]:  # Pular o primeiro <tr> que contém os headers
                                    cells = row.find_all('td')
                                    rows.append([cell.text for cell in cells])

                                # Iterar sobre as linhas e remover os caracteres de nova linha
                                for row in rows:
                                    for i, cell in enumerate(row):
                                        row[i] = cell.strip()

                                # Criar DataFrame do pandas
                                self.resultado_elemento = pd.DataFrame(rows, columns=headers)  # Primeira linha como cabeçalho
                            
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