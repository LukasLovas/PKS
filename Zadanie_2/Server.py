import socket


class Server():
    def __init__(self, ip, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((ip, port))

    def recieve(self):
        data = None
        while data == None:
            data, self.client = self.sock.recvfrom(1024)
        print(f"Recieved message: {data}")
        return str(data, encoding="utf-8")

    def send_response(self):
        self.sock.sendto(b"Message recieved...", self.client)

    def send_connection_end_message(self):
        self.sock.sendto(b"End connection message received... closing connection", self.client)

    def quit(self):
        self.sock.close()
        print("Server closed")