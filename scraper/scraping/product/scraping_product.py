import re
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from scraper.constants import DOMAIN_AMAZON
from scraper.db.manage_db import description_product, \
    short_description_product, short_description_product2, \
    generate_tags_product, swatches_attributes, create_term_product
from scraper.loader.load_url import load_url_wait
from scraper.scraping.product.elements_products import *
from scraper.scraping.scraping_setup import soup_page


def scraping_product(product_id: int, path: str, directory: str,
                     location: int, driver=None, list_logs: list[str] = None):
    # Load web page and get a raw parsed HTML
    if driver is None:
        driver = load_url_wait(DOMAIN_AMAZON, path, find_by=By.ID,
                               element_to_find='productTitle', timeout=2,
                               driver=driver, list_logs=list_logs)
    else:
        load_url_wait(DOMAIN_AMAZON, path, find_by=By.ID,
                      element_to_find='productTitle', timeout=2,
                      driver=driver, list_logs=list_logs)

    soup_product = soup_page(driver, list_logs)

    asin = re.search(r'dp/(\w+)/', path).groups()[0]
    title = get_name(soup_product, list_logs, location)
    brand = get_brand(soup_product, list_logs, location)
    create_data = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
    price = get_price(soup_product, list_logs, location)
    rrp_price = get_rrp_product(soup_product, list_logs, location)
    description = description_product(
        get_feature_bullets(soup_product, list_logs, location))
    colors = get_variation_colors(soup_product, list_logs, location)
    sizes = get_variation_size(soup_product, list_logs, location)
    average_stars = get_average_stars(soup_product, list_logs, location)
    average_reviews = get_average_reviews(soup_product, list_logs, location)
    shor_description = short_description_product(brand=brand)
    shor_description2 = short_description_product2(
        title=title, brand=brand, colors=colors, sizes=sizes,
        average_reviews=average_reviews)
    set_image_links = get_image_links(soup_product, list_logs, location)
    tags_products = generate_tags_product(title, brand)
    swatches = swatches_attributes(colors=colors, sizes=sizes)

    if len(asin) < 1:
        print(path)
        return None, driver
    """if len(price) < 1:
        return None, driver
    if len(set_image_links) < 1:
        return None, driver"""

    dataset_product = create_term_product(
        term_id=product_id, name=title, sku=asin, descr=description,
        short_descr=shor_description,
        categories=directory, tags=tags_products, swatches=swatches,
        list_colors=colors, list_sizes=sizes, images=set_image_links)

    # Set the dataset
    """data = {
        'id': product_id,
        'ASIN': asin,
        'title': title,
        'brand': brand,
        'urls': {
            'url': path,
            'affiliate_url': affiliate_url,
        },
        'create_data': create_data,
        'update_data': create_data,
        'metrics': {
            'average_stars': average_stars,
            'average_reviews': average_reviews,
        },
        'short': shor_description2,
        'price_features': {
            'price': price,
            'discount': get_discount(soup_product, list_logs, location),
            'rrp_price': rrp_price
        },
        'color_feature': {
            'current_color': get_current_color(
                soup_product, list_logs, location),
            'available_colors': colors,
        },
        'sizes': sizes,
        'features': description,
        'set_image_links': set_image_links
    }"""
    return dataset_product, driver
