import os
import csv

from scraper.constants import BASE_DIR_POSIX
from scraper.manage_files.manage_logs import create_log


def create_csv_file(path: str, filename: str, data_set: list,
                    list_logs: list[str] = None) -> None:
    """Create a CSV file at a defined path"""
    absolute_path = "/".join([BASE_DIR_POSIX, path])

    if not os.path.exists(absolute_path):
        os.makedirs(absolute_path)

    # Add JSON static to list
    try:
        with open(f'{"/".join([absolute_path, filename])}.csv', 'w',
                  encoding='UTF8', newline='') as infile:
            for line in data_set:
                writer = csv.writer(infile)
                writer.writerow(line)
    except FileNotFoundError as e:
        if len(list_logs) is not None:
            list_logs.append(create_log(e, create_csv_file))
