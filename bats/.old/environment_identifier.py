# environment_identifier.py

import os
import subprocess

def identify_and_run():
    # Lógica para identificar o ambiente aqui
    is_production = True  # Exemplo: identificar se é produção

    # Buscar o caminho da pasta principal ('RPA-Vincibot')
    dir_path = os.path.dirname(os.path.realpath(__name__))
    print('dir_path')
    print(dir_path)

    # ------------------------- Folders -------------------------
    src = 'src'
    bot_name = 'BOT_SID_Cliente_Documentos.py'
    

    if is_production:
        #script_path = "BOT_SID_Cliente_Documentos.py"  # Caminho para o script inicial
        script_path = os.path.join(dir_path, (os.path.join(src, bot_name)))
        print('script_path')
        print(script_path)
        
    else:
        script_path = "BOT_SID_Cliente_Documentos_dev.py"  # Caminho para o script de desenvolvimento

    # Executar o script inicial
    subprocess.run(["python", script_path])

if __name__ == "__main__":
    identify_and_run()
