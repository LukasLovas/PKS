import socket
from Server import Server

SERVER_IP = "147.175.161.24"  # Server host ip (public IP) A.B.C.D
SERVER_PORT = 50601  # Server port for receiving communication

if __name__ == "__main__":
    server = Server(SERVER_IP, SERVER_PORT)
    data = "empty"
    # data = server.receive()
    # if data != None:
    # server.send_response()
    # else:
    # print("Message has not been recieved.")

    server.three_way()

    while data != "End connection":
        if data != "empty":
            server.send_response()
        data = server.receive()

    server.send_last_response()
    server.quit()
