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
from Filter_TCP import Filter_TCP
from Communication import Communication

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


def check_filter(filter):
    if filter == "":
        return False
    if filter == "TCP":
        return "TCP"
    elif filter in Type_files.tcp_types().values():
        return filter
    else:
        return True


def apply_filter(filter, frames):
    frames_after_filter = []
    if filter == "TCP" or filter in Type_files.tcp_types().values():
        for frame in frames:
            if hasattr(frame, "protocol") and frame.protocol == filter:
                frames_after_filter.append(frame)
            elif hasattr(frame, "app_protocol") and frame.app_protocol == filter:
                frames_after_filter.append(frame)
        return Filter_TCP("PKS2023/24", str(file_input), frames_after_filter, filter)
    else:
        for frame in frames:
            if hasattr(frame, "app_protocol") and frame.app_protocol == filter:
                frames_after_filter.append(frame)
            elif hasattr(frame, "protocol") and frame.protocol == filter:
                frames_after_filter.append(frame)
            elif hasattr(frame, "ether_type") and frame.ether_type == filter:
                frames_after_filter.append(frame)
        return frames_after_filter


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
    sender = Sender(ipv4_counter)
    yaml = ru.YAML()
    yaml.register_class(Ethernet)
    yaml.register_class(IEEE_LLC)
    yaml.register_class(IEEE_RAW)
    yaml.register_class(IEEE_SNAP)
    yaml.register_class(Sender)
    yaml.register_class(Filter_TCP)
    yaml.register_class(Communication)
    if check_filter(filter) == "TCP" or check_filter(filter) in Type_files.tcp_types().values():
        output = apply_filter(filter, resolved_frames)

        with open(r"output.yaml", "w") as file:
            yaml.dump(output, file)
            file.close()

        with open(r"output.yaml", "r") as file:
            frames_in_yaml = file.read()

        delete = ["!Ethernet", "!IEEE_LLC", "!IEEE_SNAP", "!IEEE_RAW", "-", "!Filter_TCP", "!Communication", "\'"]

        for k, item in enumerate(delete):
            frames_in_yaml = frames_in_yaml.replace(item, "")

        yaml_rows = frames_in_yaml.split('\n')

        flag = 0
        adjusted_yaml_rows = []  # Create a new list for adjusted lines
        yaml_rows.pop(0)
        for row in yaml_rows:
            if 'hexa_frame' in row:
                row = row.replace('hexa_frame:', 'hexa_frame: |')
            if 'frame_number' in row:
                row = row.replace('frame_number:', '- frame_number:')
            if 'frame_number' not in row and "name" not in row and "comms" not in row:
                row = textwrap.indent(row, '  ')
            if "number_comm:" in row:
                row = row.replace('number_comm:', '- number_comm:')
            if 'NETBIOSNS' in row:
                row = row.replace('NETBIOSNS', 'NETBIOS-NS')
            if 'NETBIOSDGM' in row:
                row = row.replace('NETBIOSDGM', 'NETBIOS-DGM')
            if 'NETBIOSSSN' in row:
                row = row.replace('NETBIOSSSN', 'NETBIOS-SSN')
            if 'FTPDATA' in row:
                row = row.replace('FTPDATA', 'FTP-DATA')
            if 'FTPCONTROL' in row:
                row = row.replace('FTPCONTROL', 'FTP-CONTROL')
            if 'SNMPTRAP' in row:
                row = row.replace('SNMPTRAP', 'SNMP-TRAP')
            if 'DBLSPDISC' in row:
                row = row.replace('DBLSPDISC', 'DB-LSP-DISC')

            if "complete_comms:" in row or "partial_comms" in row:
                flag = 1
            elif flag == 1:
                flag = 0
                continue
            adjusted_yaml_rows.append(row)

        result = ""
        indent_level = 0
        for row in adjusted_yaml_rows:
            if "number_comm:" in row:
                indent_level = 0
                result += " " * (indent_level * 2) + row + "\n"
                indent_level = 1
            elif "frame_number:" in row:
                result += " " * (int(indent_level) * 2) + row + "\n"
            elif "partial_comms" in row:
                indent_level = 0
                result += " " * (int(indent_level) * 2) + row + "\n"
            else:
                result += " " * (int(indent_level) * 2) + row + "\n"

        if filter == "IPv4":
            data = result + "\n" + sender.__str__()
        else:
            data = result

        # print(lines)
        # print(data)

        with open('output.yaml', 'w') as file:
            file.write(data)
    else:
        resolved_frames = apply_filter(filter, resolved_frames)
        with open(r"output.yaml", "w") as file:
            yaml.dump(resolved_frames, file)
            file.close()

        with open(r"output.yaml", "r") as file:
            frames_in_yaml = file.read()

        delete = ["!Ethernet", "!IEEE_LLC", "!IEEE_SNAP", "!IEEE_RAW", "-","\'"]
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
