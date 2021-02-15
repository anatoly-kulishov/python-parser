import requests
from bs4 import BeautifulSoup as BS


class Parser:
    def __init__(self, get_url: str):
        self.status_request = None
        self.get_url = get_url

    def create_requests(self):
        self.status_request = requests.get(str(self.get_url))

    def get_status_request(self):
        if self.status_request.status_code == 200:
            status_request = True
        else:
            status_request = self.status_request.status_code
        print(self.get_url, '\n * Status Request:', str(status_request))

    @staticmethod
    def write_txt(name_txt, title, price):
        file = open(name_txt, 'a', encoding='UTF-8')
        file.write('Title: ' + title + '\n')
        file.write('Price: ' + price + '\n\n')
        file.close()


class ParseProducts(Parser):
    def __init__(self, get_url: str, max_page: int):
        super().__init__(get_url)
        self.pages = []
        self.max_page = max_page
        self.r_url = None

    def create_request_for_several_pages(self):
        for id_page in range(1, self.max_page + 1):
            self.r_url = str(self.get_url) + str(id_page)
            self.pages.append(requests.get(str(self.get_url) + str(id_page)))
            self.status_request = requests.get(self.r_url)

    @staticmethod
    def create_single_page_requests(self):
        print('create_single_page_requests')

    def get_status_request(self):
        if self.status_request.status_code == 200:
            status_request = True
        else:
            status_request = self.status_request.status_code
        for id_page in range(1, self.max_page + 1):
            print(str(self.get_url), '\n * Status Request:', str(status_request))

    def get_data(self):
        for r in self.pages:
            html = BS(r.content, 'html.parser')
            text_404 = 'None'
            title_text, price_text = text_404, text_404

            for el in html.select('li.product'):
                title = el.select('.woocommerce-loop-product__title')
                price = el.select('.price')

                title_text = title[0].text if title else text_404
                price_text = price[0].text if price else text_404

                Parser.write_txt('products.txt', title_text, price_text)


# my_site = Parser('http://absolute-nature-products.develop-web.site')
# my_site.create_requests()
# my_site.get_status_request()

my_site_products_data = ParseProducts('http://absolute-nature-products.develop-web.site/shop/page/', 2)
my_site_products_data.create_request_for_several_pages()
my_site_products_data.get_status_request()
my_site_products_data.get_data()
