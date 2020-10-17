import socket
import json

local_host = socket.gethostname()
local_port = 1234
UDPServerPort = (local_host, local_port)
buffer_size = 1024
# queue_size = 5
msg_from_server = "Welcome to UDP server"
bytes_to_send = str.encode(msg_from_server)


class ProcessData:
    client_code = ""
    client_id = ""
    dest_id = ""
    send_text = ""
    client_IP = ""

    def __init__(self, data_object):
        self.client_code = data_object["code"]
        self.client_id = data_object["client_id"]
        self.dest_id = data_object["dest_id"]
        self.send_text = data_object["send_text"]
        self.client_IP = data_object["client_ip"]


def check_code(received_data, c_code):
    if c_code == "T":
        storage[received_data.client_IP] = received_data.send_text
    else:
        if received_data.client_IP in storage.keys():
            result = storage[received_data.client_IP]
            storage.pop(received_data.client_IP)
            return result
        else:
            result = "No Text"
            return result


# Create a UDP socket
UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Bind to port
UDPServerSocket.bind(UDPServerPort)
welcome_message = "SERVER IS NOW LISTENING AT UDP SOCKET"
print(welcome_message)

storage = {}

while True:
    data, client_address = UDPServerSocket.recvfrom(buffer_size*2)
    print("MESSAGE RECEIVED: ", data.decode('utf-8'))
    print('The client at {} says {!r}'.format(client_address, data))

    # Load received data into JSON
    data_receive = json.loads(data.decode())

    # Split JSON data into specific parts
    processData = ProcessData(data_receive)

    # Specify client_ip
    processData.client_IP = client_address

    # Specify client_name
    client_name = processData.client_id

    text_msg = processData.send_text
    dest_name = processData.dest_id
    # Verify if the client_code is valid
    client_code = processData.client_code
    if processData.client_code != "T" or processData.client_code != "C":
        warning_msg = "Invalid <code> format. "
        UDPServerSocket.sendto(bytes(warning_msg, "utf-8"), client_address)
    else:
        feedback_data = check_code(processData, client_code)
        UDPServerSocket.sendto(feedback_data, client_address)

    print(storage)

    
