#!/usr/bin/python
# -*- coding: utf-8 -*-
from entropyfw import Callback
from .logger import log

"""
callbacks
Created by otger on 23/03/17.
All rights reserved.
"""


class TTiCPXCallback(Callback):
    name = 'gen_callback'
    description = "Generic callback"
    version = "0.1"

    def get_output(self):
        output = getattr(self.event.value, 'output', None)
        if output is None:
            log.error("{} event has no valid 'output' value".format(self.__class__.__name__))
            raise Exception()
        return output

    def get_curr_limit(self):
        curr_lim = getattr(self.event.value, 'current_limit', None)
        if curr_lim is None:
            log.error("{} event has no valid 'current_limit' value".format(self.__class__.__name__))
            raise Exception()
        return curr_lim

    def get_voltage(self):
        volts = getattr(self.event.value, 'voltage', None)
        if volts is None:
            log.error("{} event has no valid 'voltage' value".format(self.__class__.__name__))
            raise Exception()
        return volts


class EnableOutput(TTiCPXCallback):
    name = 'enable_output'
    description = "Enable an output of the power supply"
    version = "0.1"

    def functionality(self):
        output = self.get_output()
        try:
            self.module.enable_output(output_1=(output == 1), output_2=(output == 2))
            self.module.pub_status(output)
        except:
            log.exception('Exception on enable output callback')


class DisableOutput(TTiCPXCallback):
    name = 'disable_output'
    description = "Disable an output of the power supply"
    version = "0.1"

    def functionality(self):
        output = self.get_output()
        try:
            self.module.disable_output(output_1=(output == 1), output_2=(output == 2))
            self.module.pub_status(output)
        except:
            log.exception('Exception on disable output callback')
            raise


class UpdateI(TTiCPXCallback):
    name = 'update_curr_limit'
    description = "update current limit of an output"
    version = "0.1"

    def functionality(self):
        output = self.get_output()
        amps = self.get_curr_limit()
        self.module.set_current_limit(output=output, amps=amps)
        self.module.pub_status(output)


class UpdateV(TTiCPXCallback):
    name = 'update_voltage'
    description = "update voltage of an output"
    version = "0.1"

    def functionality(self):
        output = self.get_output()
        volts = self.get_voltage()
        self.module.set_voltage(output=output, volts=volts)
        self.module.pub_status(output)


class UpdateVI(Callback):
    name = 'update_vi'
    description = "update applied voltage and current limit of an output"
    version = "0.1"

    def functionality(self):
        output = self.get_output()
        volts = self.get_voltage()
        amps = self.get_curr_limit()
        self.module.set_current_limit(output=output, amps=amps)
        self.module.set_voltage(output=output, volts=volts)
        self.module.pub_status(output)


