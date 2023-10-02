from Output import Output


class Ethernet(Output):
    dict_ethertype = {"0806": "ARP",
                      "0800": "IPv4",
                      "88CC": "LLDP",
                      "86DD": "IPv6",
                      "9000": "ECTP"
                      }

    def __init__(self, number, lenght, data):
        super().__init__(number, lenght)
        self.frame_type = "Ethernet II"
        self.dst_mac, self.src_mac = self.resolve_mac_addresses(data)
        #self.ethertype = self.resolve_ethertype(data)
        self.hexa_frame = [" ".join(data.split()[i:i + 16]).upper() for i in range(0, len(data.split()), 16)]

    def __str__(self):
        print("frame_number: " + str(self.frame_number))
        print("len_frame_pcap: " + str(self.len_frame_pcap))
        print("len_frame_medium: " + str(self.len_frame_medium))
        print("frametype: " + str(self.frame_type))
        print("src_mac: " + str(self.src_mac))
        print("dst_mac: " + str(self.dst_mac))
        #print("ethertype: " + str(self.ethertype))
        print("hexaframe: ")
        [print(row) for row in self.hexa_frame]
        print("\n")

    def resolve_ethertype(self, data):
        byte_data = data.replace(" ", "")[24:28].upper()
        if byte_data in self.dict_ethertype.keys():
            return self.dict_ethertype[byte_data]
        else:
            return "Unknown"
