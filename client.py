import socket
import json

s = socket.socket()
host = socket.gethostname()
port = 1234


class ProcessData:
    client_code = ""
    client_id = ""
    dest_id = ""
    send_text = ""


def send_msg(sending_data):
    s.send(sending_data.encode())


def request_options():
    options = "Enter 1 -> Send text, 2-> Check for text, 3-> Quit: "
    c_option = input(options)
    return c_option


variables = ProcessData()
s.connect((host, port))
data = s.recv(1024)
print("Client received: ", data.decode('utf-8'))
print("Enter your ID as a string")
variables.client_id = input("->")
s.send(bytes(variables.client_id, "utf-8"))

client_option = request_options()

while client_option != "3":
    while client_option == "1":
        variables.client_code = "T"
        print("Enter dest ID as a string: ")
        variables.dest_id = input("-> ")
        request_send_text = "Enter your text: "
        variables.send_text = input(request_send_text)
        send_data = json.dumps(
            {"code": variables.client_code, "dest_id": variables.dest_id, "client_id": variables.client_id,
             "send_text": variables.send_text})
        print("MESSAGE TO SEND: {} To: {} From: {} Text: {}".format(variables.client_code, variables.dest_id,
                                                                    variables.client_id, variables.send_text))
        send_msg(send_data)
        client_option = request_options()

    while client_option == "2":
        variables.client_code = "C"
        print("MESSAGE TO SEND: {} From: {} ".format(variables.client_code, variables.client_id))
        send_data = json.dumps({"code": variables.client_code, "client_id": variables.client_id})
        client_option = request_options()

if client_option == "3":
    s.close()
