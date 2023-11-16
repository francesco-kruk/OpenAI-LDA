from bs4 import BeautifulSoup
import requests

from_page = 1
to_page = 6
review={}
review_list=[]

for i in range(from_page, to_page + 1):
    response = requests.get(f"https://www.trustpilot.com/review/openai.com?page={i}")
    web_page = response.text

    if response.status_code == 200:
        soup = BeautifulSoup(web_page, "html.parser")
        review_elements = soup.find_all("div", {"class": "styles_cardWrapper__LcCPA"})

        for review_element in review_elements:
            review["review_name"] = review_element.find("span", {"class": "typography_heading-xxs__QKBS8"}).text
            review["review_score"] = review_element.find("div", {"class": "star-rating_starRating__4rrcf"}).find('img').get('alt')
            review["review_title"] = review_element.find("h2", {"class": "typography_heading-s__f7029"}).text
            if review_element.find("p", {"class": "typography_body-l__KUYFJ"}) == None:
                review_list.append(review)
                review = {}
                continue
            else:
                review["review_text"] = review_element.find("p", {"class": "typography_body-l__KUYFJ"}).text
            review_list.append(review)
            review = {}

    else:
        print("Failed to retrieve the page. Status code:", response.status_code)

print(review_list)