import os
import inspect

class MyName():

    def __init__(self):
        # Variaveis gerais
        self.status = False
        self.sucesso = f'SUCESSO - {__name__}'
        self.falha = f'FALHA - {__name__}'
        self.erro = f'ERRO - {__name__}'

        # Instancias
        # Instanciar é uma boa prática e necessário
        # Não instaciar resulta na abertura de processo diferentes e erros

        # Variaveis especificas
        self.nome_arquivo = None
        self.nome_funcao = None

    # Função para identificar o nome do arquivo que chamou o log
    def my_name(self):

        # TryCatch
        try:

            # Obter a pilha de execução (qual bot chamou)
            pilha_execucao = inspect.stack()

            # O arquivo que chamou diretamente sempre será o segunda da lista [0, 1, 2, ... ] - logo, [1]
            chamador = pilha_execucao[4]

            # Obtem o nome do aquivo que chamou
            nome_arquivo_chamador = os.path.basename(chamador.filename)

            # Atualizar variaveis
            self.nome_arquivo = nome_arquivo_chamador
            print('nome_arquivo - myname')
            print(self.nome_arquivo)

            self.status = True
            print(self.sucesso)

        except Exception as aviso:
            self.status = False
            print(self.erro)
            print(aviso)

        return{'status': self.status, 'nome_arquivo': self.nome_arquivo}
    
    # Função para identificar o nome do modulo
    def mymodule(self):

        # TryCatch
        try:

            # Obtem o nome do aquivo que chamou
            nome_modulo_atual = inspect.currentframe()
            print('nome_modulo_atual')
            print(nome_modulo_atual)
            nome_modulo_anterior = nome_modulo_atual.f_back
            print('nome_modulo_anterior')
            print(nome_modulo_anterior)
            nome_modulo_chamador = nome_modulo_anterior.f_code.co_filename
            print('nome_modulo_chamador')
            print(nome_modulo_chamador)

            self.status = True
            print(self.sucesso)

        except Exception as aviso:
            self.status = False
            print(self.erro)
            print(aviso)

        return{'status': self.status, 'mymodule': nome_modulo_chamador}