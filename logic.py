# import time

from export import Export
from logger_settings import logger
from pages.purchase import PurchasePage
from pages.purchase_search_page import PurchaseSearchPage


def start_parse(search_params):
    main_purchase_search_page_link = 'https://zakupki.gov.ru/epz/order/extendedsearch/results.html'
    records_per_page = 500
    search_params["records_per_page"] = 500

    search_page = PurchaseSearchPage(main_purchase_search_page_link, search_params)
    number_of_pages = search_page.find_number_of_pages()
    page_numbers = [number + 1 for number in range(number_of_pages)]

    # TODO: когда меняю количество заказок на страницу на 500, он неправильно считает количество страниц
    logger.info(f'Количество страниц: {number_of_pages}')
    logger.info(f'Закупок на одну страницу: {records_per_page}')

    export = Export()

    # speed = []

    for page_number in page_numbers:
        search_params['page_number'] = page_number
        search_params['records_per_page'] = records_per_page
        search_page = PurchaseSearchPage(main_purchase_search_page_link, search_params)

        for count, purchase in enumerate(search_page.purchases):
            # start = time.time()

            # берем номер страницы умножаем на 10, чтоб получить количество покупок. Вычитаем 10, ибо номер страницы начинается с 1. Прибавляем 1, ведь enumerate начинает с 0

            purchases_count = count + (page_number * records_per_page - records_per_page + 1)
            status = search_page.get_status(purchase)
            link = search_page.get_link_to_purchases(purchase)
            purchase_page = PurchasePage(link, status)
            purchase_page.get_page_elements()

            logger.info(f'Страниц обработано: {purchases_count}/{len(page_numbers) * records_per_page}')

            if purchase_page.purchase_number is not None:
                export.dump_data(purchase_page, purchases_count)

            # finish = time.time()
            # time_spent_current_purchase = (finish - start) / purchases_count
            # speed.append(time_spent_current_purchase)
            # average_time = sum(map(float, speed))/len(speed)
            # average_time = average_time
            # logger.info('Время на одну закупку: {}'.format(average_time))

    logger.info('Парсинг закончен')
