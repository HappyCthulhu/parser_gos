from export import Export
from logger_settings import logger
from pages.purchase import PurchasePage

links = [
    'https://zakupki.gov.ru/epz/order/notice/ea20/view/common-info.html?regNumber=0348500001022000008',
    'https://zakupki.gov.ru/epz/order/notice/ea20/view/common-info.html?regNumber=0184200000622000006',
    'https://zakupki.gov.ru/epz/order/notice/ea20/view/common-info.html?regNumber=0174500001122000025',
    'https://zakupki.gov.ru/epz/order/notice/ea20/view/common-info.html?regNumber=0301000000222000038',
    'https://zakupki.gov.ru/epz/order/notice/ea20/view/common-info.html?regNumber=0372200105022000161',
    'https://zakupki.gov.ru/epz/order/notice/ea20/view/common-info.html?regNumber=0338300031922000012',
    'https://zakupki.gov.ru/epz/order/notice/ea20/view/common-info.html?regNumber=0820500000822003283',
    'https://zakupki.gov.ru/epz/order/notice/ea20/view/common-info.html?regNumber=0119200000122005870',
    # 'https://zakupki.gov.ru/epz/order/notice/ea20/view/common-info.html?regNumber=0373100056022000009',  doc-files
    # 'https://zakupki.gov.ru/epz/order/notice/ea20/view/common-info.html?regNumber=0329100015222000005',  doc-files
    'https://zakupki.gov.ru/epz/order/notice/ea20/view/common-info.html?regNumber=0318200077422000010',
    'https://zakupki.gov.ru/epz/order/notice/ea20/view/common-info.html?regNumber=0373200586422000006',
    'https://zakupki.gov.ru/epz/order/notice/ea20/view/common-info.html?regNumber=0318200068522000002',
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
