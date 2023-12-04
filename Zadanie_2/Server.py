import os
import socket
import struct

from crc import Calculator, Crc16


def create_file_directory(directory_path, directory_name):
    dir_path = directory_path + "\\" + directory_name
    os.makedirs(dir_path, exist_ok=True)


class Server:
    def __init__(self, ip, port):
        self.header = None
        self.client = None
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((ip, port))
        self.data = None
        create_file_directory(os.getcwd() + "\\Zadanie_2", "Prijate_subory")
        self.wait_initialization()
        self.cycle()

    def wait_initialization(self):
        while self.client is None:
            self.data = self.receive()
            if self.data is not None:
                self.header = [self.data[0],  # frame_type 1B      [0]
                               struct.unpack("H", self.data[1:3])[0],  # fragment_order 2B  [1]
                               self.data[3],  # next_fragment 1B   [2]
                               struct.unpack("H", self.data[4:6])[0],  # CRC 2B             [3]
                               self.data[6:].decode(encoding="utf-8")]  # Data XB            [4]
                print(f"-----------------------------\n"
                      f"Frame_type: {self.header[0]}\n"
                      f"Fragment_order: {self.header[1]}\n"
                      f"Next_fragment: {self.header[2]}\n"
                      f"CRC: {self.header[3]}\n"
                      f"Data: {(self.header[4] if self.header[4] != '' else 'empty')}\n")
                if self.header[0] == 1:
                    self.send_response()
                    return
            else:
                self.header = None
                self.client = None

    def cycle(self):
        while self.header[0] != 8:  # Ukončenie spojenia
            data = self.receive()
        self.quit()

    def receive(self):
        data = None
        while data is None:
            data, self.client = self.sock.recvfrom(1500)
            if self.client is not None:
                match data[0]:
                    case 3:
                        separator = b"|||"
                        separator_index = data.find(separator)
                        file_name = data[6:separator_index]
                        file_data = data[separator_index + 3:]
                        self.header = self.receive_header(data)
                        if self.validate_crc(self.header[0] + self.header[1] + self.header[2] + self.header[4],
                                             self.header[3]):
                            file_path = "Zadanie_2/Prijate_subory/" + file_name.decode("utf-8")
                            with open(file_path, "wb") as file:
                                file.write(file_data)
                            print(f"File saved successfully. Path: {file_path}")
                            self.send_response()
                            return data
                        else:
                            pass

                    case 2:
                        self.header = self.receive_header(data)
                        if data[3] == 1:
                            received_fragments = []
                            while data[3] == 1:
                                fragment_order = self.header[1]
                                if fragment_order not in received_fragments and self.validate_crc(self.header[0:4] + self.header[5], self.header[4]):
                                    received_fragments.append(fragment_order)
                                    print(f"Received fragment: {data[6:].decode(encoding='utf-8')}")
                            if self.header[2] == 0:
                                if set(received_fragments) == set(range(1, max(received_fragments) + 1)):
                                    print("All fragments received successfully.")
                                    self.send_response()
                                    return data
                                else:
                                    missing_fragments = set(range(1, max(received_fragments) + 1)) - set(received_fragments)
                                    missing_fragments_string = ""
                                    for fragment in missing_fragments:
                                        missing_fragments_string.join(str(fragment))
                                    header_to_send = self.build_header(5, 1, False, missing_fragments_string)
                                    self.sock.sendto(header_to_send, self.client)
                                    missing_fragments_response = None
                                    while missing_fragments_response is None:
                                        missing_fragments_response = self.sock.recvfrom(1500)
                                    missing_fragments_header = self.receive_header(missing_fragments_response)


                        # received_data = ""
                        # missing_fragments = []
                        # if data[3] == 1:
                        #     while data[3] == 1:
                        #         self.header = self.receive_header(data)
                        #         received_data += (data[6:].decode(encoding="utf-8") + "\n")
                        #         if not self.validate_crc(self.header[0:4] + self.header[5],self.header[4]):
                        #             missing_fragments.append(self.header[1])
                        #         data, self.client = self.sock.recvfrom(1500)
                        #         if len(missing_fragments) == 0:
                        #             print(f"Received message: {received_data}")
                        #         else:
                        #             pass
                        #             # vypytaj nove
                        #
                        # else:
                        #     self.receive_header(data)
                        #     print(f"Received message: {data[6:].decode(encoding='utf-8')}")
                    case 1:
                        self.header = self.receive_header(data)
                        print(f"Received message: {data[6:].decode(encoding='utf-8')}")
                        self.send_response()
                        return data
                    case _:
                        continue
            elif self.client is None:
                if data is not None:
                    self.header = self.receive_header(data)
                    print(f"Received message: {data[6:].decode(encoding='utf-8')}")
                    self.send_response()
                    return data
                else:
                    continue

    def receive_header(self, data):
        header = [data[0],  # frame_type 1B      [0]
                  struct.unpack("H", data[1:3])[0],  # fragment_order 2B  [1]
                  data[3],  # next_fragment 1B   [2]
                  struct.unpack("H", data[4:6])[0],  # CRC 2B             [3]
                  data[6:].decode(encoding="utf-8")]  # Data XB            [4]
        return header


    def check_fragments(self, fragment_order):
        result = []
        for i in range(len(fragment_order)):
            if fragment_order[i] != i + 1:
                result.append(fragment_order[i])
        if len(result) == 0:
            result = False
        return result

    def calculate_crc(self, data):
        crc_calculator = Calculator(Crc16.CCITT, optimized=True)
        crc_result = crc_calculator.checksum(data)
        return crc_result

    def validate_crc(self, data, crc_value):
        if self.calculate_crc(data) == crc_value:
            return True
        else:
            return False

    def build_header(self, header_type, fragment_order, next_fragment, data):
        header = (
                struct.pack("B", header_type) +
                struct.pack("H", fragment_order) +
                struct.pack("?", next_fragment)
        )
        encoded_data = data.encode(encoding="utf-8")
        checksum = struct.pack("H", self.calculate_crc(header + encoded_data))
        return header + checksum + encoded_data

    def send_response(self):
        header_to_send = self.build_header(6, 1, False, "Message delivered successfully...")
        self.sock.sendto(header_to_send, self.client)

    def send_connection_end_message(self):
        self.sock.sendto(b"End connection message received... closing connection", self.client)

    def quit(self):
        self.sock.close()
        print("Server closed")
