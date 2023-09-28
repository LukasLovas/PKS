from Output import Output


class Ethernet(Output):
    def __init__(self, number, lenght, frametype, destination, source, data):
        super().__init__(number, lenght, frametype, destination, source, data)
