import socket
import struct

from Header import Header
from crc import Calculator, Crc16


class Client:
    def __init__(self, ip, port, server_ip, server_port):
        self.server = None
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ip = ip
        self.port = port
        self.server_ip = server_ip
        self.server_port = server_port
        self.data = "empty"
        self.header = None
        self.fragment_size = None
        self.initialize_connection()
        self.cycle()

    def cycle(self):
        while True:
            if self.fragment_size is None:
                self.fragment_size = int(input("Enter fragment size: "))
            else:
                if input("Do you want to change fragment size? (Y/N): ") == "Y":
                    self.fragment_size = int(input("Enter fragment size: "))
                else:
                    pass
            self.send_message(input("Enter your message or enter 'File' for file transfer: "))
            data = self.receive()
            print(data)

    def initialize_connection(self):
        header_to_send = self.build_header(1, 1, False, "")
        self.sock.sendto(header_to_send, (self.server_ip, int(self.server_port)))
        while self.data == "empty":
            self.data = self.receive()
            if self.data == "empty":
                pass
            else:
                if (self.data[0] == 6) & (self.server == (self.server_ip, int(self.server_port))):
                    print("Connection established successfully.")
                else:
                    self.data = "empty"


    def calculate_crc(self, data):
        crc_calculator = Calculator(Crc16.CCITT, optimized=True)
        crc_result = crc_calculator.checksum(data)
        return crc_result

    # def build_header(self, header_type, fragment_order, next_fragment, data):
    #     match header_type:
    #         case "Initialize":
    #             header = (
    #                     struct.pack("B", 1) +
    #                     struct.pack("H", fragment_order) +
    #                     struct.pack("?", next_fragment)
    #
    #             )
    #             encoded_data = data.encode(encoding="utf-8")
    #             checksum = struct.pack("H", self.calculate_crc(header + encoded_data))
    #             return header + checksum + encoded_data
    #         case "Send message":
    #             header = (
    #                     struct.pack("B", 2) +
    #                     struct.pack("H", fragment_order) +
    #                     struct.pack("?", next_fragment)
    #
    #             )
    #             encoded_data = data.encode(encoding="utf-8")
    #             checksum = struct.pack("H", self.calculate_crc(header + encoded_data))
    #             return header + checksum + encoded_data
    #         case "Send file":
    #             header = (
    #                     struct.pack("B", 3) +
    #                     struct.pack("H", fragment_order) +
    #                     struct.pack("?", next_fragment)
    #
    #             )
    #             encoded_data = data.encode(encoding="utf-8")
    #             checksum = struct.pack("H", self.calculate_crc(header + encoded_data))
    #             return header + checksum + encoded_data
    #         case "Keep-alive":
    #             header = (
    #                     struct.pack("B", 4) +
    #                     struct.pack("H", fragment_order) +
    #                     struct.pack("?", next_fragment)
    #
    #             )
    #             encoded_data = data.encode(encoding="utf-8")
    #             checksum = struct.pack("H", self.calculate_crc(header + encoded_data))
    #             return header + checksum + encoded_data
    #         case "Switch":
    #             header = (
    #                     struct.pack("B", 7) +
    #                     struct.pack("H", fragment_order) +
    #                     struct.pack("?", next_fragment)
    #
    #             )
    #             encoded_data = data.encode(encoding="utf-8")
    #             checksum = struct.pack("H", self.calculate_crc(header + encoded_data))
    #             return header + checksum + encoded_data
    #         case "End connection":
    #             header = (
    #                     struct.pack("B", 8) +
    #                     struct.pack("H", fragment_order) +
    #                     struct.pack("?", next_fragment)
    #
    #             )
    #             encoded_data = data.encode(encoding="utf-8")
    #             checksum = struct.pack("H", self.calculate_crc(header + encoded_data))
    #             return header + checksum + encoded_data

    def build_header(self, header_type, fragment_order, next_fragment, data):
            header = (
                    struct.pack("B", header_type) +
                    struct.pack("H", fragment_order) +
                    struct.pack("?", next_fragment)
                )
            encoded_data = data.encode(encoding="utf-8")
            checksum = struct.pack("H", self.calculate_crc(header + encoded_data))
            return header + checksum + encoded_data

    def receive(self):
        data = None
        while data is None:
            data, self.server = self.sock.recvfrom(1500)
        return data

    def send_message(self, data):
        if data == 'File':
            data = input("Enter file path: ")                       #TODO vymysliet ako prenasat files + ako prenasat ich nazov!!! povinne aby obe strany vedeli nazov suboru
        else:
            fragmentation = True if len(data.encode(encoding="utf-8")) + 8 + 20 + 6 > self.fragment_size else False
            if fragmentation:
                pass
            else:
                header_to_send = self.build_header(2, 1, False, data)
                self.sock.sendto(header_to_send, (self.server_ip, int(self.server_port)))

    def send_end_message(self):
        self.sock.sendto(bytes("End connection", encoding="utf-8"), (self.server_ip, self.server_port))

    def quit(self):
        self.sock.close()
        print("Client closed...")
