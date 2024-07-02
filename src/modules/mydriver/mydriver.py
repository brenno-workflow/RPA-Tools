from modules.mylogger.mylogger import MyLogger
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver

class MyDriver:

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
        self.driver = None
        self.my_driver = None

    # ------------------------------------ DRIVER ------------------------------------

    # Configurar driver
    def driver_chrome(self):

        """
        Função para configurar a sessão do navegador.
        """

        # TryCatch
        try:
            
            # Verificar se drive já foi inicializado
            if self.driver:
                self.status = True
                print(self.sucesso)

            else:

                # Configurar opções de inicialização do driver do navegador
                driver_options = webdriver.ChromeOptions()

                # Iniciar navegador em tela cheia
                driver_options.add_argument('--start-maximized')

                # Configurar caminho do driver
                self.driver = webdriver.Chrome(options=driver_options)

                # Configurar espera padrão (implicitly)
                self.driver.implicitly_wait(15)

                self.my_driver: WebDriver = self.driver

                self.status = True
                print(self.sucesso)

        except Exception as aviso:
            self.status = False
            print(self.erro)
            print(aviso)

            # Alimentar log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error(str(aviso))

            return self.driver

        return{'status': self.status, 'resultado': self.driver, 'my_driver': self.my_driver}