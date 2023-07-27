import scrapy

class KitapSepetiSpider(scrapy.Spider):
    name = "kitapsepeti"
    start_urls = [
        'http://www.kitapsepeti.com/roman?stock=1&pg=1',  # replace with actual URL
    ]

    def parse(self, response):
        for book in response.css('div.productItem'):
            yield {
                'title': book.css('a.text-description.detailLink ::text').extract_first(),
                'author': book.css('a.text-title[id="productModelText"] ::text').extract_first(),
                'price': book.css('div.currentPrice ::text').extract_first().strip(),
                'publisher': book.css('.col.col-12.text-title.mt::text').get().strip(),
            }

        next_page = response.css('li.next a ::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
