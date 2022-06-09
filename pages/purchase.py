import requests
from lxml import html

from locators import PurchasePageLocators
from logger_settings import logger


class PurchasePage:
    def __init__(self, link, status):
        # self.link = 'https://zakupki.gov.ru/epz/order/notice/ea20/view/common-info.html?regNumber=0319200063622000125'
        self.link = link
        self.status = status
        self.tree = self.get_tree()
        self.element = HtmlElement(self.tree)

    def get_tree(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        }

        response = requests.get(self.link, headers=headers)

        if response.status_code != 200:
            logger.critical(f'Статус страницы закупки: {response.status_code}')

        return html.document_fromstring(response.text)

    def get_page_elements(self):
        self.purchase_number = self.element.get_purchase_number(self.link)
        self.customer = self.element.get_customer()
        self.starting_price = self.element.get_starting_price()
        self.date_and_time_of_the_application_beginning = self.element.get_date_and_time_of_the_application_beginning()
        self.date_and_time_of_the_application_deadline = self.element.get_date_and_time_of_the_application_deadline()
        self.date_of_the_procedure_for_submitting_proposals = self.element.get_date_of_the_procedure_for_submitting_proposals()
        self.ktru_block = self.element.process_ktru_blocks()
        self.ktru_sum_cost = self.element.get_ktru_sum_cost()

        print()
        # self.purchase = {
        #     'purchase_number': purchase_number,
        #     'customer': customer,
        #     'starting_price': starting_price,
        #     'date_and_time_of_the_application_beginning': date_and_time_of_the_application_beginning,
        #     'date_and_time_of_the_application_deadline': date_and_time_of_the_application_deadline,
        #     'date_of_the_procedure_for_submitting_proposals': date_of_the_procedure_for_submitting_proposals,
        #     'block_ktru': block_ktru,
        #     'code': ktru_position_code,
        #     'ktru_name_of_product_or_service': ktru_name_of_product_or_service,
        #     'ktru_count': ktru_count,
        #     'sum_cost': ktru_sum_cost
        # }

        # logger.debug(purchase)


class HtmlElement():
    def __init__(self, tree):
        self.tree = tree

    def get_ktru_block(self, block):
        #  TODO: функция, которая html возвращает
        block_html = html.tostring(block)
        ktru_tree = html.document_fromstring(block_html)
        return ktru_tree

    def process_ktru_blocks(self):
        ktru_blocks_html = self.get_ktru_blocks()
        self.ktru_blocks = []

        if len(ktru_blocks_html) != 0:
            for block in ktru_blocks_html:
                self.ktru_block_tree = self.get_ktru_block(block)
                ktru_position_code = self.get_ktru_position_code()
                ktru_name_of_product_or_service = self.get_ktru_name_of_product_or_service()
                ktru_count = self.get_ktru_count()

                self.ktru_blocks.append(
                    {
                        'ktru_position_code': ktru_position_code,
                        'ktru_name_of_product_or_service': ktru_name_of_product_or_service,
                        'ktru_count': ktru_count
                    }
                )

    def check_element_existing(self, xpath, tree=None):
        if tree == 'ktru':
            if len(self.ktru_block_tree.xpath(xpath)) == 0:
                return False
            else:
                return True
        else:
            if len(self.tree.xpath(xpath)) == 0:
                return False
            else:
                return True

    def get_purchase_number(self, link):
        self.link = 'https://zakupki.gov.ru/epz/order/notice/ea20/view/common-info.html?regNumber=0319200063622000125'
        # self.link = link
        return str(link.split('=')[1])

    def get_customer(self):
        return self.tree.xpath(PurchasePageLocators.text_customer)[0].lstrip().rstrip()

    def get_starting_price(self):
        if not self.check_element_existing(PurchasePageLocators.text_starting_price):
            return ''
        else:
            return self.tree.xpath(PurchasePageLocators.text_starting_price)[0].lstrip().rstrip()

    def get_date_and_time_of_the_application_beginning(self):
        if not self.check_element_existing(PurchasePageLocators.text_date_and_time_of_the_application_beginning):
            return ''
        else:
            return self.tree.xpath(PurchasePageLocators.text_date_and_time_of_the_application_beginning)[
                0].lstrip().rstrip()

    def get_date_and_time_of_the_application_deadline(self):
        if not self.check_element_existing(PurchasePageLocators.text_date_and_time_of_the_application_deadline):
            return ''
        else:
            return self.tree.xpath(PurchasePageLocators.text_date_and_time_of_the_application_deadline)[
                0].lstrip().rstrip()

    def get_date_of_the_procedure_for_submitting_proposals(self):
        if not self.check_element_existing(PurchasePageLocators.text_date_and_time_of_the_application_deadline):
            return ''
        else:
            return self.tree.xpath(PurchasePageLocators.text_date_and_time_of_the_application_deadline)[0].lstrip().rstrip()

    def get_ktru_blocks(self):
        return self.tree.xpath(PurchasePageLocators.block_ktru, tree='ktru')

    def get_ktru_position_code(self):
        if not self.check_element_existing(PurchasePageLocators.text_ktru_position_code, tree='ktru'):
            return ''
        else:
            return self.ktru_block_tree.xpath(PurchasePageLocators.text_ktru_position_code)[0].lstrip().rstrip()

    def get_ktru_name_of_product_or_service(self):
        if not self.check_element_existing(PurchasePageLocators.text_ktru_name_of_product_or_service, tree='ktru'):
            return ''
        else:
            return self.ktru_block_tree.xpath(PurchasePageLocators.text_ktru_name_of_product_or_service)[0].lstrip().rstrip()

    def get_ktru_count(self):
        if not self.check_element_existing(PurchasePageLocators.text_ktru_count, tree='ktru'):
            return ''
        else:
            return self.ktru_block_tree.xpath(PurchasePageLocators.text_ktru_count)[0].lstrip().rstrip()

    def get_ktru_sum_cost(self):
        if not self.check_element_existing(PurchasePageLocators.text_ktru_sum_cost):
            return ''
        else:
            return self.tree.xpath(PurchasePageLocators.text_ktru_sum_cost)[0].lstrip().rstrip()

    # def get_status(self):
