#!/usr/bin/env python3

from __future__ import print_function
from __future__ import absolute_import

import phue
import traceback
import sys

from constants import HUE_ROOM, HUE_BRIDGE_IP, HUE_BRIDGE_USERNAME


if sys.version_info < (3, 0):
    input = raw_input # pylint: disable=E0602


def on_dash(bridge, data):
    try:
        bridge.toggle()
    except OSError as e:
        print(traceback.format_exc(), file=sys.stderr)


def listen_on_stdin(bridge):
    print("Waiting for input", file=sys.stderr)
    try:
        while True:
            data = input()
            if data.startswith('Hello Dash button'):
                on_dash(bridge, data)
    except KeyboardInterrupt:
        print('Ctrl-C', file=sys.stderr)
    except:
        print('Unexpected error!', file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
        raise


class BridgeWrapper(object):
    def __init__(self, bridge):
        self.bridge = bridge

    def lights_are_on(self):
        return any(map(lambda light: light.on, self.bridge.lights))

    def set_lights(self, on):
        print("Turning lights {}".format("on" if on else "off"))
        if HUE_ROOM is not None:
            lights = self.bridge.get_group(HUE_ROOM, 'lights')
        else:
            lights = self.bridge.lights
        for light in lights:
            light.on = on

    def toggle(self):
        self.set_lights(not self.lights_are_on())


if __name__ == '__main__':
    bridge = phue.Bridge(HUE_BRIDGE_IP)
    bridge.connect()
    bridge = BridgeWrapper(bridge)
    listen_on_stdin(bridge)
