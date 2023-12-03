import socket
import struct

from crc import Calculator, Crc16


class Server:
    def __init__(self, ip, port):
        self.header = None
        self.client = None
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((ip, port))
        self.data = "empty"
        self.wait_initialization()
        self.cycle()

    def wait_initialization(self):
        while self.client is None:
            self.data = self.receive()
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
            self.send_response()

    def receive(self):
        data = None
        while data is None:
            data, self.client = self.sock.recvfrom(8000)
        if data[0] == 3:
            separator = b"|||"
            separator_index = data.find(separator)
            file_name = data[6:separator_index]
            file_data = data[separator_index + 3:]
            with open("Zadanie_2/Prijate_subory/" + file_name.decode("utf-8"), "wb") as file:
                file.write(file_data)
                file.close()
                print("File saved successfully. Path: Zadanie_2/Prijate_subory/" + file_name.decode())
        else:
            self.header = [data[0],  # frame_type 1B      [0]
                           struct.unpack("H", data[1:3])[0],  # fragment_order 2B  [1]
                           data[3],  # next_fragment 1B   [2]
                           struct.unpack("H", data[4:6])[0],  # CRC 2B             [3]
                           data[6:].decode(encoding="utf-8")]  # Data XB            [4]
            print(f"Received message: {data[6:].decode(encoding='utf-8')}")

        return data

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
