from Output import Output


class Ethernet(Output):
    dict_ethertype = {"0806": "ARP",
                      "0800": "IPv4",
                      "88CC": "LLDP",
                      "86DD": "IPv6",
                      "9000": "ECTP"
                      }

    def __init__(self, number, lenght, data):
        super().__init__(number, lenght, data)
        self.frametype = "Ethernet II"
        self.destination, self.source = self.resolve_mac_addresses()
        self.ethertype = self.resolve_ethertype()

    def resolve_ethertype(self):
        byte_data = self.data[24:28]
        if byte_data in self.dict_ethertype.keys():
            return self.dict_ethertype[byte_data]

    def resolve_ipv4_addresses(self):
        destination = self.data[0:12]
        source = self.data[12:24]
        return destination, source
