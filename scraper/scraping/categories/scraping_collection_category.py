import re

from scraper.constants import DOMAIN_AMAZON
from scraper.loader.load_url import load_url_wait
from scraper.scraping.scraping_setup import soup_page
from .elements_categories import get_items_root, next_page
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeWebDriver

from ...manage_files.manage_logs import create_log


def extract_collection_category(path: str,
                                list_logs: list[str] = None,
                                driver=None) -> tuple[list[str],
                                                      ChromeWebDriver]:
    # Load web page and get a raw parsed HTML, get category page.
    collection_list = []
    while True:
        try:
            if driver is None:
                driver = load_url_wait(domain=DOMAIN_AMAZON, path=path,
                                       scroll_to=500, driver=driver,
                                       list_logs=list_logs)
            else:
                load_url_wait(domain=DOMAIN_AMAZON, path=path, scroll_to=500,
                              driver=driver, list_logs=list_logs)

            soup = soup_page(driver, list_logs)
            collection_list.extend(get_items_root(soup, list_logs))
            path = next_page(soup, list_logs).a.get('href')

            if len(collection_list) < 50:
                create_log(Exception(f"Review: {path}"),
                           extract_collection_category)

        except AttributeError as e:
            if len(list_logs) is not None:
                list_logs.append(create_log(e, extract_collection_category))
            break
    print('>>> Collection list: ', len(collection_list))
    return collection_list, driver


def extract_subcategories(list_categories, list_to_populate,
                          directory, level=0,
                          list_logs: list[str] = None) -> list[tuple]:
    level += 1
    for category_dict in list_categories:
        for name_category, data_list in category_dict.items():
            if level != 4:
                directory += f"{name_category}/"
            list_to_populate.append(
                (level, name_category, directory, data_list['url']))
            try:
                if 'subcategories' in data_list.keys():
                    extract_subcategories(
                        data_list['subcategories'], list_to_populate,
                        directory, level)
            except AttributeError as e:
                if len(list_logs) is not None:
                    list_logs.append(
                        create_log(e, extract_collection_category))
                continue
            directory = re.sub(rf"{name_category}/[\s\w/]*", "", directory)
    level -= 1
    return list_to_populate
