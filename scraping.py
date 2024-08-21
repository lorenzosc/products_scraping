from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup
from bs4.element import Tag
from typing import Union, Any
import pandas as pd
import time
import re

class SiteScrape:

    driver: WebDriver
    home: str
    
    def __init__ (self):
        options = Options()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)

    def open_site (self) -> None:
        self.driver.get(self.home)

    def get_searchbar (self) -> WebElement:
        pass

    def search(self, text: str) -> None:
        self.get_searchbar().send_keys(text)

    def get_objects (self) -> list[Tag]:
        pass

    def get_object_name (self, element: Tag) -> str:
        pass

    def get_object_price (self, element: Tag) -> float:
        pass

    def get_object_discounted_price (self, element: Tag) -> Union[float, None]:
        pass

    def get_and_save_objects (self, text: str) -> pd.DataFrame:
        self.open_site()
        self.search(text)
        objects = self.get_objects()

        columns = ['Name', 'Price', 'DiscountedPrice']

        extracted_objects = pd.DataFrame(columns=columns)

        to_df = []
        for obj in objects:
            name = self.get_object_name(obj)
            price = self.get_object_price(obj)
            discounted_price = self.get_object_discounted_price(obj)
            to_df.append([name, price, discounted_price])

        new_rows = pd.DataFrame(to_df, columns=columns)
        extracted_objects = pd.concat([extracted_objects, new_rows], ignore_index=True)

        return extracted_objects

class AmazonScrape(SiteScrape):

    def __init__ (self):
        super().__init__()
        self.home = "https://www.amazon.com.br/"

    def get_searchbar (self) -> WebElement:
        return self.driver.find_element(By.ID, 'twotabsearchtextbox')

    def get_objects (self) -> list[Tag]:
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        return soup.find_all('div', {'data-component-type': 's-search-result'})
    
    def get_object_name (self, element: Tag) -> str:
        return element.h2.text().strip()
    
    def get_object_price (self, element: Tag) -> float:
        price_whole = element.find('span', 'a-price-whole')
        price_fraction = element.find('span', 'a-price-fraction')

        if price_whole and price_fraction:
            price = price_whole.text + price_fraction.text
        else:
            print(f"No price could be found for element {self.get_object_name(element)}")

        price = float(price)
        return price
        
    def get_object_discounted_price (self, element: Tag) -> Union[float, None]:

        try:
            price_tag = element.find('span', 'a-offscreen')
            price = re.search('[0-9]*,[0-9]{2}', price_tag.text).group(0)
            price = float(price)
            return price
        
        except:
            return None
        
    

class PichauScrape(SiteScrape):
    pass

class MagazineLuizaScrape(SiteScrape):
    pass

class KabumScrape(SiteScrape):
    pass

if __name__ == "__main__":

    amazon = AmazonScrape()
    amazon.open_site()
    amazon.search("Cadeira Gamer")
    chairs = amazon.get_objects()
    for chair in chairs:
        price = amazon.get_object_price(chair)
        discounted_price = amazon.get_object_discounted_price(chair)



