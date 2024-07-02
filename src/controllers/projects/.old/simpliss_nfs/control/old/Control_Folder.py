from modules.mylogger.mylogger import MyLogger
from modules.mysql.mysql import MySQL
from modules.myfolder.myfolder import MyFolder
from controllers.control import Control, Control_Service, Control_Module

class ControlFolder():
        
    def __init__(self, 
                 user, password, host, database,
                 column_control_path,
                 id_control,
                 table_control,
                 param_control, param_control_service, param_control_sucesso, param_control_falha, param_control_erro,
                 folder_control, folder_service, folder_sucesso, folder_falha, folder_erro, 
                 param_control_module = None,
                 folder_module = None,
                 param_control_download = None,
                 folder_download = None
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
            column_control_path,
            id_control,
            table_control,
            param_control,
            folder_control
        )
        self.control_service = Control_Service.ControlService(
            user, password, host, database, 
            column_control_path,
            id_control,
            table_control,
            param_control, param_control_service,
            folder_service
        )
        self.control_module = Control_Module.ControlModule(
            user, password, host, database, 
            column_control_path,
            id_control,
            table_control,
            param_control_service, param_control_module, param_control_sucesso, param_control_falha, param_control_erro, param_control_download,
            folder_module, folder_sucesso, folder_falha, folder_erro, folder_download
        )

        # Pastas
        self.folder_control = folder_control
        self.folder_service = folder_service
        self.folder_module = folder_module
    
    # Função para verificar se existem arquivos com extensão no caminho  
    def control_folder(self):

        # TryCtach
        try:

            # Criar pasta de controle
            status_control = self.control.control()

            if status_control['status']:
                
                # Criar pasta SID
                status_control_service = self.control_service.control_service()
                
                if status_control_service['status']:

                    # Criar pasta Cliente
                    status_control_sid_cliente = self.control_module.control_module()

                    if status_control_sid_cliente['status']:
                        self.status = True
                        mensagem = f'Sucesso ao criar as pastas: {self.control}, {self.control_service} e {self.control_module}'
                        print(mensagem)

                    else:
                        self.status = False
                        mensagem = f'Falha ao criar a pasta: {self.control_module}'
                        print(mensagem)
                
                else:
                    self.status = False
                    mensagem = f'Falha ao criar a pasta: {self.control_service}'
                    print(mensagem)

            else:
                self.status = False
                mensagem = f'Falha ao criar a pasta: {self.control}'
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
            mensagem = f'Erro ao criar as pastas: {self.control}, {self.control_service} e {self.control_module}'
            print(self.erro)
            print(mensagem)
            print(aviso)

            # Alimentar o log
            self.my_logger.log_error(self.erro)
            self.my_logger.log_error(mensagem)
            self.my_logger.log_error(str(aviso))

        return{'status': self.status}