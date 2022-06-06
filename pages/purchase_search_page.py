import requests
from lxml import html

from locators import MainPageLocators

# TODO: переименовать в purchase_search

class PurchaseSearchPage:
    def __init__(self, link):
        self.link = link
        self.tree = self.get_tree()
        self.purchases = self.get_purchases()

    def find_number_of_pages(self):
        pages_count = int(self.tree.xpath(MainPageLocators.text_pages_number)[-1])
        return pages_count

    def get_tree(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        }

        self.response = requests.get(self.link, headers=headers)
        return html.document_fromstring(self.response.text)

    def get_purchases(self):
        # TODO: проверить, присваивается ли объект в переменные класса без return
        return self.tree.xpath(MainPageLocators.divs_purchases)

    # TODO: создать BasePage и переместить общие методы (типа преобразования в tostring и обратно) туда
    # TODO: вообще подумать, можно ли иначе сделать (без костылей преобразования туда и обратно)
    def get_status(self, purchase):
        #  TODO: функция, которая html возвращает
        purchase_tree = html.tostring(purchase)
        purchase_obj = html.document_fromstring(purchase_tree)
        status = purchase_obj.xpath(MainPageLocators.text_status)[0].lstrip().rstrip()
        return status

    def get_link_to_purchases(self, purchase):
        # TODO: может некостыльный метод есть?
        purchase_tree = html.tostring(purchase)
        purchase_obj = html.document_fromstring(purchase_tree)
        link = f'https://zakupki.gov.ru{purchase_obj.xpath(MainPageLocators.text_links)[0]}'
        return link
