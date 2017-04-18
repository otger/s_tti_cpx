#!/usr/bin/python
# -*- coding: utf-8 -*-
from entropyfw import Module
from entropyfw.common import get_utc_ts
from pytticpx import CPX
from .logger import log
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

    def connect(self, ip, port=9221):
        self.cpx.connect(ip, port)

    def disconnect(self):
        self.cpx.disconnect()

    def enable_output(self, output_1=False, output_2=False):
        self.cpx.enable_output(output_1, output_2)

    def disable_output(self, output_1=False, output_2=False):
        self.cpx.disable_output(output_1, output_2)

    def set_voltage(self, output, volts):
        log.debug("Received petition to set output {} to {}V".format(output, volts))
        return self.cpx.set_voltage(output, volts)

    def set_voltage_verify(self, output, volts):
        log.debug("Received petition to set output {} to {}V and verify".format(output, volts))
        return self.cpx.set_voltage_verify(output, volts)

    def set_over_voltage_protection(self, output, volts):
        log.debug("Received petition to set over voltage protection of output {} to {}V".format(output, volts))
        return self.cpx.set_OVP(output, volts)

    def set_current_limit(self, output, amps):
        log.debug("Received petition to set output {} current limit to {}A".format(output, amps))
        return self.cpx.set_current_limit(output, amps)

    def get_voltage_setting(self, output):
        log.debug("Received petition to get voltage setting of output {}".format(output))
        return self.cpx.get_voltage(output)

    def get_current_limit_setting(self, output):
        log.debug("Received petition to get current limit of output {}".format(output))
        return self.cpx.get_current_limit(output)

    def read_voltage(self, output):
        log.debug("Received petition to get voltage at output {}".format(output))
        return self.cpx.read_voltage(output)

    def read_current(self, output):
        return self.cpx.read_current(output)

    def is_enabled(self, output):
        return self.cpx.is_enabled(output)

    def get_status(self, output):
        status = {'enabled': self.is_enabled(output),
                  'voltage_setting': self.get_voltage_setting(output),
                  'current_limit_setting': self.get_current_limit_setting(output),
                  'voltage': self.read_voltage(output),
                  'current': self.read_current(output)
                  }

    def pub_status(self, output):

        self.pub_event('status.{}'.format(output), self.get_status(output))

