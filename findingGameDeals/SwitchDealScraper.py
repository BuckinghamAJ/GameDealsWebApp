from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import pymysql

class SwitchDealSpider():
    name = "SwitchDeals"
    url = "https://www.nintendo.com/games/game-guide/#filter/:q=&dFR[generalFilters][0]=Deals&dFR[howToShop][0]=On%20Nintendo.com&dFR[platform][0]=Nintendo%20Switch"
    SwitchDomain = "https://www.nintendo.com"
    allDeals = []

    def start_scrap(self):
        opts = Options()
        #opts.headless = True
        #assert opts.headless  # Operating in headless mode
        #browser = Firefox(options=opts, executable_path="/usr/local/bin/geckodriver")
        browser = Firefox(executable_path="/usr/local/bin/geckodriver")

        self.parseSalesAndDealsPage(browser)

        browser.get(self.url)

        self.parse_games(browser)

        browser.close()

    def parse_games(self, browser):
        delay = 60
        WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "main-link")))
        allDealsInPage = browser.find_elements_by_class_name("main-link")

        for gamedeal in allDealsInPage:
            try:
                listPrice = gamedeal.find_element_by_class_name("sale-price").text
                title = gamedeal.get_attribute("data-game-title")
                gamelink = gamedeal.get_attribute("href")
                originalPrice = gamedeal.find_element_by_class_name("strike").text
                image = gamedeal.find_element_by_class_name("boxart-container").find_element_by_tag_name("img").get_attribute("src")

                self.allDeals.append(
                    {
                        "title": title,
                        "normal price": originalPrice,
                        "deal price": listPrice,
                        "link": gamelink,
                        "image": image
                    })
            except:
                continue

        nextPage = browser.find_element_by_id("btn-load-more")

        if nextPage:
            try:
                nextPage.click()
                self.parse_games(browser)
            except:
                return


    def parseSalesAndDealsPage(self, browser):
        browser.get("https://www.nintendo.com/games/sales-and-deals/")

        delay = 60
        try:
            WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "games-offers-list-container")))
        except:
            return

        game_Offers = browser.find_elements_by_class_name("games-offers-list-container")

        for game_offer in game_Offers:
            games = game_offer.find_elements_by_class_name("quickview-game")

            for game in games:

                console = game.find_element_by_class_name("info").find_element_by_tag_name("p").text

                if console == "Nintendo Switch":

                    title = game.get_attribute("data-game-title")
                    link = game.get_attribute("href")
                    both_prices = game.find_element_by_class_name("price").text
                    deal_price = both_prices.split()[0]
                    normal_price = both_prices.split()[1]
                    image = game.find_element_by_class_name("boxart-container").find_element_by_tag_name("img").get_attribute("src")


                    self.allDeals.append(
                        {
                            "title": title,
                            "normal price": normal_price,
                            "deal price": deal_price,
                            "link": link,
                            "image": image
                        })
                else:
                    continue