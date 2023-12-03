from bs4 import BeautifulSoup
import requests
import csv

from_page = 1
to_page = 6
review_list = []
fields = ["Review score (out of 5)", "Review text"]

for i in range(from_page, to_page + 1):
    response = requests.get(f"https://www.trustpilot.com/review/openai.com?page={i}")
    web_page = response.text

    if response.status_code == 200:
        soup = BeautifulSoup(web_page, "html.parser")
        review_elements = soup.find_all("div", {"class": "styles_cardWrapper__LcCPA"})

        for review_element in review_elements:
            review = []
            #review.append(review_element.find("span", {"class": "typography_heading-xxs__QKBS8"}).text)
            score = review_element.find("div", {"class": "star-rating_starRating__4rrcf"}).find('img').get('alt')
            score_num = score[6]
            review.append(score_num)
            #review.append(review_element.find("h2", {"class": "typography_heading-s__f7029"}).text)
            if review_element.find("p", {"class": "typography_body-l__KUYFJ"}) == None:
                review_list.append(review)
                continue
            else:
                review.append(review_element.find("p", {"class": "typography_body-l__KUYFJ"}).text)
            review_list.append(review)

    else:
        print("Failed to retrieve the page. Status code:", response.status_code)

with open('Trustpilot.csv', 'w') as f:
    write = csv.writer(f)
    write.writerow(fields)
    write.writerows(review_list)