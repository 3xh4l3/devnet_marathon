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
  проверив его доступность.
5. Вывести отчет в виде нескольких строк, 
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
from netmiko import ConnectHandler, Netmiko
from concurrent.futures import ThreadPoolExecutor, as_completed
from prettytable import PrettyTable
from tools import (
    get_configs,
    get_cdp_status,
    get_version,
    config_ntp
)
from config import (
    INVENTORY,
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

    # Определяем, какие задания необходимо выполнить
    fields = ["Host"]
    jobs = []
    if args.get_version:
        jobs.append(get_version)
        fields.append("Software Version")
    if args.get_cdp_status:
        jobs.append(get_cdp_status)
        fields.append("CDP status")
    if args.config_ntp:
        jobs.append(config_ntp)
        fields.append("NTP status")
    if args.get_configs:
        jobs.append(get_configs)
        fields.append("Config status")

    # Если нет заданий, просто выводим помощь
    if len(jobs) == 0:
        parser.print_help()
    else:
        # Инициализируем таблицу для вывода данных
        table = PrettyTable()

        # Выполняем задачи для хостов в 4 потока
        with ThreadPoolExecutor(max_workers=4) as ex:
            future = {ex.submit(worker, host, jobs) for host in hosts}
            for future in as_completed(future):
                table.add_row(future.result())

        # Итоговая таблица с данными
        table.field_names = fields
        print(table)


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
    con = Netmiko(**device)

    if con.find_prompt():
        device = {
            "con": con,
            "host": host
        }
        result = [host]
        for job in jobs:
            result.append(job(**device))
        return result
    else:
        return "Не удалось подключиться к f{host}"


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

    parser.add_argument(
        "--get_cdp_status",
        action='store_true',
        help="Вывести статус CDP и количество соседей"
    )

    parser.add_argument(
        "--get_version",
        action='store_true',
        help="Вывести версию ПО"
    )

    return parser, parser.parse_args()


if __name__ == "__main__":
    main()
