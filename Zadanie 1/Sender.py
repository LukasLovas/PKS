class Sender:
    def __init__(self, senders: dict):
        self.senders = senders
        self.max_send_packets = self.eval_most_used_src_ip()

    def __str__(self):
        result = "ipv4_senders:\n"
        for key, value in self.senders.items():
            result += f" - node: {key}\n"
            result += f"   number_of_sent_packets: {value}\n\n"
        result += f"max_send_packets_by:\n"
        result += f" - {self.max_send_packets}"
        return result

    def eval_most_used_src_ip(self):
        ipv4s = list(self.senders.keys())
        ip = ipv4s[0]
        maximum = self.senders[ip]
        for key in ipv4s:
            if self.senders[key] > maximum:
                ip = key
                maximum = self.senders[key]
        return ip
