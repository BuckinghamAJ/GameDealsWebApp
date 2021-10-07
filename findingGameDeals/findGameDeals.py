from findingGameDeals.PSDealScraper import PSDealSpider
from findingGameDeals.XboxDealScraper import XboxDealSpider
from scrapy.crawler import CrawlerProcess
from findingGameDeals.SwitchDealScraper import SwitchDealSpider
import pymysql
import difflib

def main():

    mainPSDeal = PSDealSpider
    mainXboxDeal = XboxDealSpider()
    mainSwitchDeal = SwitchDealSpider()


    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(mainPSDeal)
    process.start()
    process.join

    mainXboxDeal.start_scrap()
    mainSwitchDeal.start_scrap()

    videoGameDeals = placeAllDealsIntoOneDictionary(mainPSDeal.allDeals, mainXboxDeal.allDeals, mainSwitchDeal.allDeals)


    videoGameDeals = createscrapyURLs(videoGameDeals)


    placeInSQLDatabase(videoGameDeals)


def placeAllDealsIntoOneDictionary(PSDeals, XboxDeals, SwitchDeals):
    allDeals = []
    titles = []


    for XboxDeal in XboxDeals:

        result, title = notalreadyAddedTitle(XboxDeal["title"], titles)
        if result:
            addXboxDealDict = {
                "title": XboxDeal["title"],
                "Xbox Normal Price": XboxDeal["normal price"],
                "Xbox Deal Price": XboxDeal["deal price"],
                "Xbox Link": XboxDeal["link"],
                "image": XboxDeal["image"]
            }
            allDeals.append(addXboxDealDict)
            titles.append(XboxDeal["title"].lower())
        else:
            index = titles.index(title.lower())
            alreadyAddedDeal = allDeals[index]

            alreadyAddedDeal["Xbox Normal Price"] = XboxDeal["normal price"]
            alreadyAddedDeal["Xbox Deal Price"] = XboxDeal["deal price"]
            alreadyAddedDeal["Xbox Link"] = XboxDeal["link"]

    for PSdeal in PSDeals:
        #if PSdeal["title"] not in titles:
        result, title = notalreadyAddedTitle(PSdeal["title"], titles)
        if result:
            addPSDealDict = {
                "title": PSdeal["title"],
                "PS Normal Price": PSdeal["normal price"],
                "PS Deal Price": PSdeal["deal price"],
                "PS Link": PSdeal["link"],
                "image": PSdeal["image"]
            }
            allDeals.append(addPSDealDict)
            titles.append(PSdeal["title"].lower())
        else:
            index = titles.index(title.lower())
            alreadyAddedDeal = allDeals[index]
            alreadyAddedDeal["PS Normal Price"] = PSdeal["normal price"]
            alreadyAddedDeal["PS Deal Price"] = PSdeal["deal price"]
            alreadyAddedDeal["PS Link"] = PSdeal["link"]

    for SwitchDeal in SwitchDeals:
        result, title = notalreadyAddedTitle(SwitchDeal["title"], titles)
        if result:
            addSwitchDealDict = {
                "title": SwitchDeal["title"],
                "Switch Normal Price": SwitchDeal["normal price"],
                "Switch Deal Price": SwitchDeal["deal price"],
                "Switch Link": SwitchDeal["link"],
                "image": SwitchDeal["image"]
            }
            allDeals.append(addSwitchDealDict)
            titles.append(SwitchDeal["title"].lower())
        else:
            index = titles.index(title.lower())
            alreadyAddedDeal = allDeals[index]

            alreadyAddedDeal["Switch Normal Price"] = SwitchDeal["normal price"]
            alreadyAddedDeal["Switch Deal Price"] = SwitchDeal["deal price"]
            alreadyAddedDeal["Switch Link"] = SwitchDeal["link"]

    return allDeals

def notalreadyAddedTitle(title, currentlyAddedTitles):

    if title.lower() in currentlyAddedTitles:
        return False, title
    else:
        #Seeing how close the name matches since naming on different sites can be slightly different
        for addedTitle in currentlyAddedTitles:
            seq = difflib.SequenceMatcher(None, title.lower(), addedTitle.lower())
            ratio = seq.ratio()*100

            title_number = [int(s) for s in title.split() if s.isdigit()]
            addedTitle_number = [int(s) for s in addedTitle.split() if s.isdigit()]

            if title_number != addedTitle_number:
                continue
            else:
                #  
                if ratio >= 96:
                    return False, addedTitle
                else:
                    continue

    return True, None



