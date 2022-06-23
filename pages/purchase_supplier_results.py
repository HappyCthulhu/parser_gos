import requests

from locators import PurchasePageLocators
from pages.base_page import BasePage


class PurchaseSupplierResults(BasePage):
    def __init__(self, link_to_purchase_common_info):

        self.order_num = link_to_purchase_common_info.split('=')[1]
        self.tree = self.get_tree(
            'https://zakupki.gov.ru/epz/order/notice/rpec/search-results.html',
            {'orderNum': self.order_num}
        )

        contracts_blocks = self.get_contracts_blocks() # TODO: мб вынести это в получение контрактов?
        self.contract_blocks = self.get_contracts_info(contracts_blocks)
        self.contact_doc_info = self.get_doc_info()
        # проверить наличие блока "Информация о процедуре заключения контракта": information_about_the_contract_closing_procedure
        # получить regNumber
        # отправить запрос на получение div со ссылкой на контракт
        # скачать файл
        # спарсить фаел
        #

    def get_doc_block_tree(self, draft_id):
        tree = self.get_tree(
            'https://zakupki.gov.ru/epz/order/notice/rpec/documents-results.html',
            {'orderNum': self.order_num,
             'draftId': draft_id # без этого параметра возвращается 404
             }
        )
        return tree


    def get_draft_id(self):
        draft_id = self.tree.xpath(PurchasePageLocators.data_id_draft_id)[0]
        return draft_id


    def download_doc(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        }
        response = requests.get(url, allow_redirects=True, headers=headers)

        # TODO: нужно ли в принципе сохранять файл? Если да, нужно удалить потом
        with open("doc.doc", "wb") as file:
            file.write(response.content)

    def get_doc_info(self):
        # TODO: возможно в будущем окажется, что может быть несколько документов. Нужно будет перепилить
        draft_id = self.get_draft_id()
        doc_block_tree = self.get_doc_block_tree(draft_id)
        doc_link = doc_block_tree.xpath(PurchasePageLocators.a_contract_file)[0]
        self.download_doc(doc_link)


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
