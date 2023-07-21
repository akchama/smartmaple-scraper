import scrapy

class KitapyurduSpider(scrapy.Spider):
    name = "kitapyurdu"
    page_number = 1
    start_urls = [
        f'https://www.kitapyurdu.com/index.php?route=product/category&page={page_number}&filter_category_all=true&path=1&filter_in_stock=1&sort=purchased_365&order=DESC&limit=3']

    def parse(self, response):
        for book in response.css('div.product-cr'):
            author = book.css('div.author span::text').get()
            old_price = book.css('div.price-old.price-passive span.value::text').get()
            new_price = book.css('div.price-new span.value::text').get()

            yield {
                'title': book.css('div.name a span::text').get(),
                'author': author.replace("Yazar: ", "") if author else "Unknown",
                'publisher': book.css('div.publisher span::text').get(),
                'product_info': book.css('div.product-info::text').get(),
                'old_price': old_price.replace("Üretici Liste Fiyatı:", "") if old_price else "Unknown",
                'new_price': new_price.replace("Kitapyurdu Fiyatı:", "") if new_price else "Unknown"
            }

        # Going to next page
        self.page_number += 1
        next_page_url = f'https://www.kitapyurdu.com/index.php?route=product/category&page={self.page_number}&filter_category_all=true&path=1&filter_in_stock=1&sort=purchased_365&order=DESC&limit=3'

        yield scrapy.Request(url=next_page_url, callback=self.parse)
