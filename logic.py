from pages.purchase import PurchasePage
from pages.purchase_search_page import PurchaseSearchPage

# cover_text = tree_cover.xpath(LabirintLocators.cover_xpath)
# cover_text = check_html_element_existing(cover_text)
# sell_this_book_button = book_page_tree.xpath('//div[@class=" book-navigation_item"]')


if __name__ == '__main__':

    required_statuses = ['Закупка завершена', 'Подача заявок', 'Работа комиссии']

    # TODO: приделать 500 закупок на страницу
    purchase_search_page_link = 'https://zakupki.gov.ru/epz/order/extendedsearch/results.html'
    main_page = PurchaseSearchPage(purchase_search_page_link)
    number_of_pages = main_page.find_number_of_pages()
    print(f'Количество страниц: {number_of_pages}')
    page_numbers = [number + 1 for number in range(number_of_pages)]

    for page_number in page_numbers:
        print(f'Находимся на странице: {page_number}')

        next_purchase_search_page_link = f'{purchase_search_page_link}?pageNumber={page_number}'
        main_page = PurchaseSearchPage(next_purchase_search_page_link)

        for purchase in main_page.purchases:
            status = main_page.get_status(purchase)

            if status not in required_statuses:
                print(f'Этот статус не совпадает с нужными нам: {status}')
                continue

            link = main_page.get_link_to_purchases(purchase)
            page = PurchasePage(link)

            # TODO: проверка, что это не последняя страница
