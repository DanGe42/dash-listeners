#!/usr/bin/env python3
# Some of the ARP-unpacking code was very very loosely adapted from:
# https://medium.com/@xtalker/hey-ted-i-got-this-working-on-my-raspi-without-all-the-scapy-overhead-thanks-to-http-e5704e4b16a9

from __future__ import print_function
from __future__ import absolute_import

from pprint import pprint
import socket
import sys

from packets import ARP_TYPE
from packets import ArpPacket
from packets import EthernetHeader


def _check_not_none(obj):
    if obj is None:
        raise RuntimeError('argument is None')
    return obj


class ArpListener(object):
    @classmethod
    def create(cls):
        raw_socket = socket.socket(
            socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
        return cls(raw_socket)

    def __init__(self, socket):
        self.socket = _check_not_none(socket)
        self.consumers = []

    def add_consumer(self, consumer):
        self.consumers.append(consumer)

    def listen(self):
        try:
            print("Listening for ARP packets")
            while True:
                # for reference, the second return value is the source address
                packet, _ = self.socket.recvfrom(2048)

                ether_header, ether_data = EthernetHeader.unpack(packet)
                if ether_header.type_or_length != ARP_TYPE:
                    continue

                arp_packet = ArpPacket.unpack(ether_data)
                for consumer in self.consumers:
                    consumer(ether_header, arp_packet)

        except KeyboardInterrupt:
            print('Ctrl-C')
        except IOError:
            print('Quitting because of fatal IO error')
            raise
        except:
            print('Unexpected error: {}'.format(sys.exc_info()[0]))
            raise
        finally:
            self.socket.close()


def arp_printer(_, arp_packet):
    source_mac = arp_packet.sender_haddr
    dest_ip = arp_packet.target_paddr
    print("Got ARP probe from {} ({})".format(source_mac, dest_ip))
    pprint(dict(arp_packet._asdict()))


def ether_printer(ether_header, _):
    pprint(dict(ether_header._asdict()))


class DashButtonPrinter(object):
    def __init__(self, mac_addr):
        self.mac_addr = mac_addr

    def __call__(self, _, arp_packet):
        source_mac = arp_packet.sender_haddr
        sender_paddr = arp_packet.sender_paddr
        if source_mac == self.mac_addr and sender_paddr == '0.0.0.0':
            print("Hello Dash button ({})!".format(source_mac))


# XXX: Raw sockets cannot be created without superuser privileges. Before adding
# new functionality to 'main', make sure that security implications would be
# negligible if something were to go wrong.
if __name__ == '__main__':
    raw_socket = socket.socket(
        socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))

    arp_listener = ArpListener(raw_socket)
    arp_listener.add_consumer(ether_printer)
    arp_listener.add_consumer(arp_printer)
    arp_listener.add_consumer(DashButtonPrinter('74:C2:46:CB:72:5D'))
    arp_listener.listen()
