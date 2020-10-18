import socket
import json
import threading
import pickle
from process_data import ProcessData

# Create Socket options
local_host = socket.gethostname()
local_port = 1234
UDPServerPort = (local_host, local_port)
buffer_size = 1024
socket_lock = threading.Lock()

# Create a UDP socket
UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to port
UDPServerSocket.bind(UDPServerPort)
welcome_message = "SERVER IS NOW LISTENING AT UDP SOCKET"
print(welcome_message)

# Create empty dictionary to store messages
storage = {}


def handle_socket(data, client_address, local_storage):
    # print('The client at {} says {!r}'.format(client_address, data))
    # Load received data into JSON
    data_receive = json.loads(data.decode())

    # Split JSON data into specific parts
    process_data = ProcessData(data_receive)

    # Verify if the client_code is valid
    client_code = process_data.client_code

    # Verify client code
    if client_code == "T":

        print("MESSAGE RECEIVED: T To: {} From: {} Text: {}".format(process_data.dest_id, process_data.client_id,
                                                                    process_data.send_text))
        if process_data.dest_id not in local_storage:
            local_storage[process_data.dest_id] = []  # Create a queue to store data with the same key
        # local_storage[process_data.dest_id].append(process_data.send_text)
        local_storage[process_data.dest_id].append(process_data)
        # print("Storage: ")
        # print(local_storage)
        result = json.dumps({"message": "messages stored"})

    elif client_code == "C":
        if process_data.client_id in local_storage.keys():
            # text = "\n".join(local_storage[process_data.client_id])
            # del local_storage[process_data.client_id]
            obj = local_storage[process_data.client_id].pop(0)  # Pop out relative object
            if obj.send_text is not None:
                result = json.dumps({"message": obj.send_text, "sender": obj.client_id})
                print("MESSAGE TO SEND: T To: {} From: {} Text: {}".format(obj.dest_id, obj.client_id, result))
            else:
                result = json.dumps({"message": "No Text", "sender": obj.client_id})
                print("MESSAGE TO SEND: T To: {} Text: No Text".format(obj.client_id))
        else:
            result = json.dumps({"message": "No Text"})
            print("MESSAGE TO SEND: T To: {} Text: No Text".format(process_data.client_id))

    else:
        result = json.dumps({"message": "Invalid <code> format. "})
    # print(result)
    # result = str.encode(result)
    with socket_lock:
        UDPServerSocket.sendto(result.encode(), client_address)


while True:
    processing_data, processing_client_address = UDPServerSocket.recvfrom(buffer_size * 2)
    # print("receiving data from ")
    # print(processing_client_address)
    # Create threads to handle multiple clients
    thread = threading.Thread(target=handle_socket, args=(processing_data, processing_client_address, storage))
    thread.daemon = True
    thread.start()
