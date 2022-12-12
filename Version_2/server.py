import json
import socket
import threading


# The maximum size of a message, in bytes
MAX_MESSAGE_SIZE = 1024

# Create the UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the server IP and port
sock.bind(("127.0.0.1", 12345))

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
    if message["command"] == "join":
        # A client is joining the chatroom
        # Store the client's handle, IP address, and port number
        
        clients[message["handle"]] = (addr[0], addr[1])
        print("Joined")
        
    elif message["command"] == "leave":
        # A client is leaving the chatroom
        # Remove the client from the dictionary
        try:
            del clients[message["handle"]]
        except:
            pass
    elif message["command"] == "register":
        # A client is registering a handle
        # Store the client's handle, IP address, and port number
        if message["handle"] in clients:
            message_to_send = {
            "command": "error",
            "message": "Error: Registration failed. Handle or alias already exists.",
            }
            message_to_send_str = json.dumps(message_to_send)
            sock.sendto(message_to_send_str.encode(), addr)

        else:
            clients[message["handle"]] = (addr[0], addr[1])

            message_to_send = {
                "command": "register",
                "handle": message["handle"],
                "message": f'Welcome {message["handle"]}!',
            }

            message_to_send_str = json.dumps(message_to_send)
            for client in clients.values():
                sock.sendto(message_to_send_str.encode(), client)
            print(f'{message["handle"]} has registered')
    elif message["command"] == "all":
        # A client is sending a message to all clients
        # Increment the message ID
        next_message_id += 1

        # Create the message to be sent to all clients
        message_to_send = {
            "command": "all",
            "id": next_message_id,
            "handle": message["handle"],
            "message": message["message"],
        }
        

        # Encode the message as a JSON formatted string
        message_to_send_str = json.dumps(message_to_send)

        # Send the message to all registered clients
        for client in clients.values():
            sock.sendto(message_to_send_str.encode(), client)
    elif message["command"] == "msg":
        # A client is sending a message to a specific handle
        # Check if the handle exists in the dictionary
        if message["handle"] in clients:
            # Increment the message ID
            next_message_id += 1

            # Create the message to be sent to the specific handle
            message_to_send = {
                "command": "msg",
                "id": next_message_id,
                "handle": message["from"],
                "message": message["message"],
                
            }

            message_to_client = {
                "command": "msgr",
                "id": next_message_id,
                "handle": message["handle"],
                "message": message["message"],
                
            }

            # Encode the message as a JSON formatted string
            message_to_send_str = json.dumps(message_to_send)
            message_to_client_str = json.dumps(message_to_client)

            # Send the message to the specific handle
            sock.sendto(message_to_send_str.encode(), clients[message["handle"]])
            sock.sendto(message_to_client_str.encode(), clients[message["from"]])
        else:
            message_to_send = {
            "command": "error",
            "message": "Error: Handle or alias not found.",
            }

            message_to_send_str = json.dumps(message_to_send)
            sock.sendto(message_to_send_str.encode(), addr)
    else:
        message_to_send = {
        "command": "error",
        "message": "Error: Command not found.",
        }

        message_to_send_str = json.dumps(message_to_send)
        sock.sendto(message_to_send_str.encode(), addr)
