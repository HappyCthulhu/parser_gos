from datetime import datetime
from pathlib import Path

from openpyxl import load_workbook, Workbook


class Export:
    def __init__(self):
        Path('result data').mkdir(parents=True, exist_ok=True)
        f_name = self.create_file()
        self.wb = Workbook()
        ws = self.wb.active
        ws.title = "Sheet 1"
        self.wb.save(filename=Path('result data', f_name))
        self.create_titles(f_name)

    def create_file(self):
        f_name = f'result-{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}.xlsx'
        return f_name

    def create_titles(self, f_name):
        sheet = self.wb['Sheet 1']
        sheet[f'A2'].value = '№ номер'
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

        self.wb.save(filename=Path('result data', f_name))


export = Export()
