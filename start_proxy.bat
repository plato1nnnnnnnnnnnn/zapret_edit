@echo off
REM Запуск локального прокси-сервера для обхода блокировок
cd /d %~dp0
python src\proxy_server.py
pause
