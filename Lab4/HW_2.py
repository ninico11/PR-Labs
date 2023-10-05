import socket
from bs4 import BeautifulSoup

HOST = '127.0.0.1'  # IP address of your web server (localhost in this case)
PORT = 8082  # Port your web server is listening on

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Define the route to the products listing page
products_listing_route = '/products'


# Function to parse product details from a product page
def parse_product_page(response_content):
    soup = BeautifulSoup(response_content, 'html.parser')
    product_details = {}

    # Extract product details from the HTML
    product_details['name'] = soup.find('strong', text='name:').next_sibling.strip()
    product_details['author'] = soup.find('strong', text='author:').next_sibling.strip()
    product_details['price'] = float(soup.find('strong', text='price:').next_sibling.strip())
    product_details['description'] = soup.find('strong', text='description:').next_sibling.strip()

    return product_details


# Function to extract product routes from the products listing page
def extract_product_routes(response_content):
    soup = BeautifulSoup(response_content, 'html.parser')
    product_routes = []

    # Find all the product links in the HTML
    product_links = soup.find_all('a', href=True)

    for link in product_links:
        product_routes.append(link['href'])

    return product_routes


# Send an HTTP GET request to the products listing page
request = f"GET {products_listing_route} HTTP/1.1\r\nHost: {HOST}:{PORT}\r\n\r\n"
client_socket.send(request.encode('utf-8'))

# Receive the response from the server
response_data = client_socket.recv(4096).decode('utf-8')

# Check if it's the products listing page
if products_listing_route in response_data:
    product_routes = extract_product_routes(response_data)
    # Initialize a dictionary to store product details
    product_details = {}

    # Iterate through the product routes and make requests to the web server
    for route in product_routes:
        # Send an HTTP GET request for each product page
        request = f"GET {route} HTTP/1.1\r\nHost: {HOST}:{PORT}\r\n\r\n"
        client_socket.send(request.encode('utf-8'))

        # Receive the response from the server
        response_data = client_socket.recv(4096).decode('utf-8')

        # Check if it's a product page and parse the product details
        if route.startswith('/product/'):
            product_details[route] = parse_product_page(response_data)

    # Close the client socket
    client_socket.close()

    # Print the product details
    for route, details in product_details.items():
        print(f"Route: {route}")
        print("Product Details:")
        for key, value in details.items():
            print(f"{key}: {value}")
        print("\n")

else:
    print("Products listing page not found in the response.")

