import socket


class Server:
    def __init__(self, ip, port):
        self.client = None
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((ip, port))
        self.data = "empty"
        self.wait_initialization()
        self.cycle() if self.data == "Initialize" else None

    def wait_initialization(self):
        while self.data != "Initialize":
            self.data = self.recieve()
            self.send_initialization_response()
        return

    def cycle(self):
        while self.data != "End connection":
            if self.data != "initialized":
                self.send_response()
            data = self.recieve()

    def recieve(self):
        data = None
        while data is None:
            data, self.client = self.sock.recvfrom(1024)
        print(f"Received message: {data.decode()}")
        return str(data, encoding="utf-8")

    def send_response(self):
        self.sock.sendto(b"Message delivered successfully...", self.client)

    def send_initialization_response(self):
        self.sock.sendto(b"Connection initialized successfully", self.client)


    def send_connection_end_message(self):
        self.sock.sendto(b"End connection message received... closing connection", self.client)

    def quit(self):
        self.sock.close()
        print("Server closed")
