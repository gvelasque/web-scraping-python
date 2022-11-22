from bs4 import BeautifulSoup

from selenium.common.exceptions import NoSuchElementException

from scraper.manage_files.manage_logs import create_log


def categories_page(soup: BeautifulSoup, list_logs: list[str] = None) -> dict:
    """Return all categories to the current page"""
    try:
        categories = soup.find(
            'div', {
                'role': 'group',
                'class': '_p13n-zg-nav-tree-all_style_zg-browse-group__88fbz'})
        return {category.text: category.get('href')
                for category in categories.find_all('a')}
    except AttributeError as e:
        if list_logs is not None:
            list_logs.append(create_log(e, categories_page))


def next_page(soup: BeautifulSoup,
              list_logs: list[str] = None) -> BeautifulSoup:
    """Return the url the next page."""
    try:
        return soup.find('li', {'class': 'a-last'})
    except AttributeError as e:
        if list_logs is not None:
            list_logs.append(create_log(e, next_page))


def get_items_root(soup: BeautifulSoup, list_logs: list[str]) -> list:
    """Returns all item links to the current page."""
    position: int = 0
    list_items: list = []
    try:
        grid_item_root = soup.find_all('div', {'id': 'gridItemRoot'})
        for item in grid_item_root:
            try:
                a_link = item.find('a', {'class': 'a-link-normal',
                                         'tabindex': '-1'}).get('href')
                list_items.append(a_link)
            except AttributeError as e:
                if list_logs is not None:
                    list_logs.append(create_log(e, get_items_root))
                continue
            position += 1
        return list_items
    except NoSuchElementException as e:
        if list_logs is not None:
            list_logs.append(create_log(e, get_items_root))
