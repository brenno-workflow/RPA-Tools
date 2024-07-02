from modules.mylogger.mylogger import MyLogger
from modules.mysql.mysql import MySQL
from modules.myweb.myweb import MyWeb
import time

class NFSNota():
        
    def __init__(self, 
                 webdriver, 
                 button_coluna_proximo
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
        self.my_web = MyWeb(webdriver)

        # Web
        self.button_coluna_proximo = button_coluna_proximo
    
    # Função para verificar se existem arquivos com extensão no caminho  
    def nfs_nota(self, element):

        # TryCtach
        try:

            # Iniciar loop de pesquisa
            while True:

                # Clicar no elemento
                status_nfs_click = self.my_web.element(element, 'element', 'find', 'click')

                if status_nfs_click['status']:
                    time.sleep(5)      
                    self.status = True
                    print(self.sucesso)
                    break

                else:
                    
                    # Mudar de pagina
                    status_nfs_coluna_proximo = self.my_web.element(self.button_coluna_proximo, 'id', 'find', 'click')

                    if not status_nfs_coluna_proximo['status']:
                        self.status = False
                        mensagem = "Falha ao mudar de pagina"
                        break

            # Alimentar o log
            if self.status:
                self.my_logger.log_info(self.sucesso)

            else:
                self.my_logger.log_warn(self.falha)
                self.my_logger.log_warn(mensagem)

        except Exception as aviso:
            self.status = False
            print(self.erro)
            print(aviso)

            # Alimentar o log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error(str(aviso))

        return{'status': self.status}