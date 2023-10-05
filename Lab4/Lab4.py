import socket
import signal
import sys
import threading
import re
from dict_to_json import dictor, dict_to_html_manual, create_product_html

# Define the server's IP address and port
HOST = '127.0.0.1'  # IP address to bind to (localhost)
PORT = 8082  # Port to listen on
# Create a socket that uses IPv4 and TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the address and port
server_socket.bind((HOST, PORT))
# Listen for incoming connections
server_socket.listen(5)  # Increased backlog for multiple simultaneous connections
print(f"Server is listening on {HOST}:{PORT}")


# Function to handle client requests
def handle_request(client_socket):
    # Receive and print the client's request data
    request_data = client_socket.recv(1024).decode('utf-8')
    print(f"Received Request:\n{request_data}")

    # Split the request data into lines
    request_lines = request_data.split('\n')

    # Check if there are at least two lines in the request
    if len(request_lines) < 2:
        # Invalid request, close the connection or send a 400 Bad Request response
        response_content = '400 Bad Request'
        status_code = 400
    else:
        # Parse the request to get the HTTP method and path
        request_line = request_lines[0].strip().split()
        if len(request_line) != 3:
            # Invalid request line format, close the connection or send a 400 Bad Request response
            response_content = '400 Bad Request'
            status_code = 400
        else:
            method = request_line[0]
            path = request_line[1]

            # Initialize the response content and status code
            response_content = ''
            status_code = 200
            products = re.compile("/product/[0-9]")
            # Define a simple routing mechanism
            if path == '/':
                response_content = 'Hello, World!'
            elif path == '/about':
                response_content = 'This is the About page.'
            elif path == '/home':
                response_content = 'This is the Home page.'
            elif path == '/contacts':
                response_content = 'This is the Contacts page'
            elif path == '/products':
                response_content = create_product_html(dictor())
            elif products.match(path):
                if (int(path[9:])) < len(dictor()):
                    response_content = dict_to_html_manual(dictor()[int(path[9:])])
                else:
                    response_content = 'Product page'
            else:
                response_content = '404 Not Found'
                status_code = 404
            # Rest of your routing logic here...
    # Prepare the HTTP response
    response = f'HTTP/1.1 {status_code} OK\nContent-Type: text/html\n\n{response_content}'
    client_socket.send(response.encode('utf-8'))
    # Close the client socket
    client_socket.close()


# Function to handle Ctrl+C and other signals
def signal_handler(sig, frame):
    print("\nShutting down the server...")
    server_socket.close()
    sys.exit(0)


# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)
while True:
    # Accept incoming client connections
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")
    # Create a thread to handle the client's request
    client_handler = threading.Thread(target=handle_request, args=(client_socket,))
    client_handler.start()
