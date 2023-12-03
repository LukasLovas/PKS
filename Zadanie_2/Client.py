import socket
import struct
import os
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
                print("For changing the fragment size, type 'Fragment'")
            message = input("Enter your message or enter 'File' for file transfer: ")
            if message == "Fragment":
                self.fragment_size = None
                continue
            if message == "File":
                print("C:\\Users\\Lukáš\\Downloads\\fotka.png")
                file_path = input("Type file path: ")
                while not os.path.isfile(file_path):
                    print("Path does not lead to a valid file!")
                    file_path = input("Type file path: ")
                self.send_file(file_path)
            self.send_message(message)
            data = self.receive()
            print("\033[32mServer response: " + data[6:].decode(encoding="utf") + "\033[0m") if data[6:].decode(
                encoding="utf") == "Message delivered successfully..." \
                else '\033[31mServer response: ' + data[6:].decode(encoding="utf") + "\033[0m"

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

    def build_header(self, header_type, fragment_order, next_fragment, data):
        if header_type == 3:
            header = (
                    struct.pack("B", header_type) +
                    struct.pack("H", fragment_order) +
                    struct.pack("?", next_fragment)
            )
            checksum = struct.pack("H", self.calculate_crc(header + data))
            return header + checksum + data
        else:
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
        match data[0]:
            case 4:  # keep-alive
                pass
            case 5:  # CRC-NOK
                pass
            case 6:  # ACK
                return data
            case 7:  # Switch
                pass

    def send_message(self, data):
        fragmentation = True if len(data.encode(encoding="utf-8")) + 8 + 20 + 6 > self.fragment_size else False
        if fragmentation:
            pass
        else:
            header_to_send = self.build_header(2, 1, False, data)
            self.sock.sendto(header_to_send, (self.server_ip, int(self.server_port)))

    def send_file(self, file_path):
        file_name = os.path.basename(file_path).encode("utf-8")
        separator = "|||".encode("utf-8")
        with open(file_path, "rb") as file:
            header_to_send = self.build_header(3, 1, False, file_name + separator + file.read())
            self.sock.sendto(header_to_send, (self.server_ip, int(self.server_port)))

    def send_end_message(self):
        self.sock.sendto(bytes("End connection", encoding="utf-8"), (self.server_ip, self.server_port))

    def quit(self):
        self.sock.close()
        print("Client closed...")
