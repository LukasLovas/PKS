import socket
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
        self.initialize_connection()
        self.cycle()

    def cycle(self):
        while self.data != "End connection message received... closing connection":
            self.send_message(input("Enter your message: "))
            data = self.receive()
            print(data)

    def initialize_connection(self):
        header = self.build_header("Initialize", 1, False, b"", b"")
        header.crc = bytes(self.calculate_crc(header.get_byte_data()))
        self.sock.sendto(header.get_byte_data(), (self.server_ip, int(self.server_port)))
        while self.data != "Connection initialized successfully":
            self.data = self.receive()
        print(self.data)

    def calculate_crc(self, data):
        crc_calculator = Calculator(Crc16.CCITT, optimized=True)
        crc_result = crc_calculator.checksum(data)
        return crc_result

    def build_header(self, header_type, fragment_order, next_fragment, data, crc):
        match header_type:
            case "Initialize":
                return Header(bytes(1),
                              bytes(fragment_order),
                              bytes([1]) if next_fragment is True else bytes([2]),
                              bytes(data),
                              bytes(crc))
            case "Send message":
                pass
            case "Send file":
                pass
            case "Keep-alive":
                pass
            case "CRC Fault":
                pass
            case "Ack":
                pass
            case "Switch":
                pass
            case "End connection":
                pass

    def receive(self):
        data, self.server = self.sock.recvfrom(1500)
        return str(data, encoding="utf-8")

    def send_message(self, message):
        self.sock.sendto(bytes(message, encoding="utf-8"), (self.server_ip, int(self.server_port)))

    def send_end_message(self):
        self.sock.sendto(bytes("End connection", encoding="utf-8"), (self.server_ip, self.server_port))

    def quit(self):
        self.sock.close()
        print("Client closed...")
