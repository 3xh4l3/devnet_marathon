#!/usr/bin/env python3
""" Библиотека функций для работы с оборудованием
"""
import re
from pprint import pprint
from os.path import join
from datetime import datetime
from ciscoconfparse import CiscoConfParse
from config import (
    CONFDIR,
    NTP_SERVERS,
    TIMEZONE,
    NET_TEXTFSM
)


def config_ntp(**device):
    """ Осуществляет настройку NTP и возвращает статус 
    синхронизации
    """
    # Получаем список настроенных серверов
    textfsm_template = join(
        NET_TEXTFSM,
        'show_ios_ntp_config.textfsm'
    )

    ntp_servers = device["con"].send_command(
        "show ntp config",
        use_textfsm=True,
        textfsm_template=textfsm_template
    )

    cmd = []
    # Если NTP запущен, проверяем наличие лишних
    # серверов
    if "not runing" not in ntp_servers:
        # Удаляем лишние NTP серверы
        for server in ntp_servers:
            srv = server["server"]
            if srv not in NTP_SERVERS:
                cmd.append(f"no ntp server {srv}")

    # Настриваем нужные серверы с проверкой доступности
    for server in NTP_SERVERS:
        if __check_ping(device["con"], server):
            cmd.append(f"ntp server {server} minpoll 4")

    # Настриваем временную зону
    cmd.append(f"clock timezone {TIMEZONE}")

    # Применяем конфигурацию
    device["con"].enable()
    device["con"].send_config_set(cmd)
    device["con"].send_command("write")

    # Статус NTP
    ntp_status = device["con"].send_command("show ntp status")

    m = re.match(r"^Clock is (\w+)", ntp_status)
    if m:
        return f"NTP {m.group(1)}"

    return "NTP unknown"


def __check_ping(con, ip):
    out = con.send_command(f"ping {ip}")

    if re.search(r"Success rate is 0", out, flags=re.MULTILINE):
        return
    return True


def get_configs(**device):
    """ Получает конфиг из вывода команды show run и сохраняет
    его в файл с именем <device_name>_<current_date>
    Название устройства берет из конфигурации.
    Если не задан hostname, то используется host из inventory.
    """
    config = device["con"].enable()
    config = device["con"].send_command("show running-config")

    parser = CiscoConfParse(config.splitlines())
    objs = parser.find_objects(r"^hostname\s")

    if len(objs) == 0:
        device_name = device["host"]
    else:
        device_name = objs[0].re_match(r"^hostname\s(.+)$")

    current_date = datetime.now().strftime("%Y-%m-%d")
    file_name = join(CONFDIR, f"{device_name}_{current_date}.conf")

    with open(file_name, 'w') as f:
        f.write(config)

    return f"Config saved to {file_name}"


def get_cdp_status(**device):
    """ Парсит CDP соседей при помощи шаблона TextFSM, если
    вывод не вернул сообщение CDP is not enabled
    """
    textfsm_template = join(
        NET_TEXTFSM,
        'cisco_ios_show_cdp_neighbors.textfsm'
    )

    cdp_neighbors = device["con"].send_command(
        "show cdp neighbors",
        use_textfsm=True,
        textfsm_template=textfsm_template
    )

    if not "CDP is not enabled" in cdp_neighbors:
        return "CDP is ON, {} peers".format(
            len(cdp_neighbors)
        )

    return "CDP is OFF"


def get_version(**device):
    """ Парсит версию ПО при помощи шаблона TextFSM и проверяет
    тип программного обеспечения (PE, NPE)
    """
    textfsm_template = join(
        NET_TEXTFSM,
        'cisco_ios_show_version.textfsm'
    )

    version = device["con"].send_command(
        "show version",
        use_textfsm=True,
        textfsm_template=textfsm_template
    )

    if len(version) == 1:
        version = version[0]

        npe = "PE"
        if 'npe' in version["running_image"].lower():
            npe = "NPE"

        return ", ".join([
            version["rommon"],
            version["version"],
            npe
        ])

    return "Cant' get version"


if __name__ == "__main__":
    pass
