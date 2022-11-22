from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeWebDriver
from webdriver_manager.chrome import ChromeDriverManager

disable_options: bool = True


def disable_chrome_options(disable: bool) -> ChromeOptions:
    """Disable ChromeDriver options"""
    options = ChromeOptions()

    if disable:
        prefs = {
            'profile.default_content_setting_values': {
                'images': 2,
                'automatic_downloads': 2,
                'notifications': 2,
                'geolocation': 2,
            }
        }
        options.add_experimental_option("prefs", prefs)

    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    return options


def launch_browser() -> ChromeWebDriver:
    """Downloading the binary and configuring the path automatically"""
    return Chrome(options=disable_chrome_options(disable_options),
                  service=ChromeService(ChromeDriverManager().install()))
