import requests
from lxml import html

from locators import PurchasePageLocators


class PurchasePage:
    def __init__(self, link):
        self.link = link

    def get_tree(self):
        html_text = requests.get(self.link).text
        self.tree = html.document_fromstring(html_text)
