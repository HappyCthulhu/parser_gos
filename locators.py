class MainPageLocators:
    divs_purchases = "//div[@class ='search-registry-entry-block box-shadow-search-input']"
    text_links = '//div[@class="registry-entry__header-mid__number"]/a/@href'
    text_status = '//div[@class="registry-entry__header-mid__title text-normal"]/text()'
    button_next_page = '//a[@class="paginator-button paginator-button-next"]'
    text_pages_number = '//span[@class="link-text"]/text()'


# pageNumber = 150
# recordsPerPage=_50

class PurchasePageLocators:
    # text_purchase_number = '//div[@class="registry-entry__header-mid__number"]/a/text()'
    text_address = '//*[contains(text(),"Место нахождения")]/following::*[1]/text()'
    text_customer = '//*[normalize-space(text()) = "Заказчик"]/following::*[1]/a/text()'
    text_starting_price = '//*[contains(text(),"Начальная цена")]/following::*[1]/text()'
    # оператор AND приделать внутри Xpath.
    # Ибо сейчас он ищет только по слову "начала",
    # а надо еще и по "дата". Чтоб по двум словам подряд искал
    # При этом, чтоб они могли соять в рандомном порядке внутри одного элемента.

    text_date_and_time_of_the_application_beginning = '//*[contains(text(),"начала ")]/following::*[1]/text()[1]'
    text_timezone = '//*[contains(text(),"начала ")]/following::*[1]/span/text()'
    text_date_and_time_of_the_application_deadline = '//*[contains(text(),"Дата и время окончания срока подачи заявок")]/following::*[1]/text()[1]'
    text_date_of_the_procedure_for_submitting_proposals = '//*[contains(text(),"Дата проведения процедуры подачи предложений о цене контракта либо о сумме цен единиц товара, работы, услуги")]/following::*[1]/text()[1]'
    text_timezone = '(//span[@class="timeZoneName"])[1]/text()'
    blocks_ktru = '//div[@id="positionKTRU"]//tbody[@class="tableBlock__body"]/tr[@class="tableBlock__row"]'
    text_ktru_position_code = '//tr/td[2]//text()'
    text_ktru_name_of_product_or_service = '//tr/td[3]/text()'
    text_ktru_count = '//tr/td[5]/text()'
    text_ktru_sum_cost = '//span[@class="cost"]/text()'
    text_purchase_number = '//a[contains(text(),"№")]/text()'
    text_region = '//*[contains(text(),"Место нахождения")]/following::*[1]/text()'
    a_results_of_determination_of_the_supplier = '//a[contains(text(),"Результаты определения поставщика (подрядчика, исп")]'
    blocks_information_about_the_conclusion_of_the_contract = '//tbody/tr[@class="tableBlock__row"]'
    provider = '//tr/td[3]/text()'
    contract_price = '//tr/td[5]/text()'
