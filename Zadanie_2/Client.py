import socket
from Header import Header


class Client:
    def __init__(self, ip, port, server_ip, server_port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ip = ip
        self.port = port
        self.server_ip = server_ip
        self.server_port = server_port

    def build_initialization_packet(self):
        return Header(bytes(1), bytes(1), bytes(2), None,
                        bytes(1011))  # TODO treba kym zacnem posielat veci poriesit CRC

    def initialize_connection(self):
        self.sock.sendto(self.build_initialization_packet(), (self.server_ip, self.server_port))

    def receive(self):
        data, self.server = self.sock.recvfrom(1024)
        return str(data, encoding="utf-8")

    def send_message(self, message):
        self.sock.sendto(bytes(message, encoding="utf-8"), (self.server_ip, self.server_port))

    def quit(self):
        self.sock.close()
        print("Client closed...")
