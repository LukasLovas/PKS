from scapy.all import *

from Ethernet import Ethernet


def parse_pcap_file(pcap_path):
    frames = []
    fileread = rdpcap(pcap_path)
    for i in range(len(fileread)):
        for j in range(len(fileread[i])):
            frames.append(raw(fileread[i]).hex(" "))
    return frames


def diferentiate_frametype(frame, number, lenght):  # TODO funkcia ktora rozhodne ci Ethertype alebo IEEE
    # - spojit dva byte a porovnat ci je
    # vacsi alebo mensi ako 1500
    frametype_bytes = int(frame[24:26] + frame[26:28], 16)

    if frametype_bytes >= 1536:
        pass


def get_basic_params(frame):  # TODO dozistit ako zistim frame_medium_lenght
    number = frames.index(frame) + 1
    frame = frame.replace(" ", "")
    lenght = len(frame)
    destination = frame[0:13], 16
    source = frame[13:25], 16
    print(frame)
    print(str(destination) + "\n" + str(source))
    print(frame[0:13] + "\n" + frame[13:25])
    diferentiate_frametype(frame, number, lenght)


if __name__ == "__main__":
    frames = parse_pcap_file("C:\\Users\Lukáš\Documents\Repozitare git\\3. Semester\PKS\Zadanie 1\\test_pcap_files\\vzorky_pcap_na_analyzu\eth-1.pcap")
    get_basic_params(frames[0])
