import requests

from base_page import BasePage


class GispGov(BasePage):
    def __init__(self, registry_entry_numbers: list):
        self.registry_entry_numbers_links = {}
        for number in registry_entry_numbers:
            registry_entry_numbers_data = self.get_data(number)
            needed_registry_entry_numbers_data = self.get_needed_registry_entry_numbers_data(
                registry_entry_numbers_data['items'], number)
            product_writeout_url = f'https://gisp.gov.ru/{needed_registry_entry_numbers_data["product_writeout_url"]}'
            self.registry_entry_numbers_links[number] = {'link': product_writeout_url}

    def get_data(self, registry_entry_numbers):
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        }

        json_data = {
            'opt': {
                'filter': [
                    'product_reg_number',
                    'contains',
                    registry_entry_numbers,
                ],
            },
        }

        response = requests.post('https://gisp.gov.ru/pp719v2/pub/prod/b/', headers=headers, json=json_data)

        return response.json()

    def get_needed_registry_entry_numbers_data(self, registry_entry_numbers_data, registry_entry_numbers):
        for elem in registry_entry_numbers_data:
            if elem['product_reg_number'] == registry_entry_numbers:
                return elem
