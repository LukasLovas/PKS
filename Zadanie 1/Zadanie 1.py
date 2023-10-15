import textwrap
from os import listdir

from scapy.all import *

import ruamel.yaml as ru

import Type_files
from Ethernet import Ethernet
from IEEE_LLC import IEEE_LLC
from IEEE_RAW import IEEE_RAW
from IEEE_SNAP import IEEE_SNAP
from Sender import Sender
from Type_files import *

ipv4_counter = {}


def parse_pcap_file(pcap_path):
    frames = []
    fileread = rdpcap(pcap_path)
    for i in range(len(fileread)):
        frames.append(raw(fileread[i]).hex(" "))
    return frames


def check_ISL(frame):
    if frame[0:12].upper() == "01000C000000":
        return True
    else:
        return False


def diferentiate_type(frame, number, lenght):
    frame_a = frame.replace(" ", "")  # variating between frame with and without spaces for easier work
    if check_ISL(frame_a):
        frame_a = frame_a[52:]
        frame = frame[78:]
    frametype_bytes = int(frame_a[24:26] + frame_a[26:28], 16)
    if frametype_bytes >= 1536:
        return Ethernet(number, lenght, frame, ipv4_counter)
    elif frametype_bytes <= 1500 and frame_a[28:32] == "ffff":
        return IEEE_RAW(number, lenght, frame)
    elif frametype_bytes <= 1500 and frame_a[28:32] == "aaaa":
        return IEEE_SNAP(number, lenght, frame)
    else:
        return IEEE_LLC(number, lenght, frame)


def get_basic_params(frame, number):
    lenght = int(len(frame.replace(" ", "")) / 2)
    return diferentiate_type(frame, number, lenght)


def apply_filter(filter, frames):
    frames_after_filter = []
    if filter == "TCP" or filter in Type_files.tcp_types():
        for frame in frames:
            if hasattr(frame, "protocol") and frame.protocol == filter:
                frames_after_filter.append(frame)
            elif hasattr(frame, "app_protocol") and frame.app_protocol == filter:
                frames_after_filter.append(frame)
        tcp_comms_setup(frames_after_filter)
    if filter == "TFTP":
        filter = "UDP"
    else:
        for frame in frames:
            if hasattr(frame, "app_protocol") and frame.app_protocol == filter:
                frames_after_filter.append(frame)
            elif hasattr(frame, "protocol") and frame.protocol == filter:
                frames_after_filter.append(frame)
            elif hasattr(frame, "ethertype") and frame.ethertype == filter:
                frames_after_filter.append(frame)

    return frames_after_filter


def tcp_comms_setup(frames):
    connections = []
    for frame in frames:
        connection = (frame.src_port, frame.dst_port)
        if connection not in connections:
            connections.append(connection)
    check_handshakes(connections)

def check_handshakes(connections):
    three_way_handshake_flag = False
    four_way_handshake_flag = False
    handshake_string = ""

    for connection in connections:
        if connection =

if __name__ == "__main__":
    print("Choose file: ")
    frame_files = [file for file in listdir("test_pcap_files/vzorky_pcap_na_analyzu")]
    for file in frame_files:
        print(file)
    file_input = input("--------------------------------\nFile name: ")
    frames = parse_pcap_file("test_pcap_files/vzorky_pcap_na_analyzu/" + file_input + ".pcap")
    # frames = parse_pcap_file("test_pcap_files/vzorky_pcap_na_analyzu/eth-1.pcap")
    print("\n\n")
    print("name: 'PKS2023/24'")
    print("pcap_name: " + file_input)
    filter = input("Filter: ")
    print("packets:")
    resolved_frames = []
    for i in range(len(frames)):
        file_type = get_basic_params(frames[i], i + 1)
        file_type.__str__()
        resolved_frames.append(file_type)
    resolved_frames = apply_filter(filter, resolved_frames)
    sender = Sender(ipv4_counter)
    yaml = ru.YAML()
    yaml.register_class(Ethernet)
    yaml.register_class(IEEE_LLC)
    yaml.register_class(IEEE_RAW)
    yaml.register_class(IEEE_SNAP)
    yaml.register_class(Sender)
    with open(r"output.yaml", "w") as file:
        yaml.dump(resolved_frames, file)
        file.close()

    with open(r"output.yaml", "r") as file:
        frames_in_yaml = file.read()

    delete = ["!Ethernet", "!IEEE_LLC", "!IEEE_SNAP", "!IEEE_RAW", "-"]
    for item in delete:
        frames_in_yaml = frames_in_yaml.replace(item, "")

    yaml_rows = frames_in_yaml.split('\n')
    for i in range(len(yaml_rows)):
        if 'hexa_frame' in yaml_rows[i]:
            yaml_rows[i] = yaml_rows[i].replace('hexa_frame:', 'hexa_frame: |')
        if 'frame_number' in yaml_rows[i]:
            yaml_rows[i] = yaml_rows[i].replace('frame_number:', '- frame_number:')
        if 'frame_number' not in yaml_rows[i]:
            yaml_rows[i] = textwrap.indent(yaml_rows[i], '  ')

    data = '\n'.join(['' + line for line in yaml_rows])
    data = "name: PKS2023/24\npcap_name: " + str(file_input) + ".pcap\npackets: " + data + "\n" + sender.__str__()

    # print(lines)
    # print(data)

    with open('output.yaml', 'w') as file:
        file.write(data)
