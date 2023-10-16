class Communication:

    def __init__(self, number_comm, src_comm, dst_comm, frames, partial):
        self.number_comm = number_comm
        self.src_comm = src_comm
        self.dst_comm = dst_comm
        self.packets = frames
        self.partial = partial

        if partial:
            delattr(self, "src_comm")
            delattr(self, "dst_comm")
            delattr(self, "partial")
        else:
            delattr(self, "partial")
