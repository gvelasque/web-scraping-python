import os

from scraper.constants import BASE_DIR_POSIX


def create_log(exception: Exception, func: object, position: int = 0) -> str:
    """Create a log to handle an exception"""
    if position is not None:
        return f'Item position: {position:03}, ' \
               f'Exception: {exception}, Function: {func.__name__} '
    else:
        return f'Exception: {exception}, Function: {func.__name__} '


def create_logfile(path: str, filename: str,
                   list_logs: list[str] = None) -> None:
    """Create a log file at a defined path"""

    if not len(list_logs) > 0:
        return None

    path = "/".join([BASE_DIR_POSIX, path])

    if not os.path.exists(path):
        os.makedirs(path)

    try:
        with open(f'{"/".join([path, filename])}.txt', 'w') as infile:
            for log in list_logs:
                infile.write(f"{log}\n")
    except FileNotFoundError as e:
        if len(list_logs) is not None:
            list_logs.append(create_log(e, create_logfile))
