import socket
from bs4 import BeautifulSoup

# Define the server's IP address and port
HOST = '127.0.0.1'  # IP address of your web server (localhost in this case)
PORT = 8082  # Port your web server is listening on

# Define a list of routes to visit on your web server
routes_to_visit = ['/home', '/about', '/contacts', '/products']

# Initialize a dictionary to store product details
product_details = {}


# Function to parse product details from a product page
def parse_product_page(response_content):
    soup = BeautifulSoup(response_content, 'html.parser')
    product = {
        "name": soup.find('strong', string='name:').next_sibling.strip(),
        "author": soup.find('strong', string='author:').next_sibling.strip(),
        "price": float(soup.find('strong', string='price:').next_sibling.strip()),
        "description": soup.find('strong', string='description:').next_sibling.strip(),
    }
    return product


# Function to parse the product listing page and extract product routes
def parse_product_listing_page(response_content):
    soup = BeautifulSoup(response_content, 'html.parser')
    product_links = soup.find_all('a', href=True)
    product_routes = [link['href'] for link in product_links if link['href'].startswith('/product/')]
    return product_routes


# Iterate through the routes and make requests to the web server
for route in routes_to_visit:

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    # Send an HTTP GET request
    request = f"GET {route} HTTP/1.1\r\nHost: {HOST}:{PORT}\r\n\r\n"
    client_socket.send(request.encode('utf-8'))

    # Receive the response from the server
    response_data = client_socket.recv(4096).decode('utf-8')

    # Separate the headers and body of the response
    if '\r\n\r\n' in response_data:
        headers, response_content = response_data.split('\r\n\r\n', 1)
    else:
        # No headers found, treat the entire response_data as content
        headers = ""
        response_content = response_data

    # Check if it's a product page and parse the product details
    if route.startswith('/product/'):
        product_details[route] = parse_product_page(response_content)
    elif route == '/products':
        # Parse the product listing page to get product routes
        with open(f"{route.replace('/', '_')}.html", 'w') as f:
            f.write(response_content)
        product_routes = parse_product_listing_page(response_content)
        for product_route in product_routes:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((HOST, PORT))
            # Send requests for each product page
            request = f"GET {product_route} HTTP/1.1\r\nHost: {HOST}:{PORT}\r\n\r\n"
            client_socket.send(request.encode('utf-8'))
            product_response_data = client_socket.recv(4096).decode('utf-8')
            product_details[product_route] = parse_product_page(product_response_data)
    else:
        # For other pages, you can save the content
        with open(f"{route.replace('/', '_')}.html", 'w') as f:
            f.write(response_content)
# Close the client socket
client_socket.close()

# Print the product details
for route, details in product_details.items():
    print(f"Route: {route}")
    print("Product Details:")
    for key, value in details.items():
        print(f"{key}: {value}")
    print("\n")
