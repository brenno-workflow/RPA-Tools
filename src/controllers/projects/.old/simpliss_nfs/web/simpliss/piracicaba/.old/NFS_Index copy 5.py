from modules.mylogger.mylogger import MyLogger
from modules.mysql.mysql import MySQL
from modules.myweb.myweb import MyWeb
from controllers.projects.simpliss_nfs.web.simpliss.nfs import NFS_Table, NFS_Nota, NFS_Download, NFS_XML, NFS_Print

class NFSIndex():
        
    def __init__(self, 
                 webdriver, user, password, host, database, 
                 column_fluxos_id, column_status_id,
                 column_url, column_control_path,
                 table_fluxos, table_status, 
                 table_sites, table_fluxosweb, table_control, table_fluxoscontrol,
                 param_web_table, param_true, param_control_download,
                 input_coluna_numero, button_coluna_proximo,
                 button_imprimir
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
        self.nfs_table = NFS_Table.NFSTable(
            webdriver, user, password, host, database, 
            column_fluxos_id, column_status_id,
            column_url,
            table_fluxos, table_status, 
            table_sites, table_fluxosweb,
            param_web_table, param_true
        )
        self.nfs_nota = NFS_Nota.NFSNota(
            webdriver,
            button_coluna_proximo
        )
        self.nfs_xml = NFS_XML.NFSXml(
            webdriver,
        )
        self.nfs_download = NFS_Download.NFSDownload(
            webdriver, user, password, host, database, 
            column_fluxos_id, column_status_id,
            column_control_path,
            table_fluxos, table_status, 
            table_control, table_fluxoscontrol,
            param_control_download, param_true,
            button_imprimir
        )
        self.nfs_print = NFS_Print.NFSPrint(
            webdriver,
        )

        # Web
        # Table
        self.input_coluna_numero = input_coluna_numero
        self.button_coluna_proximo = button_coluna_proximo
        # NFSe
        self.button_imprimir = button_imprimir
    
    # Função para verificar se existem arquivos com extensão no caminho  
    def nfs_index(self):

        # TryCtach
        try:

            status_nfs_table_index = self.nfs_table.nfs_index_table()

            if status_nfs_table_index['status']:

                while True:

                    status_table_rows = self.my_web.element(self.input_coluna_numero, 'class', 'find_elements')

                    if status_table_rows['status']:

                        resultado = status_table_rows['resultado']
                        rows = resultado
                        self.my_logger.log_info(f'rows: {rows}')

                        for rows_count in rows:
                                
                            status_nfs_table_new = self.nfs_table.nfs_new_table()

                            if status_nfs_table_new['status']:

                                status_nfs_nota = self.nfs_nota.nfs_nota(rows_count)

                                if status_nfs_nota['status']:

                                    status_nfs_xml = self.nfs_xml

                                    if status_nfs_xml['status']:

                                        status_nfs_download = self.nfs_download.nfs_download()
                                        
                                        if status_nfs_download['status']:

                                            status_nfs_print = self.nfs_print

                                            if status_nfs_print['status']:

                                                status_nfs_table_close = self.nfs_table.nfs_close_table()

                                                if status_nfs_table_close['status']:
                                                    self.status = True
                                                    print(self.sucesso)
                                                
                                                else:
                                                    self.status = False                                                    
                                                    mensagem = 'Falha ao fechar a tabela.'
                                                    break

                                            else:
                                                self.status = False
                                                mensagem = 'Falha ao fazer o PRINT.'
                                                break

                                        else:
                                            self.status = False
                                            mensagem = 'Falha ao fazer o XML.'
                                            break

                                    else:
                                        self.status = False
                                        mensagem = 'Falha ao fazer o DOWNLOAD da nfs.'
                                        break

                                else:
                                    self.status = False
                                    mensagem = 'Falha ao fazer abrir a nota no navegador.'
                                    break

                            else:
                                self.status = False
                                mensagem = 'Falha ao fazer o DOWNLOAD da nfs.'
                                break

                        # Mudar de pagina
                        status_table_next = self.my_web.element(self.button_coluna_proximo, 'id', 'find', 'click')

                        if not status_table_next['status']:
                            self.status = True
                            mensagem = f'Falha ao localizar o elemento: "{self.button_coluna_proximo}".'
                            break

                    else:
                        self.status = False
                        mensagem = f'Falha ao localizar o elemento: "{self.input_coluna_numero}".'
                        break

            else:
                self.status = False
                mensagem = f'Falha ao abrir a tabela de notas.'

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