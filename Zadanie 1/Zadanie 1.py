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


def check_bytes(frame):
    output = Output()
    frame = frame[7:]
    output.destination_address = print("{0}.{1}".format(frame[7:13],frame[13:19]))# odstranenie preambuly
    print(output.destination_address)


if __name__ == "__main__":
    frames = parse_pcap_file("D:\eth-1.pcap")
    check_bytes(frames[0])
