class ProcessData:
    client_code = ""
    client_id = ""
    dest_id = ""
    send_text = ""
    client_IP = ""

    def __init__(self, data_object):
        # print(data_object)
        self.client_code = data_object["code"]
        self.client_id = data_object["client_id"]
        if "dest_id" in data_object:
            self.dest_id = data_object["dest_id"]
        if "send_text" in data_object:
            self.send_text = data_object["send_text"]

