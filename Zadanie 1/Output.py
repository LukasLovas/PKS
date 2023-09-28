class Output:
    def __init__(self, number, lenght, frametype, destination, source, data):
        self.frame_number = number
        self.frame_lenght = lenght
        self.frame_medium_lenght = max(64, lenght + 4)
        self.destination_address = destination
        self.source_adress = source
        self.frame_type = frametype
        self.data = data

    def __str__(self):  ##string vypis
        return
