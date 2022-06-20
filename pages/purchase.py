from locators import PurchasePageLocators
from logger_settings import logger
from pages.base_page import BasePage
from pages.purchase_supplier_results import PurchaseSupplierResults


class PurchasePage(BasePage):
    def __init__(self, link, status):
        self.link = link
        self.status = status
        self.tree = self.get_tree(self.link)
        self.element = HtmlElement(self.tree)

    def get_page_elements(self):
        self.purchase_number = self.element.get_purchase_number(self.link)
        self.customer = self.element.get_customer()
        self.region = self.element.get_region()
        self.starting_price = self.element.get_starting_price()
        self.date_and_time_of_the_application_beginning = self.element.get_date_and_time_of_the_application_beginning()
        self.date_and_time_of_the_application_deadline = self.element.get_date_and_time_of_the_application_deadline()
        self.date_of_the_procedure_for_submitting_proposals = self.element.get_date_of_the_procedure_for_submitting_proposals()
        self.ktru_blocks = self.element.process_ktru_blocks()
        self.ktru_sum_cost = self.element.get_ktru_sum_cost()
        self.purchase_supplier_results = self.element.get_purchase_supplier_results(self.link)


class HtmlElement(BasePage):
    def __init__(self, tree):
        self.tree = tree

    def process_ktru_blocks(self):
        ktru_blocks_html = self.get_ktru_blocks()
        ktru_blocks = []

        if len(ktru_blocks_html) != 0:
            for block in ktru_blocks_html:
                self.ktru_block_tree = self.from_lxml_to_html_to_lxml(block)
                ktru_position_code = self.get_ktru_position_code()
                ktru_name_of_product_or_service = self.get_ktru_name_of_product_or_service()
                ktru_count = self.get_ktru_count()

                ktru_blocks.append(
                    {
                        'ktru_position_code': ktru_position_code,
                        'ktru_name_of_product_or_service': ktru_name_of_product_or_service,
                        'ktru_count': ktru_count
                    }
                )

        return ktru_blocks

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
        logger.debug(f'Ссылка: {link}')
        purchase_number = self.tree.xpath(PurchasePageLocators.text_purchase_number)[0].lstrip().rstrip()
        logger.debug(f'purchase_number: {purchase_number}')
        return purchase_number

    def get_customer(self):
        if not self.check_element_existing(PurchasePageLocators.text_customer):
            return ''
        return self.tree.xpath(PurchasePageLocators.text_customer)[0].lstrip().rstrip()

    def get_starting_price(self):
        if not self.check_element_existing(PurchasePageLocators.text_starting_price):
            return ''
        else:
            return self.tree.xpath(PurchasePageLocators.text_starting_price)[0].replace('₽', '').lstrip().rstrip()

    def get_date_and_time_of_the_application_beginning(self):
        if not self.check_element_existing(PurchasePageLocators.text_date_and_time_of_the_application_beginning):
            return ''
        else:
            # в закупках, чья ссылка имеет regNumber, таймзона лежит в отдельном элементе
            # в закупках, чья ссылка имеет noticeInfoId, таймзона лежит в том же элементе
            if self.check_element_existing(PurchasePageLocators.text_timezone):
                timezone = self.tree.xpath(PurchasePageLocators.text_timezone)[0].lstrip().rstrip()
                time = self.tree.xpath(PurchasePageLocators.text_date_and_time_of_the_application_beginning)[
                    0].lstrip().rstrip()
                time_timezone = f'{time} {timezone}'
                return time_timezone

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
            return self.tree.xpath(PurchasePageLocators.text_date_and_time_of_the_application_deadline)[
                0].lstrip().rstrip()

    def get_ktru_blocks(self):
        return self.tree.xpath(PurchasePageLocators.blocks_ktru, tree='ktru')

    def get_ktru_position_code(self):
        if not self.check_element_existing(PurchasePageLocators.text_ktru_position_code, tree='ktru'):
            return ''
        else:
            return ''.join(self.ktru_block_tree.xpath(PurchasePageLocators.text_ktru_position_code)).lstrip().rstrip()

    def get_ktru_name_of_product_or_service(self):
        if not self.check_element_existing(PurchasePageLocators.text_ktru_name_of_product_or_service, tree='ktru'):
            return ''
        else:
            return self.ktru_block_tree.xpath(PurchasePageLocators.text_ktru_name_of_product_or_service)[
                0].lstrip().rstrip()

    def get_ktru_count(self):
        if not self.check_element_existing(PurchasePageLocators.text_ktru_count, tree='ktru'):
            return ''
        else:
            return self.ktru_block_tree.xpath(PurchasePageLocators.text_ktru_count)[0].lstrip().rstrip()

    def get_ktru_sum_cost(self):
        if not self.check_element_existing(PurchasePageLocators.text_ktru_sum_cost):
            return ''
        else:
            return self.tree.xpath(PurchasePageLocators.text_ktru_sum_cost)[0].replace('₽', '').lstrip().rstrip()

    def get_region(self):
        if not self.check_element_existing(PurchasePageLocators.text_region):
            return ''
        else:
            return self.tree.xpath(PurchasePageLocators.text_region)[0].lstrip().rstrip()

    def get_purchase_supplier_results(self, link):
        if not self.check_element_existing(PurchasePageLocators.a_results_of_determination_of_the_supplier):
            return ''
        else:
            purchase_supplier_results_page = PurchaseSupplierResults(link)
            return purchase_supplier_results_page.contract_blocks
