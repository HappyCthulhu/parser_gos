from export import Export
from logger_settings import logger
from pages.purchase import PurchasePage

links = [
    'https://zakupki.gov.ru/epz/order/notice/ea20/view/common-info.html?regNumber=0321300007522000017'
]

export = Export()
for purchases_count, link in enumerate(links):
    status = ''
    purchase_page = PurchasePage(link, status)
    purchase_page.get_page_elements()

    # logger.info(f'Страниц обработано: {purchases_count}/{len(page_numbers) * records_per_page}')

    if purchase_page.purchase_number is not None:
        export.dump_data(purchase_page, purchases_count)

logger.info('Парсинг закончен')
