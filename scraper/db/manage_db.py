import os
import shutil
from re import sub

import requests
from unidecode import unidecode

from scraper.constants import BASE_DIR_POSIX

stopwords = ['de', 'para', 'ropa', 'y', 'al', 'la', '/', 'sin']


def create_slug(slug: str, list_slugs: list[str], term_id: int = None) -> str:
    """TODO: docstring"""
    if term_id is None:
        term_id = 1
        while slug in list_slugs:
            term_id += 1
            slug = f"{slug}-{str(term_id)}"
    elif slug in list_slugs:
        slug = f"{slug}-{str(term_id)}"
    return slug


def create_term(term_id: int, name: str, name2: str, list_slugs: list[str],
                term_group: int = 0) -> list:
    """TODO: docstring"""
    raw_slug = unidecode(sub(r"[,\s]+", "-", name)).lower()
    raw_slug = "-".join(
        [word for word in raw_slug.split('-') if word not in stopwords])
    slug = create_slug(raw_slug, list_slugs, term_id)
    list_slugs.append(slug)
    return [term_id, name2, slug, term_group]


def create_term_taxonomy(term_id: int, parent_id: int, taxonomy: str,
                         term_taxonomy_id: int = None,
                         description: str = None, count: int = None) -> list:
    """TODO: docstring"""
    if term_taxonomy_id is None:
        term_taxonomy_id = term_id
    if description is None:
        description = ""
    if count is None:
        count = 0
    return [term_taxonomy_id, term_id, taxonomy, description, parent_id, count]


def short_description_product(brand: str):
    """TODO: docstring"""
    short = ""
    if len(brand) > 0:
        short = f'\n<h2 class="entry-title" ' \
                f'style="font-size:1.2rem;">{brand}</h2>'

    """if len(average_stars) > 0:
        average_stars = float(average_stars.replace(
            ' de 5 estrellas', '').replace(',', '.'))
        short += f"<div class=\"star-rating\" role=\"img\" " \
                 f"aria-label=\"Valorado en {average_stars:.2f} de 5\">\n" \
                 f"<span style=\"width:{average_stars * 20}%;\"></span>\n" \
                 f"</div>\n"""

    """if len(title) > 0:
        short += f'\n<p>{title}</p>'"""

    """if len(average_reviews) > 0:
        short += f'\n<div class="entry-title" style="font-size:0.8rem;">' \
                 f'{average_reviews} en Amazon</div>'"""

    return short


def short_description_product2(title: str, brand: str, colors: list[str],
                               sizes: list[str], average_reviews):
    """TODO: docstring"""
    short = ""
    if len(brand) > 0:
        short = f'\n<h2 class="entry-title" ' \
                f'style="font-size:1.2rem;">{brand}</h2>'

    if len(title) > 0:
        short += f'\n<p>{title}</p>'

    if len(colors) > 0 or len(sizes) > 0:
        short += '\n<div class="variations_form cart swatches-support ' \
                 'wvs-loaded">' \
                 '\n<table class="variations">' \
                 '\n<tbody>'
        if len(colors) > 0:
            short += '\n<tr>' \
                     '\n<th class="label"><label>Colors</label></th>' \
                     '\n<td class="value woo-variation-items-wrapper">' \
                     '\n<ul class="variable-items-wrapper ' \
                     'button-variable-items-wrapper wvs-style-squared">'
            for color in colors:
                short += f'\n 	<li class="variable-item ' \
                         f'button-variable-item">' \
                         f'\n<span class="variable-item-span ' \
                         f'variable-item-span-button">{color}</span></li>'
        if len(sizes) > 0:
            short += '\n<tr>' \
                     '\n<th class="label"><label>Colors</label></th>' \
                     '\n<td class="value woo-variation-items-wrapper">' \
                     '\n<ul class="variable-items-wrapper ' \
                     'button-variable-items-wrapper wvs-style-squared">'
            for size in sizes:
                short += f'\n 	<li class="variable-item ' \
                         f'button-variable-item">' \
                         f'\n<span class="variable-item-span ' \
                         f'variable-item-span-button">{size}</span></li>'
            short += '\n</ul>' \
                     '\n</td>' \
                     '\n</tr>'
        short += '\n</tbody>' \
                 '\n</table>'

    """if len(average_reviews) > 0:
        short += f'\n<div class="entry-title" style="font-size:0.8rem;">' \
                 f'{average_reviews} en Amazon</div>'"""

    return short


def description_product(paragraphe: list[str]) -> str:
    """TODO: docstring"""
    html_description = ""
    if len(paragraphe) > 0:
        html_description += "<ul class=\"\"a-unordered-list " \
                            "a-vertical a-spacing-mini\"\">"
        for li in paragraphe:
            html_description += f"<li><span class=\"a-list-item\">{li}" \
                                f"</span></li>"
        html_description += "</ul>"

    return html_description


