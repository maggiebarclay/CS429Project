# imports 
import scrapy
import os


class WebbySpider(scrapy.Spider):
    name = "webby"

    def start_requests(self):
        urls = ['https://quotes.toscrape.com/page/1/']

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        save_path = os.path.dirname(__file__)
        filename = f'quotes-{page}.html'
        completeName = os.path.join(save_path,  '../htmlFiles/', filename)         
        with open(completeName, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')