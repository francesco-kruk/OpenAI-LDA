from bs4 import BeautifulSoup
import requests

from_page = 1
to_page = 6
review={}
review_list=[]


response = requests.get(f"https://www.producthunt.com/products/openai/reviews")
web_page = response.text

if response.status_code == 200:
    soup = BeautifulSoup(web_page, "html.parser")
    review_elements = soup.find_all("div", {"class": "flex direction-column"})

    for review_element in review_elements:
        review["review_name"] = review_element.find("a", {"class": "color-darker-grey fontSize-16 fontWeight-600"}).text
        review["review_score"] = review_element.find("div", {"class": "flex direction-row"}).find('img').get('alt')
        if review_element.find("p", {"class": "styles_htmlText__iftLe"}) == None:
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
