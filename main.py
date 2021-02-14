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
    def write_txt(name_txt, title, price, availability, json):
        file = open(name_txt, 'a', encoding='UTF-8')
        file.write('Title: ' + title + '\n')
        file.write('Price: ' + price + '\n')
        file.write('Availability: ' + availability + '\n')
        file.write('JSON: ' + json + '\n\n')
        file.close()


class ParseProducts(Parser):
    def __init__(self, get_url: str, max_page: int):
        super().__init__(get_url)
        self.pages = []
        self.max_page = max_page
        self.r_url = None

    def create_requests(self):
        for id_page in range(1, self.max_page + 1):
            self.r_url = str(self.get_url) + str(id_page)
            self.pages.append(requests.get(str(self.get_url)))  # str(id_page))
            self.status_request = requests.get(self.r_url)

    def create_single_page_requests(self):
        pass

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
            title_text, price_text, availability_text = text_404, text_404, text_404

            for el in html.select('.catalog-section-item'):
                attributes_dictionary = el.attrs
                json = attributes_dictionary['data-data']

                title = el.select('.catalog-section-item-name-wrapper')
                price = el.select('div.catalog-section-item-price-discount span')
                availability = el.select('.catalog-section-item-quantity')

                title_text = title[0].text if title else text_404
                price_text = price[0].text if price else text_404
                availability_text = availability[0].text if availability else text_404

                Parser.write_txt('products.txt', title_text, price_text, availability_text, json)


# my_site = Parser('http://absolute-nature-products.develop-web.site')
# my_site.create_requests()
# my_site.get_status_request()

my_site_products_data = ParseProducts('https://greatsteve.ru/catalog/appleiphone/', 1)
my_site_products_data.create_requests()
my_site_products_data.create_single_page_requests()

# my_site_products_data.get_status_request()
# my_site_products_data.get_data()
