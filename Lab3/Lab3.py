# Import necessary libraries
from bs4 import BeautifulSoup
import requests
import re
import json

car_links = []


# Function to extract HTML document from a given URL
def getHTMLdocument(url):
    response = requests.get(url)
    return response.text


# Function to scrape car listings and return a list of links
def scrap(url_to_scrap, max_num_pag):
    current_url = url_to_scrap
    html_document = getHTMLdocument(current_url)
    soup = BeautifulSoup(html_document, 'html.parser')
    current_page = soup.find('li', class_='current')
    page_number = current_page.a.text
    if int(page_number) > max_num_pag:
        return "max_num_page is reached"
    else:
        # Find all the anchor tags with "href" attribute starting with "/ro/" and "class" containing "js-item-ad"
        for link in soup.find_all('a', attrs={'href': re.compile("/ro/"), 'class': re.compile("js-item-ad")}):
            car_links.append("https://999.md" + link.get('href'))
        # Check if there is a next page link
        next_page_link = current_page.find_next('li').find('a') if current_page else None
        # If a next page link exists, extract and print the href attribute
        if next_page_link:
            next_page_url = "https://999.md" + next_page_link['href']
        else:
            print("No next page link found.")
    return scrap(next_page_url, max_num_pag)

def info(url_scrap):
    html_document = getHTMLdocument(url_scrap)
    soup = BeautifulSoup(html_document, 'html.parser')
    data_dict = {}
    # Find all elements with class 'm-value'
    m_value_elements = soup.find_all('li', class_='m-value')

    # Iterate through the elements and extract the key-value pairs
    for element in m_value_elements:
        key_element = element.find('span', class_='adPage__content__features__key')
        value_element = element.find('span', class_='adPage__content__features__value')

        if key_element and value_element:
            key = key_element.text.strip()
            value = value_element.text.strip()
            data_dict[key] = value

    # Convert the dictionary to JSON
    json_data = json.dumps(data_dict, indent=4, ensure_ascii=False)

    # Print or save the JSON data as needed
    print(json_data)


# Example usage: Scrap the first 3 pages of car listings
scrap('https://999.md/ru/list/transport/cars', 1)
print(car_links)
info('https://999.md/ru/83845057')