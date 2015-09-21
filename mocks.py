import time


class FakeSocket(object):
    def __init__(self, packets, default_packet):
        self.packets = packets
        self.packet_index = 0
        self.default_packet = default_packet
        self.closed = False

    def recvfrom(self, size):
        if self.closed:
            raise IOError("FakeSocket closed")

        if self.packet_index < len(self.packets):
            packet = self.packets[self.packet_index]
            self.packet_index += 1
            return (packet, '')

        time.sleep(10)
        return (self.default_packet, '')

    def close(self):
        self.closed = True


arp_packet_probe = (
    {
        'dest_mac': 'FF:FF:FF:FF:FF:FF',
        'dest_mac_bytes': '\xff\xff\xff\xff\xff\xff',
        'source_mac': '74:C2:46:CB:72:5D',
        'source_mac_bytes': 't\xc2F\xcbr]',
        'type_or_length': '\x08\x06',
    },
    {
        'hlen': '\x06',
        'htype': '\x00\x01',
        'oper': '\x00\x01',
        'plen': '\x04',
        'ptype': '\x08\x00',
        'sender_haddr': '74:C2:46:CB:72:5D',
        'sender_haddr_bytes': 't\xc2F\xcbr]',
        'sender_paddr': '0.0.0.0',
        'sender_paddr_bytes': '\x00\x00\x00\x00',
        'target_haddr': '00:00:00:00:00:00',
        'target_haddr_bytes': '\x00\x00\x00\x00\x00\x00',
        'target_paddr': '192.168.0.106',
        'target_paddr_bytes': '\xc0\xa8\x00j',
    },
)

arp_packet_request = (
    {
        'dest_mac': 'FF:FF:FF:FF:FF:FF',
        'dest_mac_bytes': '\xff\xff\xff\xff\xff\xff',
        'source_mac': '74:C2:46:CB:72:5D',
        'source_mac_bytes': 't\xc2F\xcbr]',
        'type_or_length': '\x08\x06',
    },
    {
        'hlen': '\x06',
        'htype': '\x00\x01',
        'oper': '\x00\x01',
        'plen': '\x04',
        'ptype': '\x08\x00',
        'sender_haddr': '74:C2:46:CB:72:5D',
        'sender_haddr_bytes': 't\xc2F\xcbr]',
        'sender_paddr': '192.168.0.106',
        'sender_paddr_bytes': '\xc0\xa8\x00j',
        'target_haddr': '00:00:00:00:00:00',
        'target_haddr_bytes': '\x00\x00\x00\x00\x00\x00',
        'target_paddr': '192.168.0.1',
        'target_paddr_bytes': '\xc0\xa8\x00\x01',
    },
)

noise_ethernet_packet = {
    'dest_mac': 'FF:FF:FF:FF:FF:FF',
    'dest_mac_bytes': '\xff\xff\xff\xff\xff\xff',
    'source_mac': '20:C9:D0:43:CE:D7',
    'source_mac_bytes': ' \xc9\xd0C\xce\xd7',
    'type_or_length': '\x08\x06',
}
