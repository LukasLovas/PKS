class Output:
    def __init__(self, number, lenght, data):
        self.frame_number = number
        self.frame_lenght = lenght
        self.frame_medium_lenght = max(64, lenght + 4)
        self.data = data

    def __str__(self):  ##string vypis
        return

    def resolve_mac_addresses(self):  # zistit a spravit formatovanie
        d = self.data
        destination = "{0}:{1}:{2}:{3}:{4}:{5}".format(d[0:2], d[2:4], d[4:6], d[6:8], d[8:10], d[10:12])
        source = "{0}:{1}:{2}:{3}:{4}:{5}".format(d[12:14], d[14:16], d[16:18], d[18:20], d[20:22], d[22:24])
        print(destination + " " + source)
        return destination, source
