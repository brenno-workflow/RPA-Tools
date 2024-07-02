@echo off
echo Ativando ambiente virtual...
REM Ativa o ambiente virtual (se aplicável)
call %USERPROFILE%\Desktop\GitHub\Tools\.venv\Scripts\activate

REM Define o diretório de trabalho como "src"
cd /d %USERPROFILE%\Desktop\GitHub\Tools

REM Executa o script Python
echo Executando script Python...
python %USERPROFILE%\Desktop\GitHub\Tools\src\BOT_Tools.py

REM Desativa o ambiente virtual
echo Encerrando o script Python...
REM call deactivate