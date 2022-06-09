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

    def create_file(self):
        f_name = f'result-{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}.xlsx'
        # with open(Path('result data', f_name), 'w') as file:
        #     pass
        return f_name


export = Export()
