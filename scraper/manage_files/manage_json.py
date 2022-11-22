import os
import json

from scraper.constants import BASE_DIR_POSIX
from scraper.manage_files.manage_logs import create_log


def create_json_file(path: str, filename: str, data_set: list,
                     list_logs: list[str] = None) -> None:
    """Create a Json file at a defined path"""

    absolute_path = "/".join([BASE_DIR_POSIX, path])

    if not os.path.exists(absolute_path):
        os.makedirs(absolute_path)

    # Transform JSON Format
    json_string = json.dumps(data_set)
    parsed = json.loads(json_string)

    try:
        with open(f'{"/".join([absolute_path, filename])}.json',
                  'w') as infile:
            infile.write(json.dumps(parsed, indent=4))
    except FileNotFoundError as e:
        if len(list_logs) is not None:
            list_logs.append(create_log(e, create_json_file))


def load_json_file(path: str, list_logs: list[str]) -> dict:
    """Open a Json file at a defined path"""

    dict_categories = {}
    absolute_path = "/".join([BASE_DIR_POSIX, path])

    try:
        with open(absolute_path, encoding="utf-8") as infile:
            dict_categories = json.loads(infile.read())
    except FileNotFoundError as e:
        if len(list_logs) is not None:
            list_logs.append(create_log(e, load_json_file))

    return dict_categories
