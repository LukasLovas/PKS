from scapy.all import *

from Ethernet import Ethernet
from IEEE_LLC import IEEE_LLC
from IEEE_RAW import IEEE_RAW
from IEEE_SNAP import IEEE_SNAP


def parse_pcap_file(pcap_path):
    frames = []
    fileread = rdpcap(pcap_path)
    for i in range(len(fileread)):
        for j in range(len(fileread[i])):
            frames.append(raw(fileread[i]).hex(" "))
    return frames


def diferentiate_type(frame, number, lenght):
    frametype_bytes = int(frame[24:26] + frame[26:28], 16)

    if frametype_bytes >= 1536:
        return Ethernet(number, lenght, frame)
    elif frametype_bytes <= 1500 and frame[28:32] == "ffff":
        return IEEE_RAW(number, lenght, frame)
    elif frametype_bytes <= 1500 and frame[28:32] == "aaaa":
        return IEEE_SNAP(number, lenght, frame)
    else:
        return IEEE_LLC(number, lenght, frame)


def format_address(frame):
    pass


def get_basic_params(frame):  # TODO dozistit ako zistim frame_medium_lenght
    #print(frame)
    #print(frame.replace(" ", ""))
    number = frames.index(frame) + 1
    frame = frame.replace(" ", "")
    lenght = len(frame)
    diferentiate_type(frame, number, lenght)


if __name__ == "__main__":
    # frames = parse_pcap_file("C:\\Users\Lukáš\Documents\Repozitare git\\3. Semester\PKS\Zadanie 1\\test_pcap_files\\vzorky_pcap_na_analyzu\eth-1.pcap") #Desktop
    frames = parse_pcap_file("C:\eth-1.pcap")  # NTB
    get_basic_params(frames[0])
