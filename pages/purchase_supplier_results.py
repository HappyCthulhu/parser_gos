from locators import PurchasePageLocators, PurchaseSupplierResultsLocators
from pages.base_page import BasePage


class PurchaseSupplierResults(BasePage):
    def __init__(self, link_to_purchase_common_info):

        self.order_num = link_to_purchase_common_info.split('=')[1]
        # получение вкладки "РЕЗУЛЬТАТЫ ОПРЕДЕЛЕНИЯ ПОСТАВЩИКА"
        self.tree = self.get_tree(
            'https://zakupki.gov.ru/epz/order/notice/rpec/search-results.html',
            {'orderNum': self.order_num}
        )

        self.contract_blocks = self.get_contracts_info()

    def get_contracts_blocks(self):
        return self.tree.xpath(
            PurchasePageLocators.blocks_information_about_the_conclusion_of_the_contract)

    def get_supplier(self, tree):
        if not self.check_element_existing(PurchaseSupplierResultsLocators.supplier, tree):
            return ''
        else:
            return tree.xpath(PurchaseSupplierResultsLocators.supplier)[0].lstrip().rstrip()

    def get_contract_price(self, tree):
        if not self.check_element_existing(PurchaseSupplierResultsLocators.contract_price, tree):
            return ''
        else:
            return tree.xpath(PurchaseSupplierResultsLocators.contract_price)[0].lstrip().rstrip()

    def get_customer(self, tree):
        if not self.check_element_existing(PurchaseSupplierResultsLocators.customer, tree):
            return ''
        else:
            return tree.xpath(PurchaseSupplierResultsLocators.customer)[0].lstrip().rstrip()


    def check_status(self, tree):
        if not self.check_element_existing(PurchaseSupplierResultsLocators.contract_price, tree):
            return False
        else:
            status = tree.xpath(PurchaseSupplierResultsLocators.status)[0].lstrip().rstrip()

            if status == 'Контракт заключен' or status == 'Подписание поставщиком' or status == 'Подписание заказчиком':
                return True
            else:
                return False

    def get_contracts_info(self):
        contracts_blocks = self.get_contracts_blocks()
        contracts = []

        if len(contracts_blocks) != 0:

            for block in contracts_blocks:
                conclution_block_tree = self.from_lxml_to_html_to_lxml(block)
                if self.check_status(conclution_block_tree):
                    supplier = self.get_supplier(conclution_block_tree)
                    contract_price = self.get_contract_price(conclution_block_tree)
                    customer = self.get_customer(conclution_block_tree)
                # else:
                    # TODO: понять, каким образом экспорт чекает на наличие инфы. Что происходит, когда контракт не найден?
                    # TODO: продумать более прозрачную лоигку поиска контрактов. А то сейчас у меня в purchase_supplier_results это оказывается в результате...
                    # provider = ''
                    # contract_price = ''

                    contracts.append(
                        {
                            'supplier': supplier,
                            'contract_price': contract_price,
                            'customer': customer
                        }
                    )
        return contracts
