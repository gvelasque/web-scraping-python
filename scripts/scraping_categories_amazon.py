from scraper.constants import DOMAIN_AMAZON
from scraper.db.manage_db import create_term, create_term_taxonomy
from scraper.loader.load_url import load_url
from scraper.manage_files.manage_csv import create_csv_file
from scraper.manage_files.manage_json import create_json_file
from scraper.manage_files.manage_lists import create_list_file
from scraper.manage_files.manage_logs import create_log, create_logfile
from scraper.scraping.scraping_setup import soup_page
from scraper.scraping.categories.elements_categories import categories_page

output_logs, slugs, terms, terms_taxonomies = [], [], [], []


def extract_recursive(path: str, list_logs: list[str], max_level: int,
                      category_id: int = 1, level: int = None, driver=None,
                      last_category_id: int = None,
                      parent_category: str = None,
                      parent_categories: list = None) -> tuple:
    """TODO: docstring"""

    if last_category_id is None:
        last_category_id = 0
    else:
        last_category_id = category_id

    if level is None:
        level = 1
    else:
        level += 1

    if driver is None:
        driver = load_url(DOMAIN_AMAZON, path, driver=driver,
                          list_logs=list_logs)
    else:
        load_url(DOMAIN_AMAZON, path, driver=driver, list_logs=list_logs)

    categories = categories_page(soup_page(driver, list_logs), list_logs)

    if parent_categories is None:
        parent_categories = {}

    if level == 1 or level == 2:
        parent_categories = categories.keys()

    if level == 3:
        actual_list = [parent_category] + list(categories.keys())
        parent_list = list(parent_categories)
        if sorted(actual_list) == sorted(parent_list):
            return [], category_id

    return_list = []
    for category, url_category in categories.items():
        category_id += 1

        terms.append(
            create_term(category_id, category,
                        f"{str(last_category_id) + category}", slugs))

        terms_taxonomies.append(
            create_term_taxonomy(term_id=category_id,
                                 parent_id=last_category_id,
                                 taxonomy='product_cat'))

        print(f"{level}, term_id: {category_id}, "
              f"category: {category}, parent: {last_category_id}")

        try:
            if level < max_level:
                list_upper_level, category_id = extract_recursive(
                    url_category, list_logs, max_level=max_level,
                    level=level, driver=driver,
                    category_id=category_id,
                    last_category_id=last_category_id,
                    parent_category=category,
                    parent_categories=parent_categories)

                if len(list_upper_level) > 0:
                    return_list.append(
                        {category: {'url': url_category,
                                    'subcategories': list_upper_level}})
                else:
                    return_list.append(
                        {category: {'url': url_category}})
            elif level == max_level:
                return_list.append(
                    {category: {'url': url_category}})
        except Exception as e:
            list_logs.append(create_log(e, extract_recursive, level))
    return return_list, category_id


dataset, last_id = extract_recursive(
    "/gp/bestsellers/apparel/ref=zg_bs_nav_0", output_logs, max_level=3)

create_json_file("/".join(["static", "categories"]),
                 "_".join(["categories", "bestsellers"]), dataset)

create_csv_file("/".join(["static", "database"]),
                "_".join(["terms", "categories"]), terms)

create_csv_file("/".join(["static", "database"]),
                "_".join(["terms", "taxonomy", "categories"]),
                terms_taxonomies)

create_logfile("/".join(["static", "logs"]),
               "_".join(["logs", "scraping", "categories"]), output_logs)

create_list_file("/".join(["static", "lists"]),
                 "_".join(["list", "slugs", "categories"]), slugs)
