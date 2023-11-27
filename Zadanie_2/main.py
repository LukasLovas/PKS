from Server import Server
from Client import Client
from GUI import GUI
import socket
import threading
import os
import customtkinter

if __name__ == "__main__":
    #gui = GUI()
    mode = int(input("Choose client-side (1) or server-side(2): "))
    if mode == 1:
        ip = socket.gethostbyname(socket.gethostname())
        port = 50602
        server_ip = input("Server IP: ")
        server_port = input("Server port: ")
        client = Client(ip, port, server_ip, server_port)
    elif mode == 2:
        ip = socket.gethostbyname(socket.gethostname())
        port = 50602
        print(f"IP address: {ip}\nPort: {port}")
        server = Server(ip, port)
