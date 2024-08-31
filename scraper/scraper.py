from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup
from bs4.element import Tag
from typing import Union, Any
import pandas as pd
import time
import re
import psycopg2

class SiteScrape:

    driver: WebDriver
    home: str
    
    def __init__ (self):
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument('--remote-debugging-port=9222')
        service = Service('/usr/local/bin/chromedriver')

        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.maximize_window()

    def open_site (self) -> None:
        self.driver.get(self.home)

    def close (self) -> None:
        self.driver.quit()

    def get_searchbar (self) -> WebElement:
        pass

    def search(self, text: str) -> None:
        self.get_searchbar().send_keys(text, Keys.ENTER)
        WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located((By.TAG_NAME, "body"))
        )

    def get_objects (self) -> list[Tag]:
        pass

    def get_object_name (self, element: Tag) -> str:
        pass

    def get_object_price (self, element: Tag) -> float:
        pass

    def get_object_discounted_price (self, element: Tag) -> Union[float, None]:
        pass

    def get_object_link (self, element: Tag) -> str:
        pass

    def get_object_image_url (self, element: Tag) -> str:
        pass

    def get_and_save_objects (self, text: str) -> pd.DataFrame:
        time.sleep(3)
        self.open_site()
        time.sleep(3)
        self.search(text)
        objects = self.get_objects()

        columns = ['Name', 'Price', 'DiscountedPrice', 'Link', 'Image URL']

        extracted_objects = pd.DataFrame(columns=columns)

        to_df = []
        for obj in objects:
            name = self.get_object_name(obj)
            price = self.get_object_price(obj)
            discounted_price = self.get_object_discounted_price(obj)
            link = self.get_object_link(obj)
            image_url = self.get_object_image_url(obj)
            to_df.append([name, price, discounted_price, link, image_url])

        new_rows = pd.DataFrame(to_df, columns=columns)
        extracted_objects = pd.concat([extracted_objects, new_rows], ignore_index=True)

        return extracted_objects
