import sys
import json
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QCheckBox, QMessageBox, QScrollArea, QGroupBox
)

CONFIG_PATH = 'src/config.json'

SERVICES = [
    "discord", "youtube", "soundcloud", "spotify", "telegram", "whatsapp",
    "instagram", "facebook", "twitter", "tiktok", "snapchat", "linkedin",
    "pinterest", "reddit", "vimeo", "tumblr"
]

class ProxyGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Zapret Proxy Manager')
        self.setGeometry(100, 100, 400, 500)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.service_checks = {}
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
        QMessageBox.information(self, "Сохранено", "Настройки сохранены!")

    def init_ui(self):
        self.layout.addWidget(QLabel("Выберите сервисы для обхода блокировок:"))
        group = QGroupBox()
        group_layout = QVBoxLayout()
        for service in SERVICES:
            cb = QCheckBox(service)
            cb.setChecked(service in self.config.get("enabled_services", []))
            self.service_checks[service] = cb
            group_layout.addWidget(cb)
        group.setLayout(group_layout)
        scroll = QScrollArea()
        scroll.setWidget(group)
        scroll.setWidgetResizable(True)
        self.layout.addWidget(scroll)

        self.layout.addWidget(QLabel("Внешний прокси (http://host:port):"))
        self.proxy_input = QLineEdit(self.config.get("external_proxy", ""))
        self.layout.addWidget(self.proxy_input)

        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Сохранить настройки")
        save_btn.clicked.connect(self.save_config)
        btn_layout.addWidget(save_btn)

        start_btn = QPushButton("Запустить прокси")
        start_btn.clicked.connect(self.start_proxy)
        btn_layout.addWidget(start_btn)

        stop_btn = QPushButton("Остановить прокси")
        stop_btn.clicked.connect(self.stop_proxy)
        btn_layout.addWidget(stop_btn)

        self.layout.addLayout(btn_layout)

    def start_proxy(self):
        try:
            self.proxy_proc = subprocess.Popen([sys.executable, 'src/proxy_server.py'])
            QMessageBox.information(self, "Запуск", "Прокси-сервер запущен!")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось запустить: {e}")

    def stop_proxy(self):
        try:
            if hasattr(self, 'proxy_proc') and self.proxy_proc:
                self.proxy_proc.terminate()
                self.proxy_proc = None
                QMessageBox.information(self, "Остановлено", "Прокси-сервер остановлен!")
            else:
                QMessageBox.warning(self, "Нет процесса", "Прокси не был запущен через GUI.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось остановить: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = ProxyGUI()
    gui.show()
    sys.exit(app.exec_())
