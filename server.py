import json
import socket
import threading

# The server IP address and port number
SERVER_IP = "localhost"
SERVER_PORT = 8000

# The maximum size of a message, in bytes
MAX_MESSAGE_SIZE = 1024

# Create the UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the server IP and port
sock.bind(("localhost", 9999))

# A dictionary to store the registered handles and their corresponding IP addresses and port numbers
clients = {}

# A variable to keep track of the next message ID
next_message_id = 0

while True:
    # Receive a message from a client
    data, addr = sock.recvfrom(1024)
    string_data = data.decode()
    # Decode the JSON formatted string
    message = json.loads(string_data)

    # Check the type of the message
    if message["type"] == "join":
        # A client is joining the chatroom
        # Store the client's handle, IP address, and port number
        clients[message["handle"]] = (addr[0], addr[1])
        print("Joined")
    elif message["type"] == "leave":
        # A client is leaving the chatroom
        # Remove the client from the dictionary
        del clients[message["handle"]]
    elif message["type"] == "register":
        # A client is registering a handle
        # Store the client's handle, IP address, and port number
        clients[message["handle"]] = (addr[0], addr[1])
        print(f'{message["handle"]} has registered')
    elif message["type"] == "all":
        # A client is sending a message to all clients
        # Increment the message ID
        next_message_id += 1

        # Create the message to be sent to all clients
        message_to_send = {
            "type": "message",
            "id": next_message_id,
            "handle": message["handle"],
            "message": message["message"],
        }

        # Encode the message as a JSON formatted string
        message_to_send_str = json.dumps(message_to_send)

        # Send the message to all registered clients
        for client in clients.values():
            sock.sendto(message_to_send_str.encode(), client)
    elif message["type"] == "msg":
        # A client is sending a message to a specific handle
        # Check if the handle exists in the dictionary
        if message["to"] in clients:
            # Increment the message ID
            next_message_id += 1

            # Create the message to be sent to the specific handle
            message_to_send = {
                "type": "message",
                "id": next_message_id,
                "handle": message["handle"],
                "message": message["message"],
                
            }

            # Encode the message as a JSON formatted string
            message_to_send_str = json.dumps(message_to_send)

            # Send the message to the specific handle
            sock.sendto(message_to_send_str.encode(), clients[message["to"]])

