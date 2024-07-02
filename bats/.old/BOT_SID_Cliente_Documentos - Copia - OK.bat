@echo off
echo Ativando ambiente virtual...
REM Ativa o ambiente virtual (se aplicável)
call C:\Users\leonardo.vinci\Desktop\GitHub\RPA-Vincibot\.venv\Scripts\activate

REM Define o diretório de trabalho como "src"
cd /d C:\Users\leonardo.vinci\Desktop\GitHub\RPA-Vincibot

REM Executa o script Python
echo Executando script Python...
python C:\Users\leonardo.vinci\Desktop\GitHub\RPA-Vincibot\src\BOT_SID_Cliente_Documentos.py

REM Desativa o ambiente virtual
echo Encerrando o script Python...
REM call deactivate