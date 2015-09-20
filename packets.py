import binascii
from collections import namedtuple
import re
from socket import inet_ntoa
import struct

def normalize_mac(mac_bytes):
    addr = binascii.hexlify(mac_bytes)
    addr = addr.upper()
    return ':'.join(re.findall(r'..', addr))


_EthernetHeader = namedtuple(
    '_EthernetHeader',
    [
        'dest_mac_bytes',   # Destination MAC (6 bytes)
        'source_mac_bytes', # Source MAC (6 bytes)
        'type_or_length',   # Type or length (2 bytes)
    ]
)

class EthernetHeader(_EthernetHeader):
    @classmethod
    def unpack(cls, packet):
        header = packet[0:14]
        header_tuple = cls._make(struct.unpack("!6s6s2s", header))
        data = packet[14:]
        return (header_tuple, data)

    @property
    def dest_mac(self):
        return normalize_mac(super(EthernetHeader, self).dest_mac_bytes)

    @property
    def source_mac(self):
        return normalize_mac(super(EthernetHeader, self).source_mac_bytes)

    def _asdict(self):
        orig = super(EthernetHeader, self)._asdict()
        orig['source_mac'] = self.source_mac
        orig['dest_mac'] = self.dest_mac
        return orig


ARP_TYPE = '\x08\x06'  # 2054 in decimal (max ethernet data length (1500))
_ArpPacket = namedtuple(
    '_ArpPacket',
    [
        'htype',              # hardware type (2 bytes)
        'ptype',              # protocol type (2 bytes)
        'hlen',               # hardware address length (1 byte)
        'plen',               # protocol address length (1 byte)
        'oper',               # operation (2 bytes)
        'sender_haddr_bytes', # sender hardware address (SHA) (6 bytes)
        'sender_paddr_bytes', # sender protocol address (SPA) (4 bytes)
        'target_haddr_bytes', # target hardware address (THA) (6 bytes)
        'target_paddr_bytes', # target protocol address (TPA) (4 bytes)
    ]
)

class ArpPacket(_ArpPacket):
    @classmethod
    def unpack(cls, data):
        arp_header = data[0:28]
        return cls._make(struct.unpack("2s2s1s1s2s6s4s6s4s", arp_header))

    @property
    def sender_haddr(self):
        return normalize_mac(super(ArpPacket, self).sender_haddr_bytes)

    @property
    def sender_paddr(self):
        return inet_ntoa(super(ArpPacket, self).sender_paddr_bytes)

    @property
    def target_haddr(self):
        return normalize_mac(super(ArpPacket, self).target_haddr_bytes)

    @property
    def target_paddr(self):
        return inet_ntoa(super(ArpPacket, self).target_paddr_bytes)

    def _asdict(self):
        orig = super(ArpPacket, self)._asdict()
        orig['sender_haddr'] = self.sender_haddr
        orig['sender_paddr'] = self.sender_paddr
        orig['target_haddr'] = self.target_haddr
        orig['target_paddr'] = self.target_paddr
        return orig
