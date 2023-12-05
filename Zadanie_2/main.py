from Server import Server
from Client import Client
import socket
from crc import Calculator, Crc16

def calculate_crc(data):
    crc_calculator = Calculator(Crc16.CCITT, optimized=True)
    crc_result = crc_calculator.checksum(data)
    return crc_result





if __name__ == "__main__":
    mode = None
    while mode != 1 and mode != 2:
        mode = int(input("Choose client-side (1) or server-side(2): "))
        if mode == 1:
            ip = socket.gethostbyname(socket.gethostname())
            port = 50602
            server_ip = input("Server IP: ")
            server_port = input("Server port: ")
            user = Client(ip, port, server_ip, server_port)
        elif mode == 2:
            ip = socket.gethostbyname(socket.gethostname())
            port = int(input("Listening port: "))
            print(f"IP address: {ip}\nPort: {port}")
            user = Server(ip, port)

    while True:
        swap, address_info = user.mainloop()

        if swap and mode == 1:
            ip = user.ip
            port = user.port
            user.sock.close()
            user = Server(ip, port)
            mode = 2

        elif swap and mode == 2:
            ip = user.ip
            port = user.port
            server_ip = address_info[0]
            server_port = address_info[1]
            user.sock.close()
            user = Client(ip, port, server_ip, server_port)



