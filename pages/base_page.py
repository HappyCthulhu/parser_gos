import requests
from lxml import html

from logger_settings import logger


class BasePage():
    def get_tree(self, link, params=None):
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        }

        response = requests.get(link, params=params,
                                headers=headers)

        if response.status_code != 200:
            logger.critical(f'Статус страницы закупки: {response.status_code}')

        return html.document_fromstring(response.text)

    def from_lxml_to_html_to_lxml(self, lxml_obj):
        # костыль для того, чтоб получить конкретный lxml-объект на конкретного элемента на странице
        # нужно, если у нас много объектов с одним xpath на странице, и мы хотим каждый обработать отдельноkjkjk
        html_str = html.tostring(lxml_obj)
        lxml_obj = html.document_fromstring(html_str)
        return lxml_obj
