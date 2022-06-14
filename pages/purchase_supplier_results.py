from locators import PurchasePageLocators
from pages.base_page import BasePage


class PurchaseSupplierResults(BasePage):
    def __init__(self, link_to_purchase_common_info):

        order_num = link_to_purchase_common_info.split('=')[1]
        self.tree = self.get_tree(
            'https://zakupki.gov.ru/epz/order/notice/rpec/search-results.html',
            {'orderNum': order_num}
        )
        contracts_blocks = self.get_contracts_blocks()
        self.contract_blocks = self.get_contracts_info(contracts_blocks)

    def check_element_existing(self, xpath):
        if len(self.tree.xpath(xpath)) == 0:
            return False
        else:
            return True

    def get_contracts_blocks(self):
        return self.tree.xpath(
            PurchasePageLocators.blocks_information_about_the_conclusion_of_the_contract)

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

    def get_contracts_info(self, contracts_blocks):
        # https://zakupki.gov.ru/epz/order/notice/ea20/view/supplier-results.html?regNumber=0380200000122002530
        contract_blocks = []

        if len(contracts_blocks) != 0:

            for block in contracts_blocks:
                self.conclution_block_tree = self.from_lxml_to_html_to_lxml(block)
                provider = self.get_provider()
                contract_price = self.get_contract_price()

                contract_blocks.append(
                    {
                        'provider': provider,
                        'contract_price': contract_price
                    }
                )

        return contract_blocks
