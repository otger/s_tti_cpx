#!/usr/bin/python
# -*- coding: utf-8 -*-
from entropyfw import Module
from entropyfw.common import get_utc_ts
from pytticpx import CPX
from .logger import log
from . import actions
from .web.api.resources import get_api_resources
from .web.blueprints import get_blueprint
import threading
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

        self._timer = None
        self.interval = None
        self._l = threading.Lock()

        self.register_action(actions.EnableOutput)
        self.register_action(actions.DisableOutput)
        self.register_action(actions.UpdateI)
        self.register_action(actions.UpdateV)
        self.register_action(actions.UpdateVI)
        self.register_action(actions.Connect)
        for r in get_api_resources():
            self.register_api_resource(r)
        self.register_blueprint(get_blueprint(self.name))

    def connect(self, ip, port=9221):
        self.cpx.connect(ip, port)

    def disconnect(self):
        self.cpx.disconnect()

    def enable_output(self, output_1=False, output_2=False):
        self.cpx.enable_output(output_1, output_2)

    def disable_output(self, output_1=False, output_2=False):
        self.cpx.disable_output(output_1, output_2)

    def set_voltage(self, output, volts):
        # log.debug("Received petition to set output {} to {}V".format(output, volts))
        return self.cpx.set_voltage(output, volts)

    def set_voltage_verify(self, output, volts):
        # log.debug("Received petition to set output {} to {}V and verify".format(output, volts))
        return self.cpx.set_voltage_verify(output, volts)

    def set_over_voltage_protection(self, output, volts):
        # log.debug("Received petition to set over voltage protection of output {} to {}V".format(output, volts))
        return self.cpx.set_OVP(output, volts)

    def set_current_limit(self, output, amps):
        # log.debug("Received petition to set output {} current limit to {}A".format(output, amps))
        return self.cpx.set_current_limit(output, amps)

    def get_voltage_setting(self, output):
        # log.debug("Received petition to get voltage setting of output {}".format(output))
        return self.cpx.get_voltage(output)

    def get_current_limit_setting(self, output):
        # log.debug("Received petition to get current limit of output {}".format(output))
        return self.cpx.get_current_limit(output)

    def read_voltage(self, output):
        # log.debug("Received petition to get voltage at output {}".format(output))
        return self.cpx.read_voltage(output)

    def read_current(self, output):
        return self.cpx.read_current(output)

    def is_enabled(self, output):
        return self.cpx.is_enabled(output)

    def get_status(self, output):
        voltage_wunits = self.read_voltage(output)
        voltage = float(voltage_wunits[:-1])
        current_wunits = self.read_current(output)
        current = float(current_wunits[:-1])
        return {'enabled': self.is_enabled(output),
                'voltage_setting': self.get_voltage_setting(output),
                'current_limit_setting': self.get_current_limit_setting(output),
                'voltage_with_units': self.read_voltage(output),
                'current_with_units': self.read_current(output),
                'voltage': voltage,
                'current': current
               }

    def pub_status(self, output):
        self.pub_event('status.{}'.format(output), self.get_status(output))

    def _timer_func(self):
        self.pub_status(1)
        self.pub_status(2)
        self._timer = threading.Timer(self.interval, self._timer_func)
        self._timer.start()

    def start_timer(self, interval):
        with self._l:
            self.interval = interval
            if self._timer is None:
                self._timer_func()

    def stop_timer(self):
        with self._l:
            if self._timer is not None:
                self._timer.cancel()
                self._timer = None

