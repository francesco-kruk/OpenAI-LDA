from bs4 import BeautifulSoup
import requests
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time

driver = webdriver.Chrome()
driver.get("https://www.producthunt.com/products/openai/reviews")

while True:
    try:
        button = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, "//button[@class='styles_reset__1_PU9 styles_button__7X8Df styles_full__wgSm4 mb-8']")))
        # button = driver.find_element(By.XPATH,"//button[@class=
        #                                       'styles_reset__1_PU9 styles_button__7X8Df styles_full__wgSm4 mb-8']")
        button.click()
    except:
        print("Page loaded!")
        break

print("Progressing")
page_source = driver.page_source
review_list = []
fields = ["Review text"]

# response = requests.get("https://www.producthunt.com/products/openai/reviews")
# web_page = response.text

soup = BeautifulSoup(page_source, "html.parser")
target = soup.find("div", {"class": "flex direction-column flex-column-gap-8 mt-6 mb-default"})
review_elements = target.findChildren("div", recursive=False)

for review_element in review_elements:
    review = []
    if review_element.find("div", {"class": "styles_htmlText__iftLe"}) == None:
        review_list.append(review)
        continue
    else:
        review.append(review_element.find("div", {"class": "styles_htmlText__iftLe"}).text)
    review_list.append(review)

with open('Product_Hunt.csv', 'w') as f:
    write = csv.writer(f)
    write.writerow(fields)
    write.writerows(review_list)