def generate_tags_product(title: str, brand: str) -> list[str]:
    """TODO: docstring"""
    list_tags = []
    raw_title = ""
    if len(brand) > 0:
        raw_title = sub(brand.lower(), "", title.lower())
    list_words = raw_title.split()
    for word in list_words:
        if word not in stopwords and len(word) > 3:
            list_tags.append(word)
    return list_tags[:6] if len(list_tags) > 6 else list_tags


def save_image(product_id, path, directory, counter):
    """TODO: docstring"""
    absolute_path = "/".join(
        [BASE_DIR_POSIX, 'static', 'img', 'product', directory,
         str(product_id)])

    if not os.path.exists(absolute_path):
        os.makedirs(absolute_path)
    if os.path.exists(f"{absolute_path}/{product_id}_{counter}.jpg"):
        print("File exist.")
        return

    response = requests.get(path, stream=True)
    if response.status_code == 200:

        with open(f"{absolute_path}/{product_id}_{counter}.jpg",
                  'wb') as infile:
            shutil.copyfileobj(response.raw, infile)
    else:
        print('Image Couldn\'t be retrieved')


def swatches_attributes(colors: list[str], sizes: list[str]) -> dict:
    """TODO: docstring"""
    temp_dict, dict_colors, dict_sizes = {}, {}, {}
    if len(colors) > 0:
        for color in colors:
            temp_dict[color] = {
                "name": color, "color": "",
                "image": "",
                "show_tooltip": "",
                "tooltip_text": "",
                "tooltip_image": "",
                "image_size": ""
            }
        dict_colors = {"name": "Color", "type": "button", "terms": temp_dict}

    if len(sizes) > 0:
        for size in sizes:
            temp_dict[size] = {
                "name": size, "color": "",
                "image": "",
                "show_tooltip": "",
                "tooltip_text": "",
                "tooltip_image": "",
                "image_size": ""
            }
        dict_sizes = {"name": "Talla", "type": "button", "terms": temp_dict}

    if len(colors) > 0 and len(sizes) > 0:
        return {"Color": dict_colors, "Talla": dict_sizes}
    elif len(colors) > 0:
        return {"Color": dict_colors}
    elif len(sizes) > 0:
        return {"Color": dict_sizes}


def create_term_product(term_id: int, name: str, sku: str, descr: str,
                        short_descr: str, categories: str,
                        tags: list[str], swatches: dict,
                        list_colors: list[str], list_sizes: list[str],
                        images: list = ''):
    """TODO: docstring"""
    term_type: str = 'external'
    published: str = "1"
    featured: str = str(0)
    visibility: str = 'visible'
    day_price_sale_start: str = ''
    day_price_sale_end: str = ''
    status_tax: str = 'taxable'
    class_stock: str = ''
    in_inventory: str = str(1)
    inventory: str = ''
    low_inventory_quantity: str = ''
    reservations_sold_out: str = str(0)
    sold_individually: str = str(0)
    weight: str = ''
    length: str = ''
    width: str = ''
    height: str = ''
    customer_reviews: str = str(0)
    purchase_note: str = ''
    reduced_price: str = ''
    normal_price: str = ''
    if len(tags) > 0:
        tags: str = ", ".join(tags).title()
    shipping_lass: str = ''
    if len(images) > 0:
        images: str = ", ".join(images)
    else:
        images: str = ""
    limit_download: str = str(0)
    download_expiration_days: str = ''
    higher: str = ''
    bundled_products: str = ''
    directed_sales: str = ''
    cross_selling: str = ''
    external_url: str = ''
    button_text: str = 'Ver en Amazon'
    position: str = str(0)
    attribute_name_1: str = 'Color'
    if len(list_colors) > 0:
        attribute_value_1: str = ", ".join(list_colors)
    else:
        attribute_value_1: str = ""
    visible_attribute_1: str = str(1)
    global_attribute_1: str = str(1)
    attribute_name_2: str = 'Talla'
    if len(list_sizes) > 0:
        attribute_value_2: str = ", ".join(list_sizes)
    else:
        attribute_value_2: str = ""
    visible_attribute_2: str = str(1)
    global_attribute_2: str = str(1)

    to_join = []
    categories = categories.replace('_', ' ')
    for element in categories.split('/'):
        if len(element) > 1:
            to_join.append(element.capitalize())
    categories = " > ".join(to_join)

    return [str(term_id), term_type, sku, name, published, featured,
            visibility, short_descr, descr, day_price_sale_start,
            day_price_sale_end, status_tax, class_stock, in_inventory,
            inventory, low_inventory_quantity, reservations_sold_out,
            sold_individually, weight, length, width, height, customer_reviews,
            purchase_note, reduced_price, normal_price, categories, tags,
            shipping_lass, images, limit_download, download_expiration_days,
            higher, bundled_products, directed_sales, cross_selling,
            external_url, button_text, position, swatches, attribute_name_1,
            attribute_value_1, visible_attribute_1, global_attribute_1,
            attribute_name_2, attribute_value_2, visible_attribute_2,
            global_attribute_2]
