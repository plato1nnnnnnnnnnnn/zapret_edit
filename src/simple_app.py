import sys
import json
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QCheckBox, QMessageBox
)
import os

def get_config_path():
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_path, 'config.json')
    if not os.path.exists(config_path):
        config_path = os.path.join(os.getcwd(), 'src', 'config.json')
    return config_path

def ensure_config_exists(path):
    if not os.path.exists(path):
        default_config = {
            "enabled_services": ["discord", "youtube", "soundcloud", "spotify"],
            "external_proxy": ""
        }
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=2)

CONFIG_PATH = get_config_path()
ensure_config_exists(CONFIG_PATH)
SERVICES = [
    "discord", "youtube", "soundcloud", "spotify", "telegram", "whatsapp",
    "instagram", "facebook", "twitter", "tiktok", "snapchat", "linkedin",
    "pinterest", "reddit", "vimeo", "tumblr"
]

class SimpleProxyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Zapret Proxy')
        self.setGeometry(100, 100, 350, 350)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.service_checks = {}
        self.proxy_proc = None
        self.load_config()
        self.init_ui()

    def load_config(self):
        try:
            with open(CONFIG_PATH, 'r') as f:
                self.config = json.load(f)
        except Exception:
            self.config = {"enabled_services": [], "external_proxy": ""}

    def save_config(self):
        self.config["enabled_services"] = [s for s, cb in self.service_checks.items() if cb.isChecked()]
        self.config["external_proxy"] = self.proxy_input.text()
        with open(CONFIG_PATH, 'w') as f:
            json.dump(self.config, f, indent=2)

    def init_ui(self):
        self.layout.addWidget(QLabel("Сервисы для обхода блокировок:"))
        for service in SERVICES:
            cb = QCheckBox(service)
            cb.setChecked(service in self.config.get("enabled_services", []))
            self.service_checks[service] = cb
            self.layout.addWidget(cb)

        self.layout.addWidget(QLabel("Внешний прокси (http://host:port):"))
        self.proxy_input = QLineEdit(self.config.get("external_proxy", ""))
        self.layout.addWidget(self.proxy_input)

        self.start_btn = QPushButton("Запустить прокси и сохранить настройки")
        self.start_btn.clicked.connect(self.start_proxy)
        self.layout.addWidget(self.start_btn)

        self.stop_btn = QPushButton("Остановить прокси")
        self.stop_btn.clicked.connect(self.stop_proxy)
        self.layout.addWidget(self.stop_btn)

        self.autorun_btn = QPushButton("Добавить в автозапуск (Windows)")
        self.autorun_btn.clicked.connect(self.add_autorun)
        self.layout.addWidget(self.autorun_btn)

    def start_proxy(self):
        self.save_config()
        try:
            if self.proxy_proc is None:
                self.proxy_proc = subprocess.Popen([sys.executable, 'src/proxy_server.py'])
                QMessageBox.information(self, "Запуск", "Прокси-сервер запущен!")
            else:
                QMessageBox.warning(self, "Уже запущено", "Прокси уже работает.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось запустить: {e}")

    def stop_proxy(self):
        try:
            if self.proxy_proc:
                self.proxy_proc.terminate()
                self.proxy_proc = None
                QMessageBox.information(self, "Остановлено", "Прокси-сервер остановлен!")
            else:
                QMessageBox.warning(self, "Нет процесса", "Прокси не был запущен.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось остановить: {e}")

    def add_autorun(self):
        if sys.platform.startswith('win'):
            bat_path = os.path.abspath('start_proxy.bat')
            startup_dir = os.path.expandvars(r'%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup')
            try:
                import shutil
                shutil.copy(bat_path, startup_dir)
                QMessageBox.information(self, "Автозапуск", "Файл автозапуска добавлен!")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось добавить в автозапуск: {e}")
        else:
            QMessageBox.information(self, "Автозапуск", "Для Linux используйте systemd (см. README)")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = SimpleProxyApp()
    gui.show()
    sys.exit(app.exec_())
