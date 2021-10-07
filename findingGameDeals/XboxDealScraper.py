from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import pymysql

class XboxDealSpider():
    name ="XboxDeals"
    url = "https://www.xbox.com/en-us/games/xbox-one?cat=onsale"

    allDeals = []

    def start_scrap(self):
        opts = Options()
        opts.headless = True
        assert opts.headless  # Operating in headless mode
        #browser = Firefox(options=opts, executable_path="/usr/local/bin/geckodriver")
        browser = Firefox(executable_path="/usr/local/bin/geckodriver")

        browser.get(self.url)

        self.parse_games(browser)

        browser.close()

        self.removeNonGames()

    def parse_games(self, browser):
        delay = 60
        WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "m-product-placement-item")))
        allDealsInPage = browser.find_elements_by_class_name("m-product-placement-item")

        for gamedeal in allDealsInPage:
            try:
                listPrice = gamedeal.get_attribute("data-listprice")
                gamelink = gamedeal.find_element_by_tag_name("a").get_attribute("href")
                title = gamedeal.find_element_by_tag_name("h3").text
                originalPrice = gamedeal.find_element_by_tag_name("s").text
                image = gamedeal.find_element_by_class_name("c-image").get_attribute("src")
                self.allDeals.append(
                    {
                        "title": title.replace("’","'"),
                        "normal price": originalPrice.split("\n")[1],
                        "deal price": listPrice,
                        "link": gamelink,
                        "image": image
                    })
            except:
                continue

        nextPage = browser.find_element_by_class_name("paginatenext")

        if nextPage:
            try:
                nextPage.click()
                self.parse_games(browser)
            except:
                return

    def removeNonGames(self):
        nonGameIndicators = ["pack", "season pass", "chest", "episode", "additional", "expansion", "upgrade"]
        for index,deal in enumerate(self.allDeals):
            for indicator in nonGameIndicators:
                if indicator in deal["title"].lower():
                    del self.allDeals[index]


