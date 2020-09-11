
import socket
import json

host = socket.gethostname()
port = 1234
buffer_size = 1024
queue_size = 5
msg_from_server = "Welcome to UDP server"
bytes_to_send = str.encode(msg_from_server)


class ProcessData:
    client_code = ""
    client_id = ""
    dest_id = ""
    send_text = ""


s = socket.socket()  # Create socket object
s.bind((host, port))  # Bind to port
s.listen(queue_size)  # Listen to connect with queue of 5
print("SERVER IS NOW LISTENING AT UDP SOCKET")

while True:
    conn, address = s.accept()  # Establish connection with client
    print("Got connection from: ", address)
    conn.send(bytes(' Welcome to the server !', "utf-8"))
    data = conn.recv(1024)
    print("Server received: ", data.decode('utf-8'))
    text_data = conn.recv(4096)
    data_receive = json.loads(text_data.decode())
    conn.close()
    print(data_receive)
