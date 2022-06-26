import requests
from docx.api import Document

from locators import PurchaseSupplierResultsLocators, DocumentsResultsLocators
from pages.base_page import BasePage


class DocumentsResults(BasePage):
    def __init__(self, purchase_search_page_tree, order_num):
        self.order_num = order_num
        self.purchase_search_page_tree = purchase_search_page_tree

    def get_status(self):
        if not self.check_element_existing(PurchaseSupplierResultsLocators.status, self.purchase_search_page_tree):
            return ''
        else:

            status = self.purchase_search_page_tree.xpath(PurchaseSupplierResultsLocators.status)[0].lstrip().rstrip()
        return status

    def download_doc(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        }
        response = requests.get(url, allow_redirects=True, headers=headers)

        # TODO: статичный путь сделать
        with open("doc.docx", "wb") as file:
            file.write(response.content)

    def get_contract_file(self, doc_block_tree):
        if not self.check_element_existing(DocumentsResultsLocators.a_contract_file, doc_block_tree):
            return ''
        else:
            status = doc_block_tree.xpath(DocumentsResultsLocators.a_contract_file)[0].lstrip().rstrip()
        return status

    def get_ru_from_table(self, table_rows):
        ru = []
        for row in table_rows:
            for cell in row.cells:
                text = cell.text
                if 'Номер регистрационного удостоверения' in text:
                    # https://zakupki.gov.ru/epz/order/notice/ea20/view/common-info.html?regNumber=0322100001622000024
                    # test = text.split('Номер регистрационного удостоверения: ')
                    text = text.split('Номер регистрационного удостоверения: ')[1].lstrip().rstrip()
                    if text not in ru:
                        ru.append(text)

        return ru

    def find_specification_table(self, tables):
        for table in tables:
            for row in table.rows:
                for cell in row.cells:
                    text = cell.text
                    # if 'Номер регистрационного удостоверения' in text:
                    if '№ п/п' in text:
                        return table

        return ''

    def get_draft_id(self):
        if not self.check_element_existing(PurchaseSupplierResultsLocators.data_id_draft_id,
                                           self.purchase_search_page_tree):
            return ''
        else:
            draft_id = self.purchase_search_page_tree.xpath(PurchaseSupplierResultsLocators.data_id_draft_id)[0]
        return draft_id

    def get_doc_block_tree(self):
        draft_id = self.get_draft_id()
        if draft_id:

            tree = self.get_tree(
                # разворачиваем часть страницы "Информация о процедуре заключения контракта"
                'https://zakupki.gov.ru/epz/order/notice/rpec/documents-results.html',
                {'orderNum': self.order_num,
                 'draftId': draft_id  # idшник документа, судя во всему. Без него возвращает 404
                 }
            )
            return tree
        else:
            return ''

    def get_ru_numbers(self):
        # TODO: возможно в будущем окажется, что может быть несколько документов. Нужно будет перепилить
        status = self.get_status()

        doc_block_tree = self.get_doc_block_tree()
        if doc_block_tree != '':
            if status == 'Контракт не заключен':
                self.ru_number = []
            else:
                doc_link = self.get_contract_file(doc_block_tree)
                if doc_link:
                    self.download_doc(doc_link)
                    document = Document('doc.docx')
                    specification_table = self.find_specification_table(document.tables)
                    if specification_table:
                        ru = self.get_ru_from_table(specification_table.rows)
                        return ru
                    else:
                        return []

                else:
                    self.ru_number = []
        else:
            return []
