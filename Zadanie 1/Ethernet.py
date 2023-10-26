import Type_files
from Output import Output
from Type_files import *


class Ethernet(Output):
    dict_ethertype = {}
    dict_ipv4 = {}
    dict_tcp = {}
    dict_udp = {}
    ipv4_counter = {}

    def __init__(self, number, lenght, data, ipv4_counter):
        super().__init__(number, lenght)
        self.frame_type = "Ethernet II"
        self.dst_mac, self.src_mac = self.resolve_mac_addresses(data)
        self.ether_type = self.resolve_ethertype(data)
        self.dst_ip, self.src_ip = self.resolve_ip_adresses(data, ipv4_counter)
        self.protocol = self.resolve_protocol_ipv4(data)
        self.src_port, self.dst_port, self.app_protocol = self.resolve_ports(data)
        if self.app_protocol is None:
            delattr(self, "app_protocol")
        self.hexa_frame = [" ".join(data.split()[i:i + 16]).upper() for i in range(0, len(data.split()), 16)]

        if self.ether_type == "ARP":
            delattr(self,"src_port")
            delattr(self,"dst_port")
            delattr(self,"protocol")



    def __str__(self):
        print("frame_number: " + str(self.frame_number))
        print("len_frame_pcap: " + str(self.len_frame_pcap))
        print("len_frame_medium: " + str(self.len_frame_medium))
        print("frametype: " + str(self.frame_type))
        print("src_mac: " + str(self.src_mac))
        print("dst_mac: " + str(self.dst_mac))
        print("ethertype: " + str(self.ether_type))
        print("src_ip: " + str(self.src_ip))
        print("dst_ip: " + str(self.dst_ip))
        if self.ether_type != "ARP":
            print("protocol: " + str(self.protocol))
            print("src_port: " + str(self.src_port))
            print("dst_port: " + str(self.dst_port))
        print("hexaframe: ")
        [print(row) for row in self.hexa_frame]
        print("\n")

    def resolve_ethertype(self, data):
        dict_ethertype = Type_files.ether_type_types()
        byte_data = data.replace(" ", "")[24:28].upper()
        if byte_data in dict_ethertype.keys():
            return dict_ethertype[byte_data]
        else:
            return "Akos"

    def resolve_ip_adresses(self, data, ipv4_counter):
        d = data.replace(" ", "")
        source = "{0}.{1}.{2}.{3}".format(int(d[52:54], 16), int(d[54:56], 16), int(d[56:58], 16), int(d[58:60], 16))
        destination = "{0}.{1}.{2}.{3}".format(int(d[60:62], 16), int(d[62:64], 16), int(d[64:66], 16),
                                               int(d[66:68], 16))

        if source in ipv4_counter:
            ipv4_counter[source] += 1
        else:
            key, value = (source, 1)
            ipv4_counter[key] = value
        return destination, source

    def resolve_protocol_ipv4(self, data):
        dict_ipv4 = Type_files.ipv4_types()
        d = data.replace(" ", "")
        protocol = d[46: 48]
        if protocol in dict_ipv4.keys():
            return dict_ipv4[protocol]
        else:
            return protocol

    def resolve_ports(self, data):
        app_protocol = None
        d = data.replace(" ", "")
        source = str(int(d[68:72], 16))
        destination = str(int(d[72:76], 16))
        if self.protocol == "TCP":
            dict_tcp = Type_files.tcp_types()
            if source in dict_tcp.keys():
                app_protocol = dict_tcp[source]
            if destination in dict_tcp.keys():
                app_protocol = dict_tcp[destination]
        elif self.protocol == "UDP":
            dict_udp = Type_files.udp_types()
            if source in dict_udp.keys():
                app_protocol = dict_udp[source]
            if destination in dict_udp.keys():
                app_protocol = dict_udp[destination]
        return source, destination, app_protocol
