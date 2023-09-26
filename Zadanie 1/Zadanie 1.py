from binascii import hexlify

from scapy.all import *


class Output:
    def __init__(self):
        pass
    destination_address = ""
    source_address = ""


class Ethernet(Output):
    def __init__(self):
        super().__init__()


def parse_pcap_file(pcap_path):
    frames = []
    fileread = rdpcap(pcap_path)
    counter = 0
    for i in range(len(fileread)):
        for j in range(len(fileread[i])):
            counter += 1
            frames.append(raw(fileread[i]).hex(" "))
    print(frames[0])

    return frames


if __name__ == "__main__":
    frames = parse_pcap_file("C:\eth-1.pcap")
    print(frames)
