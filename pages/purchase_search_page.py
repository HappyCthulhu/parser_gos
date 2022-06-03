import requests
from lxml import html

from locators import MainPageLocators


class PurchaseSearchPage:
    def __init__(self, link):
        self.link = link
        self.tree = self.get_tree()
        self.purchases = self.get_purchases()

    def find_number_of_pages(self):
        pages_count = int(self.tree.xpath(MainPageLocators.text_pages_number)[-1])
        return pages_count

    def get_tree(self):
        html_text = requests.get(self.link).text
        return html.document_fromstring(html_text)

    def get_purchases(self):
        return self.tree.xpath(MainPageLocators.divs_purchases)

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
        link = (f'https://zakupki.gov.ru{purchase_obj.xpath(MainPageLocators.text_links)[0]}')
        return link
