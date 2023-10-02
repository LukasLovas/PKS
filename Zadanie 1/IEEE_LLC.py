from Output import Output


class IEEE_LLC(Output):
    dict_sap = {
        "42": "STP",
        "E0": "IPX",
        "F0": "NETBIOS"
    }

    def __init__(self, number, lenght, data):
        super().__init__(number, lenght)
        self.frame_type = "IEEE 802.3 LLC"
        self.dst_mac, self.src_mac = self.resolve_mac_addresses(data)
        self.sap = self.resolve_sap(data)
        self.hexa_frame = [" ".join(data.split()[i:i + 16]).upper() for i in range(0, len(data.split()), 16)]

    def __str__(self):
        print("frame_number: " + str(self.frame_number))
        print("len_frame_pcap: " + str(self.len_frame_pcap))
        print("len_frame_medium: " + str(self.len_frame_medium))
        print("frametype: " + str(self.frame_type))
        print("src_mac: " + str(self.src_mac))
        print("dst_mac: " + str(self.dst_mac))
        print("sap: " + str(self.sap))
        print("hexaframe: ")
        [print(row) for row in self.hexa_frame]
        print("\n")

    def resolve_sap(self,data):
        byte_data = data.replace(" ", "")[30:32].upper()
        if byte_data in self.dict_sap.keys():
            return self.dict_sap[byte_data]
