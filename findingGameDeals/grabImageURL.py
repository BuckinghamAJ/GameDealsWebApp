import pymysql
from findingGameDeals.MetacriticImageFinder import MetaCriticImageSpider
from scrapy.crawler import CrawlerProcess


def main():
    allDealsInDatabase = getAllDealsStored()

    callMetaCriticImageSpider(allDealsInDatabase)


def getAllDealsStored():

    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='Password1',
                                 db='Game_Deals',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM deals WHERE `imageURL` IS NULL")
        allDeals = cursor.fetchall()

    return allDeals

def callMetaCriticImageSpider(allDealsInDatabase):
    mainMetaCriticSpider = MetaCriticImageSpider
    mainMetaCriticSpider.allDeals = allDealsInDatabase

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(mainMetaCriticSpider)
    process.start()

    updateDatabaseWithImages(mainMetaCriticSpider.images)

def updateDatabaseWithImages(images):
    
    # Could have a connection setup globally instead of locally?
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='Password1',
                                 db='Game_Deals',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    with connection.cursor() as cursor:
        for imageKey in images:
            updateStatement = f"UPDATE deals SET imageURL='{images[imageKey]}' WHERE metacriticURL='{imageKey}';"

            cursor.execute(updateStatement)

    connection.commit()

if __name__ == "__main__":
    main()
