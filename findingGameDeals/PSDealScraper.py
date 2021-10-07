import scrapy
import pymysql

class PSDealSpider(scrapy.Spider):
    name = "PSDeals"
    PSdomain = "https://store.playstation.com"
    urls = []

    allDeals = []

    def start_requests(self):
        urls = ["https://store.playstation.com/en-us/grid/STORE-MSF77008-WEEKLYDEALS/1"]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        dealContainer = response.xpath('//div[contains(@class,"grid-cell-row__container")]')

        categoryOfDealsLinks = dealContainer.xpath('.//a[contains(@class,"internal-app-link")]/@href').getall()


        for link in categoryOfDealsLinks:
            full_link = self.PSdomain + link + "/1?gameContentType=games%2Cbundles"
            yield scrapy.Request(url=full_link, callback=self.parse_PSDeals)


    def parse_PSDeals(self, response):

        #cell_body = response.xpath('//div[contains(@class, "grid-cell__body")]')
        cell_game = response.xpath('//div[contains(@class, "grid-cell--game")]')


        for game in cell_game:

            body = game.xpath('.//div[contains(@class, "grid-cell__body")]')

            console = body.xpath('.//div[contains(@class, "grid-cell__left-detail--detail-1")]/text()').get()

            if console == "PS4":

                imageURL = game.xpath('.//div[contains(@class, "product-image__img--main")]/img/@src').get()


                self.allDeals.append({
                    'title' : body.xpath('.//div[contains(@class, "grid-cell__title")]/span/@title').get().replace("’","'"),
                    'normal price' : body.xpath('.//span[contains(@class,"price-display__strikethrough")]/div/text()').get(),
                    'deal price':  body.xpath('.//h3[contains(@class,"price-display__price")]/text()').get(),
                    'link': self.PSdomain + body.xpath('.//a[contains(@class,"internal-app-link")]/@href').get(),
                    'image': imageURL
                })
            else:
                continue

        next_page_partial_url = response.xpath('//a[contains(@class,"paginator-control__next")]/@href').get()

        if next_page_partial_url:
            next_page_url = self.PSdomain + next_page_partial_url
            yield scrapy.Request(url=next_page_url, callback=self.parse_PSDeals)


    def grabAllPSDeals(self):
        return self.allDeals

    def placeInDatabase(self):
        PSDeals = self.allDeals

        connection = pymysql.connect(host='localhost',
                             user='user',
                             password='passwd',
                             db='db',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

        with connection.cursor() as cursor:
            for deal in PSDeals:
                title = deal["title"]
                normPrice = float(deal["normal price"].replace("$",""))
                dealPrice = float(deal["deal price"].replace("$",""))
                link = deal["link"]

                insertStatement = f"Insert INTO Deals (title, normal_price, deal_price, link) " \
                    f"VALUES (`{title}`, {normPrice}, {dealPrice}, `{link}`)"

                cursor.execute(insertStatement)

        connection.commit()