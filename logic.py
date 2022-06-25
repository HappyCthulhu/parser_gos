from export import Export
from logger_settings import logger
from pages.purchase import PurchasePage
from pages.purchase_search_page import PurchaseSearchPage

# TODO: добавить user-agent?

def start_parse(search_params):
    main_purchase_search_page_link = 'https://zakupki.gov.ru/epz/order/extendedsearch/results.html'

    search_page = PurchaseSearchPage(main_purchase_search_page_link, search_params)
    number_of_pages = search_page.find_number_of_pages()
    page_numbers = [number + 1 for number in range(number_of_pages)]

    purchases_count = 0
    # TODO: когда меняю количество заказок на страницу на 500, он неправильно считает количество страниц
    records_per_page = 10
    logger.info(f'Количество страниц: {number_of_pages}')
    logger.info(f'Закупок на одну страницу: {records_per_page}')

    export = Export()

    for page_number in page_numbers:

        search_params['page_number'] = page_number
        search_params['records_per_page'] = records_per_page
        search_page = PurchaseSearchPage(main_purchase_search_page_link, search_params)

        for purchase in search_page.purchases:
            status = search_page.get_status(purchase)
            link = search_page.get_link_to_purchases(purchase)
            purchase_page = PurchasePage(link, status)
            purchase_page.get_page_elements()

            purchases_count += 1
            logger.info(f'Страниц обработано: {purchases_count}/{len(page_numbers) * records_per_page}')

            export.dump_data(purchase_page, purchases_count)

    logger.info('Парсинг закончен')