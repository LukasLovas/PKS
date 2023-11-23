class Header:
    def __init__(self, packet_type, fragment_order, next_fragment, data, crc):
        self.packet_type = packet_type
        self.fragment_order = fragment_order
        self.next_fragment = True if next_fragment == "00000001" else False
        self.data = data
        self.crc = crc
