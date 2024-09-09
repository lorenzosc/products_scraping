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
from selenium_stealth import stealth
from bs4 import BeautifulSoup
from bs4.element import Tag
import time
from pytesseract import image_to_string
import pytesseract
import cv2
import random
from PIL import Image
from io import BytesIO
import base64
import numpy as np
import requests


# Wasn't enough, didn't work properly
def tesseract_solve (img) -> str:
    gry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    (h, w) = gry.shape[:2]
    gry = cv2.resize(gry, (w*2, h*2))
    cls = cv2.morphologyEx(gry, cv2.MORPH_CLOSE, None)
    thr = cv2.threshold(cls, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    txt = image_to_string(thr)
    return txt

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

options = Options()

options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("start-maximized")
options.add_argument('--disable-popup-blocking')
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--headless")

driver = webdriver.Chrome(options=options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
stealth(driver,
    languages=["en-US", "en"],
    vendor="Google Inc.",
    platform="Win32",
    webgl_vendor="Intel Inc.",
    renderer="Intel Iris OpenGL Engine",
    fix_hairline=True,
    )

time.sleep(1)

driver.get("https://www.amazon.com.br/")
espera = 3*random.random()

# time.sleep(espera)
soup = BeautifulSoup(driver.page_source, 'html.parser')
captcha_form = soup.find('form', {'method': 'get', 'action': "/errors/validateCaptcha"})
if captcha_form:
    print("I'm in the captcha page")
    img_element = driver.find_element(By.TAG_NAME, "img")
    url = img_element.get_attribute('src')
    response = requests.get(url)

    # Decode the Base64 string to image data
    image_data = response.content

    image_np = np.frombuffer(image_data, np.uint8)

    image_cv = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

    txt = tesseract_solve(image_cv)

    print(txt)

else:
    print("I'm in the main page")
time.sleep(10)