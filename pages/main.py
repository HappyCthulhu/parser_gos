import requests
from lxml import html

from locators import MainPageLocators


class MainPage:
    def __init__(self):
        self.link = 'https://zakupki.gov.ru/epz/order/extendedsearch/results.html'


    def get_tree(self):
        html_text = requests.get(self.link).text
        self.tree = html.document_fromstring(html_text)

    def get_purchases(self):
        self.purchases = self.tree.xpath(MainPageLocators.divs_purchases)

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

