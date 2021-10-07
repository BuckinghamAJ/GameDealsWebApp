from findingGameDeals.SwitchDealScraper import SwitchDealSpider
from findingGameDeals.XboxDealScraper import XboxDealSpider
from findingGameDeals.PSDealScraper import PSDealSpider
from scrapy.crawler import CrawlerProcess

def test():
    #mainSwitchDeal = SwitchDealSpider()
    #mainSwitchDeal.start_scrap()

    #print(mainSwitchDeal.allDeals)


    """
    mainPSDeal = PSDealSpider

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(mainPSDeal)
    process.start()
    process.join

    print(mainPSDeal.allDeals)
    """

    mainXboxDeal = XboxDealSpider()
    mainXboxDeal.start_scrap()

    #print(mainXboxDeal.allDeals)

if __name__ == "__main__":
    test()