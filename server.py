import socket
import threading
import queue
import json



class json_command():          # leave this empty
    def __init__(self):   # constructor function using self
        self.command = None  # variable using self.
        self.handle = None
        self

json_string = '{"command":" ", "handle":" ", "message":"*^8tjqdkb", "ip":" ", "port":" "}'
command_json = json.loads(json_string)


messages = queue.Queue()
clients = []
names = []
commands = queue


server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("localhost", 9999))



def receive():
    global command_json

    while True:
        try:
            message, addr = server.recvfrom(1024)
            messages.put((message, addr))
            json_string = message.decode()
            command_json = json.loads(json_string)

        except:
            pass


def broadcast():
    global command_json

    while True:
        while not messages.empty():
            message, addr = messages.get()
            if command_json["command"] == "all":
                print(command_json["message"])
        
            if addr not in clients:
                clients.append(addr)

            for client in clients:
                try:
                    if command_json["command"] == "join":
                        command_json["message"] = "Connection successful"
                        result = json.dumps(command_json)
                        server.sendto(result.encode(), client)

                    elif command_json["command"] == "register":
                        name = command_json["handle"]
                        names.append(name)
                    
                    elif command_json["command"] == "all":
                        server.sendto(f'{command_json["message"]}'.encode(), client)

                    
                    else:
                        server.sendto(message, client)

                except:
                    print("smth")
                    clients.remove(client)
                    names.remove(name)


t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=broadcast)



t1.start()
t2.start()
