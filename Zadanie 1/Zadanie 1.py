from binascii import hexlify

from scapy.all import *


def parse_pcap_file(pcap_path):
    frames = []
    fileread = rdpcap(pcap_path)
    for i in range(len(fileread)):
        for j in range(len(fileread[i])):
            frames.append(raw(fileread[i]).hex(" "))
    return frames


def check_frametype(frame):  # TODO funkcia ktora rozhodne ci Ethertype alebo IEEE
    # - spojit dva byte a porovnat ci je
    # vacsi alebo mensi ako 1500
    frametype_bytes = frame[12:16]
    print(frame)
    print(frametype_bytes)


def check_hexcode(frame):
    number = frames.index(frame) + 1
    frame = frame[6:]  # odstranenie preambuly
    frame = frame.replace(" ", "")
    lenght = len(frame)
    frametype = check_frametype(frame)


if __name__ == "__main__":
    frames = parse_pcap_file("C:\eth-1.pcap")
    check_hexcode(frames[0])
