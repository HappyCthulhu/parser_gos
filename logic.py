import sys

from progress.bar import Bar

from export import Export
from logger_settings import logger
from pages.purchase import PurchasePage
from pages.purchase_search_page import PurchaseSearchPage

if __name__ == '__main__':

    required_statuses = ['Закупка завершена', 'Подача заявок', 'Работа комиссии']
    main_purchase_search_page_link = 'https://zakupki.gov.ru/epz/order/extendedsearch/results.html'

    main_page = PurchaseSearchPage(main_purchase_search_page_link)
    number_of_pages = main_page.find_number_of_pages()
    page_numbers = [number + 1 for number in range(number_of_pages)]

    purchases_count = 0
    number_of_purchases_per_page = 10
    logger.info(f'Количество страниц: {number_of_pages}')
    logger.info(f'Закупок на одну страницу: {number_of_purchases_per_page}')

    export = Export()

    bar = Bar('Страниц обработано:', max=len(page_numbers) * number_of_purchases_per_page)
    for page_number in page_numbers:

        purchase_search_page_link = f'{main_purchase_search_page_link}?pageNumber={page_number}&recordsPerPage=_{number_of_purchases_per_page}'
        main_page = PurchaseSearchPage(purchase_search_page_link)


        for purchase in main_page.purchases:
            status = main_page.get_status(purchase)
            link = main_page.get_link_to_purchases(purchase)
            purchase_page = PurchasePage(link, status)
            purchase_page.get_page_elements()

            purchases_count += 1

            export.dump_data(purchase_page, purchases_count)

            bar.next()
    bar.finish()
    logger.info('Парсинг закончен')
