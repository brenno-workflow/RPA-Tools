from modulos.mylogger.mylogger import MyLogger
from modulos.mysql.mysql import MySQL
from modulos.mypath.mypath import MyPath
from procedimentos.ecossistemanf.controle.Controle_RPA import ControleRPA
import os

class ControleFsist:
        
    def __init__(self, 
                 user, host, database, name_sucesso, name_falha, name_erro, name_download, 
                 coluna_module, coluna_name, coluna_path, coluna_folder, coluna_type, coluna_local, 
                 module_controle, module_fsist, 
                 type_controle, type_subcontrole, 
                 tabela_controle):

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
        self.my_path = MyPath()
        self.controle_rpa = ControleRPA(
            user, host, database, module_controle, 
            coluna_local, coluna_folder, coluna_module, coluna_path, 
            tabela_controle
            )

        # Variaveis especificas
        self.user = user
        self.host = host
        self.database = database

        # Valores
        self.name_sucesso = name_sucesso
        self.name_falha = name_falha
        self.name_erro = name_erro
        self.name_download = name_download

        # Colunas
        self.coluna_module = coluna_module
        self.coluna_name = coluna_name
        self.coluna_path = coluna_path
        self.coluna_folder = coluna_folder
        self.coluna_type = coluna_type

        # Modulos
        self.module_controle = module_controle
        self.module_fsist = module_fsist

        # Tipos
        self.type_controle = type_controle
        self.type_subcontrole = type_subcontrole

        # Tabela controle 
        self.tabela_controle = tabela_controle

    # MySQL Controle
    def criar_controle_fsist(self):

        # Listas
        coluna_filtro_fsist = [self.coluna_module, self.coluna_type]
        filtro_fsist_controle = [self.module_fsist, self.type_controle]

        # TryCtach
        try:

            # Criar pasta Controle
            status_controle_rpa = self.controle_rpa.criar_controle_rpa()

            if status_controle_rpa['status']:

                # Buscar path da pasta controle
                status_path_controle = self.my_sql.mysql_select(
                    self.user, 
                    self.host,
                    self.database,
                    self.coluna_path, 
                    self.tabela_controle, 
                    self.coluna_module, 
                    self.module_controle
                    )

                if status_path_controle['status']:

                    # Atualizar caminho path
                    path_controle = status_path_controle['resultado'][0]
                
                    # Bucar o nome da pasta do Fsist
                    status_fsist_controle = self.my_sql.mysql_select(
                        self.user,
                        self.host,
                        self.database,
                        self.coluna_folder, 
                        self.tabela_controle, 
                        coluna_filtro_fsist, 
                        filtro_fsist_controle
                        )

                    if status_fsist_controle['status']:
                        
                        # Pegar nome
                        fsist_folder = status_fsist_controle['resultado'][0]

                        # Criar path
                        path_controle_fsist = os.path.join(path_controle, fsist_folder)

                        # Criar pasta crontrole no path especificado no MySQL
                        status_mypath_path = self.my_path.criar_path(path_controle_fsist)

                        if status_mypath_path['status']:

                            # Atualizar path no banco de dados
                            status_mysql_update = self.my_sql.mysql_update(
                                self.user, 
                                self.host,
                                self.database,
                                self.coluna_path, 
                                self.tabela_controle, 
                                coluna_filtro_fsist, 
                                filtro_fsist_controle, 
                                path_controle_fsist
                                )

                            if status_mysql_update['status']:

                                # Criar subpastas
                                status_criar_subpastas_controle_fsist = self.criar_subpastas_controle_fsist()
                                
                                if status_criar_subpastas_controle_fsist['status']:
                                    self.status = True
                                    print(self.sucesso)

                                else:
                                    self.status = False
                                    print(self.falha)
                            
                            else:
                                self.status = False
                                print(self.falha)

                        else:
                            self.status = False
                            print(self.falha)

                    else:
                        self.status = False
                        print(self.falha)

                else:
                    self.status = False
                    print(self.falha)

            else:
                self.status = False
                print(self.falha)

            # Alimentar o log
            if self.status:
                self.my_logger.log_info(self.sucesso)
                self.my_logger.log_info('Criar pasta de Controle Fsist')

            else:
                self.my_logger.log_warn(self.falha)
                self.my_logger.log_warn('Criar pasta de Controle Fsist')

        except Exception as aviso:
            self.status = False
            print(self.erro)
            print(aviso)

            # Alimentar o log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error('Criar pasta de Controle Fsist')
            self.my_logger.log_error(str(aviso))

        return{'status': self.status}
    
    # MySQL Controle Subpastas
    def criar_subpastas_controle_fsist(self):

        # Variaveis
        subprocesso_name = [self.name_sucesso, self.name_falha, self.name_erro, self.name_download]

        # Colunas
        coluna_filtro_fsist_path = [self.coluna_module, self.coluna_type]
        coluna_filtro_fsist_subpath = [self.coluna_module, self.coluna_type, self.coluna_name]

        # Filtros
        filtro_fsist_controle_path = [self.module_fsist, self.type_controle]
        filtro_fsist_subcontrole_folder = [self.module_fsist, self.type_subcontrole]
        
        
        
        # TryCtach
        try:

            status_processo_folder = self.my_sql.mysql_select(
                self.user,
                self.host,
                self.database,
                self.coluna_path,
                self.tabela_controle,
                coluna_filtro_fsist_path,
                filtro_fsist_controle_path                
            )

            if status_processo_folder['status']:

                path_fsist_folder = status_processo_folder['resultado'][0]
            
                status_subprocessos_folder = self.my_sql.mysql_select(
                    self.user, 
                    self.host,
                    self.database,
                    self.coluna_folder, 
                    self.tabela_controle, 
                    coluna_filtro_fsist_path, 
                    filtro_fsist_subcontrole_folder
                    )

                if status_subprocessos_folder['status']:

                    # Pegar a lista de resultados
                    lista_subpastas = status_subprocessos_folder['resultado']
                    print('lista_subpastas')
                    print(lista_subpastas)

                    for count in range(len(lista_subpastas)):

                        # Criar path da subpasta
                        path_subpasta = os.path.join(path_fsist_folder, lista_subpastas[count])
                        print(path_subpasta)

                        # Criar filtro para update
                        filtro_fsist_subcontrole_subpath = [self.module_fsist, self.type_subcontrole, subprocesso_name[count]]

                        # Chamar a função para criar pasta
                        status_criar_subpastas = self.my_path.criar_path(path_subpasta)
                        print(path_subpasta)

                        if status_criar_subpastas['status']:

                            status_subpasta_path_update = self.my_sql.mysql_update(
                                self.user, 
                                self.host,
                                self.database,
                                self.coluna_path, 
                                self.tabela_controle, 
                                coluna_filtro_fsist_subpath,
                                filtro_fsist_subcontrole_subpath,
                                path_subpasta
                                )
                            
                            if status_subpasta_path_update['status']:
                                self.status = True
                                print(self.sucesso)

                            else:
                                self.status = False
                                print(self.falha)

                        else:
                            self.status = False
                            print(self.falha)

                else:
                    self.status = False
                    print(self.falha)

            else:
                self.status = False
                print(self.falha)

            # Alimentar o log
            if self.status:
                self.my_logger.log_info(self.sucesso)
                self.my_logger.log_info('Criar subpastas de Controle Fsist')

            else:
                self.my_logger.log_warn(self.falha)
                self.my_logger.log_warn('Criar subpastas de Controle Fsist')

        except Exception as aviso:
            self.status = False
            print(self.erro)
            print(aviso)

            # Alimentar o log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error('Criar subpastas de Controle Fsist')
            self.my_logger.log_error(str(aviso))

        return{'status': self.status}
    

    