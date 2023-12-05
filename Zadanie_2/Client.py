import socket
import struct
import os
from crc import Calculator, Crc16
import random



class Client:
    def __init__(self, ip, port, server_ip, server_port):
        self.server = None
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ip = ip
        self.port = port
        self.server_ip = server_ip
        self.server_port = server_port
        self.data = "empty"
        self.header = None
        self.fragment_size = None
        self.initialize_connection()
        self.cycle()

    def cycle(self):
        while True:
            if self.fragment_size is None:
                fragment_size = int(
                    input("Fragment size can vary between 64B to 1466B\nEnter fragment size: "))  # IP/UDP/CUSTOM
                self.fragment_size = self.check_fragment_size(fragment_size)
                print(f"Your fragment size is: {self.fragment_size}\n For changing the fragment size, type 'Fragment'")
            message = input("Enter your message (enter 'File' for file transfer, or enter 'Testing' for a menu with testing features)\nMessage: ")
            if message == "Fragment":
                self.fragment_size = None
                continue
            if message == "File":
                print("C:\\Users\\Lukáš\\Downloads\\fotka.png")
                file_path = input("Type file path: ")
                while not os.path.isfile(file_path):
                    print("Path does not lead to a valid file!")
                    file_path = input("Type file path: ")
                self.send_file(file_path)
            if message == "Testing":
                self.testing_mode()
                continue
            self.send_message(message)
            print("\033[32mServer response: " + self.header[4] + "\033[0m") if self.header[
                                                                                   4] == "Message delivered successfully..." \
                else '\033[31mServer response: ' + self.header[4] + "\033[0m"

    def initialize_connection(self):
        header_to_send = self.build_header(1, 1, False, "")
        self.sock.sendto(header_to_send, (self.server_ip, int(self.server_port)))
        while self.data == "empty":
            self.data = self.receive()
            if self.data == "empty":
                pass
            else:
                if (self.data[0] == 6) & (self.server == (self.server_ip, int(self.server_port))):
                    print("Connection established successfully.")
                else:
                    self.data = "empty"

    def calculate_crc(self, data):
        crc_calculator = Calculator(Crc16.CCITT, optimized=True)
        crc_result = crc_calculator.checksum(data)
        return crc_result

    def check_fragment_size(self, fragment_size):
        if fragment_size >= 1466:
            return 1466
        elif fragment_size <= 64:
            return 64
        else:
            return fragment_size

    def build_header(self, header_type, fragment_order, next_fragment, data):
        if header_type == 3:
            header = (
                    struct.pack("B", header_type) +
                    struct.pack("H", fragment_order) +
                    struct.pack("?", next_fragment)
            )
            checksum = struct.pack("H", self.calculate_crc(header + data))
            return header + checksum + data
        else:
            header = (
                    struct.pack("B", header_type) +
                    struct.pack("H", fragment_order) +
                    struct.pack("?", next_fragment)
            )
            encoded_data = data.encode(encoding="utf-8")
            checksum = struct.pack("H", self.calculate_crc(header + encoded_data))
            return header + checksum + encoded_data

    def receive(self):
        data = None
        while data is None:
            data, self.server = self.sock.recvfrom(1500)
        self.header = self.receive_header(data)
        print("ACK received") if self.header[0] == 6 else None
        return data

    def send_message(self, data):
        fragmentation = True if len(data.encode(encoding="utf-8")) + 8 + 20 + 6 > self.fragment_size else False
        if fragmentation:
            fragment_number = 1
            total_fragments = (len(data) // self.fragment_size) + 1
            fragments_sent = []
            while data:
                fragment, data = data[:self.fragment_size], data[self.fragment_size:]
                fragments_sent.append(fragment)
                header_to_send = self.build_header(2, fragment_number, True if len(data) > 0 else False, fragment)
                self.sock.sendto(header_to_send, (self.server_ip, int(self.server_port)))
                fragment_number += 1
            received_data = None
            while received_data is None:
                received_data = self.receive()
            if self.header[0] == 5:
                missing_fragments_string = self.header[4]
                missing_fragments = [int(fragment) for fragment in missing_fragments_string.split(" ")]
                dummy_header = self.header
                for fragment in missing_fragments:
                    self.header = dummy_header
                    missing_fragment_data = fragments_sent.__getitem__(fragment-1)
                    while self.header[0] != 6:
                        header_to_send = self.build_header(2, fragment, True if len(missing_fragments) >= 1 else False,
                                                           missing_fragment_data)
                        self.sock.sendto(header_to_send, (self.server_ip, int(self.server_port)))
                        response_to_fragments = self.receive()
                        if response_to_fragments[0] == 6:
                            pass

            elif self.header[0] == 6:
                return
        else:
            header_to_send = self.build_header(2, 1, False, data)
            self.sock.sendto(header_to_send, (self.server_ip, int(self.server_port)))
            response_data = self.receive()
            if response_data[0] == 6:
                return

    def send_file(self, file_path):
        file_name = os.path.basename(file_path).encode("utf-8")
        separator = "|||".encode("utf-8")
        with open(file_path, "rb") as file:
            data = file.read()
            fragmentation = True if len(data) + 8 + 20 + 6 > self.fragment_size else False
            if fragmentation:
                fragment_number = 1
                total_fragments = (len(data) // self.fragment_size) + 1
                fragments_sent = []
                while data:
                    fragment, data = data[:self.fragment_size], data[self.fragment_size:]
                    fragments_sent.append(fragment)
                    header_to_send = self.build_header(3, fragment_number, True if len(data) > 0 else False, fragment)
                    self.sock.sendto(header_to_send, (self.server_ip, int(self.server_port)))
                    fragment_number += 1
                received_data = None
                while received_data is None:
                    received_data = self.receive()
                if self.header[0] == 5:
                    missing_fragments_string = self.header[4]
                    missing_fragments = [int(fragment) for fragment in missing_fragments_string.split(" ")]
                    dummy_header = self.header
                    for fragment in missing_fragments:
                        self.header = dummy_header
                        missing_fragment_data = fragments_sent.__getitem__(fragment - 1)
                        while self.header[0] != 6:
                            header_to_send = self.build_header(3, fragment,
                                                               True if len(missing_fragments) >= 1 else False,
                                                               missing_fragment_data)
                            self.sock.sendto(header_to_send, (self.server_ip, int(self.server_port)))
                            response_to_fragments = self.receive()
                            if response_to_fragments[0] == 6:
                                pass

                elif self.header[0] == 6:
                    return

            else:
                header_to_send = self.build_header(3, 1, False, file_name + separator + data)
                self.sock.sendto(header_to_send, (self.server_ip, int(self.server_port)))
                response_data = self.receive()
                if response_data[0] == 6:
                    return

    def receive_header(self, data):
        header = [data[0],  # frame_type 1B      [0]
                  struct.unpack("H", data[1:3])[0],  # fragment_order 2B  [1]
                  data[3],  # next_fragment 1B   [2]
                  struct.unpack("H", data[4:6])[0],  # CRC 2B             [3]
                  data[6:].decode(encoding="utf-8")]  # Data XB            [4]
        return header

    def send_end_message(self):
        self.sock.sendto(bytes("End connection", encoding="utf-8"), (self.server_ip, self.server_port))

    def quit(self):
        self.sock.close()
        print("Client closed...")

    def testing_mode(self):
        feature = input("Availible features:\n1. Send a fragmented message with a data error (checksum error because of modified data)\nInput: ")
        match feature:
            case "1":
                self.send_fragmented_message_with_errors("Lorem ipsum dolor sit amet . Grafickí a typografickí operátori to dobre vedia, v skutočnosti všetky profesie zaoberajúce sa vesmírom komunikácie majú k týmto slovám stabilný vzťah, ale čo to je? Lorem ipsum je atrapa textu bez zmyslu. Je to sekvencia latinských slov , ktoré sú umiestnené tak, ako sú umiestnené „netvorte vety s úplným zmyslom, ale dajte život testovaciemu textu užitočnému na vyplnenie medzier, ktoré budú následne obsadené textami ad hoc zostavenými odborníkmi na komunikáciu. Je určite najznámejší zástupný text , aj keď existujú rôzne verzie odlišujúce sa od poradia, v ktorom sa latinské slová opakujú. Lorem ipsum obsahuje používané písma , ktoré sa viac používajú, čo je aspekt čo vám umožní mať prehľad o vykreslení textu z hľadiska výberu písma a veľkosť písma. Pri odkazovaní na Lorem ipsum sa používajú rôzne výrazy, a to vyplniť text , fiktívny text , slepý text alebo zástupný text : v skratke, jeho význam môže byť tiež nulový, ale jeho užitočnosť je taká jasná, že môže prechádzať storočiami a odolávať ironickým a moderným verziám, ktoré prišli s príchodom webu. AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA KONIEEEC")
    def send_fragmented_message_with_errors(self, data):
        fragmentation = True if len(data.encode(encoding="utf-8")) + 8 + 20 + 6 > self.fragment_size else False
        data_save = data
        if fragmentation:
            fragment_number = 1
            total_fragments = (len(data) // self.fragment_size) + 1
            num_of_errors = 0
            error_counter = 0
            fragments_sent = []
            while data:
                fragment, data = data[:self.fragment_size], data[self.fragment_size:]
                fragments_sent.append(fragment)
                header_to_send, error_predicate = self.build_header_for_error(2, fragment_number, True if len(data) > 0 else False, fragment, None if data else 1, error_counter)
                num_of_errors += error_predicate
                self.sock.sendto(header_to_send, (self.server_ip, int(self.server_port)))
                fragment_number += 1
            received_data = None
            while received_data is None:
                received_data = self.receive()
            if self.header[0] == 5:
                missing_fragments_string = self.header[4]
                missing_fragments = [int(fragment) for fragment in missing_fragments_string.split(" ")]
                dummy_header = self.header
                for fragment in missing_fragments:
                    self.header = dummy_header
                    missing_fragment_data = fragments_sent.__getitem__(fragment-1)
                    while self.header[0] != 6:
                        header_to_send = self.build_header(2, fragment, True if len(missing_fragments) >= 1 else False,
                                                           missing_fragment_data)
                        self.sock.sendto(header_to_send, (self.server_ip, int(self.server_port)))
                        response_to_fragments = self.receive()
                        if response_to_fragments[0] == 6:
                            pass

    def build_header_for_error(self, header_type, fragment_order, next_fragment, data, flag, error_counter):
        if header_type == 3:
            header = (
                    struct.pack("B", header_type) +
                    struct.pack("H", fragment_order) +
                    struct.pack("?", next_fragment)
            )
            checksum = struct.pack("H", self.calculate_crc(header + data))
            if flag is None and error_counter <= 2:
                roll = random.choice([0, 1])
                if roll == 1:
                    return header + checksum + data + b'\x00', 1
                else:
                    return header + checksum + data, 0
            else:
                return header + checksum + data + b'\x00', 0

        else:
            header = (
                    struct.pack("B", header_type) +
                    struct.pack("H", fragment_order) +
                    struct.pack("?", next_fragment)
            )
            encoded_data_real = data.encode(encoding="utf-8")
            checksum = struct.pack("H", self.calculate_crc(header + encoded_data_real))
            rand_index = random.randint(0, self.fragment_size)
            encoded_data_fault = (data[:rand_index] + "errorfault123" + data[rand_index:len(data) - len("errorfault123")]).encode(encoding="utf-8")
            if error_counter >= 2:
                return header + checksum + encoded_data_real, 0
            elif flag is None:
                roll = random.choice([0, 1])
                if roll == 1:
                    return header + checksum + encoded_data_fault, 1
                else:
                    return header + checksum + encoded_data_real, 0
            else:
                return header + checksum + encoded_data_fault, 0


