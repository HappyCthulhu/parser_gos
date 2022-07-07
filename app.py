import json
import time

import requests
import yaml
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
from yaml.loader import SafeLoader

from logger_settings import logger
from logic import start_parse
from new_ui import Ui_MainWindow


def check_access():
    try:
        response = requests.get('http://5.44.41.237:8080/status')
        response = json.loads(response.text)
        status = response['status']
        if status == 'stop':
            return False
        elif status == 'start':
            return True

        return status

    except:
        status = True
        return status


# PyQt5.uic.pyuic -x [FILENAME].ui -o [FILENAME].py
class Reactions():
    def __init__(self, ui):
        self.ui = ui
        self.thread = None
        self.link_params = {}

    def ui_reactions(self):
        self.ui.pushButton_14.clicked.connect(self.start)
        self.ui.pushButton_13.clicked.connect(self.stop)
        self.ui.pushButton_3.clicked.connect(self.clear_input)
        self.ui.pushButton_5.clicked.connect(self.save_search_string)
        self.ui.pushButton_4.clicked.connect(self.load_search_string)
        self.ui.checkbox.clicked.connect(self.get_publish_date)
        self.ui.checkbox_2.clicked.connect(self.get_price_general)

    def get_price_general(self):
        if self.ui.checkbox_2.checkState():
            self.link_params['price_from_general'] = self.ui.lineEdit_3.text()
            self.link_params['price_to_general'] = self.ui.lineEdit_2.text()

            self.ui.lineEdit_3.setEnabled(False)
            self.ui.lineEdit_2.setEnabled(False)

        else:
            self.ui.lineEdit_3.setEnabled(True)
            self.ui.lineEdit_2.setEnabled(True)

    def get_publish_date(self):
        if self.ui.checkbox.checkState():
            self.link_params['publish_date_from'] = self.ui.dateEdit.date().toString("dd.MM.yyyy")
            self.link_params['publish_date_to'] = self.ui.dateEdit_2.date().toString("dd.MM.yyyy")

            self.ui.dateEdit.setEnabled(False)
            self.ui.dateEdit_2.setEnabled(False)

        else:
            self.ui.dateEdit.setEnabled(True)
            self.ui.dateEdit_2.setEnabled(True)

    # TODO: как-нибудь переименовать в start_parsing
    def start(self):
        # TODO: добавить проверку на то, были ли найдены записи: //a[contains(text(),"№")]

        print(check_access)
        if check_access():
            pass
        else:
            print('Sorry, this app cant run on your device')
            sys.exit(app.exec_())

        self.link_params['search_string'] = self.ui.lineEdit.text()
        self.thread = ThreadClass(parent=None, index=1, link_params=self.link_params)
        self.thread.start()
        self.ui.pushButton_14.setEnabled(False)

    def stop(self):
        self.thread.stop()
        self.ui.pushButton_14.setEnabled(True)

    def load_search_string(self):
        # очищаем поле ввода
        self.ui.lineEdit.text()
        with open(search_string_file, 'r') as file:
            self.link_params['search_string'] = yaml.load(file, Loader=SafeLoader)
        self.ui.lineEdit.setText(self.link_params['search_string'])

    def save_search_string(self):
        search_string = self.ui.lineEdit.text().lstrip().rstrip()
        with open(search_string_file, 'w') as file:
            yaml.dump(search_string, file)

    def clear_input(self):
        self.ui.lineEdit.setText('')


class ThreadClass(QtCore.QThread):
    any_signal = QtCore.pyqtSignal(int)

    def __init__(self, parent=None, index=0, link_params: dict = None):
        super(ThreadClass, self).__init__(parent)
        self.index = index
        self.link_params = link_params
        self.is_running = True

    def run(self):
        logger.info('Starting thread...', self.index)
        start_parse(self.link_params)

    def stop(self):
        self.is_running = False
        logger.info('Stopping thread...', self.index)
        self.terminate()


if __name__ == "__main__":
    import sys

    search_string_file = 'search_query.yaml'

    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    reactions = Reactions(ui)
    reactions.ui_reactions()

    MainWindow.show()

    sys.exit(app.exec_())

