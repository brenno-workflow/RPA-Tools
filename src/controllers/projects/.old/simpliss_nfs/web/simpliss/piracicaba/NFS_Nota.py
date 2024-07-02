from modules.mylogger.mylogger import MyLogger
from modules.mysql.mysql import MySQL
from modules.myweb.myweb import MyWeb
from modules.mypandas.mypandas import MyPandas
from controllers.projects.simpliss_nfs.web.simpliss.piracicaba import NFS_Table
import time

class NFSNota():
        
    def __init__(self, 
                 webdriver, user, password, host, database, 
                 column_fluxos_id, column_status_id,
                 column_url,
                 table_fluxos, table_status, 
                 table_sites, table_fluxosweb, 
                 param_web_table, param_true,
                 input_coluna_numero, button_coluna_proximo,
                 button_imprimir
                 ):

        # Variaveis gerais
        self.status = False
        self.sucesso = f'SUCESSO - {__name__}'
        self.falha = f'FALHA - {__name__}'
        self.erro = f'ERRO - {__name__}'
        self.resultado = None

        # Instancias
        # Instanciar é uma boa prática e necessário
        # Não instaciar resulta na abertura de processo diferentes e erros
        self.my_logger = MyLogger()
        self.my_sql = MySQL()
        self.my_pandas = MyPandas()
        self.nfs_table = NFS_Table.NFSTable(
            webdriver, user, password, host, database, 
            column_fluxos_id, column_status_id,
            column_url,
            table_fluxos, table_status, 
            table_sites, table_fluxosweb,
            param_web_table, param_true
        )

        # Metodo de 'INJEÇÃO DE DEPENDENCIA'
        # ref.: https://www.youtube.com/watch?v=5DBfVnQn1Ow
        self.my_web = MyWeb(webdriver)

        # Web
        # Table
        self.input_table = "//table/tbody/tr"
        self.input_status_href = ".//a[@href=\"javascript:__doPostBack('ctl00$ContentPlaceHolder1$lv_Pesquisa$ctrl0$LinkButton9','')\"]"
        self.input_coluna_numero = input_coluna_numero
        self.button_coluna_proximo = button_coluna_proximo
        # NFSe
        self.button_imprimir = button_imprimir
    
    # Verificar e baixar notas ativas
    def nfs_notas(self, web_table, filters, columns):

        # Variaveis
        self.resultado = []

        # TryCtach
        try:

            # Abrir tabela
            status_index_table = self.nfs_table.nfs_index_table()

            if status_index_table['status']:

                # Entrar no loop para pesquisar todas as paginas
                #while True:

                    status_table_rows = self.my_web.browser('page_source')

                    if status_table_rows['status']:

                        resultado = status_table_rows['resultado']
                        html_content = resultado

                        # Criar tabela virtual
                        status_table_new = self.my_pandas.table(html_content, 'element', 'create_table', 'html_parser', web_table)

                        if status_table_new['status']:

                            resultado = status_table_new['resultado']                            
                            table_new = resultado

                            # Filtrar
                            status_table_filter = self.my_pandas.table(table_new, 'element', 'read', 'query', filters)

                            if status_table_filter['status']:

                                resultado = status_table_filter['resultado']
                                table_filter = resultado
                                
                                # Concatenar
                                status_table_concat = self.my_pandas.table(table_filter, 'element', 'read', 'concat', columns, ' ')

                                if status_table_concat['status']:
                                    
                                    resultado = status_table_concat['resultado']
                                    table_concat = resultado
                                    self.my_logger.log_info(f'table_concat = "{table_concat}"')
                                    self.resultado.extend(table_concat)

                                    self.status = True
                                    print(self.sucesso)

                                else:
                                    self.status = False
                                    mensagem = 'Falha ao tentar concatenar as tabelas.'
                                    self.my_logger.log_info(mensagem)
                                    #break

                            else:
                                self.status = False
                                mensagem = 'Falha ao tentar filtrar a tabela de notas.'
                                self.my_logger.log_info(mensagem)
                                #break
                        
                        else:
                            self.status = False
                            mensagem = 'Falha ao tentar criar uma tabela virtual.'
                            #break
                    
                    else:
                        self.status = False
                        mensagem = 'Falha ao tentar acessar a tabela de notas.'
                        #break

                    # Clicar no elemento para proxima pagina
                    status_nfs_click = self.my_web.element(self.button_coluna_proximo, 'element', 'find', 'click')

                    if status_nfs_click['status']:
                        time.sleep(5)      
                        self.status = True
                        print(self.sucesso)

                    else:
                        self.status = False
                        mensagem = f'Falha ao localizar o elemento: "{self.button_coluna_proximo}".'
                        #break

            else:
                self.status = False
                mensagem = 'Falha ao tentar acessar a tabela de notas.'

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

        return{'status': self.status, 'resultado': self.resultado}