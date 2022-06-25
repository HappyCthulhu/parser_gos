from locators import PurchasePageLocators
from logger_settings import logger
from pages.base_page import BasePage
from pages.documents_results import DocumentsResults
from pages.purchase_supplier_results import PurchaseSupplierResults


class PurchasePage(BasePage):
    def __init__(self, link, status):
        self.link = link
        self.status = status  # TODO было бы грамотнее на странице закупки статус забирать
        self.tree = self.get_tree(self.link)
        self.element = HtmlElement(self.tree)
        self.purchase_supplier_results_page = self.get_purchase_supplier_results_page(
            self.link)
        self.documents_results_page = self.get_documents_results_page(self.purchase_supplier_results_page)

    # TODO: мб в init все перенести?
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
        self.email = self.element.get_email()
        self.phone_number = self.element.get_phone_number()
        self.purchase_supplier_results = self.element.get_purchase_supplier_results(self.purchase_supplier_results_page)
        self.ru_numbers = self.element.get_ru_numbers(self.documents_results_page)
        # TODO: действительно ли purchase_supplier_results много блоков может быть? Имеет ли смысл словарь делать?
        # self.provider = self.element.get_provider(self.purchase_supplier_results_page)
        # TODO: проверить таки, почему победитель не парсится

    def get_purchase_supplier_results_page(self, link):
        if not self.check_element_existing(PurchasePageLocators.a_results_of_determination_of_the_supplier, self.tree):
            return ''
        else:
            purchase_supplier_results_page = PurchaseSupplierResults(link)
            return purchase_supplier_results_page

    def get_documents_results_page(self, purchase_supplier_results_page):
        if not purchase_supplier_results_page:
            return ''
        else:
            documents_results_page = DocumentsResults(purchase_supplier_results_page.tree,
                                                      purchase_supplier_results_page.order_num)
            return documents_results_page


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

    def get_purchase_number(self, link):
        logger.info(f'Ссылка: {link}')
        purchase_number = self.tree.xpath(PurchasePageLocators.text_purchase_number)[0].lstrip().rstrip()
        logger.info(f'purchase_number: {purchase_number}')
        return purchase_number

    def get_customer(self):
        if not self.check_element_existing(PurchasePageLocators.text_customer, self.tree):
            return ''
        return self.tree.xpath(PurchasePageLocators.text_customer)[0].lstrip().rstrip()

    def get_starting_price(self):
        if not self.check_element_existing(PurchasePageLocators.text_starting_price, self.tree):
            return ''
        else:
            return self.tree.xpath(PurchasePageLocators.text_starting_price)[0].replace('₽', '').lstrip().rstrip()

    def get_date_and_time_of_the_application_beginning(self):
        if not self.check_element_existing(PurchasePageLocators.text_date_and_time_of_the_application_beginning,
                                           self.tree):
            return ''
        else:
            # в закупках, чья ссылка имеет regNumber, таймзона лежит в отдельном элементе
            # в закупках, чья ссылка имеет noticeInfoId, таймзона лежит в том же элементе
            if self.check_element_existing(PurchasePageLocators.text_timezone, self.tree):
                timezone = self.tree.xpath(PurchasePageLocators.text_timezone)[0].lstrip().rstrip()
                time = self.tree.xpath(PurchasePageLocators.text_date_and_time_of_the_application_beginning)[
                    0].lstrip().rstrip()
                time_timezone = f'{time} {timezone}'
                return time_timezone

            else:
                return self.tree.xpath(PurchasePageLocators.text_date_and_time_of_the_application_beginning)[
                    0].lstrip().rstrip()

    def get_date_and_time_of_the_application_deadline(self):
        if not self.check_element_existing(PurchasePageLocators.text_date_and_time_of_the_application_deadline,
                                           self.tree):
            return ''
        else:
            return self.tree.xpath(PurchasePageLocators.text_date_and_time_of_the_application_deadline)[
                0].lstrip().rstrip()

    def get_date_of_the_procedure_for_submitting_proposals(self):
        if not self.check_element_existing(PurchasePageLocators.text_date_and_time_of_the_application_deadline,
                                           self.tree):
            return ''
        else:
            return self.tree.xpath(PurchasePageLocators.text_date_and_time_of_the_application_deadline)[
                0].lstrip().rstrip()

    def get_ktru_blocks(self):
        return self.tree.xpath(PurchasePageLocators.blocks_ktru, tree='ktru')

    def get_ktru_position_code(self):
        if not self.check_element_existing(PurchasePageLocators.text_ktru_position_code, self.ktru_block_tree):
            return ''
        else:
            return ''.join(self.ktru_block_tree.xpath(PurchasePageLocators.text_ktru_position_code)).lstrip().rstrip()

    def get_ktru_name_of_product_or_service(self):
        if not self.check_element_existing(PurchasePageLocators.text_ktru_name_of_product_or_service,
                                           self.ktru_block_tree):
            return ''
        else:
            return self.ktru_block_tree.xpath(PurchasePageLocators.text_ktru_name_of_product_or_service)[
                0].lstrip().rstrip()

    def get_ktru_count(self):
        if not self.check_element_existing(PurchasePageLocators.text_ktru_count, self.ktru_block_tree):
            return ''
        else:
            return self.ktru_block_tree.xpath(PurchasePageLocators.text_ktru_count)[0].lstrip().rstrip()

    def get_ktru_sum_cost(self):
        if not self.check_element_existing(PurchasePageLocators.text_ktru_sum_cost, self.tree):
            return ''
        else:
            return self.tree.xpath(PurchasePageLocators.text_ktru_sum_cost)[0].replace('₽', '').lstrip().rstrip()

    def get_region(self):
        if not self.check_element_existing(PurchasePageLocators.text_region, self.tree):
            return ''
        else:
            return self.tree.xpath(PurchasePageLocators.text_region)[0].lstrip().rstrip()

    def get_purchase_supplier_results(self, purchase_supplier_results_page):
        # TODO: посмотреть сюда. Здесь я проверяю наличие всего блока purchase_supplier_results_page на странице, хотя сейчас я в любом случае класс его создаю
        if not self.check_element_existing(PurchasePageLocators.a_results_of_determination_of_the_supplier, self.tree):
            return ''
        else:
            return purchase_supplier_results_page.contract_blocks

    def get_phone_number(self):
        if not self.check_element_existing(PurchasePageLocators.phone_number, self.tree):
            return ''
        else:
            return self.tree.xpath(PurchasePageLocators.phone_number)[0].lstrip().rstrip()

    def get_email(self):
        if not self.check_element_existing(PurchasePageLocators.email, self.tree):
            return ''
        else:
            return self.tree.xpath(PurchasePageLocators.email)[0].lstrip().rstrip()

    def get_ru_numbers(self, documents_results_page):
        if documents_results_page:
            ru_numbers = documents_results_page.get_ru_numbers()
            if ru_numbers:
                logger.info(f'ru_numbers: {ru_numbers}')
            return ru_numbers
        else:
            return ''

    # def get_provider(self, purchase_supplier_results_page):
    #     if purchase_supplier_results_page == '':
    #         return ''
    #     else:
    #         return purchase_supplier_results_page.get_provider()



# test = PurchasePage('https://zakupki.gov.ru/epz/order/notice/ea20/view/common-info.html?regNumber=0188100001822000001', 'status')
# test.get_page_elements()
