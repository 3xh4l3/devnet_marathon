# /usr/bin/env python3
from os import path, environ

# Рабочая директория
WDIR = path.dirname(path.realpath(__file__))

# Список узлов
INVENTORY = path.join(WDIR, "devices.yaml")

# TextFSM
NET_TEXTFSM = path.join(WDIR, "ntc-templates/templates/")

# Сохраненнные конфигурации
CONFDIR = path.join(WDIR, "configs/")

# Настройки NTP
NTP_SERVERS = ["10.7.0.1", "192.168.88.1", "1.2.3.4"]
TIMEZONE = "UTC 0 0"

# Подключение к оборудованию
USERNAME = "admin"
PASSWORD = "cisco"
SECRET = "cisco"
