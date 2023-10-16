def ether_type_types():
    dict_ethertype = {}
    file = open("type_files/ether_type", "r")
    for line in file:
        pair = line.strip().split(':')
        if len(pair) == 2:
            key, value = pair[0].strip(), pair[1].strip()
            dict_ethertype[key] = value
    return dict_ethertype


def ipv4_types():
    dict_ipv4 = {}
    file = open("type_files/ipv4", "r")
    for line in file:
        pair = line.strip().split(':')
        if len(pair) == 2:
            key, value = pair[0].strip(), pair[1].strip()
            dict_ipv4[key] = value
    return dict_ipv4


def tcp_types():
    dict_tcp = {}
    file = open("type_files/tcp", "r")
    for line in file:
        pair = line.strip().split(':')
        if len(pair) == 2:
            key, value = pair[0].strip(), pair[1].strip()
            dict_tcp[key] = value
    return dict_tcp


def udp_types():
    dict_udp = {}
    file = open("type_files/udp", "r")
    for line in file:
        pair = line.strip().split(':')
        if len(pair) == 2:
            key, value = pair[0].strip(), pair[1].strip()
            dict_udp[key] = value
    return dict_udp