def createscrapyURLs(videoGameDeals):

    for deal in videoGameDeals:
        if "Switch Link" in deal:
            urlTitleFormat = deal["title"].lower().replace(" ", "-").replace("®", "").replace("™", "").replace(":", "").replace("'","")
            metacriticURL = "https://www.metacritic.com/game/switch/" + urlTitleFormat
            deal["metacriticURL"] = metacriticURL
        elif "Xbox Link" in deal:
            urlTitleFormat = deal["title"].lower().replace(" ", "-").replace("®","").replace("™", "").replace(":","").replace("'","")
            metacriticURL = "https://www.metacritic.com/game/xbox-one/" + urlTitleFormat
            deal["metacriticURL"] = metacriticURL
        elif "PS Link" in deal:
            urlTitleFormat = deal["title"].lower().replace(" ", "-").replace("®", "").replace("™", "").replace(":", "").replace("'","")
            metacriticURL = "https://www.metacritic.com/game/playstation-4/" + urlTitleFormat
            deal["metacriticURL"] = metacriticURL

    return videoGameDeals

def placeInSQLDatabase(videoGameDeals):

    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='22ehH0C2!View2011!',
                                 db='Game_Deals',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    with connection.cursor() as cursor:
        cursor.execute("UPDATE deals SET updated = FALSE;")
        connection.commit()

        for deal in videoGameDeals:
            title = deal["title"].replace("'","\\'")
            metacriticURL = deal["metacriticURL"]
            imageURL = deal["image"]

            try:
                PS_normal_price = float(deal["PS Normal Price"].replace("$", ""))
                PS_deal_price = float(deal["PS Deal Price"].replace("$", ""))
                PS_link = deal["PS Link"]
            except:
                PS_normal_price = "NULL"
                PS_deal_price = "NULL"
                PS_link = "NULL"

            try:
                Xbox_normal_price = float(deal["Xbox Normal Price"].replace("$", ""))
                Xbox_deal_price = float(deal["Xbox Deal Price"].replace("$", ""))
                Xbox_link = deal["Xbox Link"]
            except:
                Xbox_normal_price = "NULL"
                Xbox_deal_price = "NULL"
                Xbox_link = "NULL"

            try:
                Switch_normal_price = float(deal["Switch Normal Price"].replace("$", ""))
                Switch_deal_price = float(deal["Switch Deal Price"].replace("$", ""))
                Switch_link = deal["Switch Link"]
            except:
                Switch_normal_price = "NULL"
                Switch_deal_price = "NULL"
                Switch_link = "NULL"



            existStatement = f"SELECT * FROM deals WHERE title='{title}';"
            try:
                cursor.execute(existStatement)
                exists = cursor.fetchall()
            except:
                exists = None

            if exists:
                insertStatement = f"""
                update deals set PS_normal_price={PS_normal_price}, PS_deal_price={PS_deal_price}, PS_link='{PS_link}', 
                    Xbox_normal_price={Xbox_normal_price}, Xbox_deal_price={Xbox_deal_price}, Xbox_link='{Xbox_link}',
                    Switch_normal_price={Switch_normal_price}, Switch_deal_price={Switch_deal_price}, Switch_link='{Switch_link}', updated=TRUE
                where title='{title}';"""
            else:
                insertStatement = f"""
        insert into deals (`title`, `PS_normal_price`, `PS_deal_price`, `PS_link`, `Xbox_normal_price`, `Xbox_deal_price`, `Xbox_link`, `Switch_normal_price`, `Switch_deal_price`, `Switch_link`, `metacriticURL`,`imageURL`,`updated`) 
        values('{title}',{PS_normal_price},{PS_deal_price},'{PS_link}',{Xbox_normal_price},{Xbox_deal_price},'{Xbox_link}',{Switch_normal_price},{Switch_deal_price},'{Switch_link}','{metacriticURL}','{imageURL}',TRUE);
    """

            cursor.execute(insertStatement)
            connection.commit()

        cursor.execute("DELETE FROM deals Where PS_deal_price IS NULL AND Xbox_deal_price IS NULL AND Switch_deal_price IS NULL;")
        cursor.execute("DELETE FROM deals Where updated=FALSE;")

    connection.commit()


if __name__ == "__main__":
    main()
