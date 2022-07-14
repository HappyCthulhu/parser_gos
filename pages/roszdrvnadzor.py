import json

import requests

from pages.base_page import BasePage
from logger_settings import logger


class RoszDravNadzor(BasePage):
    def __init__(self, ru_numbers: list):
        # TODO: переделать в словарь?
        self.ru_numbers_data = {}
        for ru_number in ru_numbers:
            ru_data = self.get_data(ru_number)
            if ru_data:
                ru_data[ru_number]['download_link'] = self.get_download_link(ru_data)
                self.ru_numbers_data.update(ru_data)

    def get_data(self, ru: str):

        ru_data = {}

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        }

        data = {
            'draw': '6',
            'order[0][column]': '0',
            'order[0][dir]': 'asc',
            'start': '0',
            'length': '25',
            'search[value]': '',
            'search[regex]': 'false',
            'prev_total': '43',
            'q_mi_label_application': ru,
            'q_no_uniq': '',
            'q_appl_address_post': '',
            'q_in_accordance_nomen': '',
            'q_prescription': '',
            'q_address_production': '',
            'id_sclass': '',
            'q_appl_address': '',
            'q_appl_label': '',
            'q_prod_address': '',
            'q_okp': '',
            'q_prod_address_post': '',
            'dt_ru_from': '',
            'dt_ru_to': '',
            'q_prod_label': '',
            'dt_ru_end_from': '',
            'dt_ru_end_to': '',
            'q_no': '',
            'q_interchangeability_med_products': '',
        }

        logger.info(f'Отправляем запрос к roszdravnadzor. Это может занять время. РУ: {ru}')
        response = requests.post('https://roszdravnadzor.gov.ru/ajax/services/misearch', headers=headers, data=data)
        elems = response.json()['data']
        if not elems:
            logger.debug(f'Не были найдены записи для РУ: {ru}. Status code: {response.status_code}')
        else:
            for elem in elems:

                ru_from_elem = elem['col2']['label'].split()[1]
                if ru_from_elem == ru:
                    table_name, id = elem['DT_RowId'].split('-')

                    ru_data[ru] = {
                        'the_term_of_the_certificate': elem['col4']['label'],
                        'id': id,
                        'table_name': table_name
                    }

        if not ru_data:
            logger.debug(f'Не были найдены записи для РУ: {ru}')

        return ru_data

    def get_download_link(self, ru_data: dict):

        for ru_numbers, ru_value in ru_data.items():
            params = {
                'id': ru_value['id'],
                'table_name': ru_value['table_name'],
                'fancybox': 'true',
            }

            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest',
            }

            tree = self.get_tree('https://roszdravnadzor.gov.ru/services/misearch', params=params, headers=headers)

            if self.check_element_existing('//a[@title="скачать РУ"]/@href', tree):
                link_part = tree.xpath('//a[@title="скачать РУ"]/@href')[0]
                return f'https://roszdravnadzor.gov.ru/services/misearch{link_part}'
            else:
                logger.debug(f'Не была найдена ссылка на скачивание РУ для РУ {ru_numbers}\n'
                             f'Информация: {json.dumps(ru_data, indent=4, ensure_ascii=False)}')
