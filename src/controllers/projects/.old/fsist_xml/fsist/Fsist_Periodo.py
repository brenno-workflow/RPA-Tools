from modules.mylogger.mylogger import MyLogger
from modules.mysql.mysql import MySQL
from modules.myweb.myweb import MyWeb
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta
import time

class FsistPeriodo:
        
    def __init__(self, driver, 
                 dias_ativas, dias_canceladas, btn_data, btn_data_incial, btn_confirmar, barra_pesquisa
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
        self.my_sql = MySQL()
        
        # Metodo de 'INJEÇÃO DE DEPENDENCIA'
        # ref.: https://www.youtube.com/watch?v=5DBfVnQn1Ow
        self.my_web = MyWeb(driver)


        self.dias_ativas = dias_ativas
        self.data_canceladas = dias_canceladas
        self.btn_data = btn_data
        self.btn_data_inicial = btn_data_incial
        self.btn_confirmar = btn_confirmar
        self.barra_pesquisa = barra_pesquisa
    # Periodo
    def fsist_periodo_ativas(self):

        # Query - Parametros

        try:
            dia_atual = datetime.now()
            print(dia_atual)
            # Data ativas
            data_ativas = (dia_atual - timedelta(int(self.dias_ativas))).strftime('%d/%m/%Y')
            print(data_ativas)
            time.sleep(2)
            # Pesquisar e clicar
            status_elemento = self.my_web.element(self.btn_data, 'id', 'find', 'click')

            if status_elemento['status']:

                time.sleep(2)
                status_elemento = self.my_web.element(self.btn_data_inicial, 'id', 'click', 'send_keys', data_ativas)

                if status_elemento['status']:
                    status_elemento = self.my_web.element(self.btn_data_inicial, 'id', 'find', 'send_keys', Keys.ENTER)

                    if status_elemento['status']:
                        status_elemento = self.my_web.element(self.btn_confirmar, 'xpath', 'find', 'click' )

                        if status_elemento['status']:
                            self.status = True
                        
                        else:
                            self.status = False
                
                    else:
                        self.status = False
                
                else:
                    self.status = False

            else:
                self.status = False

            # Alimentar o log
            if self.status:
                self.my_logger.log_info(self.sucesso)

            else:
                self.my_logger.log_warn(self.falha)
                print(self.falha)

        except Exception as aviso:
            self.status = False
            print(self.erro)
            print(aviso)

            # Alimentar o log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error(str(aviso))

        return{'status': self.status}
    

    # Periodo
    def fsist_periodo_canceladas(self):
        try:
            # Data ativas
            data_canceladas = (datetime.now() - timedelta(int(self.data_canceladas))).strftime('%d/%m/%Y')
            print(self.data_canceladas)
            status_elemento = self.my_web.element(self.barra_pesquisa, 'id', 'find', 'send_keys', '') 
            if status_elemento['status']:
                # Pesquisar e clicar
                status_elemento = self.my_web.element(self.btn_data, 'id', 'find', 'click')

                if status_elemento['status']:

                    status_elemento = self.my_web.element(self.btn_data_inicial, 'id', 'find', 'send_keys', data_canceladas)

                    if status_elemento['status']:
                        status_elemento = self.my_web.element(self.btn_data_inicial, 'id', 'find', 'send_keys', Keys.ENTER)

                        if status_elemento['status']:
                            status_elemento = self.my_web.element(self.btn_confirmar, 'xpath', 'find', 'click' )

                            if status_elemento['status']:
                                self.status = True
                                

                            else:
                                self.status = False

                        else:
                            self.status = False
                         
                    else:
                        self.status = False
                  
                else:
                    self.status = False
                       
            else:
                self.status = False
                

            # Alimentar o log
            if self.status:
                self.my_logger.log_info(self.sucesso)
                print(self.sucesso)
            else:
                self.my_logger.log_warn(self.falha)
                print(self.falha)

        except Exception as aviso:
            self.status = False
            print(self.erro)
            print(aviso)

            # Alimentar o log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error(str(aviso))

        return{'status': self.status}