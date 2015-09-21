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
        'dest_mac': b'FF:FF:FF:FF:FF:FF',
        'dest_mac_bytes': b'\xff\xff\xff\xff\xff\xff',
        'source_mac': b'74:C2:46:CB:72:5D',
        'source_mac_bytes': b't\xc2F\xcbr]',
        'type_or_length': b'\x08\x06',
    },
    {
        'hlen': b'\x06',
        'htype': b'\x00\x01',
        'oper': b'\x00\x01',
        'plen': b'\x04',
        'ptype': b'\x08\x00',
        'sender_haddr': b'74:C2:46:CB:72:5D',
        'sender_haddr_bytes': b't\xc2F\xcbr]',
        'sender_paddr': b'0.0.0.0',
        'sender_paddr_bytes': b'\x00\x00\x00\x00',
        'target_haddr': b'00:00:00:00:00:00',
        'target_haddr_bytes': b'\x00\x00\x00\x00\x00\x00',
        'target_paddr': b'192.168.0.106',
        'target_paddr_bytes': b'\xc0\xa8\x00j',
    },
)

arp_packet_request = (
    {
        'dest_mac': b'FF:FF:FF:FF:FF:FF',
        'dest_mac_bytes': b'\xff\xff\xff\xff\xff\xff',
        'source_mac': b'74:C2:46:CB:72:5D',
        'source_mac_bytes': b't\xc2F\xcbr]',
        'type_or_length': b'\x08\x06',
    },
    {
        'hlen': b'\x06',
        'htype': b'\x00\x01',
        'oper': b'\x00\x01',
        'plen': b'\x04',
        'ptype': b'\x08\x00',
        'sender_haddr': b'74:C2:46:CB:72:5D',
        'sender_haddr_bytes': b't\xc2F\xcbr]',
        'sender_paddr': b'192.168.0.106',
        'sender_paddr_bytes': b'\xc0\xa8\x00j',
        'target_haddr': b'00:00:00:00:00:00',
        'target_haddr_bytes': b'\x00\x00\x00\x00\x00\x00',
        'target_paddr': b'192.168.0.1',
        'target_paddr_bytes': b'\xc0\xa8\x00\x01',
    },
)

noise_ethernet_packet = {
    'dest_mac': b'FF:FF:FF:FF:FF:FF',
    'dest_mac_bytes': b'\xff\xff\xff\xff\xff\xff',
    'source_mac': b'20:C9:D0:43:CE:D7',
    'source_mac_bytes': b' \xc9\xd0C\xce\xd7',
    'type_or_length': b'\x00\x06',
}
