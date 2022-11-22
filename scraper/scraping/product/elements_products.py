from re import findall, sub
from bs4 import BeautifulSoup

# Get product static
from scraper.manage_files.manage_logs import create_log


def get_id(soup: BeautifulSoup, list_logs: list[str] = None,
           position: int = None) -> str:
    """Get id product"""
    try:
        id_product = soup.find(
            'table', {'id': 'productDetails_detailBullets_sections1'})
        asin = id_product.find('td', {'class': 'a-size-base prodDetAttrValue'})
        return asin.text.strip()
    except AttributeError:
        try:
            id_product = soup.find('div', {'id': 'detailBullets_feature_div'})
            raw_data = id_product.find_all('li')
            for data in raw_data:
                if 'ASIN' in data.find('span', {'class': 'a-text-bold'}).text:
                    return data.text.split('\n')[-1].strip()
        except AttributeError as e:
            if list_logs is not None:
                list_logs.append(create_log(e, get_id, position))
            return ''


def get_affiliate_url(soup: BeautifulSoup, list_logs: list[str] = None,
                      position: int = None) -> str:
    """Get Affiliate url"""
    try:
        affiliate_url = soup.find(
            'div', {'class': 'amzn-ss-text-textarea-container'})
        return affiliate_url.textarea.text.strip()
    except AttributeError as e:
        if list_logs is not None:
            list_logs.append(create_log(e, get_affiliate_url, position))
        return ''


def get_brand(soup: BeautifulSoup, list_logs: list[str] = None,
              position: int = None) -> str:
    """Get brand name"""
    try:
        brand_name = soup.find('div', {'id': 'bylineInfo_feature_div'})
        return sub('Visita la Store de|Marca:', '', brand_name.text).strip()
    except AttributeError as e:
        if list_logs is not None:
            list_logs.append(create_log(e, get_brand, position))
        return ''


def get_name(soup: BeautifulSoup, list_logs: list[str] = None,
             position: int = None) -> str:
    """Get product name"""
    try:
        name = soup.find('div', {'id': 'titleSection'})
        return name.text.strip()
    except AttributeError as e:
        if list_logs is not None:
            list_logs.append(create_log(e, get_name, position))
        return ''


# Metrics
def get_average_stars(soup: BeautifulSoup, list_logs: list[str] = None,
                      position: int = None) -> str:
    """Get the average star of the product"""
    try:
        stars = soup.find('span', {'id': 'acrPopover'})  # acrPopover
        return stars.text.strip()
    except AttributeError as e:
        if list_logs is not None:
            list_logs.append(create_log(e, get_average_stars, position))
        return '0 de 5 estrellas'


def get_average_reviews(soup: BeautifulSoup, list_logs: list[str] = None,
                        position: int = None) -> str:
    """Get the average reviews of the product"""
    try:
        reviews = soup.find(
            'span', {'id': 'acrCustomerReviewText'})
        return reviews.text.strip()
    except AttributeError as e:
        if list_logs is not None:
            list_logs.append(create_log(e, get_average_reviews, position))
        return '0 valoraciones'


# Price feature
def get_price(soup: BeautifulSoup, list_logs: list[str] = None,
              position: int = None) -> str:
    """Get product price"""
    try:
        try:
            price_product = soup.find('div', {'id': 'corePrice_feature_div'})
            price_to_day = price_product.find(
                'span', {'class': 'a-offscreen'})
            return price_to_day.text.strip()
        except AttributeError:
            try:
                price_product = soup.find('div', {'id': 'corePrice_desktop'})
                price_to_day = price_product.find(
                    'span', {'class': 'a-offscreen'})
                return price_to_day.text.strip()
            except AttributeError:
                price_product = soup.find(
                    'div', {'id': 'corePriceDisplay_desktop_feature_div'})
                price_to_day = price_product.find(
                    'span', {'class': 'a-offscreen'})
                return price_to_day.text.strip()
    except AttributeError:
        try:
            price_range = soup.find('span', {'class': 'a-price-range'})
            price_to_day = price_range.find_all(
                'span', {'class': 'a-offscreen'})
            return ' - '.join([current_price.text.strip()
                               for current_price in price_to_day])
        except AttributeError as e:
            if list_logs is not None:
                list_logs.append(create_log(e, get_price, position))
            return ''


def get_discount(soup: BeautifulSoup, list_logs: list[str] = None,
                 position: int = None) -> str:
    """Get discount product"""
    try:
        saving_price = soup.find(
            'div', {'id': 'corePriceDisplay_desktop_feature_div'})
        saving = saving_price.find(
            'span', {
                'class': 'a-size-large a-color-price '
                         'savingPriceOverride aok-align-center '
                         'reinventPriceSavingsPercentageMargin '
                         'savingsPercentage'})
        return saving.text.strip()
    except AttributeError as e:
        if list_logs is not None:
            list_logs.append(create_log(e, get_discount, position))
        return 'No hay ningún descuento aplicable'


