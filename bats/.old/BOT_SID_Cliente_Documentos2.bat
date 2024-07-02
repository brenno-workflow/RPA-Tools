@echo off
echo Ativando ambiente virtual...
REM Ativa o ambiente virtual (se aplicável)
call %USERPROFILE%\Desktop\GitHub\RPA-Vincibot\.venv\Scripts\activate

REM Define o diretório de trabalho como "src"
cd /d %USERPROFILE%\Desktop\GitHub\RPA-Vincibot

REM Executa o script Python
echo Executando script Python...
python %USERPROFILE%\Desktop\GitHub\RPA-Vincibot\src\BOT_SID_Cliente_Documentos.py

REM Desativa o ambiente virtual
echo Encerrando o script Python...
REM call deactivate