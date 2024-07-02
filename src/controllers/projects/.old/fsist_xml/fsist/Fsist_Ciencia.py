from modules.mylogger.mylogger import MyLogger
from modules.mysql.mysql import MySQL
from modules.myweb.myweb import MyWeb
import time

class FsistCiencia:
        
    def __init__(self, 
                 driver, btn_select_all, btn_download, element_msg, btn_ciencia, btn_cancel, btn_sim, btn_ok, data_download):

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
        self.my_web = MyWeb(driver)


        self.btn_select_all = btn_select_all
        self.btn_download = btn_download
        self.element_msg = element_msg
        self.btn_ciencia = btn_ciencia
        self.btn_cancel = btn_cancel
        self.btn_sim = btn_sim
        self.btn_ok = btn_ok
        self.data_download = data_download
       

    # Ciencia
    def fsist_ciencia(self):


        try:
            # Pesquisar e clicar
            status_elemento = self.my_web.element(self.btn_select_all, 'id', 'click')

            if status_elemento['status']:
                status_elemento = self.my_web.element(self.btn_download, 'id', 'click')

                if status_elemento['status']:
                    status_elemento = self.my_web.element(self.btn_ciencia, 'xpath', 'find')
                    self.my_logger.log_info(status_elemento['status'])
                    
                    if status_elemento['status']:

                        
                        # Se tiver, vai efetuar a ciencia
                        status_elemento = self.my_web.element(self.btn_ciencia, 'xpath', 'click')

                        if status_elemento['status']:
                            
                            status_elemento = self.my_web.element(self.btn_ok, 'xpath', 'find')

                            if status_elemento['status']:
                                status_elemento = self.my_web.element(self.btn_ok, 'xpath', 'find', 'click')

                                if status_elemento['status']:
                                    
                                    # Selecionar todas para limpar
                                    status_elemento = self.my_web.element(self.btn_select_all, 'id', 'find', 'click')

                                    if status_elemento['status']:

                                        status_elemento = self.my_web.element(self.btn_sim, 'id', 'find', 'click')

                                        if status_elemento['status']:

                                            self.status = True
                                            print(self.sucesso)
                                        
                                        else:
                                            self.status = False
                                            
                                    else:
                                        self.status = False

                                else:
                                    self.status = False
                            else:
                                pass
                        
                        else:
                            self.status = False

                        # Verifica se apareceu a mensagem para baixar
                        status_elemento = self.my_web.element(self.data_download,'xpath', 'find')
                        print(status_elemento['status'])

                        if status_elemento['status']:
                            # Ira efetuar o cancelamento depois
                            status_elemento = self.my_web.element(self.btn_cancel, 'xpath', 'click')

                            if status_elemento['status']:
                            
                                # Selecionar todas para limpar
                                status_elemento = self.my_web.element(self.btn_select_all, 'id', 'find', 'click')

                                if status_elemento['status']:

                                    status_elemento = self.my_web.element(self.btn_sim, 'id', 'find', 'click')

                                    if status_elemento['status']:

                                        self.status = True
                                        print(self.sucesso)
                                    
                                    else:
                                        self.status = False
                                        
                                else:
                                    self.status = False

                            else:
                            
                                self.status = False
                        else:
                            self.status = True

                    else:
                        # Ira efetuar o cancelamento depois
                        status_elemento = self.my_web.element(self.btn_cancel, 'xpath', 'click')

                        if status_elemento['status']:
                        # Selecionar todas para limpar
                            status_elemento = self.my_web.element(self.btn_select_all, 'id', 'find', 'click')

                            if status_elemento['status']:
                                status_elemento = self.my_web.element(self.btn_sim, 'id', 'find', 'click')

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
           

        except Exception as aviso:
            self.status = False
            print(self.erro)
            print(aviso)

            # Alimentar o log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error(str(aviso))

        return{'status': self.status}