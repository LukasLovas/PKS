from Output import Output


class Ethernet(Output):
    dict_ethertype = {}
    dict_ipv4 = {}
    dict_tcp = {}
    dict_udp = {}

    def __init__(self, number, lenght, data):
        super().__init__(number, lenght)
        self.ether_type_types()
        self.ipv4_types()
        self.frame_type = "Ethernet II"
        self.dst_mac, self.src_mac = self.resolve_mac_addresses(data)
        self.ethertype = self.resolve_ethertype(data)
        self.dst_ip, self.src_ip = self.resolve_ip_adresses(data)
        self.protocol = self.resolve_protocol_ipv4(data)
        self.src_port, self.dst_port = self.resolve_ports(data, self.protocol)
        self.hexa_frame = [" ".join(data.split()[i:i + 16]).upper() for i in range(0, len(data.split()), 16)]

    def __str__(self):
        print("frame_number: " + str(self.frame_number))
        print("len_frame_pcap: " + str(self.len_frame_pcap))
        print("len_frame_medium: " + str(self.len_frame_medium))
        print("frametype: " + str(self.frame_type))
        print("src_mac: " + str(self.src_mac))
        print("dst_mac: " + str(self.dst_mac))
        print("ethertype: " + str(self.ethertype))
        print("src_ip: " + str(self.src_ip))
        print("dst_ip: " + str(self.dst_ip))
        print("protocol: " + str(self.protocol))
        print("src_port: " + str(self.src_port))
        print("dst_port: " + str(self.dst_port))
        print("hexaframe: ")
        [print(row) for row in self.hexa_frame]
        print("\n")

    def resolve_ethertype(self, data):
        byte_data = data.replace(" ", "")[24:28].upper()
        if byte_data in self.dict_ethertype.keys():
            return self.dict_ethertype[byte_data]
        else:
            return "Unknown"

    def resolve_ip_adresses(self, data):
        d = data.replace(" ", "")
        source = "{0}.{1}.{2}.{3}".format(int(d[52:54], 16), int(d[54:56], 16), int(d[56:58], 16), int(d[58:60], 16))
        destination = "{0}.{1}.{2}.{3}".format(int(d[60:62], 16), int(d[62:64], 16), int(d[64:66], 16),
                                               int(d[66:68], 16))
        return destination, source

    def resolve_protocol_ipv4(self, data):
        d = data.replace(" ", "")
        protocol = d[46: 48]
        if protocol in self.dict_ipv4.keys():
            return self.dict_ipv4[protocol]
        else:
            return protocol

    def resolve_ports(self, data, protocol):
        d = data.replace(" ", "")
        source = str(int(d[68:72], 16))
        destination = str(int(d[72:76], 16))
        if protocol == "TCP":
            self.tcp_types()
            if source in self.dict_tcp.keys():
                source = self.dict_tcp[source]
            if destination in self.dict_tcp.keys():
                destination = self.dict_tcp[destination]
        elif protocol == "UDP":
            self.udp_types()
            if source in self.dict_udp.keys():
                source = self.dict_udp[source]
            if destination in self.dict_udp.keys():
                destination = self.dict_udp[destination]
        return source, destination

    def ether_type_types(self):
        file = open("type_files/ether_type", "r")
        for line in file:
            pair = line.strip().split(':')
            if len(pair) == 2:
                key, value = pair[0].strip(), pair[1].strip()
                self.dict_ethertype[key] = value

    def ipv4_types(self):
        file = open("type_files/ipv4", "r")
        for line in file:
            pair = line.strip().split(':')
            if len(pair) == 2:
                key, value = pair[0].strip(), pair[1].strip()
                self.dict_ipv4[key] = value

    def tcp_types(self):
        file = open("type_files/tcp", "r")
        for line in file:
            pair = line.strip().split(':')
            if len(pair) == 2:
                key, value = pair[0].strip(), pair[1].strip()
                self.dict_tcp[key] = value

    def udp_types(self):
        file = open("type_files/udp", "r")
        for line in file:
            pair = line.strip().split(':')
            if len(pair) == 2:
                key, value = pair[0].strip(), pair[1].strip()
                self.dict_udp[key] = value
