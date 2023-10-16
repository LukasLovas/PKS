from Communication import Communication


class Filter_TCP:

    def __init__(self, name, pcap_name, frames, filter):
        self.name = name
        self.pcap_name = pcap_name + ".pcap"
        self.filter_name = filter
        self.packets = frames
        self.complete_comms = []
        self.partial_comms = []

        self.tcp_comms_setup()

        delattr(self, "packets")
        if not self.complete_comms:
            delattr(self, "complete_comms")
        if not self.partial_comms:
            delattr(self, "partial_comms")

    def tcp_comms_setup(self):
        connections = []
        completed_connections_counter = 0
        partial_connections_counter = 0
        for frame in self.packets:
            connection = (frame.src_port, frame.dst_port)
            if ((frame.src_port, frame.dst_port) not in connections
                    and (frame.dst_port, frame.src_port) not in connections):
                connections.append(connection)

        for connection in connections:
            frames_in_connection_stream = []
            if self.check_handshake(connection):
                completed_connections_counter += 1
                for frame in self.packets:
                    if (frame.src_port, frame.dst_port) == connection or (frame.dst_port, frame.src_port) == connection:
                        frames_in_connection_stream.append(frame)

                comm = Communication(completed_connections_counter, frame.src_ip, frame.dst_ip, frames_in_connection_stream, False)
                self.complete_comms.append(comm)

            elif self.check_handshake(connection) == 0:
                partial_connections_counter += 1
                for frame in self.packets:
                    if (frame.src_port, frame.dst_port) == connection or (frame.dst_port, frame.src_port) == connection:
                        frames_in_connection_stream.append(frame)

                comm = Communication(partial_connections_counter, frame.src_ip, frame.dst_ip, frames_in_connection_stream, True)
                self.partial_comms.append(comm)

    def check_handshake(self, connection):
        three_way_handshake_flag = False
        four_way_handshake_flag = False
        first_shake = False
        second_shake = False

        for frame in self.packets:
            if (frame.src_port, frame.dst_port) == connection or (frame.dst_port, frame.src_port) == connection:
                hex_string = ''.join(frame.hexa_frame).replace(" ", "")
                flag_byte = int(''.join(hex_string[94:96]), 16)
                if not first_shake:
                    if flag_byte == 2:
                        first_shake = True
                elif first_shake and not second_shake:
                    if flag_byte == 18:
                        second_shake = True
                elif first_shake and second_shake:
                    if flag_byte == 16:
                        three_way_handshake_flag = True
                        break
        if not three_way_handshake_flag:
            return 0

        four_way_handshake_bytes = ""

        for frame in self.packets:
            if (frame.src_port, frame.dst_port) == connection or (frame.dst_port, frame.src_port) == connection:
                hex_string = ''.join(frame.hexa_frame).replace(" ", "")
                flag_byte = int(''.join(hex_string[94:96]), 16)
                four_way_handshake_bytes += str(flag_byte)
                four_way_handshake_bytes += " "

        four_way_handshake_bytes = four_way_handshake_bytes.split(" ")[:-1]

        # [RST][4]
        if four_way_handshake_bytes[-1] == "4":
            four_way_handshake_flag = True

        # [RST/ACK][20]
        elif four_way_handshake_bytes[-1] == "20":
            four_way_handshake_flag = True
        # [FIN/ACK,FIN/ACK][17,17]
        elif four_way_handshake_bytes[-1] == "17" and four_way_handshake_bytes[-2] == "17":
            four_way_handshake_flag = True

        # [FIN/ACK/PUSH,FIN/ACK/PUSH,ACK][25,25,16]
        elif (four_way_handshake_bytes[-1] == "16" and four_way_handshake_bytes[-2] == "25"
              and four_way_handshake_bytes[-3] == "25"):
            four_way_handshake_flag = True

        # [FIN/ACK,ACK,FIN/ACK,ACK][17,16,17,16]
        elif (four_way_handshake_bytes[-1] == "16" and four_way_handshake_bytes[-2] == "17"
              and four_way_handshake_bytes[-3] == "16" and four_way_handshake_bytes[-4] == "17"):
            four_way_handshake_flag = True

        # [FIN/ACK,FIN/ACK,ACK][17,17,16]
        elif (four_way_handshake_bytes[-1] == "16" and four_way_handshake_bytes[-2] == "17"
              and four_way_handshake_bytes[-3] == "17"):
            four_way_handshake_flag = True

        # [FIN,FIN/ACK,ACK][1,17,16]
        elif (four_way_handshake_bytes[-1] == "16" and four_way_handshake_bytes[-2] == "17"
              and four_way_handshake_bytes[-3] == "1"):
            four_way_handshake_flag = True

        if three_way_handshake_flag and four_way_handshake_flag:
            return True
        if three_way_handshake_flag and not four_way_handshake_flag:
            return 0
        else:
            return False
