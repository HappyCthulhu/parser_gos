from locators import MainPageLocators

from pages.base_page import BasePage


class PurchaseSearchPage(BasePage):
    def __init__(self, link):
        self.link = link
        self.tree = self.get_tree(self.link)
        self.purchases = self.get_purchases()

    def find_number_of_pages(self):
        pages_count = int(self.tree.xpath(MainPageLocators.text_pages_number)[-1])
        return pages_count

    def get_purchases(self):
        return self.tree.xpath(MainPageLocators.divs_purchases)

    def get_status(self, purchase):
        purchase_obj = self.from_lxml_to_html_to_lxml(purchase)
        status = purchase_obj.xpath(MainPageLocators.text_status)[0].lstrip().rstrip()
        return status

    def get_link_to_purchases(self, purchase):
        purchase_obj = self.from_lxml_to_html_to_lxml(purchase)
        link = f'https://zakupki.gov.ru{purchase_obj.xpath(MainPageLocators.text_links)[0]}'
        return link
