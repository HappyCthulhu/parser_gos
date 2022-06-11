from datetime import datetime
from pathlib import Path

from openpyxl import Workbook


class Export:
    def __init__(self):
        Path('result data').mkdir(parents=True, exist_ok=True)
        self.f_name = self.create_file()
        self.wb = Workbook()
        ws = self.wb.active
        ws.title = "Sheet 1"
        self.wb.save(filename=Path('result data', self.f_name))
        self.create_titles()

    def create_file(self):
        f_name = f'result-{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}.xlsx'
        return f_name

    def create_titles(self):
        sheet = self.wb['Sheet 1']
        sheet[f'A2'].value = '№ номер'
        sheet.column_dimensions['A'].width = 40
        sheet[f'B2'].value = '№ аукциона'
        sheet[f'C2'].value = 'Статус контракта'
        sheet[f'D2'].value = 'Начало подачи заявок'
        sheet[f'E2'].value = 'Конец подачи заявок'
        sheet[f'F2'].value = 'Дата и время проведения'
        sheet[f'G2'].value = 'НМЦ'
        sheet[f'H2'].value = 'Регион'
        sheet[f'I2'].value = 'Заказчик'
        sheet[f'J2'].value = 'КТРУ'
        sheet[f'K2'].value = 'Наименование товара'
        sheet[f'L2'].value = 'Количество товара'
        sheet[f'M2'].value = 'Список участников'
        sheet[f'N2'].value = 'Сумма в заявке'
        sheet[f'O2'].value = 'Победитель аукциона'
        sheet[f'P2'].value = 'Сумма по аукциону'
        sheet[f'Q2'].value = 'Сумма контракта'
        sheet[f'R2'].value = 'Производитель товара'
        sheet[f'S2'].value = 'Страна происхождения'
        sheet[f'T2'].value = 'Номер РУ'
        sheet[f'U2'].value = 'Ссылка на РУ'
        sheet[f'V2'].value = 'Срок действия РУ'
        sheet[f'W2'].value = '№ Реестровой записи'
        sheet[f'X2'].value = 'Ссылка на выписку из реестра МинПромТорга'
        sheet[f'Y2'].value = 'Файлы'
        sheet[f'Z2'].value = 'Упоминание'

        self.wb.save(filename=Path('result data', self.f_name))

    # TODO: нужно ли заранее знать, какое количество строк понадобится?
    # TODO: нужно ли хранить количество заполненных строк или будем выяснять каждый раз
    # находим последнюю заполненную строку
    # последовательно заполняем все строки (последняя заполненная строка + 1), кроме ктру и результатов аукциона

    # print("Python defined max_column " + str(sheet.max_row))
    def dump_ktru(self, row, sheet, purchase_page):
        if purchase_page.ktru_blocks:
            for block in purchase_page.ktru_blocks:
                if block['ktru_position_code']:
                    print()
                sheet[f'J{row}'].value = block['ktru_position_code']
                sheet[f'K{row}'].value = block['ktru_name_of_product_or_service']
                sheet[f'L{row}'].value = block['ktru_count']
                row += 1
                print(f'Блок КТРУ: {block["ktru_name_of_product_or_service"]}')
            print(f'Последний блок КТРУ должен находиться на строке: {row}')

    def dump_purchase_supplier_results(self, row, sheet, purchase_page):
        if purchase_page.purchase_supplier_results:
            for block in purchase_page.purchase_supplier_results:
                sheet[f'M{row}'].value = block['provider']
                sheet[f'Q{row}'].value = block['contract_price']
                row += 1

    def dump_data(self, purchase_page):
        # TODO: sheet, purchase_page в self добавить
        sheet = self.wb['Sheet 1']
        row = sheet.max_row + 1
        print(f'Заносим основную информацию на строку: {row}')
        # sheet[f'A{row}'].value = purchase_page.
        sheet[f'B{row}'].value = purchase_page.purchase_number
        sheet[f'C{row}'].value = purchase_page.status
        sheet[f'D{row}'].value = purchase_page.date_and_time_of_the_application_beginning
        sheet[f'E{row}'].value = purchase_page.date_and_time_of_the_application_deadline
        sheet[f'F{row}'].value = purchase_page.date_of_the_procedure_for_submitting_proposals
        # sheet[f'G{row}'].value = purchase_page.
        sheet[f'H{row}'].value = purchase_page.region
        sheet[f'I{row}'].value = purchase_page.customer
        sheet[f'P{row}'].value = purchase_page.ktru_sum_cost
        # sheet[f'Q{row}'].value = purchase_page.
        # sheet[f'R{row}'].value = purchase_page.
        # sheet[f'S{row}'].value = purchase_page.
        # sheet[f'T{row}'].value = purchase_page.
        # sheet[f'U{row}'].value = purchase_page.
        # sheet[f'V{row}'].value = purchase_page.
        # sheet[f'W{row}'].value = purchase_page.
        # sheet[f'X{row}'].value = purchase_page.
        # sheet[f'Y{row}'].value = purchase_page.
        # sheet[f'Z{row}'].value = purchase_page.

        self.dump_ktru(row, sheet, purchase_page)
        self.dump_purchase_supplier_results(row, sheet, purchase_page)

        self.wb.save(filename=Path('result data', self.f_name))


#
# export = Export()
