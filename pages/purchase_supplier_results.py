import requests
from lxml import html

from locators import PurchasePageLocators
from logger_settings import logger


class PurchaseSupplierResults:
    def __init__(self, link_to_purchase_common_info):

        order_num = link_to_purchase_common_info.split('=')[1]
        self.tree = self.get_tree(order_num)
        self.contracts_blocks = self.get_contracts_blocks()
        self.contract_blocks = self.get_contracts_info()

    def get_tree(self, order_num):
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        }

        params = {
            'orderNum': order_num,
        }

        response = requests.get('https://zakupki.gov.ru/epz/order/notice/rpec/search-results.html', params=params, headers=headers)

        if response.status_code != 200:
            logger.critical(f'Статус страницы закупки: {response.status_code}')

        return html.document_fromstring(response.text)

    def check_element_existing(self, xpath):
        if len(self.tree.xpath(xpath)) == 0:
            return False
        else:
            return True

    def get_contracts_blocks(self):
        return self.tree.xpath(
            PurchasePageLocators.blocks_information_about_the_conclusion_of_the_contract)

    # TODO: мб в одну функцию объединить с get_ktru_block()?
    def get_contract_block_tree(self, block):
        #  TODO: функция, которая html возвращает
        block_html = html.tostring(block)
        block_tree = html.document_fromstring(block_html)
        return block_tree

    def get_provider(self):
        if not self.check_element_existing(PurchasePageLocators.provider):
            return ''
        else:
            return self.tree.xpath(PurchasePageLocators.provider)[0].lstrip().rstrip()

    def get_contract_price(self):
        if not self.check_element_existing(PurchasePageLocators.contract_price):
            return ''
        else:
            return self.tree.xpath(PurchasePageLocators.contract_price)[0].lstrip().rstrip()

    def get_contracts_info(self):
        # https://zakupki.gov.ru/epz/order/notice/ea20/view/supplier-results.html?regNumber=0380200000122002530
        contract_blocks = []

        if len(self.contracts_blocks) != 0:

            for block in self.contracts_blocks:
                self.conclution_block_tree = self.get_contract_block_tree(block)
                provider = self.get_provider()
                contract_price = self.get_contract_price()

                contract_blocks.append(
                    {
                        'provider': provider,
                        'contract_price': contract_price
                    }
                )

        return contract_blocks
