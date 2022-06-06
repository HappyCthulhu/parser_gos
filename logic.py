import sys

from progress.bar import Bar

from logger_settings import logger
from pages.purchase import PurchasePage
from pages.purchase_search_page import PurchaseSearchPage

if __name__ == '__main__':

    required_statuses = ['Закупка завершена', 'Подача заявок', 'Работа комиссии']

    purchase_search_page_link = 'https://zakupki.gov.ru/epz/order/extendedsearch/results.html'
    main_page = PurchaseSearchPage(purchase_search_page_link)
    number_of_pages = main_page.find_number_of_pages()
    page_numbers = [number + 1 for number in range(number_of_pages)]

    purchases_count = 0
    number_of_purchases_per_page = 10
    logger.info(f'Количество страниц: {number_of_pages}')
    logger.info(f'Закупок на одну страницу: {number_of_purchases_per_page}')

    bar = Bar('Страниц обработано:', max=len(page_numbers) * number_of_purchases_per_page)
    for page_number in page_numbers:

        purchase_search_page_link = f'{purchase_search_page_link}?pageNumber={page_number}&recordsPerPage=_{number_of_purchases_per_page}'
        main_page = PurchaseSearchPage(purchase_search_page_link)

        if main_page.response.status_code != 200:
            logger.critical(f'Статус код: {main_page.response.status_code}')
            logger.debug(main_page.response.text)
            sys.exit()

        for purchase in main_page.purchases:

            status = main_page.get_status(purchase)

            if status not in required_statuses:
                logger.debug(f'Этот статус не совпадает с нужными нам: {status}')
                continue

            link = main_page.get_link_to_purchases(purchase)
            page = PurchasePage(link)
            page.parse_page()
            purchases_count += 1
            bar.next()
    bar.finish()
