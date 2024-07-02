from modules.mylogger.mylogger import MyLogger
import requests
from bs4 import BeautifulSoup

class MyRequest:
        
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
        self.request = None
        self.resultado = None
        self.lista_resultado = None

    # Função para buscar os valores da URL
    def requests_get(self, url, tag):

        """
        Módulo para fazer um REQUEST de uma pagina da web.
        Sempre irá retornar uma lista de resultados por coluna -> resultado = [[lista1], [lista2]]

        Args:
            url (str/list): Nome(s) da(s) url(s) para realizar o request.
            filtro (str): Elemento para filtrar no resultado do(s) reuqet(s).
        """

        # Variaveis
        url_list = isinstance(url, list)
        tag_list = isinstance(tag, list)

        # TryCtach
        try:

            # Verificar se existe uma lista de urls
            if url_list:
                urls = url

            else:
                urls = [url]

            if tag_list:
                tags = tag

            else:
                tags = [tag]

            # Gerar lista em branco para resultados
            self.resultado = []

            for elemento in urls:

                # Fazer o request
                self.request = requests.get(elemento)
                print('request - request')
                print(self.request)

                if self.request.status_code == 200:

                    # Obter o conteudo do request
                    resultado = self.request.text
                    print('resultado - request')                
                    print(resultado)

                    # Usar BeautifulSoup para fazer o parsing do HTML
                    # 'html.parser', especifica o parser a ser usado pelo BeautifulSoup para analisar o HTML (padrão do Python para HTML)
                    soup = BeautifulSoup(resultado, 'html.parser')

                    # Localizar a TAG
                    tag_search = soup.find_all(tags[0])
                    print('tag_localizar')
                    print(tag_search)

                    for tag_search_count in tag_search:

                        self.lista_resultado = tag_search_count.text
                        self.resultado.append(self.lista_resultado)

                    self.status = True
                    print(self.sucesso)

                else:
                    self.status = False
                    print(self.falha)

            # Alimentar o log
            if self.status:
                self.my_logger.log_info(self.sucesso)
                self.my_logger.log_info('Sucesso ao fazer o REQUEST GET')

            else:
                self.my_logger.log_warn(self.falha)
                self.my_logger.log_warn('Falha ao fazer o REQUEST GET')

        except Exception as aviso:
            self.status = False
            print(self.erro)
            print(aviso)

            # Alimentar o log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error('Erro ao fazer o REQUEST GET')
            self.my_logger.log_error(str(aviso))
            
        return{'status': self.status, 'resultado': self.resultado}
    
    def request_doPostBack(self, url, controlId):
        """
        Simula o clique em um link com doPostBack e captura a URL gerada.
        
        Args:
            url (str): URL da página onde está o link.
            controlId (str): ID do controle que aciona o doPostBack.
        
        Returns:
            str: URL gerada após o doPostBack.
        """
        try:
            # Criar a URL completa com o controle alvo
            target_url = f"{url}javascript:__doPostBack('{controlId}','')"
            
            # Fazer uma requisição GET para a URL simulando o doPostBack
            response = requests.get(target_url)
            response.raise_for_status()  # Lançar exceção se a resposta não for bem-sucedida (status != 200)
            
            # Extrair a URL gerada do conteúdo da resposta
            soup = BeautifulSoup(response.content, 'html.parser')
            link_element = soup.find('a', {'id': controlId})
            
            if link_element:
                generated_url = link_element['href']
                self.resultado = generated_url
                
                self.status = True
                print(self.sucesso)
                
            else:
                self.status = False
                print(self.falha)

            # Alimentar o log
            if self.status:
                self.my_logger.log_info(self.sucesso)
                self.my_logger.log_info('Sucesso ao fazer o REQUEST doPostBack')

            else:
                self.my_logger.log_warn(self.falha)
                self.my_logger.log_warn('Falha ao fazer o REQUEST doPostBack')
        
        except requests.RequestException as aviso:
            self.status = False
            print(self.erro)
            print(aviso)

            self.my_logger.log_error(self.erro)
            self.my_logger.log_error(f"Erro ao simular doPostBack: {str(aviso)}")
        
        return{'status': self.status, 'resultado': self.resultado}
