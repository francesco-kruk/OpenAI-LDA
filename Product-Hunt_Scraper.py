from bs4 import BeautifulSoup
import requests

review = {}
review_list = []
count = 0

response = requests.get(f"https://www.producthunt.com/products/openai/reviews")
web_page = response.text

"""
To add more elements per page could use Postman/Insomnia as shown in https://www.youtube.com/watch?v=DqtlR0y0suo
"""

if response.status_code == 200:
    soup = BeautifulSoup(web_page, "html.parser")
    target = soup.find("div", {"class": "flex direction-column flex-column-gap-8 mt-6 mb-default"})
    review_elements = target.findChildren("div", recursive=False)
    print(review_elements)

    for review_element in review_elements:
        review["review_name"] = review_element.find("a", {"class": "color-darker-grey fontSize-16 fontWeight-600"}).text
        # review["review_score"] = review_element.find("div", {"class": "flex direction-row"}).find('img').get('alt')
        # Score could be implemented by going through the stars and counting how many filled in
        if review_element.find("div", {"class": "styles_htmlText__iftLe"}) == None:
            review_list.append(review)
            review = {}
            continue
        else:
            review["review_text"] = review_element.find("div", {"class": "styles_htmlText__iftLe"}).text
        review_list.append(review)
        review = {}
        count = count + 1
        print(count)

else:
    print("Failed to retrieve the page. Status code:", response.status_code)

print(review_list)