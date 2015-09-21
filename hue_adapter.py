#!/usr/bin/env python3

from __future__ import print_function
from __future__ import absolute_import


import phue
import sys


if sys.version < (3, 0):
    input = raw_input


def listen_on_stdin(bridge):
    print("Waiting for input", file=sys.stderr)
    try:
        while True:
            data = input()
            print(data)
            if data.startswith(b'Hello Dash button'):
                bridge.toggle()
    except KeyboardInterrupt:
        print('Ctrl-C', file=sys.stderr)
    except:
        print('Unexpected error: {}'.format(sys.exc_info()[0]), file=sys.stderr)
        raise


class BridgeWrapper(object):
    def __init__(self, bridge):
        self.bridge = bridge

    def lights_are_on(self):
        return any(map(lambda light: light.on, self.bridge.lights))

    def set_lights(self, on):
        print("Turning lights {}".format("on" if on else "off"))
        for light in self.bridge.lights:
            light.on = on

    def toggle(self):
        if self.lights_are_on():
            self.set_lights(False)
        else:
            self.set_lights(True)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: {} <bridge IP> <username>".format(sys.argv[0]),
              file=sys.stderr)
        sys.exit(1)

    bridge = phue.Bridge(sys.argv[1], username=sys.argv[2])
    bridge.connect()
    bridge = BridgeWrapper(bridge)
    listen_on_stdin(bridge)
