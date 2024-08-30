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
import re

from .scraper import SiteScrape

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
            price = price_whole.text.replace(".", "") + "." + price_fraction.text
        else:
            print(f"No price could be found for element {self.get_object_name(element)}")

        price = float(price)
        return price
        
    def get_object_discounted_price (self, element: Tag) -> Union[float, None]:

        try:
            price_tag = element.find('span', 'a-offscreen')
            price = re.search('[0-9]*,[0-9]{2}', price_tag.text).group(0).replace(".", "").replace(",", ".")
            price = float(price)
            return price
        
        except:
            return None
        
    def get_object_link(self, element: Tag) -> str:
        link = element.find(
            'a', 
            class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'
        )['href']

        return link

    def get_object_image_url (self, element: Tag) -> str:
        imgtag = element.find('img', class_='s-image')

        return imgtag['src']
