import json
import socket
import threading
import random

# The client handle
handle = ""

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

            # Check the command of the message
            if message["command"] == "all":
                # Print the message to the screen
                print(f"{message['handle']}: {message['message']}")

            elif message["command"] == "register":
                print(f"{message['message']}")

            elif message["command"] == "msg":
                print(f"[From {message['handle']}]: {message['message']}")

            elif message["command"] == "msgr":
                print(f"[To {message['handle']}]: {message['message']}")

            elif message["command"] == "join":
                print("heyyyyyyy")
                print(f"{message['message']}")

            elif message["command"] == "error":
                print(f"{message['message']}")
        except:
            pass

# Start the thread to receive messages

timeout_sec = 5

while True:
    # Read the user's input
    user_input = input()

    # Split the input into words
    words = user_input.split()

    # Check the first word of the input
    if words[0] == "/join":
        check = None
        # The user is trying to join the chatroom
        # Set the server IP address and port number
        try:
            SERVER_IP = words[1]
            SERVER_PORT = words[2]

            try:
                val = int(SERVER_PORT)
            except:
                print ("Error: Invalid port number")
                check = 1
        except:
            check = 1
        
        if check is None:
            try:
                result = sock.bind((SERVER_IP, random.randint(7000,9000)))
            except:
                result = "Error occured"


            if result is None:
                print("Connection to the Message Board, Server is successful!")
                receive_thread = threading.Thread(target=receive_messages)
                receive_thread.start()

            else:
                print ("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.")
        else:
            print ("Error: Either you have invalid/lack of arguments or you are already connected to a server")

        
    elif words[0] == "/leave":
        # The user is trying to leave the chatroom
        # Create the message to be sent to the server
        try:
            message = {
                "command": "leave",
                "handle": handle,
            }
            # Encode the message as a JSON formatted string
            message_str = json.dumps(message)

            # Send the message to the server
            sock.sendto(message_str.encode(), (SERVER_IP, int(SERVER_PORT)))
            sock.close()
            print("Connection closed. Thank you!")
        except:
            print("Error: Disconnection failed. Please connect to the server first.")

    elif words[0] == "/register":
        # The user is trying to register a handle
        # Set the handle
        try: 
            handle = words[1]
        except:
            print("Error: No name entered")

        # Create the message to be sent to the server
        message = {
            "command": "register",
            "handle": handle,
            "message": "Welcome"
        }

        try:
            message_str = json.dumps(message)
            sock.sendto(message_str.encode(), (SERVER_IP, int(SERVER_PORT)))
        except:
            print("Error: Registration failed. Please connect to the server first.")

    elif words[0] == "/all":
        # The user is trying to send a message to all clients
        # Join the words of the input into a single string
        message = " ".join(words[1:])

        # Create the message to be sent to the server
        message_to_send = {
            "command": "all",
            "handle": handle,
            "message": message,
        }

        # Encode the message as a JSON formatted

        message_to_send_str = json.dumps(message_to_send)

        # Send the message to the server
        try:
            sock.sendto(message_to_send_str.encode(), (SERVER_IP, int(SERVER_PORT)))
        except:
            print("Error: You are not connected to a server.")

    elif words[0] == "/msg":
        message = " ".join(words[2:])

        try:
            message_to_send = {
                "command": "msg",
                "from": handle,
                "handle": words[1],
                "message": message,
                
            }

        # Encode the message as a JSON formatted string
            message_to_send_str = json.dumps(message_to_send)
        except:
            print("Error: Missing argument(s)")

        # Send the message to the server
        try:
            sock.sendto(message_to_send_str.encode(), (SERVER_IP, int(SERVER_PORT)))
        except:
            print("Error: You are not connected to a server.")
    
    elif words[0] == "/?":
        print("/join <server_ip_add> <port> : Connect to the server application\n")
        print("/leave : Disconnect to the server application\n")
        print("/register <handle> : Register a unique handle or alias \n")    
        print("/all <message> : Send message to all\n")    
        print("/msg <handle> <message> : Send direct message to a single handle\n")    
        

    else:
        print("Error: Invalid command")
