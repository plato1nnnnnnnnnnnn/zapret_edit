#!/bin/bash
set -e

# Установка зависимостей
pip install -r requirements.txt

# Сборка exe через PyInstaller
pyinstaller zapret_proxy_simple.spec

echo "Сборка завершена. Файл находится в папке dist/"
