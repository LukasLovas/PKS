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
            self.header = [self.data[0],                                    # frame_type 1B      [0]
                           struct.unpack("H", self.data[1:3])[0],   # fragment_order 2B  [1]
                           self.data[3],                                    # next_fragment 1B   [2]
                           struct.unpack("H", self.data[4:6])[0],   # CRC 2B             [3]
                           self.data[6:].decode(encoding="utf")]            # Data XB            [4]
            print(f"-----------------------------\n"
                  f"Frame_type: {self.header[0]}\n"
                  f"Fragment_order: {self.header[1]}\n"
                  f"Next_fragment: {self.header[2]}\n"
                  f"CRC: {self.header[3]}\n"
                  f"Data: {(self.header[4] if self.header[4] != '' else 'empty')}\n")
            if self.header[0] == 1:
                self.send_initialization_response()
                return
            else:
                self.header = None
                self.client = None

    def cycle(self):
        while self.header[0] != 8:                  # Ukončenie spojenia
            data = self.receive()
            self.header = [self.data[0],                                    # frame_type 1B      [0]
                           struct.unpack("H", self.data[1:3])[0],   # fragment_order 2B  [1]
                           self.data[3],                                    # next_fragment 1B   [2]
                           struct.unpack("H", self.data[4:6])[0],   # CRC 2B             [3]
                           self.data[6:].decode(encoding="utf")]            # Data XB            [4]
            self.send_response()

    def receive(self):
        data = None
        while data is None:
            data, self.client = self.sock.recvfrom(1500)
        print(f"Received message: {data}")
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
        match header_type:
            case "Keep-alive":
                header = (
                        struct.pack("B", 4) +
                        struct.pack("H", fragment_order) +
                        struct.pack("?", next_fragment)
                )
                encoded_data = data.encode(encoding="utf-8")
                checksum = struct.pack("H", self.calculate_crc(header + encoded_data))
                return header + checksum + encoded_data
            case "CRC Fault":
                header = (
                struct.pack("B", 5) +
                struct.pack("H", fragment_order) +
                struct.pack("?", next_fragment)
                )
                encoded_data = data.encode(encoding="utf-8")
                checksum = struct.pack("H", self.calculate_crc(header + encoded_data))
                return header + checksum + encoded_data
            case "Ack":
                header = (
                        struct.pack("B", 6) +
                        struct.pack("H", fragment_order) +
                        struct.pack("?", next_fragment)

                )
                encoded_data = data.encode(encoding="utf-8")
                checksum = struct.pack("H", self.calculate_crc(header + encoded_data))
                return header + checksum + encoded_data
            case "Switch":
                header = (
                        struct.pack("B", 7) +
                        struct.pack("H", fragment_order) +
                        struct.pack("?", next_fragment)
                )
                encoded_data = data.encode(encoding="utf-8")
                checksum = struct.pack("H", self.calculate_crc(header + encoded_data))
                return header + checksum + encoded_data

    def send_response(self):
        self.sock.sendto(b"Message delivered successfully...", self.client)

    def send_initialization_response(self):
        header_to_send = self.build_header("Ack", 1, False, "")
        self.sock.sendto(header_to_send, self.client)

    def send_connection_end_message(self):
        self.sock.sendto(b"End connection message received... closing connection", self.client)

    def quit(self):
        self.sock.close()
        print("Server closed")
