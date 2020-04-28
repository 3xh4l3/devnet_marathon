#!/usr/bin/env python3
""" Набор функций для работы с оборудованием

"""
from os.path import join
from datetime import datetime
from config import CONFDIR
from ciscoconfparse import CiscoConfParse

def config_ntp(**device):
    """
    """
    ntp_config = con.send_command('show ntp config')
    pprint(ntp_config)


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
    file_name = join(CONFDIR, f"{device_name}_{current_date}")

    with open(file_name, 'w') as f:
        f.write(config)

def get_cdp_status(**device):
    pass

def get_version(**device):
    pass

if __name__ == "__main__":
    pass
