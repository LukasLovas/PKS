from Output import Output


class IEEE_RAW(Output):
    def __init__(self, number, lenght, data):
        super().__init__(number, lenght)
        self.frame_type = "IEEE 802.3 RAW"
        self.dst_mac, self.src_mac = self.resolve_mac_addresses(data)
        self.hexa_frame = [" ".join(data.split()[i:i + 16]).upper() for i in range(0, len(data.split()), 16)]

    def __str__(self):
        print("frame_number: " + str(self.frame_number))
        print("len_frame_pcap: " + str(self.len_frame_pcap))
        print("len_frame_medium: " + str(self.len_frame_medium))
        print("frametype: " + str(self.frame_type))
        print("src_mac: " + str(self.src_mac))
        print("dst_mac: " + str(self.dst_mac))
        print("hexaframe: ")
        [print(row) for row in self.hexa_frame]
        print("\n")
