import os.path
import re
import time

from scraper.constants import BASE_DIR_POSIX
from scraper.manage_files.manage_csv import create_csv_file
from scraper.manage_files.manage_json import load_json_file
from scraper.manage_files.manage_lists import create_list_file, open_list_file
from scraper.manage_files.manage_logs import create_logfile, create_log
from scraper.scraping.categories.scraping_collection_category \
    import extract_collection_category
from scraper.scraping.product.scraping_product import scraping_product


def collection_product_dataset(collection_path, term_id, directory,
                               driver=None, count_product=0):
    # collection_dataset = []
    collection_products = []
    collection_log_list = []

    """if driver is None:
        driver = load_signin_amazon(
            SIGNIN_PATH_AMAZON, collection_log_list, driver)
    time.sleep(0.3)"""

    urls_collection, driver = extract_collection_category(
        collection_path, driver=driver, list_logs=collection_log_list)

    if len(collection_products) < 1:
        collection_products.append([
            'ID', 'Tipo', 'SKU', 'Nombre', 'Publicado', '¿Está destacado?',
            'Visibilidad en el catálogo', 'Descripción corta', 'Descripción',
            'Día en que empieza el precio rebajado',
            'Día en que termina el precio rebajado', 'Estado del impuesto',
            'Clase de impuesto', '¿En inventario?', 'Inventario',
            'Cantidad de bajo inventario',
            '¿Permitir reservas de productos agotados?',
            '¿Vendido individualmente?', 'Peso (kg)', 'Longitud (cm)',
            'Anchura (cm)', 'Altura (cm)',
            '¿Permitir valoraciones de clientes?', 'Nota de compra',
            'Precio rebajado', 'Precio normal', 'Categorías', 'Etiquetas',
            'Clase de envío', 'Imágenes', 'Límite de descargas',
            'Días de caducidad de la descarga', 'Superior',
            'Productos agrupados', 'Ventas dirigidas', 'Ventas cruzadas',
            'URL externa', 'Texto del botón', 'Posición',
            'Swatches Attributes', 'Nombre del atributo 1',
            'Valor(es) del atributo 1', 'Atributo visible 1',
            'Atributo global 1', 'Nombre del atributo 2',
            'Valor(es) del atributo 2', 'Atributo visible 2',
            'Atributo global 2'])

    for index, url_product in enumerate(urls_collection):
        tic_p = time.perf_counter()
        print("Starting scraping product")

        dataset_products, driver = scraping_product(
            product_id=term_id, path=url_product, directory=directory,
            list_logs=collection_log_list, location=index, driver=driver)

        if dataset_products is None:
            print("Dataset is None")
            continue

        term_id += 1

        """if dataset is None:
            print(url_product)
            continue
        collection_dataset.append(dataset)"""
        collection_products.append(dataset_products)

        toc_p = time.perf_counter()
        print(f"Finish scraping product, downloaded "
              f"in {toc_p - tic_p:0.4f} seconds")
        if count_product == 1:
            break
        count_product += 1
    return collection_products, collection_log_list, term_id, driver, count_product


def get_subcategories(list_categories, list_to_populate,
                      directory, level=0, list_logs: list[str] = None):
    # TODO: docstring
    level += 1
    for category_dict in list_categories:
        for name_category, data_list in category_dict.items():
            name_category = "_".join(name_category.lower().split())
            if level != 4:
                directory += f"{name_category}/"
            list_to_populate.append(
                (level, name_category, directory, data_list['url']))
            try:
                if 'subcategories' in data_list.keys():
                    get_subcategories(
                        data_list['subcategories'], list_to_populate,
                        directory, level, list_logs=list_logs)
            except AttributeError as e:
                if list_logs is not None:
                    list_logs.append(create_log(e, get_subcategories))
                continue
            directory = re.sub(rf"{name_category}/[\s\w/_]*", "", directory)
    level -= 1
    return list_to_populate


def get_all_categories(path, list_logs: list[str] = None):
    new_list_categories = []
    get_subcategories(
        load_json_file(path, list_logs), new_list_categories, directory='/')
    return new_list_categories


l_list = []

all_categories = get_all_categories(
    'static/categories/categories_bestsellers.json', l_list)

browser = None
count = 0
product_id = int(open_list_file('static/lists/product_id.txt', l_list)[0])
for r_level, category, dir_category, url in all_categories:
    tic_c = time.perf_counter()
    print("Starting scraping collection")

    absolute_path = f"{BASE_DIR_POSIX}/static/products" \
                    f"{dir_category}{category}.csv"

    products, logs = [], []
    if not os.path.exists(absolute_path):
        products, logs, product_id, browser, count = \
            collection_product_dataset(url, product_id, dir_category, browser,
                                       count)
    else:
        print("The file exists: ", absolute_path)
        continue

    """create_json_file(
        dataset_json, f"static/products/{dir_category}", category, l_list)"""

    create_csv_file(f"static/products/{dir_category}", category, products,
                    l_list)

    create_list_file('static/lists/', 'product_id', [str(product_id)], l_list)

    create_logfile(f"static/logs/products/{dir_category}", category, logs)

    toc_c = time.perf_counter()
    print(f"Finish scraping collection. Downloaded the collection in "
          f"{toc_c - tic_c:0.4f} seconds")
    if count == 1:
        break
    count += 1
