import socket
import json
import sys  # for exit

# Create a UDP socket at client side
UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Initialize variables
udp_port = 1234
local_host = socket.gethostname()
serverAddressPort = (local_host, udp_port)
IPAddr = socket.gethostbyname(local_host)
buffer_size = 1024

UDPClientSocket.connect(serverAddressPort)


def send_msg(sending_data):
    UDPClientSocket.sendto(sending_data.encode(), serverAddressPort)


def request_options():
    options = "Enter 1 -> Send text, 2-> Check for text, 3-> Quit: "
    c_option = input(options)
    return c_option


def receiving_data(data, opt, local_id):
    recv_data, server_add = UDPClientSocket.recvfrom(buffer_size * 2)
    recv_data = json.loads(recv_data.decode())
    if opt == "2":
        print("TEXT RECEIVED: To: {} From: {} Text: {}".format(local_id, recv_data["sender"], recv_data["message"]))
    else:
        print("MESSAGE RECEIVED FROM SERVER: {}".format(recv_data["message"]))


variables = ProcessData()
variables.client_IP = IPAddr

print("Enter your ID as a string")
variables.client_id = input("->")
option = request_options()

while option == "1" or option == "2":
    if option == "1":
        variables.client_code = "T"
        print("Enter dest ID as a string: ")
        variables.dest_id = input("-> ")
        request_send_text = "Enter your text: "
        variables.send_text = input(request_send_text)
        send_data = json.dumps(
            {"code": variables.client_code, "dest_id": variables.dest_id, "client_id": variables.client_id,
             "send_text": variables.send_text, "client_ip": variables.client_IP})
        print("MESSAGE TO SEND: {} To: {} From: {} Text: {}".format(variables.client_code, variables.dest_id,
                                                                    variables.client_id, variables.send_text))
        send_msg(send_data)
        receiving_data(variables, option, variables.client_id)

    elif option == "2":
        variables.client_code = "C"
        print("MESSAGE TO SEND: {} From: {} ".format(variables.client_code, variables.client_id))
        send_data = json.dumps({"code": variables.client_code, "client_id": variables.client_id})
        send_msg(send_data)
        receiving_data(variables, option, variables.client_id)

    option = request_options()


else:
    UDPClientSocket.close()
    sys.exit()
