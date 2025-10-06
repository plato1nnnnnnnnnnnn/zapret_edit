## Сборка простого exe-файла

1. Установите PyInstaller:
	```bash
	pip install pyinstaller
	```
2. Соберите exe-файл:
	```bash
	pyinstaller --onefile --name zapret_proxy_simple --icon icon.ico src/simple_app.py
	```
	В папке `dist` появится файл `zapret_proxy_simple.exe`.

3. Запустите `zapret_proxy_simple.exe` как обычную программу.

4. Для автозапуска используйте кнопку в приложении или скопируйте exe-файл в папку автозагрузки (`shell:startup`).
## Графический интерфейс (GUI)

Для удобного управления настройками и запуском сервиса используйте GUI:

1. Установите PyQt5:
	```bash
	pip install pyqt5
	```
2. Запустите GUI:
	```bash
	python src/gui.py
	```
3. В окне выберите нужные сервисы, укажите внешний прокси, сохраните настройки и запустите/остановите прокси-сервер кнопками.
## Создание инсталлятора для Windows

1. Установите [Inno Setup](https://jrsoftware.org/isinfo.php).
2. Соберите exe-файл через PyInstaller (см. выше).
3. Откройте файл `zapret_proxy_installer.iss` в Inno Setup и соберите инсталлятор.
4. После установки программа будет доступна в меню Пуск и запускаться автоматически.
## Сборка exe-файла для Windows

1. Установите Python и PyInstaller:
	```bash
	pip install pyinstaller
	```

2. Соберите exe-файл с иконкой:
	```bash
	pyinstaller --onefile --name zapret_proxy --icon icon.ico src/proxy_server.py
	```
	В папке `dist` появится файл `zapret_proxy.exe` с вашей иконкой.

	Если хотите использовать свою иконку, замените файл `icon.ico` на свой.

3. Запустите `zapret_proxy.exe` как обычную программу.

4. Для автозапуска скопируйте exe-файл в папку автозагрузки (`shell:startup`).
## Автозапуск

### Windows
1. Скопируйте файл `start_proxy.bat` в папку автозагрузки:
	- Нажмите Win+R, введите `shell:startup` и нажмите Enter.
	- Скопируйте `start_proxy.bat` в открывшуюся папку.
2. Прокси-сервер будет запускаться автоматически при входе в систему.

### Linux
1. Создайте unit-файл для systemd:
	```ini
	[Unit]
	Description=Zapret Proxy Server

	[Service]
	WorkingDirectory=/workspaces/zapret_edit
	ExecStart=/usr/bin/python3 src/proxy_server.py
	Restart=always

	[Install]
	WantedBy=multi-user.target
	```
2. Сохраните файл как `/etc/systemd/system/zapret_proxy.service`.
3. Активируйте автозапуск:
	```bash
	sudo systemctl enable zapret_proxy
	sudo systemctl start zapret_proxy
	```
# zapret_edit

## Описание

Этот проект позволяет обходить блокировки для выбранных приложений и сервисов (например, Discord, YouTube, SoundCloud, Spotify), не затрагивая трафик других программ.

## Настройка и запуск

1. В файле `config.json` укажите приложения, для которых требуется обход блокировок, и адрес внешнего прокси:
	```json
	{
	  "enabled_services": [ ... ],
	  "external_proxy": "http://your-external-proxy:3128"
	}
	```

2. Запустите прокси-сервер:
	```bash
	python3 src/proxy_server.py &
	```
	или добавьте в автозагрузку через systemd.

3. Настройте систему, браузер или нужные приложения на использование локального прокси:
	- Адрес: 127.0.0.1
	- Порт: 8080

4. Трафик заблокированных сервисов будет автоматически перенаправляться через внешний прокси, остальные приложения будут работать напрямую.

## Структура
- `config.json` — список приложений для обхода блокировок и адрес внешнего прокси
- `proxy_server.py` — основной прокси-сервер
- `handlers/` — обработчики для каждого приложения (расширяемые)

## Список поддерживаемых заблокированных сервисов
- Discord
- YouTube
- SoundCloud
- Spotify
- Telegram
- WhatsApp
- Instagram
- Facebook
- Twitter
- TikTok
- Snapchat
- LinkedIn
- Pinterest
- Reddit
- Vimeo
- Tumblr
