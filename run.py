#!/usr/bin/env python3
"""
Необходимо:
1.Собрать со всех устройств файлы конфигураций, сохранить их на диск,
  используя имя устройства и текущую дату в составеимени файла. 
2. Проверить на всех коммутаторах-включен ли протокол CDP и есть ли 
  упроцесса CDPна каждом из устройств данные о соседях. 
3. Проверить, какой типпрограммного обеспечения(NPEили PE)* используется 
  на устройствах исобрать со всех устройств данные о версиииспользуемого ПО. 
4. Настроить на всех устройствах timezone GMT+0, получение данных для 
  синхронизациивремени от источника во внутренней сети, предварительно 
  проверив его доступность.5. Вывести отчет в виде нескольких строк, 
  каждая изкоторых имеет следующийформат, близкий к такому:
  Имя устройства 
  - тип устройства 
  - версия ПО 
  - NPE/PE 
  - CDP on/off, Xpeers
  - NTP in sync/not sync.
  Пример: 
  ms-gw-01|ISR4451/K9|BLD_V154_3_S_XE313_THROTTLE_LATEST |PE |CDP is ON,5peers |Clock in Sync 
  ms-gw-02|ISR4451/K9|BLD_V154_3_S_XE313_THROTTLE_LATEST |NPE|CDP is ON,0 peers|Clock in Sync
"""
import argparse
import yaml
import os
from netmiko import ConnectHandler
from concurrent.futures import ThreadPoolExecutor
from tools import (
    get_configs,
    get_cdp_status,
    get_version,
    config_ntp
)
from config import (
    INVENTORY,
    NTP_PEERS,
    TIMEZONE,
    USERNAME,
    PASSWORD,
    SECRET
)


def main():
    parser, args = get_args()

    # Загружаем список хостов
    try:
        with open(INVENTORY) as f:
            hosts = yaml.load(
                f.read(),
                Loader=yaml.Loader
            )
    except Exception as e:
        exit(e)

    # Выполняем указанные в аргументах задачи
    jobs = []
    if args.config_ntp:
        jobs.append(config_ntp)
    if args.get_configs:
        jobs.append(get_configs)

    # Если нет заданий, просто выводим помощь
    if len(jobs) == 0:
        parser.print_help()
    else:
        # Выполняем задачи для хостов
        for host in hosts:
            worker(host, jobs)


def worker(host, jobs):
    """ Обработчик заданий
    """
    device = {
        "device_type": "cisco_ios",
        "host": host,
        "username": USERNAME,
        "password": PASSWORD,
        "secret": SECRET
    }
    con = ConnectHandler(**device)
    
    if con:

        device = {
            "con": con,
            "host": host
        }

        for job in jobs:
            job(**device)
    else:
        print("Не удалось подключиться к f{host}")


def get_args():
    """ Парсер аргументов командной строки
    """
    parser = argparse.ArgumentParser(prog="DEVNET")

    parser.add_argument(
        "--get_configs",
        action='store_true',
        help="Собрать конфигурации со всех устройств"
    )

    parser.add_argument(
        "--config_ntp",
        action='store_true',
        help="Настроить NTP на всех устройствах"
    )

    return parser, parser.parse_args()


if __name__ == "__main__":
    main()
