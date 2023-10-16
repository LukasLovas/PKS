from Output import Output


class IEEE_SNAP(Output):
    dict_pid = {
        "2000": "CDP",
        "2004": "DTP",
        "010B": "PVSTP+",
        "809B": "AppleTalk"
    }
    def __init__(self, number, lenght, data):
        super().__init__(number, lenght)
        self.frame_type = "IEEE 802.3 LLC & SNAP"
        self.dst_mac, self.src_mac = self.resolve_mac_addresses(data)
        self.pid = self.resolve_pid(data)
        self.hexa_frame = [" ".join(data.split()[i:i + 16]).upper() for i in range(0, len(data.split()), 16)]

    def __str__(self):
        print("frame_number: " + str(self.frame_number))
        print("len_frame_pcap: " + str(self.len_frame_pcap))
        print("len_frame_medium: " + str(self.len_frame_medium))
        print("frametype: " + str(self.frame_type))
        print("src_mac: " + str(self.src_mac))
        print("dst_mac: " + str(self.dst_mac))
        print("pid: " + str(self.pid))
        print("hexaframe: ")
        [print(row) for row in self.hexa_frame]
        print("\n")


    def resolve_pid(self,data):
        byte_data = data.replace(" ", "")[40:44].upper()
        if byte_data in self.dict_pid.keys():
            return self.dict_pid[byte_data]

