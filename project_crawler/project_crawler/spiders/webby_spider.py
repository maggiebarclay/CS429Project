# imports 
from urllib import response
import scrapy
import os

# spider
class WebbySpider(scrapy.Spider):
    
    # name of spider, do scrapy crawl webby to start
    name = "webby"

    # start url 
    allowed_domains = ['nookipedia.com']
    start_urls = ['https://nookipedia.com/wiki/List_of_villagers']

    def parse(self, response):
        print("\n\n\nPARSE STARTING NOW")

        # get the table rows from the nookipedia page, use these to attach urls to the base url
        table = response.xpath('//*[@id="mw-content-text"]/div/div[3]/table/tbody')
        rows = table.xpath('//tr//th[2]/a/@href')
        urlEnds = rows.extract()

        base_url = 'https://nookipedia.com'
        for url in urlEnds:
            yield scrapy.Request(((str(base_url) + str(url))), self.urlParse)

    def urlParse(self, response):

        # save page with unique name
        page = response.url.split("/")[-1]
        save_path = os.path.dirname(__file__)

        # all html pages will be saved in the folder htmlfiles
        filename = f'ac-{page}.html'
        completeName = os.path.join(save_path,  '../htmlFiles/', filename)         
        with open(completeName, 'wb') as f:
            f.write(response.body)
        print(f'Saved file {filename}')