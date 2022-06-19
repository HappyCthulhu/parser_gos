from locators import MainPageLocators

from pages.base_page import BasePage


class PurchaseSearchPage(BasePage):
    def __init__(self, main_link, link_params: dict):
        self.link = self.create_link(main_link, link_params)
        self.tree = self.get_tree(self.link)
        self.purchases = self.get_purchases()

    def create_link(self, main_link, link_params):

        link = f'{main_link}?&search-filter=Дате+размещения&sortBy=UPDATE_DATE'

        if link_params.get("search_string"):
            link = f'{link}&searchString={link_params["search_string"]}'

        if link_params.get("page_number"):
            link = f'{link}&pageNumber={link_params["page_number"]}'

        if link_params.get("publish_date_from"):
            link = f'{link}&publishDateFrom={link_params["publish_date_from"]}'

        if link_params.get("publish_date_to"):
            link = f'{link}&publishDateTo={link_params["publish_date_to"]}'

        if link_params.get("publish_date_from"):
            link = f'{link}&publishDateFrom={link_params["publish_date_from"]}'

        if link_params.get("price_from_general"):
            link = f'{link}&priceFromGeneral={link_params["price_from_general"]}'

        if link_params.get("price_to_general"):
            link = f'{link}&priceToGeneral={link_params["price_to_general"]}'

        if link_params.get("records_per_page"):
            link = f'{link}&recordsPerPage={link_params["records_per_page"]}'

        return link

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
