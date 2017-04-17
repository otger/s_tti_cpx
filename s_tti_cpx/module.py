#!/usr/bin/python
# -*- coding: utf-8 -*-
from entropyfw import Module
from entropyfw.common import get_utc_ts
from pytticpx import CPX
from .callbacks import UpdateV, UpdateI, UpdateVI
# from .web.api.resources import get_api_resources
# from .web.blueprints import get_blueprint
"""
module
Created by otger on 17/04/17.
All rights reserved.
"""


class EntropyTTiCPX(Module):
    name = 'TTiCPX'
    description = "Power Supply Controller"

    def __init__(self, name=None):
        Module.__init__(self, name=name)
        self.cpx = CPX()
        self.v_keyword = None
        self.i_keyword = None

    def pub_status(self):
        self.pub_event('status', self.te.status)

    def register_event_v_applied(self, pattern, v_keyword, flags=0):
        if self.v_keyword is None:
            self.v_keyword = v_keyword
            self.register_callback(callback=UpdateV, pattern=pattern, flags=flags)
        else:
            raise Exception('Only one event for V values can be registered')

    def connect(self, ip, port):
        self.cpx.connect(ip, port)
        # May return any exception (TimeOut)

    def register_event_apply_i(self, channel, pattern, i_keyword, flags=0):
        if self.i_keyword is None:
            self.i_keyword = i_keyword
            self.register_callback(callback=UpdateI, pattern=pattern, flags=flags)
        else:
            raise Exception('Only one event for I values can be registered')

    def register_event_apply_iv(self, pattern, v_keyword, i_keyword, flags=0):
        if self.i_keyword is None and self.v_keyword is None:
            self.i_keyword = i_keyword
            self.v_keyword = v_keyword
            self.register_callback(callback=UpdateVI, pattern=pattern, flags=flags)
        else:
            raise Exception('Only one event for I values can be registered')

    def update_values(self, v=None, i=None):
        if v:
            self.cpx.setVoltage()
        if i:
            self.te.I = i
        self.pub_status()

