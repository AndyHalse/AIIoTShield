# Import necessary libraries
import socket

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_address = ('localhost', 10000)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    connection, client_address = sock.accept()

    try:
        # Receive data from the client
        data = connection.recv(1024)

        # Process the data and send a response back
        response = "Your data has been processed."
        connection.sendall(response.encode('utf-8'))

    finally:
        # Clean up the connection
        connection.close()
