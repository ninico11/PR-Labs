from bs4 import BeautifulSoup
import requests
import json


# Function to extract HTML document from a given URL
def getHTMLdocument(url):
    response = requests.get(url)
    return response.text


def info(url_scrap, output_file_name):
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

    # Specify the output JSON file name
    with open(output_file_name, 'w', encoding='utf-8') as json_file:
        # Write the JSON data to the file
        json.dump(data_dict, json_file, indent=4, ensure_ascii=False)


info('https://999.md/ru/83845057', 'cars.json')
