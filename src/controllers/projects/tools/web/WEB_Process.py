from modules.mylogger.mylogger import MyLogger
from modules.myweb.myweb import MyWeb
from controllers.projects.tools.db import CHALLENGE_Data

class WEBProcess():
        
    def __init__(self, 
                 webdriver, 
                 url_rpachallenge,
                 input_fname, input_lname, input_company, input_role, input_adress, input_email, input_phone,
                 button_submit,
                 column_a, column_b, column_c, column_d, column_e, column_f, column_g,
                 path_challenge
                 ):

        # Variaveis gerais
        self.status = False
        self.sucesso = f'SUCESSO - {__name__}'
        self.falha = f'FALHA - {__name__}'
        self.erro = f'ERRO - {__name__}'

        # Instancias
        # Instanciar é uma boa prática e necessário
        # Não instaciar resulta na abertura de processo diferentes e erros
        self.my_logger = MyLogger()
        self.my_web = MyWeb(webdriver)

        # Metodo de 'INJEÇÃO DE DEPENDENCIA'
        # ref.: https://www.youtube.com/watch?v=5DBfVnQn1Ow
        self.challenge_data = CHALLENGE_Data.CHALLENGEData(
            column_a, column_b, column_c, column_d, column_e, column_f, column_g,
            path_challenge
        )

        # Excel
        # Url
        self.url = url_rpachallenge
        # Columns
        self.column_a = column_a
        self.column_b = column_b
        self.column_c = column_c
        self.column_d = column_d
        self.column_e = column_e
        self.column_f = column_f
        self.column_g = column_g

        # Web
        # Inputs
        self.input_fname = input_fname
        self.input_lname = input_lname
        self.input_company = input_company
        self.input_role = input_role
        self.input_adress = input_adress
        self.input_email = input_email
        self.input_phone = input_phone
        # Button
        self.button_submit = button_submit

    # Função para preencher a pagina da web
    def web_process(self):

        # TryCtach
        try:

            status_url_challenge = self.my_web.browser('get', None, self.url)

            if status_url_challenge:

                # Buscar os dados
                status_challenge_data = self.challenge_data.data()  

                if status_challenge_data['status']:

                    # Retorna a lista de resultados
                    resultado = status_challenge_data['resultado']

                    # Mapear as colunas para os campos do formulário
                    columns_to_inputs = {
                        self.column_a: self.input_fname,
                        self.column_b: self.input_lname,
                        self.column_c: self.input_company,
                        self.column_d: self.input_role,
                        self.column_e: self.input_adress,
                        self.column_f: self.input_email,
                        self.column_g: self.input_phone
                    }

                    for index, row in resultado.iterrows():
                        
                        # Preenche os inputs
                        for column, input_field in columns_to_inputs.items():
                            status_input = self.my_web.element(input_field, 'xpath', 'find', 'send_keys', row[column])

                            if status_input:
                                mensagem = f'Preenchido os dados do formulário: "{row[column]}"'
                                self.my_logger.log_info(mensagem)
                                
                            else:
                                mensagem = f'Falha ao tentar preencher os dados do formulário: "{row[column]}"'
                                self.my_logger.log_warn(mensagem)
                                break

                        if status_input:

                            status_button_submit = self.my_web.element(self.button_submit, 'xpath', 'find', 'click')

                            if status_button_submit:
                                self.status = True
                                mensagem = 'Sucesso ao preencher os dados do formulário'
                                print(self.sucesso)

                            else:
                                self.status = False
                                mensagem = f'Falha ao tentar clicar no botão: "{self.button_submit}"'
                                print(self.falha)

                else:
                    self.status = False
                    mensagem = 'Falha ao tentar buscar os dados da tabela'
                    print(self.falha)

            else:
                self.status = False
                mensagem = f'Falha ao tentar acessar o site: "{self.url}"'
                print(self.falha)

            # Alimentar o log
            if self.status:
                self.my_logger.log_info(self.sucesso)
                self.my_logger.log_info(mensagem)

            else:
                self.my_logger.log_warn(self.falha)
                self.my_logger.log_warn(mensagem)

        except Exception as aviso:
            self.status = False
            mensagem = 'Erro na execução da função web_process.'
            print(self.erro)
            print(mensagem)
            print(aviso)

            # Alimentar o log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error(mensagem)
            self.my_logger.log_error(str(aviso))

        return{'status': self.status}