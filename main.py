import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import math

option = webdriver.ChromeOptions()
option.add_argument("--log-level=OFF")
option.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(options=option)

url = "https://skin.club/en/cases/open/covert"
case_url = "https://skin.club/en"

driver.get(case_url)
driver.set_window_position(1,1)
driver.set_window_size(1,1)


wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'case-entity__button')))

elements = driver.find_elements(By.TAG_NAME, 'a')

matching_urls = []

for element in elements:
    href = element.get_attribute("href")
    if href and href.startswith("https://skin.club/en/cases/open/"):
        matching_urls.append(href)

driver.quit()




def get_roi(url):
    driver = webdriver.Chrome(options=option)
    print("")
    driver.get(url)
    driver.set_window_position(1,1)
    driver.set_window_size(1,1)

    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'price')))
    time.sleep(10)


    we_chances = driver.find_elements(By.CLASS_NAME, 'chance-text')
    we_prices = driver.find_elements(By.CLASS_NAME, 'case-skin__price')
    we_case_price = driver.find_elements(By.CLASS_NAME, 'price')
    price = 0.00
    for pr in we_case_price:
        pattern = r'\$(?:100\.00|\d{1,2}(?:\.\d{2})?)'
        if re.match(pattern, pr.text):
            price = float(pr.text.strip("$"))

    chances = []

    for ch in we_chances:
        chances.append(ch.text)

    values = []

    for v in we_prices:
        values.append(v.text)

    driver.quit()


    avg = calculate_weighted_average(chances, values, price)

    print("Case: " + url)
    print("Expected ROI: ", avg)


def calculate_weighted_average(chances, values, price):
    if len(chances) != len(values):
        raise ValueError("Not the fecking same.")
    
    weighted_sum = 0

    use = len(chances)
    use_values = values[-use:]
    
    for chance_str, value_str in zip(chances, use_values):
        chance = float(chance_str.strip('%')) / 100
        match = re.search(r'\$\d+\.\d+', value_str)

        if match:
            dollar_amount_str = match.group(0) 
            value = float(dollar_amount_str[1:])
        weighted_sum += chance * value
    
    roi = (weighted_sum / price)
    return f"{roi*100:.2f}%"


for url in matching_urls:
    try:
        get_roi(url)
    except:
        print("Fuck")
