class Output:
    def __init__(self, number, lenght):
        self.frame_number = number
        self.len_frame_pcap = lenght
        self.len_frame_medium = max(64, lenght + 4)

    def resolve_mac_addresses(self,hexframe):  # zistit a spravit formatovanie
        d = hexframe.replace(" ", "")
        destination = "{0}:{1}:{2}:{3}:{4}:{5}".format(d[0:2], d[2:4], d[4:6], d[6:8], d[8:10], d[10:12]).upper()
        source = "{0}:{1}:{2}:{3}:{4}:{5}".format(d[12:14], d[14:16], d[16:18], d[18:20], d[20:22], d[22:24]).upper()
        return destination, source
