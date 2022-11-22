import time

from selenium.webdriver.chrome.webdriver import WebDriver as ChromeWebDriver
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from scraper.browser.chrome_manager import launch_browser
from scraper.manage_files.manage_logs import create_log


def load_url(domain: str, path: str, driver: ChromeWebDriver = None,
             list_logs: list[str] = None) -> ChromeWebDriver:
    """Load the given web page"""

    absolute_path = domain + path

    if driver is None:
        try:
            driver = launch_browser()
        except WebDriverException as e:
            if len(list_logs) is not None:
                list_logs.append(create_log(e, load_url))

    try:
        driver.get(absolute_path)
    except WebDriverException as e:
        if len(list_logs) is not None:
            list_logs.append(create_log(e, load_url))
    return driver


def load_url_wait(domain: str, path: str, timeout: float = 0.5,
                  find_by: str = None, element_to_find: str = None,
                  scroll_to: int = None, driver: ChromeWebDriver = None,
                  list_logs: list[str] = None) -> ChromeWebDriver:
    """Load the given web page"""
    absolute_path = domain + path

    if driver is None:
        driver = launch_browser()

    try:
        driver.get(absolute_path)
    except WebDriverException as e:
        if len(list_logs) is not None:
            list_logs.append(create_log(e, load_url))

    if scroll_to is not None:
        start_scroll = 2500
        new_scroll_to = scroll_to + start_scroll

        while True:
            # Scroll down to bottom
            driver.execute_script(
                f"window.scrollTo({start_scroll}, {new_scroll_to})")
            new_scroll_to += scroll_to
            # Wait to load page
            time.sleep(0.3)

            body_height = driver.execute_script(
                "return document.body.scrollHeight")

            if body_height < new_scroll_to:
                break

    if element_to_find is not None and find_by is not None:
        try:
            element_present = ec.presence_of_element_located(
                (find_by, element_to_find))
            WebDriverWait(driver, timeout).until(element_present)
        except TimeoutException as e:
            if len(list_logs) is not None:
                list_logs.append(create_log(e, load_url))

    return driver
