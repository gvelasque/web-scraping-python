import os

from scraper.constants import BASE_DIR_POSIX
from scraper.manage_files.manage_logs import create_log


def create_list_file(path: str, filename: str, list_of: list or tuple,
                     list_logs: list[str] = None) -> None:
    """Create a list file"""

    if not len(list_of) > 0:
        return None

    path = "/".join([BASE_DIR_POSIX, path])

    if not os.path.exists(path):
        os.makedirs(path)

    try:
        with open(f'{"/".join([path, filename])}.txt', 'w') as infile:
            for i in list_of:
                infile.write(f'{i}\n')
    except FileNotFoundError as e:
        if len(list_logs) is not None:
            list_logs.append(create_log(e, open_list_file))


def open_list_file(path: str, list_logs: list[str] = None) -> list:
    """Open a list file at a defined path"""

    absolute_path = "/".join([BASE_DIR_POSIX, path])

    try:
        with open(absolute_path, encoding="utf-8") as infile:
            list_in_file = infile.readlines()
    except FileNotFoundError as e:
        if len(list_logs) is not None:
            list_logs.append(create_log(e, open_list_file))

    return list_in_file
