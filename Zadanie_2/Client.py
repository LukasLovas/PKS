import socket
from Header import Header


class Client:
    def __init__(self, ip, port, server_ip, server_port):
        self.server = None
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ip = ip
        self.port = port
        self.server_ip = server_ip
        self.server_port = server_port
        self.data = "empty"
        self.initialize_connection()
        self.cycle()

    def cycle(self):
        while self.data != "End connection message received... closing connection":
            self.send_message(input("Enter your message: "))
            data = self.receive()
            print(data)

    def build_initialization_packet(self):
        pass
        #return Header(bytes(1), bytes(1), bytes(2), None, bytes(1011))  # TODO treba kym zacnem posielat veci poriesit CRC

    def initialize_connection(self):
        self.sock.sendto(bytes("Initialize", encoding="utf-8"), (self.server_ip, int(self.server_port)))
        while self.data != "Connection initialized successfully":
            self.data = self.receive()
        print(self.data)

    def receive(self):
        data, self.server = self.sock.recvfrom(1024)
        return str(data, encoding="utf-8")

    def send_message(self, message):
        self.sock.sendto(bytes(message, encoding="utf-8"), (self.server_ip, int(self.server_port)))

    def send_end_message(self):
        self.sock.sendto(bytes("End connection", encoding="utf-8"), (self.server_ip, self.server_port))

    def quit(self):
        self.sock.close()
        print("Client closed...")
