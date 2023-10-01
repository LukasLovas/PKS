from Output import Output


class IEEE_RAW(Output):
    def __init__(self, number, lenght, data):
        super().__init__(number, lenght, data)
        self.frametype = "IEEE 802.3"
