from modules.mylogger.mylogger import MyLogger
from modules.mysql.mysql import MySQL
from modules.myfolder.myfolder import MyFolder
from controllers.control import Control, Subcontrol

class ControlFolder():
        
    def __init__(self, 
                 user, password, host, database,
                 column_fluxos_id, column_status_id,
                 column_control_id, column_control_path,
                 table_fluxos, table_status, table_fluxoscontrol, table_control,
                 param_true, param_control, 
                 param_control_sucesso, param_control_falha, param_control_erro, param_control_download,
                 folder_control, folder_sucesso, folder_falha, folder_erro, folder_download,
                 param_control_service = None, param_control_module = None,
                 folder_service = None, folder_module = None
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
        self.my_folder = MyFolder()
        self.control = Control.Control(
            user, password, host, database,
            column_fluxos_id, column_status_id,
            column_control_id, column_control_path,
            table_fluxos, table_status, table_fluxoscontrol, table_control,
            param_control, param_true,
            folder_control
            )
        
        self.subcontrol = Subcontrol.Subcontrol(
            user, password, host, database, 
            column_fluxos_id, column_status_id,
            column_control_id, column_control_path,
            table_fluxos, table_status, table_fluxoscontrol, table_control,
            param_true
        )

        # Parametros
        self.param_control = param_control
        self.param_control_sucesso = param_control_sucesso
        self.param_control_falha = param_control_falha
        self.param_control_erro = param_control_erro
        self.param_control_download = param_control_download
        self.param_control_service = param_control_service
        self.param_control_module = param_control_module

        # Pastas
        self.folder_control = folder_control
        self.folder_sucesso = folder_sucesso
        self.folder_falha = folder_falha
        self.folder_erro = folder_erro
        self.folder_download = folder_download
        self.folder_service = folder_service
        self.folder_module = folder_module
    
    # Função para verificar se existem arquivos com extensão no caminho  
    def control_folder(self):

        # Variaveis
        param_subcontrol = [self.param_control_sucesso, self.param_control_falha, self.param_control_erro, self.param_control_download]
        folder_subcontrol = [self.folder_sucesso, self.folder_falha, self.folder_erro, self.folder_download]

        # TryCtach
        try:

            # Criar pasta de controle
            status_control = self.control.control()
            print(status_control['status'])

            if status_control['status']:
                
                # Criar pasta Fsist
                status_control_service = True
                
                if status_control_service:

                    # Criar pasta Cliente
                    status_control_module = self.subcontrol.subcontrol(self.param_control, self.param_control_service, self.folder_service)

                    if status_control_module['status']:

                        # Criar pasta Subcontrol
                        for param_subcontrol_count, folder_subcontrol_count in zip(param_subcontrol, folder_subcontrol):

                            status_control_module = self.subcontrol.subcontrol(self.param_control_module, param_subcontrol_count, folder_subcontrol_count)

                            if status_control_module['status']:
                                self.status = True
                                mensagem = f'Sucesso ao criar as pastas: "{self.folder_control}", "{self.folder_service}"'
                                print(mensagem)

                            else:
                                self.status = False
                                mensagem = f'Falha ao criar as pastas: "{folder_subcontrol}"'
                                print(mensagem)

                    else:
                        self.status = False
                        mensagem = f'Falha ao criar a pasta: "{self.folder_module}"'
                        print(mensagem)
                
                else:
                    self.status = False
                    mensagem = f'Falha ao criar a pasta: "{self.folder_service}"'
                    print(mensagem)

            else:
                self.status = False
                mensagem = f'Falha ao criar a pasta: "{self.folder_control}"'
                print(mensagem)

            # Alimentar o log
            if self.status:
                self.my_logger.log_info(self.sucesso)
                self.my_logger.log_info(mensagem)

            else:
                self.my_logger.log_warn(self.falha)
                self.my_logger.log_warn(mensagem)

        except Exception as aviso:
            self.status = False
            mensagem = f'Erro ao criar as pastas: "{self.folder_control}", "{self.folder_service}"'
            print(self.erro)
            print(mensagem)
            print(aviso)

            # Alimentar o log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error(mensagem)
            self.my_logger.log_error(str(aviso))

        return{'status': self.status}