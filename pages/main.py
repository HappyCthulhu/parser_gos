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
        self.purchases = self.tree.xpath(MainPageLocators.purchases)

    def get_link_to_purchases(self, purchase_tree):
        test = purchase_tree.xpath('//div[@class="registry-entry__body-value"]/text()')
        print()
