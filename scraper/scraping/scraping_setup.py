from bs4 import BeautifulSoup

from selenium.webdriver.chrome.webdriver import WebDriver as ChromeWebDriver

from scraper.manage_files.manage_logs import create_log


def soup_page(driver: ChromeWebDriver,
              list_logs: list[str] = None) -> BeautifulSoup:
    """A static structure representing a parsed HTML"""

    try:
        return BeautifulSoup(driver.page_source, 'html.parser')
    except AttributeError as e:
        if len(list_logs) is not None:
            list_logs.append(create_log(e, soup_page))
