from pages.main import MainPage

    # cover_text = tree_cover.xpath(LabirintLocators.cover_xpath)
    # cover_text = check_html_element_existing(cover_text)
    # sell_this_book_button = book_page_tree.xpath('//div[@class=" book-navigation_item"]')



if __name__ == '__main__':
    main_page = MainPage()
    main_page.get_tree()
    main_page.get_purchases()

    for purchase in main_page.purchases:
        main_page.get_link_to_purchases(purchase)

