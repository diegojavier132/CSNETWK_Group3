import json
import socket
import threading

# The client handle
handle = ""

# The server IP address and port number
SERVER_IP = "localhost"
SERVER_PORT = 4353

# The maximum size of a message, in bytes
MAX_MESSAGE_SIZE = 1024

# Create the UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# A function to receive messages in a separate thread
def receive_messages():
    while True:
        try:
            # Receive a message from the server
            data, addr = sock.recvfrom(1024)
            string = data.decode()
            # Decode the JSON formatted string
            message = json.loads(string)

            # Check the type of the message
            if message["type"] == "message":
                # Print the message to the screen
                print(f"{message['handle']}: {message['message']}")
        except:
            pass

# Start the thread to receive messages


while True:
    # Read the user's input
    user_input = input()

    # Split the input into words
    words = user_input.split()

    # Check the first word of the input
    if words[0] == "/join":
        # The user is trying to join the chatroom
        # Set the server IP address and port number
        SERVER_IP = words[1]
        SERVER_PORT = words[2]
        sock.bind((SERVER_IP, int(SERVER_PORT)))
        receive_thread = threading.Thread(target=receive_messages)
        receive_thread.start()
        
    elif words[0] == "/leave":
        # The user is trying to leave the chatroom
        # Create the message to be sent to the server
        message = {
            "type": "leave",
            "handle": handle,
        }

        # Encode the message as a JSON formatted string
        message_str = json.dumps(message)

        # Send the message to the server
        sock.sendto(message_str.encode(), (SERVER_IP, 9999))

        # Break out of the loop
        break
    elif words[0] == "/register":
        # The user is trying to register a handle
        # Set the handle
        handle = words[1]

        # Create the message to be sent to the server
        message = {
            "type": "register",
            "handle": handle,
        }

        # Encode the message as a JSON formatted string
        message_str = json.dumps(message)

        # Send the message to the server
        sock.sendto(message_str.encode(), (SERVER_IP, 9999))
    elif words[0] == "/all":
        # The user is trying to send a message to all clients
        # Join the words of the input into a single string
        message = " ".join(words[1:])

        # Create the message to be sent to the server
        message_to_send = {
            "type": "all",
            "handle": handle,
            "message": message,
        }

        # Encode the message as a JSON formatted

        message_to_send_str = json.dumps(message_to_send)

        # Send the message to the server
        sock.sendto(message_to_send_str.encode(), (SERVER_IP, 9999))

    elif words[0] == "/msg":
        message = " ".join(words[2:])

            # Create the message to be sent to the server
        message_to_send = {
              "type": "msg",
              "handle": handle,
              "to": words[1],
              "message": message,
            
        }

        # Encode the message as a JSON formatted string
        message_to_send_str = json.dumps(message_to_send)

        # Send the message to the server
        sock.sendto(message_to_send_str.encode(), (SERVER_IP, 9999))
