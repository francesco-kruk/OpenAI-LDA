from bs4 import BeautifulSoup
import requests
import csv

from_page = 1
to_page = 2
review_list = []
fields = ["Review text"]

for i in range(from_page, to_page + 1):
    response = requests.get(f"https://omr.com/de/reviews/product/openai-chatgpt/all/{i}")
    web_page = response.text

    if response.status_code == 200:
        soup = BeautifulSoup(web_page, "html.parser")
        review_elements = soup.find_all("div", {"class": "row mb-4 pb-1 justify-start"})

        for review_element in review_elements:
            review = []
            if review_element.find("div", {"class": "pl-2 answer positive"}) == None:
                continue
            else:
                review.append(review_element.find("div", {"class": "pl-2 answer positive"}).text)
            if review_element.find("div", {"class": "pl-2 answer negative"}) == None:
                continue
            else:
                review[0] = review[0] + review_element.find("div", {"class": "pl-2 answer negative"}).text
            if review_element.find("div", {"class": "pl-2 answer neutral"}) == None:
                continue
            else:
                review[0] = review[0] + review_element.find("div", {"class": "pl-2 answer neutral"}).text
            review_list.append(review)

    else:
        print("Failed to retrieve the page. Status code:", response.status_code)

with open('OMR.csv', 'w') as f:
    write = csv.writer(f)
    write.writerow(fields)
    write.writerows(review_list)