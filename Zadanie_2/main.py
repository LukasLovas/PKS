from Server import Server
from Client import Client
from Header import Header
import socket
import threading
import os
import struct
from crc import Calculator, Crc16

def calculate_crc(data):
    crc_calculator = Calculator(Crc16.CCITT, optimized=True)
    crc_result = crc_calculator.checksum(data)
    return crc_result





if __name__ == "__main__":
    mode = int(input("Choose client-side (1) or server-side(2): "))
    if mode == 1:
        ip = socket.gethostbyname(socket.gethostname())
        port = 50602
        server_ip = input("Server IP: ")
        server_port = input("Server port: ")
        client = Client(ip, port, server_ip, server_port)
    elif mode == 2:
        ip = socket.gethostbyname(socket.gethostname())
        port = int(input("Listening port: "))
        print(f"IP address: {ip}\nPort: {port}")
        server = Server(ip, port)
