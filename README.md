# Марафон Cisco DevNET  - День 1

## Использование

Скрипт поддерживает аргументы командной строки. На выполнение можно указать любой набор.

```bash
#./run.py
usage: DEVNET [-h] [--get_configs] [--config_ntp] [--get_cdp_status]
              [--get_version]

optional arguments:
  -h, --help        show this help message and exit
  --get_configs     Собрать конфигурации со всех устройств
  --config_ntp      Настроить NTP на всех устройствах
  --get_cdp_status  Вывести статус CDP и количество соседей
  --get_version     Вывести версию ПО
```

Пример вывода работы скрипта с полным набором аргументов.
```bash
#./run.py --config_ntp --get_configs --get_cdp_status --get_version
+---------------+-------------------------+--------------------+------------------+------------------------------------------------------------------------------------+
|      Host     |     Software Version    |     CDP status     |    NTP status    |                                   Config status                                    |
+---------------+-------------------------+--------------------+------------------+------------------------------------------------------------------------------------+
| 192.168.88.92 |   IOS-XE, 16.8.1a, PE   | CDP is ON, 2 peers | NTP synchronized | Config saved to /home/xhale/Dev/python3/devnet_marathon/configs/R1_2020-04-28.conf |
| 192.168.88.90 | Bootstrap, 15.6(2)T, PE | CDP is ON, 3 peers | NTP synchronized | Config saved to /home/xhale/Dev/python3/devnet_marathon/configs/R3_2020-04-28.conf |
| 192.168.88.91 | Bootstrap, 15.6(2)T, PE | CDP is ON, 4 peers | NTP synchronized | Config saved to /home/xhale/Dev/python3/devnet_marathon/configs/R2_2020-04-28.conf |
+---------------+-------------------------+--------------------+------------------+------------------------------------------------------------------------------------+
```

### Настройка

- Предварительные настройки можно произвести в файле `config.py`
- Список устройст указывается в файле `devices.yaml`

## Зависимости

```
netmiko==3.1.0
PTable==0.9.2
PyYAML==5.3
textfsm==1.1.0
```

