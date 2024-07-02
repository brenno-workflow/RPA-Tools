@echo off
REM Ativa o ambiente virtual (se aplicável)
REM call %USERPROFILE%\Desktop\GitHub\RPA-Vincibot\.venv\Scripts\activate

REM Define o diretório de trabalho como "src"
cd /d %USERPROFILE%\Desktop\GitHub\RPA-Vincibot

REM Executa o script Python
python %USERPROFILE%\Desktop\GitHub\RPA-Vincibot\src\BOT_SID_Cliente_Documentos.py

pause

REM Desativa o ambiente virtual (se aplicável)
REM call deactivate