def get_rrp_product(soup: BeautifulSoup, list_logs: list[str] = None,
                    position: int = None) -> str:
    """Get Recommended Retail Price product"""
    try:
        saving_price = soup.find(
            'div', {'id': 'corePriceDisplay_desktop_feature_div'})
        rrp = saving_price.find(
            'span', {
                'class': 'a-size-small a-color-secondary '
                         'aok-align-center basisPrice'})
        return rrp.span.span.text.strip()
    except AttributeError as e:
        if list_logs is not None:
            list_logs.append(create_log(e, get_rrp_product, position))
        return ''


def get_variation_material(soup: BeautifulSoup, list_logs: list[str] = None,
                           position: int = None) -> list:
    """Get different product materials"""
    try:
        variation_material = soup.find(
            'div', {'id': 'variation_material_type'})
        list_items = variation_material.find_all('li')
        return [material.text.strip() for material in list_items]
    except AttributeError as e:
        if list_logs is not None:
            list_logs.append(create_log(e, get_variation_material, position))
        return []


# Color feature
def get_current_color(soup: BeautifulSoup, list_logs: list[str] = None,
                      position: int = None) -> str:
    """Get current color"""
    try:
        try:
            color = soup.find('div', {'id': 'variation_color_name'})
            return color.span.text.strip()
        except AttributeError:
            color = soup.find('div', {'id': 'variation_color_name'})
            return color.div.span.text.strip()
    except AttributeError as e:
        if list_logs is not None:
            list_logs.append(create_log(e, get_current_color, position))
        return ''


def get_variation_colors(soup: BeautifulSoup, list_logs: list[str] = None,
                         position: int = None) -> list[str]:
    """Get different product colors"""
    try:
        variation_color = soup.find('div', {'id': 'variation_color_name'})
        colors = variation_color.find_all('li')
        return [color.get('title').replace('Haz clic para seleccionar ', '')
                .strip() for color in colors]
    except AttributeError as e:
        if list_logs is not None:
            list_logs.append(create_log(e, get_variation_colors, position))
        return []


def get_variation_color_image_links(soup: BeautifulSoup,
                                    list_logs: list[str] = None,
                                    position: int = None) -> list[str]:
    """Get different product color links"""
    try:

        image_links = soup.find_all(
            'div', {'class': 'twisterImageDivWrapper'})
        return [link.img.get('src').strip() for link in image_links]
    except AttributeError as e:
        if list_logs is not None:
            list_logs.append(
                create_log(e, get_variation_color_image_links, position))
        return []


def get_variation_colors_with_links(
        soup: BeautifulSoup, list_logs: list[str] = None,
        position: int = None) -> list[tuple[str, str]] or list[str]:
    colors = get_variation_colors(soup, list_logs, position)
    links = get_variation_color_image_links(soup, list_logs, position)
    if len(colors) > 0 and len(links) > 0:
        return list(zip(colors, links))
    elif len(colors) > 0 and len(links) == 0:
        return colors
    else:
        return []


def get_variation_size(soup: BeautifulSoup, list_logs: list[str] = None,
                       position: int = None) -> list[str]:
    """Get different product sizes"""
    try:
        variation_size = soup.find('div', {'id': 'variation_size_name'})
        list_items = variation_size.find_all('option')
        return [size.text.strip() for size in list_items][1:]
    except AttributeError as e:
        if list_logs is not None:
            list_logs.append(create_log(e, get_variation_size, position))
        return []


def is_availability(soup: BeautifulSoup, list_logs: list[str] = None,
                    position: int = None) -> str:
    """Product availability"""
    try:
        not_availability_feature = soup.find(
            'div', {'id': 'availability_feature_div'})
        if len(not_availability_feature.text.strip()) < 1:
            return 'Disponible'
        return not_availability_feature.text.replace('.', '').strip()
    except AttributeError as e:
        if list_logs is not None:
            list_logs.append(create_log(e, is_availability, position))
        return 'Disponible'


def get_feature_bullets(soup: BeautifulSoup, list_logs: list[str] = None,
                        position: int = None) -> list[str]:
    """Get feature bullets"""
    try:
        feature_bullets = soup.find('div', {'id': 'feature-bullets'})
        list_items = feature_bullets.find_all('li')
        return [features.text.strip() for features in list_items]
    except AttributeError as e:
        if list_logs is not None:
            list_logs.append(create_log(e, get_feature_bullets, position))
        return []


def get_image_links(soup, list_logs: list[str] = None,
                    position: int = None) -> list[str]:
    """Get image links"""
    try:
        links = []
        raw_scripts = soup.find_all('script', {'type': 'text/javascript'})
        for script in raw_scripts:
            if 'ImageBlockATF' in script.text:
                str_script = str(script)
                links = findall(r'"hiRes":"([+\w\s:./-]+)"', str_script)
                if len(links) < 1:
                    links = findall(r'"large":"([+\w\s:./-]+)"', str_script)
        return links
    except AttributeError as e:
        if list_logs is not None:
            list_logs.append(create_log(e, get_image_links, position))
        return []
