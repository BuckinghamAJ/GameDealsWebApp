import scrapy


class MetaCriticImageSpider(scrapy.Spider):
    name = "MetaCriticImageSpider"


    images = {}
    allDeals = []
    allDealIndex = 0

    def grabUrls(self):
        urls = [deal["metacriticURL"] for deal in self.allDeals]
        return urls


    def start_requests(self):

        urls = ["https://www.metacritic.com/game/xbox-one/resident-evil-4"]

        self.grabUrls()

        for index, url in enumerate(self.grabUrls()):
            self.allDealIndex = index
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        image = response.xpath('//img[contains(@class,"product_image")]/@src').get()
        urlUsed = response.request.url

        self.images[urlUsed] = image

        #yield image
