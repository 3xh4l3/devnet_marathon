# /usr/bin/env python3
from os import path

# Рабочая директория
WDIR = path.dirname(path.realpath(__file__))

# Список узлов
INVENTORY = path.join(WDIR, "devices.yaml")

# TextFSM
TEMPLATES = path.join(WDIR, "templates/")

# Сохраненнные конфигурации
CONFDIR = path.join(WDIR, "configs/")

# Настройки NTP
NTP_PEERS = ["10.7.0.1"]
TIMEZONE = "UTC 0 0"

# Подключение к оборудованию
USERNAME = "admin"
PASSWORD = "cisco"
SECRET = "cisco"
