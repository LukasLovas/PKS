from Output import Output


class IEEE_SNAP(Output):
    def __init__(self, number, lenght, data):
        super().__init__(number, lenght, data)
        self.frametype = "IEEE 802.3 with LLC & SNAP"
