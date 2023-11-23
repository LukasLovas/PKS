import socket


class Server:
    def __init__(self, ip, port) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP_socket creation
        self.sock.bind((ip, port))  # needs to be tuple(string, int)

    def receive(self):
        data = None
        while data == None:
            data, self.client = self.sock.recvfrom(1024)  # buffersize is 1024 bytes
        print("Received message: %s" % data)
        # return data  # 1
        return str(data, encoding="utf-8")

    def three_way(self):
        data = None
        while data == None:
            data, self.client = self.sock.recvfrom(1024)
        print("Syn received...")
        self.send_initial_response()
        while data == "Syn=1":
            data = self.sock.recvfrom(1024)
        print("Ack received, connection initialized...")
        self.sock.sendto(b"Connection initialized successfully...", self.client)

    def send_initial_response(self):
        self.sock.sendto(b"Syn=1,Ack=1", self.client)

    def send_response(self):
        self.sock.sendto(b"Message received... ", self.client)

    def send_last_response(self):
        self.sock.sendto(b"End connection message received... closing connection", self.client)

    def quit(self):
        self.sock.close()  # correctly closing socket
        print("Server closed..")
