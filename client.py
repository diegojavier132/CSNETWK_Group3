import socket
import threading
import random
import re
import json

command = '{"command":"test", "handle":"why", "message":"*^8tjqdkb", "ip":"   ", "port":"  "}'
command_json = json.loads(command)



def receive():
    global command_json

    while True:
        try:
            message, addr = client.recvfrom(1024)
            json_string = message.decode()
            command_json = json.loads(json_string)
            if command_json["command"] == "join":
                print("Sucessful Connection")

        except:
            pass

message = input("")

if message.startswith("/join"): 
    res = message.split()
    command_json["command"] = "join"
    command_json["ip"] = res[1]
    command_json["port"] = res[2]
    server_ip = command_json["ip"]
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.bind((server_ip, int(command_json["port"])))
    t = threading.Thread(target=receive)
    t.start()

    result = json.dumps(command_json)
    client.sendto(result.encode(), (server_ip, 9999))


while True:
    message = input("")

    if message.startswith("/register"):
        res = message.split()
        command_json["command"] = "register"
        command_json["handle"] = res[1]
        message = json.dumps(command_json)
        client.sendto(message.encode(), (server_ip, 9999))

    elif message.startswith("/all"):
        res = message.split()
        command_json["command"] = "all"
        command_json["message"] = re.sub(r'.', '', message, count = 5)
        command_json["message"] = f'{command_json["handle"]}: {command_json["message"]}'
        result = json.dumps(command_json)
        client.sendto(result.encode(), (server_ip, 9999))

    elif message.startswith("/message"):
        res = message.split()
        command_json["command"] = "message"
        command_json["handle"] = res[1]
        command_json["message"] = res[2]
        message = json.dumps(command_json)
        client.sendto(message.encode(), (server_ip, 9999))


    else:
        print("Invalid Command")




