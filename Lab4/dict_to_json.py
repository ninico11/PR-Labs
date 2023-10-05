import json


def dictor():
    with open('products.json', 'r') as JSON:
        json_dict = json.load(JSON)
    return json_dict


def dict_to_html_manual(data_dict):
    html = "<ul>"
    for key, value in data_dict.items():
        html += f"<li><strong>{key}:</strong> {value}</li>"
    html += "</ul>"
    return html


def create_product_html(products):
    html = "<html>\
                <head>\
                <title>Products</title>\
                </head>\
                <body>\
                <ul>"

    # Iterate through the list of products and create a list item for each
    for index, product in enumerate(products):
        html += '<li>\n'
        html += f'<a href="/product/{index}">{product["name"]}</a>\n'
        html += '</li>\n'

    html += "</ul>\
                </body>\
                </html>"

    return html
