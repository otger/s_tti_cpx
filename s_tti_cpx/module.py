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
        self.v_keyword = None
        self.i_keyword = None

    def set_voltage(self, output, volts):
        log.debug("Received petition to set output {} to {}V".format(output, volts))
        output = int(output)
        if output not in (1, 2):
            raise Exception("Invalid channel")
        volts = float(volts)
        return self.cpx.setVoltage(output, volts)

    def set_voltage_verify(self, output, volts):
        log.debug("Received petition to set output {} to {}V and verify".format(output, volts))
        output = int(output)
        if output not in (1, 2):
            raise Exception("Invalid channel")
        volts = float(volts)
        return self.cpx.setVoltageVerify(output, volts)

    def set_over_voltage_protection(self, output, volts):
        log.debug("Received petition to set over voltage protection of output {} to {}V".format(output, volts))
        output = int(output)
        if output not in (1, 2):
            raise Exception("Invalid channel")
        volts = float(volts)
        return self.cpx.setOVP(output, volts)

    def set_current_limit(self, output, amps):
        log.debug("Received petition to set output {} current limit to {}A".format(output, amps))
        output = int(output)
        if output not in (1, 2):
            raise Exception("Invalid channel")
        amps = float(amps)
        return self.cpx.setCurrent(output, amps)

    def get_voltage_setting(self, output):
        log.debug("Received petition to get voltage setting of output {}".format(output))
        output = int(output)
        if output not in (1, 2):
            raise Exception("Invalid channel")
        return self.cpx.getVoltage(output)

    def get_current_limit_setting(self, output):
        log.debug("Received petition to get current limit of output {}".format(output))
        output = int(output)
        if output not in (1, 2):
            raise Exception("Invalid channel")
        return self.cpx.getCurrent(output)

    def read_voltage(self, output):
        log.debug("Received petition to get voltage at output {}".format(output))
        output = int(output)
        if output not in (1, 2):
            raise Exception("Invalid channel")
        return self.cpx.readVoltage(output)


    def pub_status(self):
        self.pub_event('status', self.te.status)

